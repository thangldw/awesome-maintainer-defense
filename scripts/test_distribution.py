#!/usr/bin/env python3
"""Verify release versions, artifacts, metadata, and clean installation."""

from __future__ import annotations

import base64
import hashlib
import json
import re
import subprocess
import sys
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
EXPECTED_VERSION = "1.1.0"


class DistributionTests(unittest.TestCase):
    def test_all_public_versions_match(self) -> None:
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        project = pyproject.split("[project]", 1)[1].split("\n[", 1)[0]
        version = re.search(r'^version = "([^"]+)"$', project, re.MULTILINE)
        self.assertIsNotNone(version)
        self.assertEqual(version.group(1), EXPECTED_VERSION)
        source = (ROOT / "scripts/install_kit.py").read_text(encoding="utf-8")
        self.assertEqual(
            set(re.findall(r'^(?:KIT|AUDITOR)_VERSION = "([^"]+)"', source, re.MULTILINE)),
            {EXPECTED_VERSION},
        )
        plugin_versions = {
            json.loads(path.read_text(encoding="utf-8"))["version"]
            for path in (
                ROOT / ".codex-plugin/plugin.json",
                ROOT / ".claude-plugin/plugin.json",
                ROOT / ".kimi-plugin/plugin.json",
            )
        }
        self.assertEqual(plugin_versions, {EXPECTED_VERSION})

    def test_standalone_assets_and_formula(self) -> None:
        for name in ("maintainer-defense-kit.py", "maintainer-defense.py"):
            artifact = DIST / name
            checksum_path = DIST / f"{name}.sha256"
            self.assertTrue(artifact.is_file(), f"missing {artifact}; run make package")
            digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
            self.assertEqual(checksum_path.read_text(encoding="ascii"), f"{digest}  {name}\n")
        standalone = DIST / "maintainer-defense-kit.py"
        embedded_payloads = re.findall(
            r"^    '[^']+': '([^']+)',?$",
            standalone.read_text(encoding="utf-8"),
            re.MULTILINE,
        )
        self.assertTrue(embedded_payloads)
        self.assertTrue(all(base64.b64decode(payload)[9] == 255 for payload in embedded_payloads))
        digest = hashlib.sha256(standalone.read_bytes()).hexdigest()
        formula = (ROOT / "Formula/maintainer-defense-kit.rb").read_text(encoding="utf-8")
        self.assertIn(f"/v{EXPECTED_VERSION}/maintainer-defense-kit.py\"", formula)
        self.assertIn(f'  sha256 "{digest}"', formula)
        self.assertIn(f"auditor {EXPECTED_VERSION}; kit {EXPECTED_VERSION}", formula)
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "repository"
            target.mkdir()
            version = subprocess.run(
                [sys.executable, str(standalone), "--version"],
                text=True,
                capture_output=True,
                check=True,
            )
            self.assertEqual(
                version.stdout.strip(),
                f"maintainer-defense auditor {EXPECTED_VERSION}; kit {EXPECTED_VERSION}",
            )
            audit = subprocess.run(
                [sys.executable, str(standalone), "audit", str(target), "--format", "json"],
                text=True,
                capture_output=True,
                check=True,
            )
            self.assertEqual(json.loads(audit.stdout)["schema_version"], 1)

    def test_wheel_and_sdist_contracts(self) -> None:
        wheel_name = f"maintainer_defense_kit-{EXPECTED_VERSION}-py3-none-any.whl"
        sdist_name = f"maintainer_defense_kit-{EXPECTED_VERSION}.tar.gz"
        wheel = DIST / wheel_name
        sdist = DIST / sdist_name
        self.assertTrue(wheel.is_file(), f"missing {wheel_name}; run make package")
        self.assertTrue(sdist.is_file(), f"missing {sdist_name}; run make package")
        with zipfile.ZipFile(wheel) as archive:
            names = set(archive.namelist())
            dist_info = f"maintainer_defense_kit-{EXPECTED_VERSION}.dist-info"
            required = {
                "maintainer_defense_kit.py",
                f"{dist_info}/entry_points.txt",
                f"{dist_info}/METADATA",
            }
            self.assertFalse(required - names)
            entries = archive.read(f"{dist_info}/entry_points.txt").decode("utf-8")
            self.assertIn("maintainer-defense = maintainer_defense_kit:main", entries)
            metadata = archive.read(f"{dist_info}/METADATA").decode("utf-8")
            self.assertIn(f"Version: {EXPECTED_VERSION}", metadata)
        with tarfile.open(sdist, "r:gz") as archive:
            prefix = f"maintainer_defense_kit-{EXPECTED_VERSION}/"
            names = set(archive.getnames())
            required = {
                f"{prefix}pyproject.toml",
                f"{prefix}build_backend.py",
                f"{prefix}generated/maintainer_defense_kit.py",
                f"{prefix}maintainer-defense-config.schema.json",
            }
            self.assertFalse(required - names)

    def test_clean_wheel_install_smoke(self) -> None:
        wheel = DIST / f"maintainer_defense_kit-{EXPECTED_VERSION}-py3-none-any.whl"
        self.assertTrue(wheel.is_file(), f"missing {wheel}; run make package")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            environment = root / "venv"
            subprocess.run([sys.executable, "-m", "venv", str(environment)], check=True)
            python = environment / "bin/python"
            executable = environment / "bin/maintainer-defense"
            subprocess.run(
                [str(python), "-m", "pip", "install", "--no-index", "--no-deps", str(wheel)],
                text=True,
                capture_output=True,
                check=True,
            )
            version = subprocess.run(
                [str(executable), "--version"], text=True, capture_output=True, check=True
            )
            self.assertEqual(
                version.stdout.strip(),
                f"maintainer-defense auditor {EXPECTED_VERSION}; kit {EXPECTED_VERSION}",
            )
            target = root / "repository"
            target.mkdir()
            audit = subprocess.run(
                [str(executable), "audit", str(target), "--format", "json"],
                text=True,
                capture_output=True,
                check=True,
            )
            self.assertEqual(json.loads(audit.stdout)["schema_version"], 1)

    def test_clean_sdist_install_smoke(self) -> None:
        sdist = DIST / f"maintainer_defense_kit-{EXPECTED_VERSION}.tar.gz"
        self.assertTrue(sdist.is_file(), f"missing {sdist}; run make package")
        with tempfile.TemporaryDirectory() as tmp:
            environment = Path(tmp) / "venv"
            subprocess.run([sys.executable, "-m", "venv", str(environment)], check=True)
            python = environment / "bin/python"
            executable = environment / "bin/maintainer-defense"
            subprocess.run(
                [str(python), "-m", "pip", "install", "--no-deps", str(sdist)],
                text=True,
                capture_output=True,
                check=True,
            )
            version = subprocess.run(
                [str(executable), "--version"], text=True, capture_output=True, check=True
            )
            self.assertEqual(
                version.stdout.strip(),
                f"maintainer-defense auditor {EXPECTED_VERSION}; kit {EXPECTED_VERSION}",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)

#!/usr/bin/env python3
"""Verify the deterministic OpenAI skills-only plugin upload bundle."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
EXPECTED_VERSION = "1.1.1"
BUNDLE = DIST / f"awesome-maintainer-defense-openai-skills-v{EXPECTED_VERSION}.zip"
BUILDER = ROOT / "scripts/build_plugin_bundle.py"


class PluginBundleTests(unittest.TestCase):
    def test_skill_frontmatter_is_discoverable(self) -> None:
        text = (ROOT / "skills/audit-repository-workflows/SKILL.md").read_text(encoding="utf-8")
        frontmatter = text.split("---", 2)[1]
        self.assertIn("name: audit-repository-workflows", frontmatter)
        description = next(
            line.removeprefix("description: ")
            for line in frontmatter.splitlines()
            if line.startswith("description: ")
        )
        self.assertTrue(description.startswith("Use when "), description)

    def test_manifest_is_read_only_and_current(self) -> None:
        manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], EXPECTED_VERSION)
        self.assertEqual(manifest["interface"]["category"], "Security")
        self.assertEqual(manifest["interface"]["capabilities"], ["Read"])
        self.assertEqual(manifest["skills"], "./skills/")

    def test_bundle_contains_only_required_public_contracts(self) -> None:
        self.assertTrue(BUNDLE.is_file(), f"missing {BUNDLE}; run make package")
        with zipfile.ZipFile(BUNDLE) as archive:
            names = archive.namelist()
            required = {
                ".codex-plugin/plugin.json",
                "skills/audit-repository-workflows/SKILL.md",
                "skills/audit-repository-workflows/agents/openai.yaml",
                "skills/audit-repository-workflows/references/commands.md",
                "skills/audit-repository-workflows/scripts/run_auditor.py",
                "skills/audit-repository-workflows/scripts/maintainer-defense.py",
                "assets/plugin-icon.png",
                "LICENSE",
                "PRIVACY.md",
                "TERMS.md",
                "SUPPORT.md",
            }
            self.assertFalse(required - set(names))
            self.assertFalse(any("__pycache__" in name or name.endswith(".pyc") for name in names))
            self.assertTrue(all(item.date_time == (1980, 1, 1, 0, 0, 0) for item in archive.infolist()))
            manifest = json.loads(archive.read(".codex-plugin/plugin.json"))
            self.assertEqual(manifest["version"], EXPECTED_VERSION)
            self.assertEqual(
                archive.read("skills/audit-repository-workflows/scripts/maintainer-defense.py"),
                (DIST / "maintainer-defense-kit.py").read_bytes(),
            )

    def test_bundle_is_reproducible_and_executable(self) -> None:
        self.assertTrue(BUILDER.is_file(), f"missing {BUILDER}")
        subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT, check=True)
        first = hashlib.sha256(BUNDLE.read_bytes()).hexdigest()
        subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT, check=True)
        second = hashlib.sha256(BUNDLE.read_bytes()).hexdigest()
        self.assertEqual(first, second)
        with tempfile.TemporaryDirectory() as tmp:
            with zipfile.ZipFile(BUNDLE) as archive:
                archive.extractall(tmp)
            runner = Path(tmp) / "skills/audit-repository-workflows/scripts/run_auditor.py"
            result = subprocess.run(
                [sys.executable, str(runner), "--version"],
                text=True,
                capture_output=True,
                check=True,
            )
            self.assertEqual(
                result.stdout.strip(),
                f"maintainer-defense auditor {EXPECTED_VERSION}; kit {EXPECTED_VERSION}",
            )

    def test_sha256sums_covers_every_public_asset(self) -> None:
        checksums = DIST / "SHA256SUMS.txt"
        self.assertTrue(checksums.is_file(), "missing SHA256SUMS.txt; run make package")
        rows = {}
        for line in checksums.read_text(encoding="ascii").splitlines():
            digest, name = line.split("  ", 1)
            rows[name] = digest
        expected = {
            "maintainer-defense-kit.py",
            "maintainer-defense-kit.py.sha256",
            "maintainer-defense.py",
            "maintainer-defense.py.sha256",
            f"maintainer_defense_kit-{EXPECTED_VERSION}-py3-none-any.whl",
            f"maintainer_defense_kit-{EXPECTED_VERSION}.tar.gz",
            BUNDLE.name,
        }
        self.assertEqual(set(rows), expected)
        for name, digest in rows.items():
            self.assertEqual(hashlib.sha256((DIST / name).read_bytes()).hexdigest(), digest)


if __name__ == "__main__":
    unittest.main(verbosity=2)

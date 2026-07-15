#!/usr/bin/env python3
"""End-to-end tests for every install profile and deployment language."""

from __future__ import annotations

import json
import hashlib
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts/install_kit.py"
BUILDER = ROOT / "scripts/build_standalone.py"


class InstallerTests(unittest.TestCase):
    def run_kit(self, target: Path, *args: str, ok: bool = True) -> subprocess.CompletedProcess:
        result = subprocess.run(
            [sys.executable, str(INSTALLER), "--target", str(target), *args],
            text=True,
            capture_output=True,
            check=False,
        )
        if ok and result.returncode:
            self.fail(f"installer failed:\nstdout={result.stdout}\nstderr={result.stderr}")
        if not ok and not result.returncode:
            self.fail(f"installer unexpectedly succeeded:\n{result.stdout}")
        return result

    def test_profile_language_matrix(self) -> None:
        markers = {"en": "Bug report", "vi": "Báo lỗi", "ja": "バグ報告"}
        expected_workflows = {"observe": 1, "balanced": 1, "hardened": 3}
        for profile in ("observe", "balanced", "hardened"):
            for language in ("en", "vi", "ja"):
                with self.subTest(profile=profile, language=language), tempfile.TemporaryDirectory() as tmp:
                    target = Path(tmp)
                    common = [
                        "--profile", profile,
                        "--language", language,
                        "--repo", "example/project",
                    ]
                    dry_run = self.run_kit(target, *common)
                    self.assertIn("DRY RUN", dry_run.stdout)
                    self.assertFalse((target / ".maintainer-defense-kit.json").exists())

                    self.run_kit(target, *common, "--apply")
                    manifest = json.loads(
                        (target / ".maintainer-defense-kit.json").read_text(encoding="utf-8")
                    )
                    self.assertEqual(manifest["profile"], profile)
                    self.assertEqual(manifest["language"], language)
                    self.assertEqual(len(list((target / ".github/workflows").glob("*.yml"))), expected_workflows[profile])
                    bug = (target / ".github/ISSUE_TEMPLATE/bug.yml").read_text(encoding="utf-8")
                    self.assertIn(markers[language], bug)
                    config = (target / ".github/ISSUE_TEMPLATE/config.yml").read_text(encoding="utf-8")
                    self.assertIn("example/project/security/advisories/new", config)
                    self.assertNotIn("{{REPOSITORY}}", config)
                    self.run_kit(target, "--verify")
                    self.run_kit(target, "--uninstall")
                    self.assertFalse((target / ".maintainer-defense-kit.json").exists())
                    self.assertFalse(any(target.rglob("*")))

    def test_modified_owned_file_blocks_verify_and_uninstall(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            args = ["--repo", "example/project", "--apply"]
            self.run_kit(target, *args)
            path = target / ".github/PULL_REQUEST_TEMPLATE.md"
            original = path.read_bytes()
            path.write_text("local edit\n", encoding="utf-8")
            self.assertIn("MODIFIED", self.run_kit(target, "--verify", ok=False).stderr)
            self.assertIn("refusing", self.run_kit(target, "--uninstall", ok=False).stderr)
            self.assertTrue(path.exists())
            path.write_bytes(original)
            self.run_kit(target, "--uninstall")

    def test_conflict_is_atomic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            conflict = target / ".github/PULL_REQUEST_TEMPLATE.md"
            conflict.parent.mkdir(parents=True)
            conflict.write_text("project-owned\n", encoding="utf-8")
            result = self.run_kit(
                target, "--repo", "example/project", "--apply", ok=False
            )
            self.assertIn("CONFLICT", result.stderr)
            self.assertEqual(conflict.read_text(encoding="utf-8"), "project-owned\n")
            self.assertFalse((target / ".maintainer-defense-kit.json").exists())
            self.assertFalse((target / ".github/ISSUE_TEMPLATE/bug.yml").exists())

    def test_identical_preexisting_file_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as source_tmp, tempfile.TemporaryDirectory() as target_tmp:
            source = Path(source_tmp)
            target = Path(target_tmp)
            args = ["--repo", "example/project", "--apply"]
            self.run_kit(source, *args)
            relative = Path(".github/PULL_REQUEST_TEMPLATE.md")
            existing = target / relative
            existing.parent.mkdir(parents=True)
            existing.write_bytes((source / relative).read_bytes())
            self.run_kit(target, *args)
            manifest = json.loads(
                (target / ".maintainer-defense-kit.json").read_text(encoding="utf-8")
            )
            entry = next(item for item in manifest["files"] if item["path"] == str(relative))
            self.assertFalse(entry["owned"])
            self.run_kit(target, "--uninstall")
            self.assertTrue(existing.exists())

    def test_symlink_destination_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as outside_tmp:
            target = Path(tmp)
            outside = Path(outside_tmp)
            os.symlink(outside, target / ".github")
            result = self.run_kit(
                target, "--repo", "example/project", "--apply", ok=False
            )
            self.assertIn("symbolic link", result.stderr)
            self.assertFalse(any(outside.iterdir()))

    def test_unsafe_manifest_path_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            manifest = {
                "schema_version": 1,
                "files": [
                    {"path": "../outside", "sha256": "0" * 64, "owned": True}
                ],
            }
            (target / ".maintainer-defense-kit.json").write_text(
                json.dumps(manifest), encoding="utf-8"
            )
            result = self.run_kit(target, "--uninstall", ok=False)
            self.assertIn("unsafe manifest path", result.stderr)

    def test_standalone_release_cli_works_outside_repository(self) -> None:
        subprocess.run([sys.executable, str(BUILDER)], check=True, capture_output=True)
        built = ROOT / "dist/maintainer-defense-kit.py"
        auditor = ROOT / "dist/maintainer-defense.py"
        checksum = built.with_suffix(".py.sha256")
        self.assertTrue(checksum.is_file())
        expected = checksum.read_text(encoding="ascii").split()[0]
        self.assertEqual(hashlib.sha256(built.read_bytes()).hexdigest(), expected)
        self.assertTrue(auditor.is_file())
        audit = subprocess.run(
            [sys.executable, str(auditor), "audit", str(ROOT), "--format", "json"],
            text=True, capture_output=True, check=True,
        )
        self.assertEqual(json.loads(audit.stdout)["schema_version"], 1)
        with tempfile.TemporaryDirectory() as outside_tmp, tempfile.TemporaryDirectory() as target_tmp:
            outside = Path(outside_tmp) / built.name
            outside.write_bytes(built.read_bytes())
            target = Path(target_tmp)
            common = [
                sys.executable,
                str(outside),
                "--target",
                str(target),
            ]
            for args in (
                ["--profile", "observe", "--language", "ja", "--repo", "example/project"],
                ["--profile", "observe", "--language", "ja", "--repo", "example/project", "--apply"],
                ["--verify"],
                ["--uninstall"],
            ):
                result = subprocess.run(common + args, text=True, capture_output=True, check=False)
                self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(any(target.rglob("*")))


if __name__ == "__main__":
    unittest.main(verbosity=2)

#!/usr/bin/env python3
"""Exercise the built artifact referenced by each public quickstart."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READMES = ("README.md", "README.vi.md", "README.ja.md")
AUDIT_COMMAND = re.compile(
    r"^python3\s+(?P<path>\S*maintainer-defense-kit\.py)\s+audit\s+\.$",
    re.MULTILINE,
)
SOURCE_QUICKSTART = re.compile(
    r"^make standalone\npython3\s+(?P<path>\S*maintainer-defense-kit\.py)\s+audit\s+\.$",
    re.MULTILINE,
)


class QuickstartTests(unittest.TestCase):
    def test_root_locale_audit_commands_use_the_same_artifact(self) -> None:
        paths = {}
        for filename in READMES:
            text = (ROOT / filename).read_text(encoding="utf-8")
            match = AUDIT_COMMAND.search(text)
            self.assertIsNotNone(match, f"{filename} has no source-checkout audit command")
            paths[filename] = match.group("path")
        self.assertEqual(set(paths.values()), {"dist/maintainer-defense-kit.py"})

    def test_documented_built_artifact_exists_and_runs(self) -> None:
        root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
        source_quickstart = SOURCE_QUICKSTART.search(root_readme)
        self.assertIsNotNone(source_quickstart, "README.md has no executable source quickstart")
        subprocess.run(
            ["make", "standalone"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(source_quickstart.group("path"), "dist/maintainer-defense-kit.py")

        for filename in READMES:
            with self.subTest(readme=filename):
                text = (ROOT / filename).read_text(encoding="utf-8")
                match = AUDIT_COMMAND.search(text)
                self.assertIsNotNone(match, f"{filename} has no source-checkout audit command")
                artifact = ROOT / match.group("path")
                self.assertTrue(artifact.is_file(), f"{filename} points to missing {artifact}")
                result = subprocess.run(
                    [sys.executable, str(artifact), "audit", str(ROOT), "--format", "summary"],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("findings", result.stdout)

    def test_validator_rejects_a_missing_public_pilot_form(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            checkout = Path(directory) / "repository"
            shutil.copytree(
                ROOT,
                checkout,
                ignore=shutil.ignore_patterns(".git", ".worktrees", "dist", "generated", "__pycache__"),
            )
            (checkout / ".github/ISSUE_TEMPLATE/auditor-pilot.yml").unlink(missing_ok=True)
            result = subprocess.run(
                [sys.executable, "scripts/validate.py"],
                cwd=checkout,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("auditor-pilot.yml", result.stderr)

    def test_validator_rejects_a_missing_field_report_form(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "repository"
            shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns(".git", ".worktrees", "dist"))
            target.joinpath(".github/ISSUE_TEMPLATE/field-report.yml").unlink()
            result = subprocess.run(
                [sys.executable, str(target / "scripts/validate.py")],
                cwd=target,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("field-report.yml", result.stderr)

    def test_validator_rejects_a_missing_release_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "repository"
            shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns(".git", ".worktrees", "dist"))
            target.joinpath(".github/workflows/release.yml").unlink(missing_ok=True)
            result = subprocess.run(
                [sys.executable, str(target / "scripts/validate.py")],
                cwd=target,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("release.yml", result.stderr)

    def test_validator_rejects_release_without_pypi_trusted_publishing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "repository"
            shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns(".git", ".worktrees", "dist"))
            release = target / ".github/workflows/release.yml"
            release.write_text(
                release.read_text(encoding="utf-8")
                .replace("environment: pypi", "environment: test")
                .replace("id-token: write", "id-token: none"),
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(target / "scripts/validate.py")],
                cwd=target,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Trusted Publishing", result.stderr)

    def test_validator_rejects_release_without_pinned_pilot_verification(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "repository"
            shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns(".git", ".worktrees", "dist"))
            release = target / ".github/workflows/release.yml"
            release.write_text(
                release.read_text(encoding="utf-8").replace("make pilot-verify && ", ""),
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(target / "scripts/validate.py")],
                cwd=target,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("pilot evidence", result.stderr)

    def test_validator_rejects_shallow_release_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "repository"
            shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns(".git", ".worktrees", "dist"))
            release = target / ".github/workflows/release.yml"
            release.write_text(
                release.read_text(encoding="utf-8").replace("fetch-depth: 0", "fetch-depth: 1"),
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(target / "scripts/validate.py")],
                cwd=target,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("provenance history", result.stderr)

    def test_validator_rejects_non_resumable_publication(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "repository"
            shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns(".git", ".worktrees", "dist"))
            release = target / ".github/workflows/release.yml"
            release.write_text(
                release.read_text(encoding="utf-8")
                .replace(" --clobber", "")
                .replace("          skip-existing: true\n", ""),
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(target / "scripts/validate.py")],
                cwd=target,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("resumable", result.stderr)

    def test_github_release_job_checks_out_tag_without_credentials(self) -> None:
        release = (ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8")
        publish_github = release.split("\n  publish-github:\n", 1)[1].split(
            "\n  publish-pypi:\n", 1
        )[0]
        self.assertIn("actions/checkout@", publish_github)
        self.assertIn("persist-credentials: false", publish_github)


if __name__ == "__main__":
    unittest.main(verbosity=2)

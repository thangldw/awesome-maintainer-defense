#!/usr/bin/env python3
"""Exercise the source-checkout quickstart published in every README."""

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


class QuickstartTests(unittest.TestCase):
    def test_documented_built_artifact_exists_and_runs(self) -> None:
        subprocess.run(
            [sys.executable, "scripts/build_standalone.py"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

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


if __name__ == "__main__":
    unittest.main(verbosity=2)

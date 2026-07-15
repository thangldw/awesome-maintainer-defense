#!/usr/bin/env python3
"""Corpus, contract, patch, and mutation tests for the repository auditor."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts/install_kit.py"
CORPUS = ROOT / "tests/fixtures/auditor/corpus.json"
PIN = "9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0"

spec = importlib.util.spec_from_file_location("maintainer_defense", CLI)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

BASE_FILES = {
    "SECURITY.md": "Report vulnerabilities privately through GitHub Security Advisories.\n",
    ".github/CODEOWNERS": "/.github/ @maintainers\n/SECURITY.md @maintainers\n",
    ".github/ISSUE_TEMPLATE/bug.yml": "name: Bug report\ndescription: Provide reproducible evidence\nbody: []\n",
    ".github/dependabot.yml": "version: 2\nupdates: []\n",
    "docs/OPERATIONS.md": "Branch protection requires review and passing status checks.\n",
    ".github/workflows/ci.yml": f"""name: CI
on: [pull_request]
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@{PIN}
        with:
          persist-credentials: false
      - run: python -m unittest
""",
}


def materialize(target: Path, case: dict) -> None:
    files = dict(BASE_FILES)
    files.update(case.get("files", {}))
    if "workflow" in case:
        files[".github/workflows/ci.yml"] = case["workflow"]
    for relative in case.get("remove", []):
        files.pop(relative, None)
    for relative, content in files.items():
        path = target / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


class AuditorTests(unittest.TestCase):
    def test_labeled_corpus(self) -> None:
        corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(corpus["cases"]), 50)
        for case in corpus["cases"]:
            with self.subTest(case=case["id"]), tempfile.TemporaryDirectory() as tmp:
                target = Path(tmp)
                materialize(target, case)
                report = module.audit_repository(target)
                rules = {finding["rule_id"] for finding in report["findings"]}
                self.assertEqual(set(case.get("expected", [])), rules)
                self.assertFalse(set(case.get("absent", [])) & rules, rules)

    def test_json_and_sarif_contracts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            materialize(target, {"id": "contract"})
            target.joinpath(".github/workflows/ci.yml").write_text(
                BASE_FILES[".github/workflows/ci.yml"].replace(f"@{PIN}", "@v4"),
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(CLI), "audit", str(target), "--format", "json"],
                text=True, capture_output=True, check=True,
            )
            report = json.loads(result.stdout)
            self.assertEqual(report["schema_version"], 1)
            finding = next(item for item in report["findings"] if item["rule_id"] == "MD-WF-003")
            self.assertGreater(finding["location"]["line"], 0)
            self.assertIn("threat_scenario", finding)
            sarif = module.render_sarif(report)
            self.assertEqual(sarif["version"], "2.1.0")
            self.assertEqual(sarif["runs"][0]["results"][0]["locations"][0]["physicalLocation"]["region"]["startLine"], finding["location"]["line"])

    def test_fix_emits_patch_without_modifying_repository(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            materialize(target, {"id": "fix", "workflow": "name: triage\non: [issues]\njobs:\n  triage:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: owner/moderator@0123456789abcdef0123456789abcdef01234567\n        with:\n          close-pr: true\n          min-account-age: 30\n"})
            workflow = target / ".github/workflows/ci.yml"
            before = workflow.read_bytes()
            result = subprocess.run(
                [sys.executable, str(CLI), "fix", str(target), "--dry-run"],
                text=True, capture_output=True, check=True,
            )
            self.assertEqual(workflow.read_bytes(), before)
            self.assertIn("permissions: {}", result.stdout)
            self.assertIn("close-pr: false", result.stdout)
            self.assertIn("min-account-age: 0", result.stdout)

    def test_fingerprint_survives_unrelated_line_shift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            materialize(target, {"id": "fingerprint"})
            workflow = target / ".github/workflows/ci.yml"
            workflow.write_text(
                BASE_FILES[".github/workflows/ci.yml"].replace(f"@{PIN}", "@v4"),
                encoding="utf-8",
            )
            before = next(
                item for item in module.audit_repository(target)["findings"]
                if item["rule_id"] == "MD-WF-003"
            )
            workflow.write_text("# unrelated comment\n" + workflow.read_text(encoding="utf-8"), encoding="utf-8")
            after = next(
                item for item in module.audit_repository(target)["findings"]
                if item["rule_id"] == "MD-WF-003"
            )
            self.assertNotEqual(before["location"]["line"], after["location"]["line"])
            self.assertEqual(before["fingerprint"], after["fingerprint"])

    def test_permission_and_pin_mutations_are_killed(self) -> None:
        mutations = {
            "remove-permissions": lambda value: value.replace("permissions:\n  contents: read\n", ""),
            "grant-write-all": lambda value: value.replace("permissions:\n  contents: read", "permissions: write-all"),
            "unpin-action": lambda value: value.replace(PIN, "v4"),
            "enable-persisted-token": lambda value: value.replace("contents: read", "contents: write").replace("        with:\n          persist-credentials: false\n", ""),
        }
        expected = {
            "remove-permissions": "MD-WF-001",
            "grant-write-all": "MD-WF-002",
            "unpin-action": "MD-WF-003",
            "enable-persisted-token": "MD-WF-006",
        }
        for name, mutate in mutations.items():
            with self.subTest(mutation=name), tempfile.TemporaryDirectory() as tmp:
                target = Path(tmp)
                materialize(target, {"id": name})
                workflow = target / ".github/workflows/ci.yml"
                workflow.write_text(mutate(workflow.read_text(encoding="utf-8")), encoding="utf-8")
                rules = {item["rule_id"] for item in module.audit_repository(target)["findings"]}
                self.assertIn(expected[name], rules)

    def test_fail_on_threshold(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            materialize(target, {"id": "threshold"})
            target.joinpath(".github/workflows/ci.yml").write_text("name: bad\non: [push]\npermissions: write-all\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(CLI), "audit", str(target), "--fail-on", "high"],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)

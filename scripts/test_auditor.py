#!/usr/bin/env python3
"""Corpus, contract, patch, and mutation tests for the repository auditor."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts/install_kit.py"
CORPUS = ROOT / "tests/fixtures/auditor/corpus.json"
PIN = "9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0"
UPLOAD_PIN = "043fb46d1a93c77aae656e7c1c64a875d1fc6a0a"
DOWNLOAD_PIN = "3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c"

spec = importlib.util.spec_from_file_location("maintainer_defense", CLI)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
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

UNTRUSTED_ARTIFACT_PRODUCER = f"""name: PR Tests
on:
  pull_request:
permissions:
  contents: read
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: mkdir -p output && printf '#!/bin/sh\\necho report\\n' > output/report.sh
      - uses: actions/upload-artifact@{UPLOAD_PIN}
        with:
          name: pr-output
          path: output
"""

PRIVILEGED_ARTIFACT_CONSUMER = f"""name: Publish
on:
  workflow_run:
    workflows: [\"PR Tests\"]
    types: [completed]
permissions: {{}}
jobs:
  publish:
    permissions:
      contents: write
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@{DOWNLOAD_PIN}
        with:
          name: pr-output
          path: downloaded
      - run: sh downloaded/report.sh
"""


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
    def run_cli(self, *arguments: object) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CLI), *(str(value) for value in arguments)],
            text=True,
            capture_output=True,
            check=False,
        )

    def audit_files(self, files: dict[str, str]) -> dict:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            materialize(target, {"id": "multi-file", "files": files})
            return module.audit_repository(target)

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
            rule = next(
                item
                for item in sarif["runs"][0]["tool"]["driver"]["rules"]
                if item["id"] == "MD-WF-003"
            )
            self.assertTrue(rule["helpUri"].endswith("AUDITOR_RULES.md#md-wf-003"))
            self.assertEqual(
                rule["shortDescription"]["text"],
                "GitHub Action is not pinned to a full commit SHA",
            )
            self.assertEqual(sarif["runs"][0]["results"][0]["locations"][0]["physicalLocation"]["region"]["startLine"], finding["location"]["line"])

    def test_human_output_leads_with_summary_and_guidance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            materialize(target, {"id": "human-output"})
            workflow = target / ".github/workflows/ci.yml"
            workflow.write_text(
                BASE_FILES[".github/workflows/ci.yml"].replace(f"@{PIN}", "@v4"),
                encoding="utf-8",
            )
            output = module.render_human(module.audit_repository(target))
            self.assertEqual(output.splitlines()[0], "1 finding · 1 medium")
            self.assertIn("Evidence:", output)
            self.assertIn("Safe remediation:", output)
            self.assertIn("AUDITOR_RULES.md#md-wf-003", output)

    def test_readme_output_matches_published_corpus_case(self) -> None:
        corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
        case = next(item for item in corpus["cases"] if item["id"] == "pwn-request")
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            materialize(target, case)
            summary = module.render_summary(module.audit_repository(target))
            expected = "```text\n" + summary + "```"
        readme = ROOT.joinpath("README.md").read_text(encoding="utf-8")
        documented = readme.split("<!-- auditor-output:start -->", 1)[1].split(
            "<!-- auditor-output:end -->", 1
        )[0].strip()
        self.assertEqual(documented, expected)
        screenshot = ROOT.joinpath("assets/audit-result.svg").read_text(encoding="utf-8")
        for line in summary.splitlines():
            if line:
                self.assertIn(line, screenshot)

    def test_rule_registry_matches_implementation_docs_and_corpus(self) -> None:
        registry = module.rule_catalog()
        implemented = set(
            re.findall(r'"(MD-(?:GOV|WF|MOD)-[0-9]{3})"', CLI.read_text(encoding="utf-8"))
        )
        documented = set(
            re.findall(
                r"^### (MD-(?:GOV|WF|MOD)-[0-9]{3})$",
                ROOT.joinpath("docs/AUDITOR_RULES.md").read_text(encoding="utf-8"),
                re.MULTILINE,
            )
        )
        corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
        expected = {
            rule_id
            for case in corpus["cases"]
            for rule_id in case.get("expected", []) + case.get("absent", [])
        }
        self.assertEqual(set(registry), implemented)
        self.assertEqual(set(registry), documented)
        self.assertEqual(set(registry), expected)

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

    def test_all_write_scopes_count_as_job_authority(self) -> None:
        write_scopes = (
            "actions",
            "artifact-metadata",
            "attestations",
            "checks",
            "code-quality",
            "contents",
            "deployments",
            "discussions",
            "id-token",
            "issues",
            "packages",
            "pages",
            "pull-requests",
            "security-events",
            "statuses",
        )
        for scope in write_scopes:
            with self.subTest(scope=scope), tempfile.TemporaryDirectory() as tmp:
                target = Path(tmp)
                materialize(
                    target,
                    {
                        "id": scope,
                        "workflow": f"""name: dangerous
on:
  pull_request_target:
permissions: {{}}
jobs:
  publish:
    permissions:
      {scope}: write
    runs-on: ubuntu-latest
    steps:
      - run: git fetch origin refs/pull/1/head && ./publish.sh
""",
                    },
                )
                rules = {item["rule_id"] for item in module.audit_repository(target)["findings"]}
                self.assertIn("MD-WF-005", rules)

    def test_untrusted_job_does_not_borrow_unrelated_job_authority(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            materialize(
                target,
                {
                    "id": "separate-authority",
                    "workflow": """name: separated
on:
  pull_request_target:
permissions: {}
jobs:
  inspect:
    permissions:
      contents: read
    runs-on: ubuntu-latest
    steps:
      - run: git fetch origin refs/pull/1/head && ./inspect.sh
  publish:
    permissions:
      checks: write
    runs-on: ubuntu-latest
    steps:
      - run: echo publish trusted metadata
""",
                },
            )
            rules = {item["rule_id"] for item in module.audit_repository(target)["findings"]}
            self.assertNotIn("MD-WF-005", rules)

    def test_untrusted_artifact_to_privileged_workflow(self) -> None:
        report = self.audit_files(
            {
                ".github/workflows/test.yml": UNTRUSTED_ARTIFACT_PRODUCER,
                ".github/workflows/publish.yml": PRIVILEGED_ARTIFACT_CONSUMER,
            }
        )
        findings = [item for item in report["findings"] if item["rule_id"] == "MD-WF-008"]
        self.assertEqual(len(findings), 1)
        self.assertIn(".github/workflows/test.yml", findings[0]["threat_scenario"])
        self.assertIn(".github/workflows/publish.yml", findings[0]["threat_scenario"])

    def test_artifact_trust_path_requires_execution_and_authority(self) -> None:
        download_only = PRIVILEGED_ARTIFACT_CONSUMER.replace(
            "      - run: sh downloaded/report.sh\n", "      - run: sha256sum downloaded/report.sh\n"
        )
        no_authority = PRIVILEGED_ARTIFACT_CONSUMER.replace(
            "    permissions:\n      contents: write\n", "    permissions: {}\n"
        )
        for name, consumer in (("download-only", download_only), ("no-authority", no_authority)):
            with self.subTest(case=name):
                report = self.audit_files(
                    {
                        ".github/workflows/test.yml": UNTRUSTED_ARTIFACT_PRODUCER,
                        ".github/workflows/publish.yml": consumer,
                    }
                )
                rules = {item["rule_id"] for item in report["findings"]}
                self.assertNotIn("MD-WF-008", rules)

    def test_new_only_accepts_one_baseline_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            materialize(target, {"id": "baseline", "remove": ["SECURITY.md"]})
            baseline_path = target / "baseline.json"
            baseline_path.write_text(
                json.dumps(module.audit_repository(target)), encoding="utf-8"
            )
            workflow = target / ".github/workflows/ci.yml"
            workflow.write_text(
                workflow.read_text(encoding="utf-8").replace(f"@{PIN}", "@v4"),
                encoding="utf-8",
            )
            result = self.run_cli(
                "audit", target, "--baseline", baseline_path, "--new-only", "--format", "json"
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual([item["rule_id"] for item in report["findings"]], ["MD-WF-003"])
            self.assertEqual(report["summary"]["total"], 1)

    def test_new_only_rejects_invalid_comparison_sources(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            materialize(target, {"id": "comparison-errors"})
            malformed = target / "malformed.json"
            malformed.write_text('{"schema_version": 2, "findings": []}', encoding="utf-8")
            cases = (
                ("missing", ("audit", target, "--new-only"), 2),
                (
                    "both",
                    (
                        "audit", target, "--new-only", "--baseline", malformed,
                        "--compare-ref", "HEAD",
                    ),
                    2,
                ),
                (
                    "malformed",
                    ("audit", target, "--new-only", "--baseline", malformed),
                    1,
                ),
                (
                    "unknown-ref",
                    ("audit", target, "--new-only", "--compare-ref", "not-a-ref"),
                    1,
                ),
            )
            for name, arguments, expected_code in cases:
                with self.subTest(case=name):
                    result = self.run_cli(*arguments)
                    self.assertEqual(result.returncode, expected_code, result.stderr)

    def test_compare_ref_reports_only_findings_added_after_commit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            materialize(target, {"id": "git-delta"})
            subprocess.run(["git", "init", "-q"], cwd=target, check=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=target, check=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=target, check=True)
            subprocess.run(["git", "add", "."], cwd=target, check=True)
            subprocess.run(["git", "commit", "-qm", "safe baseline"], cwd=target, check=True)
            workflow = target / ".github/workflows/ci.yml"
            workflow.write_text(
                workflow.read_text(encoding="utf-8").replace(f"@{PIN}", "@v4"),
                encoding="utf-8",
            )
            subprocess.run(["git", "add", "."], cwd=target, check=True)
            subprocess.run(["git", "commit", "-qm", "introduce finding"], cwd=target, check=True)
            result = self.run_cli(
                "audit", target, "--compare-ref", "HEAD^", "--new-only", "--format", "json"
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual([item["rule_id"] for item in report["findings"]], ["MD-WF-003"])

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

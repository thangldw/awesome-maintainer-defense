#!/usr/bin/env python3
"""Tests for deterministic, non-invented pilot evidence bundles."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts/build_pilot_bundle.py"

spec = importlib.util.spec_from_file_location("pilot_bundle", BUILDER)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)

FINDING = {
    "rule_id": "MD-WF-003",
    "severity": "medium",
    "confidence": "high",
    "location": {"path": ".github/workflows/ci.yml", "line": 9, "column": 15},
    "message": "Action is not pinned.",
    "threat_scenario": "A mutable tag can move.",
    "recommendation": "Pin the reviewed commit.",
    "fingerprint": "0123456789abcdef01234567",
    "fix": {"available": False},
}
REPORT = {
    "schema_version": 1,
    "tool": {"name": "maintainer-defense", "version": "1.1.0"},
    "target": "/tmp/example",
    "summary": {
        "total": 1,
        "by_severity": {"critical": 0, "high": 0, "medium": 1, "low": 0, "note": 0},
    },
    "findings": [FINDING],
}
METADATA = {
    "pilot_id": "2026-08-23-example",
    "disclosure": "public",
    "pilot_type": "internal-owner-directed",
    "run_at": "2026-08-23T12:00:00Z",
    "auditor_version": "1.1.0",
    "source_commit": "a" * 40,
    "standalone_sha256": "b" * 64,
    "command": "python3 maintainer-defense-kit.py audit . --format json",
    "target_repository": "example/project",
    "target_commit": "c" * 40,
    "allow_aggregate_metrics": False,
    "limitations": ["Owner-directed dogfood; not independent or representative."],
}
COMPLETE_LABEL = {
    "classification": "true-positive",
    "independent": True,
    "reviewer_role": "repository maintainer",
    "consent_statement": "Approved for public release.",
    "recommendation_safety": "safe",
    "recommendation_practicality": "practical",
    "review_effort_minutes": 4,
    "remediation_outcome": "fixed",
    "notes": "Confirmed against the workflow.",
}


class PilotBundleTests(unittest.TestCase):
    def test_checked_in_minimal_fixture_builds(self) -> None:
        fixture = json.loads(
            (ROOT / "pilots/fixtures/minimal-input.json").read_text(encoding="utf-8")
        )
        bundle = module.build_bundle(
            fixture["metadata"],
            fixture["raw_report"],
            fixture["effective_report"],
            fixture["labels"],
        )
        self.assertEqual(bundle["reviews"][0]["classification"], "unresolved")

    def test_missing_labels_remain_unresolved(self) -> None:
        bundle = module.build_bundle(METADATA, REPORT, REPORT, {})
        self.assertEqual(bundle["reviews"][0]["classification"], "unresolved")
        self.assertNotIn("precision", bundle["summary"])

    def test_invalid_revisions_and_mismatched_fingerprints_fail(self) -> None:
        for field, value in (
            ("source_commit", "abc"),
            ("target_commit", "d" * 39),
            ("standalone_sha256", "z" * 64),
        ):
            with self.subTest(field=field):
                metadata = dict(METADATA)
                metadata[field] = value
                with self.assertRaises(module.PilotError):
                    module.build_bundle(metadata, REPORT, REPORT, {})
        with self.assertRaises(module.PilotError):
            module.build_bundle(METADATA, REPORT, REPORT, {"f" * 24: COMPLETE_LABEL})
        effective = json.loads(json.dumps(REPORT))
        effective["findings"][0]["fingerprint"] = "f" * 24
        with self.assertRaises(module.PilotError):
            module.build_bundle(METADATA, REPORT, effective, {})

    def test_aggregate_precision_requires_independent_authorized_labels(self) -> None:
        labels = {FINDING["fingerprint"]: COMPLETE_LABEL}
        owner_bundle = module.build_bundle(METADATA, REPORT, REPORT, labels)
        self.assertNotIn("precision", owner_bundle["summary"])

        metadata = dict(METADATA)
        metadata["pilot_type"] = "external-maintainer-reviewed"
        metadata["allow_aggregate_metrics"] = True
        independent_bundle = module.build_bundle(metadata, REPORT, REPORT, labels)
        self.assertEqual(independent_bundle["summary"]["precision"], 1.0)
        self.assertNotIn("recall", independent_bundle["summary"])

    def test_json_ordering_and_markdown_are_deterministic(self) -> None:
        second = json.loads(json.dumps(FINDING))
        second["rule_id"] = "MD-GOV-001"
        second["fingerprint"] = "00112233445566778899aabb"
        second["location"]["path"] = "SECURITY.md"
        raw = json.loads(json.dumps(REPORT))
        raw["findings"] = [FINDING, second]
        raw["summary"]["total"] = 2
        raw["summary"]["by_severity"]["medium"] = 2
        first = module.build_bundle(METADATA, raw, raw, {})
        second_build = module.build_bundle(METADATA, raw, raw, {})
        self.assertEqual(module.serialize_bundle(first), module.serialize_bundle(second_build))
        self.assertEqual(module.render_markdown(first), module.render_markdown(second_build))
        self.assertEqual(
            [item["fingerprint"] for item in first["reviews"]],
            sorted(item["fingerprint"] for item in first["reviews"]),
        )

    def test_cli_writes_valid_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            inputs = {
                "metadata.json": METADATA,
                "raw.json": REPORT,
                "effective.json": REPORT,
                "labels.json": {},
            }
            for name, payload in inputs.items():
                root.joinpath(name).write_text(json.dumps(payload), encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(BUILDER),
                    "--metadata", str(root / "metadata.json"),
                    "--raw-report", str(root / "raw.json"),
                    "--effective-report", str(root / "effective.json"),
                    "--labels", str(root / "labels.json"),
                    "--json-output", str(root / "pilot.json"),
                    "--markdown-output", str(root / "README.md"),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads((root / "pilot.json").read_text())["schema_version"], 1)
            self.assertIn("unresolved", (root / "README.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main(verbosity=2)

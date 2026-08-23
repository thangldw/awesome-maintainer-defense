#!/usr/bin/env python3
"""Build deterministic Maintainer Defense pilot evidence bundles."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from datetime import datetime
from pathlib import Path

CLASSIFICATIONS = {"true-positive", "false-positive", "not-applicable", "unresolved"}
PILOT_TYPES = {"internal-owner-directed", "external-maintainer-reviewed"}
DISCLOSURES = {"public", "sanitized", "private", "repository-and-sanitized-results"}
SAFETY_VALUES = {"safe", "unsafe", "not-reviewed"}
PRACTICALITY_VALUES = {"practical", "impractical", "not-reviewed"}
OUTCOMES = {"fixed", "accepted", "rejected", "not-attempted", "not-reviewed"}


class PilotError(Exception):
    pass


def validate_metadata(metadata: dict) -> None:
    required = {
        "pilot_id",
        "disclosure",
        "pilot_type",
        "run_at",
        "auditor_version",
        "source_commit",
        "standalone_sha256",
        "command",
        "target_repository",
        "target_commit",
        "allow_aggregate_metrics",
        "limitations",
    }
    optional = {"reviewer_role"}
    if (
        not isinstance(metadata, dict)
        or not required <= set(metadata)
        or set(metadata) - required - optional
    ):
        raise PilotError("pilot metadata has missing or unknown fields")
    for field in ("pilot_id", "auditor_version", "command"):
        if not isinstance(metadata[field], str) or not metadata[field].strip():
            raise PilotError(f"metadata {field} must be a non-empty string")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", metadata["pilot_id"]):
        raise PilotError("pilot_id must be filesystem-safe")
    if metadata["disclosure"] not in DISCLOSURES:
        raise PilotError("unsupported disclosure level")
    if metadata["pilot_type"] not in PILOT_TYPES:
        raise PilotError("unsupported pilot_type")
    if "reviewer_role" in metadata and (
        not isinstance(metadata["reviewer_role"], str) or not metadata["reviewer_role"].strip()
    ):
        raise PilotError("metadata reviewer_role must be a non-empty string")
    try:
        parsed_run_at = datetime.fromisoformat(metadata["run_at"].replace("Z", "+00:00"))
    except (AttributeError, ValueError) as exc:
        raise PilotError("run_at must be an ISO-8601 timestamp") from exc
    if parsed_run_at.tzinfo is None:
        raise PilotError("run_at must include a timezone")
    if not re.fullmatch(r"[0-9a-f]{40}", metadata["source_commit"]):
        raise PilotError("source_commit must be a full lowercase Git SHA")
    if not re.fullmatch(r"[0-9a-f]{40}", metadata["target_commit"]):
        raise PilotError("target_commit must be a full lowercase Git SHA")
    if not re.fullmatch(r"[0-9a-f]{64}", metadata["standalone_sha256"]):
        raise PilotError("standalone_sha256 must be 64 lowercase hexadecimal characters")
    if not re.fullmatch(r"[^/\s]+/[^/\s]+", metadata["target_repository"]):
        raise PilotError("target_repository must use OWNER/REPOSITORY")
    if not isinstance(metadata["allow_aggregate_metrics"], bool):
        raise PilotError("allow_aggregate_metrics must be boolean")
    limitations = metadata["limitations"]
    if not isinstance(limitations, list) or not limitations or any(
        not isinstance(item, str) or not item.strip() for item in limitations
    ):
        raise PilotError("limitations must contain at least one non-empty statement")


def validate_report(report: dict, label: str) -> dict[str, dict]:
    required = {"schema_version", "tool", "target", "summary", "findings"}
    if not isinstance(report, dict) or set(report) != required or report.get("schema_version") != 1:
        raise PilotError(f"{label} must be a schema-v1 audit report")
    tool = report["tool"]
    if not isinstance(tool, dict) or tool.get("name") != "maintainer-defense" or not isinstance(tool.get("version"), str):
        raise PilotError(f"{label} has invalid tool metadata")
    if not isinstance(report["target"], str) or not report["target"]:
        raise PilotError(f"{label} has an invalid target")
    findings = report["findings"]
    if not isinstance(findings, list):
        raise PilotError(f"{label} findings must be an array")
    indexed: dict[str, dict] = {}
    counts = {severity: 0 for severity in ("critical", "high", "medium", "low", "note")}
    for finding in findings:
        if not isinstance(finding, dict):
            raise PilotError(f"{label} contains a non-object finding")
        fingerprint = finding.get("fingerprint")
        if not isinstance(fingerprint, str) or not re.fullmatch(r"[0-9a-f]{24}", fingerprint):
            raise PilotError(f"{label} contains an invalid finding fingerprint")
        if fingerprint in indexed:
            raise PilotError(f"{label} contains duplicate fingerprint {fingerprint}")
        severity = finding.get("severity")
        if severity not in counts:
            raise PilotError(f"{label} contains an invalid finding severity")
        if not isinstance(finding.get("rule_id"), str):
            raise PilotError(f"{label} contains an invalid rule_id")
        location = finding.get("location")
        if not isinstance(location, dict) or not isinstance(location.get("path"), str):
            raise PilotError(f"{label} contains an invalid finding location")
        indexed[fingerprint] = finding
        counts[severity] += 1
    summary = report["summary"]
    if not isinstance(summary, dict) or summary.get("total") != len(findings) or summary.get("by_severity") != counts:
        raise PilotError(f"{label} summary does not match its findings")
    return indexed


def validate_label(fingerprint: str, label: dict) -> dict:
    required = {
        "classification",
        "independent",
        "reviewer_role",
        "consent_statement",
        "recommendation_safety",
        "recommendation_practicality",
        "review_effort_minutes",
        "remediation_outcome",
        "notes",
    }
    if not isinstance(label, dict) or set(label) != required:
        raise PilotError(f"label {fingerprint} has missing or unknown fields")
    if label["classification"] not in CLASSIFICATIONS:
        raise PilotError(f"label {fingerprint} has an invalid classification")
    if not isinstance(label["independent"], bool):
        raise PilotError(f"label {fingerprint} independent must be boolean")
    for field in ("reviewer_role", "consent_statement"):
        if not isinstance(label[field], str) or not label[field].strip():
            raise PilotError(f"label {fingerprint} requires {field}")
    if label["recommendation_safety"] not in SAFETY_VALUES:
        raise PilotError(f"label {fingerprint} has invalid recommendation_safety")
    if label["recommendation_practicality"] not in PRACTICALITY_VALUES:
        raise PilotError(f"label {fingerprint} has invalid recommendation_practicality")
    effort = label["review_effort_minutes"]
    if not isinstance(effort, int) or isinstance(effort, bool) or effort < 0:
        raise PilotError(f"label {fingerprint} review_effort_minutes must be non-negative")
    if label["remediation_outcome"] not in OUTCOMES:
        raise PilotError(f"label {fingerprint} has invalid remediation_outcome")
    if not isinstance(label["notes"], str):
        raise PilotError(f"label {fingerprint} notes must be a string")
    return dict(label)


def unresolved_review(finding: dict, emitted: bool) -> dict:
    return {
        "fingerprint": finding["fingerprint"],
        "rule_id": finding["rule_id"],
        "path": finding["location"]["path"],
        "emitted": emitted,
        "classification": "unresolved",
        "independent": False,
        "reviewer_role": None,
        "consent_statement": None,
        "recommendation_safety": "not-reviewed",
        "recommendation_practicality": "not-reviewed",
        "review_effort_minutes": None,
        "remediation_outcome": "not-reviewed",
        "notes": "",
    }


def build_bundle(
    metadata: dict,
    raw_report: dict,
    effective_report: dict,
    labels: dict[str, dict],
) -> dict:
    """Return one schema-v1 pilot bundle without inventing review labels."""
    validate_metadata(metadata)
    raw = validate_report(raw_report, "raw_report")
    effective = validate_report(effective_report, "effective_report")
    if raw_report["target"] != effective_report["target"]:
        raise PilotError("raw and effective reports must have the same target")
    if raw_report["tool"]["version"] != metadata["auditor_version"] or effective_report["tool"]["version"] != metadata["auditor_version"]:
        raise PilotError("report and metadata auditor versions differ")
    if not set(effective) <= set(raw):
        raise PilotError("effective report contains fingerprints absent from raw report")
    for fingerprint, finding in effective.items():
        if finding != raw[fingerprint]:
            raise PilotError(f"effective finding {fingerprint} differs from raw evidence")
    if not isinstance(labels, dict):
        raise PilotError("labels must be an object keyed by finding fingerprint")
    unknown = set(labels) - set(raw)
    if unknown:
        raise PilotError(f"labels contain unknown fingerprints: {sorted(unknown)}")

    reviews = []
    for fingerprint in sorted(raw):
        finding = raw[fingerprint]
        review = unresolved_review(finding, fingerprint in effective)
        if fingerprint in labels:
            review.update(validate_label(fingerprint, labels[fingerprint]))
        reviews.append(review)
    classification_counts = {
        classification: sum(review["classification"] == classification for review in reviews)
        for classification in sorted(CLASSIFICATIONS)
    }
    summary: dict[str, object] = {
        "raw_findings": len(raw),
        "effective_findings": len(effective),
        "suppressed_findings": len(raw) - len(effective),
        "classification_counts": classification_counts,
        "independently_labeled": sum(
            review["independent"] and review["classification"] != "unresolved"
            for review in reviews
        ),
    }
    complete_independent = bool(reviews) and all(
        review["independent"] and review["classification"] != "unresolved"
        for review in reviews
    )
    aggregation_allowed = (
        metadata["pilot_type"] == "external-maintainer-reviewed"
        and metadata["allow_aggregate_metrics"]
        and complete_independent
    )
    denominator = classification_counts["true-positive"] + classification_counts["false-positive"]
    if aggregation_allowed and denominator:
        summary["precision"] = round(classification_counts["true-positive"] / denominator, 6)
    return {
        "schema_version": 1,
        "metadata": dict(metadata),
        "reports": {"raw": raw_report, "effective": effective_report},
        "reviews": reviews,
        "summary": summary,
    }


def serialize_bundle(bundle: dict) -> str:
    return json.dumps(bundle, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def markdown_value(value: object) -> str:
    if value is None:
        return "—"
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(bundle: dict) -> str:
    metadata = bundle["metadata"]
    summary = bundle["summary"]
    lines = [
        f"# Reproducible pilot evidence: {metadata['pilot_id']}",
        "",
        "> Generated from pinned metadata, reports, and reviewer labels. Edit the JSON inputs, not this page.",
        "",
        "## Provenance",
        "",
        f"- Pilot type: `{metadata['pilot_type']}`",
        f"- Disclosure: `{metadata['disclosure']}`",
        f"- Run timestamp: `{metadata['run_at']}`",
        f"- Auditor: `{metadata['auditor_version']}` at `{metadata['source_commit']}`",
        f"- Standalone SHA-256: `{metadata['standalone_sha256']}`",
        f"- Target: `{metadata['target_repository']}@{metadata['target_commit']}`",
        f"- Command: `{metadata['command']}`",
        "",
        "The report represents the pinned auditor and target revisions. It does not claim that a historical auditor equals the current runtime.",
        "",
        "## Review state",
        "",
        f"- Raw findings: {summary['raw_findings']}",
        f"- Effective findings: {summary['effective_findings']}",
        f"- Suppressed findings: {summary['suppressed_findings']}",
        f"- Independently labeled: {summary['independently_labeled']}",
    ]
    if "reviewer_role" in metadata:
        lines.insert(8, f"- Reviewer role: `{metadata['reviewer_role']}`")
    if "precision" in summary:
        lines.append(f"- Precision over independently reviewed applicable findings: {summary['precision']:.6f}")
    else:
        lines.append("- Aggregate precision: not calculated")
    lines.extend(
        [
            "- Recall: not calculated; the bundle contains findings, not an independently labeled negative sample",
            "",
            "## Finding labels",
            "",
            "| Rule | Path | Fingerprint | Emitted | Classification | Independent | Reviewer | Outcome |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for review in bundle["reviews"]:
        lines.append(
            "| " + " | ".join(
                markdown_value(value)
                for value in (
                    review["rule_id"],
                    review["path"],
                    review["fingerprint"],
                    str(review["emitted"]).lower(),
                    review["classification"],
                    str(review["independent"]).lower(),
                    review["reviewer_role"],
                    review["remediation_outcome"],
                )
            ) + " |"
        )
    lines.extend(["", "## Evidence limitations", ""])
    lines.extend(f"- {item}" for item in metadata["limitations"])
    return "\n".join(lines) + "\n"


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PilotError(f"cannot read {path}: {exc}") from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata", required=True, type=Path)
    parser.add_argument("--raw-report", required=True, type=Path)
    parser.add_argument("--effective-report", required=True, type=Path)
    parser.add_argument("--labels", type=Path)
    parser.add_argument("--json-output", required=True, type=Path)
    parser.add_argument("--markdown-output", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        labels = load_json(args.labels) if args.labels else {}
        bundle = build_bundle(
            load_json(args.metadata),
            load_json(args.raw_report),
            load_json(args.effective_report),
            labels,
        )
        atomic_write(args.json_output, serialize_bundle(bundle))
        atomic_write(args.markdown_output, render_markdown(bundle))
    except PilotError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Render the evidence-backed resource audit from catalog and audit data."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def main() -> None:
    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    audit_data = json.loads((ROOT / "audits.json").read_text(encoding="utf-8"))
    audits = {item["id"]: item for item in audit_data["audits"]}
    lines = [
        "# Resource audit",
        "",
        f"Verified against official project sources on **{audit_data['verified_on']}**.",
        "Repository activity is a point-in-time snapshot, not an endorsement or a guarantee of future maintenance.",
        "",
        "## How to read this audit",
        "",
        "- **Low impact:** read-only analysis or documentation in normal use.",
        "- **Medium impact:** can label, comment, fail checks, publish reports, or modify local files.",
        "- **High impact:** can close, lock, delete, block, limit interactions, or change repository settings.",
        "- Impact is maximum documented capability, not a security score. Actual behavior depends on configuration.",
        "- Data boundaries identify where repository content, metadata, or credentials may travel. Verify current privacy terms yourself.",
        "",
    ]
    for category in catalog["categories"]:
        items = [
            resource
            for resource in catalog["resources"]
            if resource["category"] == category["id"]
        ]
        lines.extend([f"## {category['name']}", ""])
        for resource in items:
            audit = audits[resource["id"]]
            evidence = " · ".join(
                f"[source {index}]({url})"
                for index, url in enumerate(audit["evidence"], start=1)
            )
            snapshot = audit["repo_snapshot"]
            lines.extend(
                [
                    f"### [{resource['name']}]({resource['url']})",
                    "",
                    f"- **Deployment:** {audit['deployment']}",
                    f"- **Default mode:** {audit['default_mode']}",
                    f"- **Maximum automation impact:** {audit['automation_impact'].upper()} — "
                    + ", ".join(audit["maximum_effects"]),
                    f"- **Data boundaries:** {', '.join(audit['data_boundaries'])}",
                    f"- **Access:** {audit['access']}",
                    f"- **Important limitation:** {audit['limitations']}",
                    f"- **Repository snapshot:** archived=`{str(snapshot['archived']).lower()}`, "
                    f"last source push=`{snapshot['pushed_at']}`, "
                    f"GitHub license detection=`{snapshot['license_detected']}`",
                    f"- **Evidence:** {evidence}",
                    "",
                ]
            )
    (ROOT / "docs/RESOURCE_AUDIT.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()

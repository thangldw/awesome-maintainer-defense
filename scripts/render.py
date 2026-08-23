#!/usr/bin/env python3
"""Render the evidence-reviewed resource catalog to docs/CATALOG.md."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = "docs/CATALOG.md"


def inline(value: object) -> str:
    return str(value).replace("\n", " ").strip()


def link_evidence(urls: list[str]) -> str:
    return " · ".join(f"[source {index}]({url})" for index, url in enumerate(urls, 1))


def render_catalog(catalog: dict, audit_data: dict) -> str:
    audits = {item["id"]: item for item in audit_data["audits"]}
    lines = [
        "# Evidence-reviewed catalog",
        "",
        "> Generated from `catalog.json` and `audits.json`. Edit the structured sources, not this file.",
        "",
        "## Reading the evidence",
        "",
        f"Official project sources were last reviewed on **{audit_data['verified_on']}**. "
        "The snapshot is not an endorsement, certification, or promise of future maintenance.",
        "",
        "Impact records the maximum documented automation effect: `low` is normally read-only; "
        "`medium` can publish, fail checks, comment, label, or modify local files; `high` can close, "
        "lock, delete, block, limit interactions, or change settings. Configuration may reduce the actual effect.",
        "",
    ]
    for category in catalog["categories"]:
        lines.extend([f"## {category['name']}", "", category["description"], ""])
        resources = [
            item for item in catalog["resources"] if item["category"] == category["id"]
        ]
        for resource in resources:
            audit = audits[resource["id"]]
            snapshot = audit["repo_snapshot"]
            featured = " · featured" if resource.get("featured") else ""
            lines.extend(
                [
                    f"### [{resource['name']}]({resource['url']})",
                    "",
                    inline(resource["description"]),
                    "",
                    f"- **Classification:** `{resource['type']}` · `{resource['license']}`{featured}",
                    f"- **Deployment/default:** {inline(audit['deployment'])}; {inline(audit['default_mode'])}",
                    f"- **Maximum impact:** `{audit['automation_impact']}` — "
                    + ", ".join(inline(item) for item in audit["maximum_effects"]),
                    f"- **Data boundaries:** {', '.join(inline(item) for item in audit['data_boundaries'])}",
                    f"- **Access:** {inline(audit['access'])}",
                    f"- **Limitation:** {inline(audit['limitations'])}",
                    f"- **Repository snapshot:** archived=`{str(snapshot['archived']).lower()}`, "
                    f"last push=`{snapshot['pushed_at']}`, license detection=`{snapshot['license_detected']}`",
                    f"- **Evidence:** {link_evidence(audit['evidence'])}",
                    "",
                ]
            )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    audit_data = json.loads((ROOT / "audits.json").read_text(encoding="utf-8"))
    output = ROOT / OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_catalog(catalog, audit_data), encoding="utf-8")
    print(f"WROTE {OUTPUT}")


if __name__ == "__main__":
    main()

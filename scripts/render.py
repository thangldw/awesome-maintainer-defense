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
        "The snapshot is not an endorsement, certification, or promise of future maintenance. "
        "Access, data boundaries, and repository snapshots are recorded in `audits.json`.",
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
            featured = " · featured" if resource.get("featured") else ""
            lines.extend(
                [
                    f"### [{resource['name']}]({resource['url']})",
                    "",
                    inline(resource["description"]),
                    "",
                    f"- `{resource['type']}` · `{resource['license']}`{featured} · "
                    f"impact `{audit['automation_impact']}` ({', '.join(inline(item) for item in audit['maximum_effects'])})",
                    f"- **Default:** {inline(audit['default_mode'])}",
                    f"- **Limitation:** {inline(audit['limitations'])}",
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

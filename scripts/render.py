#!/usr/bin/env python3
"""Render the catalog section in README.md from catalog.json."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog.json"
README_PATH = ROOT / "README.md"
START = "<!-- catalog:start -->"
END = "<!-- catalog:end -->"


def escape_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def render() -> str:
    data = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    resources = data["resources"]
    sections: list[str] = []
    for category in data["categories"]:
        rows = [item for item in resources if item["category"] == category["id"]]
        sections.extend(
            [
                f"### {category['name']}",
                "",
                category["description"],
                "",
                "| Resource | Type | License | Why it matters |",
                "| --- | --- | --- | --- |",
            ]
        )
        for item in rows:
            marker = " ⭐" if item.get("featured") else ""
            sections.append(
                "| "
                f"[{escape_cell(item['name'])}]({item['url']}){marker} | "
                f"{escape_cell(item['type'])} | "
                f"{escape_cell(item['license'])} | "
                f"{escape_cell(item['description'])} |"
            )
        sections.append("")
    return "\n".join(sections).rstrip()


def main() -> None:
    readme = README_PATH.read_text(encoding="utf-8")
    if readme.count(START) != 1 or readme.count(END) != 1:
        raise SystemExit("README.md must contain exactly one catalog marker pair")
    before, remainder = readme.split(START, 1)
    _, after = remainder.split(END, 1)
    README_PATH.write_text(
        f"{before}{START}\n\n{render()}\n\n{END}{after}", encoding="utf-8"
    )


if __name__ == "__main__":
    main()

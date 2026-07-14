#!/usr/bin/env python3
"""Render the catalog section in README.md from catalog.json."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog.json"
START = "<!-- catalog:start -->"
END = "<!-- catalog:end -->"


def escape_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def render(data: dict, translations: dict | None = None) -> str:
    translations = translations or {}
    translated_categories = translations.get("categories", {})
    translated_resources = translations.get("resources", {})
    translated_types = translations.get("types", {})
    table = translations.get(
        "table",
        {
            "resource": "Resource",
            "type": "Type",
            "license": "License",
            "why": "Why it matters",
        },
    )
    resources = data["resources"]
    sections: list[str] = []
    for category in data["categories"]:
        localized_category = translated_categories.get(category["id"], {})
        category_name = localized_category.get("name", category["name"])
        category_description = localized_category.get(
            "description", category["description"]
        )
        rows = [item for item in resources if item["category"] == category["id"]]
        sections.extend(
            [
                f"### {category_name}",
                "",
                category_description,
                "",
                f"| {table['resource']} | {table['type']} | {table['license']} | {table['why']} |",
                "| --- | --- | --- | --- |",
            ]
        )
        for item in rows:
            marker = " ⭐" if item.get("featured") else ""
            description = translated_resources.get(item["id"], item["description"])
            resource_type = translated_types.get(item["type"], item["type"])
            sections.append(
                "| "
                f"[{escape_cell(item['name'])}]({item['url']}){marker} | "
                f"{escape_cell(resource_type)} | "
                f"{escape_cell(item['license'])} | "
                f"{escape_cell(description)} |"
            )
        sections.append("")
    return "\n".join(sections).rstrip()


def render_file(path: Path, rendered_catalog: str) -> None:
    readme = path.read_text(encoding="utf-8")
    if readme.count(START) != 1 or readme.count(END) != 1:
        raise SystemExit(f"{path.name} must contain exactly one catalog marker pair")
    before, remainder = readme.split(START, 1)
    _, after = remainder.split(END, 1)
    path.write_text(
        f"{before}{START}\n\n{rendered_catalog}\n\n{END}{after}", encoding="utf-8"
    )


def load_translations(locale: str, data: dict) -> dict:
    path = ROOT / "i18n" / f"{locale}.json"
    translations = json.loads(path.read_text(encoding="utf-8"))
    expected_categories = {item["id"] for item in data["categories"]}
    expected_resources = {item["id"] for item in data["resources"]}
    if set(translations.get("categories", {})) != expected_categories:
        raise SystemExit(f"{path} category translations are incomplete")
    if set(translations.get("resources", {})) != expected_resources:
        raise SystemExit(f"{path} resource translations are incomplete")
    return translations


def main() -> None:
    data = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    render_file(ROOT / "README.md", render(data))
    for locale in ("vi", "ja"):
        translations = load_translations(locale, data)
        render_file(ROOT / f"README.{locale}.md", render(data, translations))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Validate catalog structure, generated docs, and starter-kit safety basics."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_TYPES = {
    "awesome-list",
    "github-action",
    "templates",
    "tool",
    "working-group",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def validate_catalog() -> dict:
    path = ROOT / "catalog.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid catalog.json: {exc}")

    categories = data.get("categories", [])
    resources = data.get("resources", [])
    category_ids = [item.get("id") for item in categories]
    resource_ids = [item.get("id") for item in resources]
    if len(category_ids) != len(set(category_ids)):
        fail("category IDs must be unique")
    if len(resource_ids) != len(set(resource_ids)):
        fail("resource IDs must be unique")
    if not resources:
        fail("catalog must contain at least one resource")

    urls: set[str] = set()
    for item in resources:
        missing = {
            "id",
            "name",
            "url",
            "category",
            "type",
            "license",
            "description",
            "signals",
        } - item.keys()
        if missing:
            fail(f"{item.get('id', '<unknown>')} is missing {sorted(missing)}")
        if item["category"] not in category_ids:
            fail(f"{item['id']} has unknown category {item['category']}")
        if item["type"] not in ALLOWED_TYPES:
            fail(f"{item['id']} has unsupported type {item['type']}")
        parsed = urlparse(item["url"])
        if parsed.scheme != "https" or not parsed.netloc:
            fail(f"{item['id']} must use a valid HTTPS URL")
        if item["url"] in urls:
            fail(f"duplicate URL: {item['url']}")
        urls.add(item["url"])
        if len(item["description"]) < 24 or item["description"].endswith("!"):
            fail(f"{item['id']} needs a factual, non-promotional description")
        if not isinstance(item["signals"], list) or not item["signals"]:
            fail(f"{item['id']} must include at least one signal")
    return data


def validate_readme(data: dict) -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if "<!-- catalog:start -->" not in readme or "<!-- catalog:end -->" not in readme:
        fail("README catalog markers are missing")
    catalog_section = readme.split("<!-- catalog:start -->", 1)[1].split(
        "<!-- catalog:end -->", 1
    )[0]
    for item in data["resources"]:
        if catalog_section.count(item["url"]) != 1:
            fail(f"generated catalog must contain {item['url']} exactly once")


def validate_workflows() -> None:
    workflow_files = list(ROOT.glob("**/.github/workflows/*.yml"))
    if not workflow_files:
        fail("no workflow files found")
    for path in workflow_files:
        text = path.read_text(encoding="utf-8")
        if re.search(r"permissions:\s*write-all", text):
            fail(f"{path.relative_to(ROOT)} grants write-all")
        if "pull_request_target:" in text and "actions/checkout" in text:
            fail(f"{path.relative_to(ROOT)} combines pull_request_target with checkout")


def validate_generated_readme() -> None:
    before = (ROOT / "README.md").read_text(encoding="utf-8")
    subprocess.run([sys.executable, str(ROOT / "scripts/render.py")], check=True)
    after = (ROOT / "README.md").read_text(encoding="utf-8")
    if before != after:
        fail("README catalog is stale; run python3 scripts/render.py")


def main() -> None:
    data = validate_catalog()
    validate_readme(data)
    validate_workflows()
    validate_generated_readme()
    print(f"OK: {len(data['resources'])} resources across {len(data['categories'])} categories")


if __name__ == "__main__":
    main()

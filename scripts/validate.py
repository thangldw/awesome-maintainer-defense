#!/usr/bin/env python3
"""Validate catalog structure, generated docs, and starter-kit safety basics."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_TYPES = {
    "awesome-list",
    "github-action",
    "github-app",
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


def validate_audits(catalog: dict) -> dict:
    path = ROOT / "audits.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid audits.json: {exc}")

    audits = data.get("audits", [])
    audit_ids = [item.get("id") for item in audits]
    catalog_ids = [item["id"] for item in catalog["resources"]]
    if len(audit_ids) != len(set(audit_ids)):
        fail("audit IDs must be unique")
    if set(audit_ids) != set(catalog_ids):
        fail(
            "audit/catalog IDs differ: "
            f"missing={sorted(set(catalog_ids) - set(audit_ids))}, "
            f"extra={sorted(set(audit_ids) - set(catalog_ids))}"
        )
    if data.get("verified_on") != catalog.get("last_verified"):
        fail("catalog.last_verified and audits.verified_on must match")
    try:
        verified = date.fromisoformat(data["verified_on"])
    except (KeyError, ValueError) as exc:
        fail(f"invalid audit verification date: {exc}")
    age = (date.today() - verified).days
    if age < 0:
        fail("audit verification date is in the future")
    if age > 180:
        fail("resource audit is older than 180 days; re-verify official sources")

    required = {
        "id",
        "repository",
        "repo_snapshot",
        "deployment",
        "default_mode",
        "automation_impact",
        "maximum_effects",
        "data_boundaries",
        "access",
        "limitations",
        "evidence",
    }
    resources = {item["id"]: item for item in catalog["resources"]}
    for item in audits:
        missing = required - item.keys()
        if missing:
            fail(f"audit {item.get('id', '<unknown>')} is missing {sorted(missing)}")
        if item["automation_impact"] not in {"low", "medium", "high"}:
            fail(f"audit {item['id']} has invalid automation impact")
        if not item["maximum_effects"] or not item["data_boundaries"]:
            fail(f"audit {item['id']} must describe effects and data boundaries")
        if len(item["limitations"]) < 40:
            fail(f"audit {item['id']} needs a meaningful limitation")
        if not item["evidence"] or any(
            urlparse(url).scheme != "https" for url in item["evidence"]
        ):
            fail(f"audit {item['id']} needs HTTPS evidence links")
        snapshot = item["repo_snapshot"]
        if not {"archived", "pushed_at", "license_detected"} <= snapshot.keys():
            fail(f"audit {item['id']} has incomplete repository snapshot")
        if not isinstance(snapshot["archived"], bool):
            fail(f"audit {item['id']} archived must be a boolean")
        try:
            datetime.fromisoformat(snapshot["pushed_at"].replace("Z", "+00:00"))
        except (AttributeError, ValueError) as exc:
            fail(f"audit {item['id']} has invalid pushed_at: {exc}")
        canonical_prefix = f"https://github.com/{item['repository']}"
        if not resources[item["id"]]["url"].startswith(canonical_prefix):
            fail(f"audit {item['id']} repository does not match its catalog URL")
        catalog_license = resources[item["id"]]["license"]
        detected = snapshot["license_detected"]
        if catalog_license not in {"N/A", "Unspecified"} and detected not in {
            catalog_license,
            "NOASSERTION",
            "NONE",
        }:
            fail(
                f"audit {item['id']} license mismatch: catalog={catalog_license}, "
                f"snapshot={detected}"
            )
    return data


def validate_readme(data: dict) -> None:
    for filename in ("README.md", "README.vi.md", "README.ja.md"):
        readme = (ROOT / filename).read_text(encoding="utf-8")
        if "<!-- catalog:start -->" not in readme or "<!-- catalog:end -->" not in readme:
            fail(f"{filename} catalog markers are missing")
        catalog_section = readme.split("<!-- catalog:start -->", 1)[1].split(
            "<!-- catalog:end -->", 1
        )[0]
        for item in data["resources"]:
            if catalog_section.count(item["url"]) != 1:
                fail(
                    f"{filename} generated catalog must contain {item['url']} exactly once"
                )


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
        for action_ref in re.findall(r"^\s*-?\s*uses:\s*[^@\s]+@([^\s#]+)", text, re.MULTILINE):
            if not re.fullmatch(r"[0-9a-f]{40}", action_ref):
                fail(
                    f"{path.relative_to(ROOT)} must pin every Action to a full commit SHA; "
                    f"found @{action_ref}"
                )


def validate_local_markdown_links() -> None:
    link_pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for raw_target in link_pattern.findall(text):
            target = raw_target.strip().split(" ", 1)[0].strip("<>")
            parsed = urlparse(target)
            if parsed.scheme or target.startswith("#"):
                continue
            relative_path = unquote(parsed.path)
            if not relative_path:
                continue
            resolved = (path.parent / relative_path).resolve()
            if not resolved.exists():
                fail(
                    f"broken local Markdown link in {path.relative_to(ROOT)}: {raw_target}"
                )


def validate_generated_files() -> None:
    paths = [
        ROOT / "README.md",
        ROOT / "README.vi.md",
        ROOT / "README.ja.md",
        ROOT / "docs/RESOURCE_AUDIT.md",
    ]
    before = {path: path.read_text(encoding="utf-8") for path in paths}
    subprocess.run([sys.executable, str(ROOT / "scripts/render.py")], check=True)
    subprocess.run([sys.executable, str(ROOT / "scripts/render_audit.py")], check=True)
    after = {path: path.read_text(encoding="utf-8") for path in paths}
    changed = [str(path.relative_to(ROOT)) for path in paths if before[path] != after[path]]
    if changed:
        fail(f"generated files are stale: {changed}; run make render")


def main() -> None:
    catalog = validate_catalog()
    audits = validate_audits(catalog)
    validate_readme(catalog)
    validate_workflows()
    validate_local_markdown_links()
    validate_generated_files()
    print(
        f"OK: {len(catalog['resources'])} resources, {len(audits['audits'])} audits, "
        f"{len(catalog['categories'])} categories"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Compare audit snapshots with live GitHub repository metadata."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def resolve_token() -> str:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        return token
    if shutil.which("gh"):
        result = subprocess.run(
            ["gh", "auth", "token"],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    return ""


TOKEN = resolve_token()


def fetch(audit: dict) -> tuple[dict, dict]:
    url = f"https://api.github.com/repos/{audit['repository']}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "awesome-maintainer-defense-metadata-verifier",
        "X-GitHub-Api-Version": "2026-03-10",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    request = Request(url, headers=headers)
    with urlopen(request, timeout=20) as response:
        return audit, json.load(response)


def main() -> None:
    audit_data = json.loads((ROOT / "audits.json").read_text(encoding="utf-8"))
    errors: list[str] = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(fetch, audit): audit for audit in audit_data["audits"]}
        for future in as_completed(futures):
            audit = futures[future]
            try:
                item, live = future.result()
            except (HTTPError, URLError, TimeoutError) as exc:
                errors.append(f"{audit['id']}: metadata request failed: {exc}")
                continue
            expected = item["repo_snapshot"]
            actual = {
                "archived": live["archived"],
                "pushed_at": live["pushed_at"],
                "license_detected": (live.get("license") or {}).get("spdx_id")
                or "NONE",
            }
            drift = [
                f"{field}: expected={expected[field]!r}, live={actual[field]!r}"
                for field in actual
                if expected[field] != actual[field]
            ]
            if drift:
                errors.append(f"{item['id']}: " + "; ".join(drift))
            else:
                print(f"OK: {item['id']}")

    if errors:
        for error in sorted(errors):
            print(f"DRIFT: {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"All {len(audit_data['audits'])} repository snapshots match the live GitHub API")


if __name__ == "__main__":
    main()

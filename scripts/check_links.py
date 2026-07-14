#!/usr/bin/env python3
"""Check catalog, audit-evidence, and documentation links without CI dependencies."""

from __future__ import annotations

import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
def check(item: dict) -> tuple[str, int | None, str]:
    headers = {
        "Accept": "text/html,application/xhtml+xml",
        "User-Agent": "awesome-maintainer-defense-link-checker",
    }
    request = Request(item["url"], headers=headers, method="GET")
    try:
        with urlopen(request, timeout=20) as response:
            return item["id"], response.status, ""
    except HTTPError as exc:
        return item["id"], exc.code, str(exc.reason)
    except (URLError, TimeoutError) as exc:
        return item["id"], None, str(exc)


def main() -> None:
    data = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    audits = json.loads((ROOT / "audits.json").read_text(encoding="utf-8"))
    items = list(data["resources"])
    known_urls = {item["url"] for item in items}
    for audit in audits["audits"]:
        for index, url in enumerate(audit["evidence"], start=1):
            if url not in known_urls:
                items.append({"id": f"{audit['id']}-evidence-{index}", "url": url})
                known_urls.add(url)
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        for index, url in enumerate(
            re.findall(r"\]\((https://[^)\s]+)", path.read_text(encoding="utf-8")),
            start=1,
        ):
            if url not in known_urls:
                label = str(path.relative_to(ROOT)).replace("/", "-")
                items.append({"id": f"docs-{label}-{index}", "url": url})
                known_urls.add(url)
    failures: list[str] = []
    warnings: list[str] = []
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(check, item): item for item in items}
        for future in as_completed(futures):
            item = futures[future]
            resource_id, status, reason = future.result()
            if status in {404, 410}:
                failures.append(f"{resource_id}: HTTP {status} ({item['url']})")
            elif status is None or status >= 400:
                warnings.append(
                    f"{resource_id}: {f'HTTP {status}' if status else 'network error'}"
                    f" {reason} ({item['url']})"
                )
            else:
                print(f"OK {status}: {resource_id}")

    for warning in sorted(warnings):
        print(f"WARNING: {warning}", file=sys.stderr)
    if failures:
        for failure in sorted(failures):
            print(f"ERROR: {failure}", file=sys.stderr)
        raise SystemExit(1)
    print(f"Checked {len(items)} unique links; {len(warnings)} transient warning(s)")


if __name__ == "__main__":
    main()

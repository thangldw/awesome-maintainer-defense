#!/usr/bin/env python3
"""Verify that pinned GitHub Actions still match signed upstream tag commits."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
API = "https://api.github.com"


def token() -> str | None:
    value = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if value:
        return value
    result = subprocess.run(
        ["gh", "auth", "token"], text=True, capture_output=True, check=False
    )
    return result.stdout.strip() if result.returncode == 0 else None


def api(path: str, auth: str | None) -> dict:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "maintainer-defense-pin-audit"}
    if auth:
        headers["Authorization"] = f"Bearer {auth}"
    request = Request(API + path, headers=headers)
    try:
        with urlopen(request, timeout=30) as response:
            return json.load(response)
    except HTTPError as exc:
        detail = exc.read().decode(errors="replace")
        raise RuntimeError(f"GitHub API {exc.code} for {path}: {detail[:200]}") from exc


def resolve_tag(repository: str, tag: str, auth: str | None) -> str:
    ref = api(f"/repos/{repository}/git/ref/tags/{quote(tag, safe='')}", auth)["object"]
    for _ in range(5):
        if ref["type"] == "commit":
            return ref["sha"]
        if ref["type"] != "tag":
            raise RuntimeError(f"{repository}@{tag} resolves to unsupported {ref['type']}")
        ref = api(f"/repos/{repository}/git/tags/{ref['sha']}", auth)["object"]
    raise RuntimeError(f"too many annotated-tag levels for {repository}@{tag}")


def main() -> None:
    data = json.loads((ROOT / "pins.json").read_text(encoding="utf-8"))
    auth = token()
    failures = []
    for pin in data["pins"]:
        label = f"{pin['repository']}@{pin['tag']}"
        try:
            resolved = resolve_tag(pin["repository"], pin["tag"], auth)
            if resolved != pin["sha"]:
                raise RuntimeError(f"tag now resolves to {resolved}, expected {pin['sha']}")
            commit = api(f"/repos/{pin['repository']}/commits/{pin['sha']}", auth)
            if pin.get("commit_verified") and not commit["commit"]["verification"]["verified"]:
                raise RuntimeError("commit signature is no longer reported as verified")
            api(
                f"/repos/{pin['repository']}/contents/{pin['metadata_path']}?ref={pin['sha']}",
                auth,
            )
            print(f"OK {label} -> {pin['sha']} (verified commit, Action metadata present)")
        except (KeyError, RuntimeError) as exc:
            failures.append(f"{label}: {exc}")
    if failures:
        print("PIN VERIFICATION FAILED", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        raise SystemExit(1)
    print(f"OK: {len(data['pins'])} Action pins verified against upstream tags")


if __name__ == "__main__":
    main()

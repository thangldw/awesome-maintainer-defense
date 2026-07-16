#!/usr/bin/env python3
"""Verify release artifacts, wheel metadata, entry points, and Homebrew checksum."""

from __future__ import annotations

import hashlib
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
VERSION = "1.1"
PACKAGE_VERSION = "1.1.0"


def main() -> None:
    standalone = DIST / "maintainer-defense-kit.py"
    checksum_path = standalone.with_suffix(".py.sha256")
    if not standalone.is_file() or not checksum_path.is_file():
        raise SystemExit("standalone release artifacts are missing; run make standalone")
    digest = hashlib.sha256(standalone.read_bytes()).hexdigest()
    if checksum_path.read_text(encoding="ascii") != f"{digest}  {standalone.name}\n":
        raise SystemExit("standalone checksum does not match the release artifact")

    wheels = list(DIST.glob(f"maintainer_defense_kit-{PACKAGE_VERSION}-py3-none-any.whl"))
    if len(wheels) != 1:
        raise SystemExit("expected exactly one v1.1 universal wheel in dist/")
    with zipfile.ZipFile(wheels[0]) as archive:
        names = set(archive.namelist())
        module = "maintainer_defense_kit.py"
        entry_points = (
            f"maintainer_defense_kit-{PACKAGE_VERSION}.dist-info/entry_points.txt"
        )
        metadata = f"maintainer_defense_kit-{PACKAGE_VERSION}.dist-info/METADATA"
        if {module, entry_points, metadata} - names:
            raise SystemExit("wheel is missing its module, metadata, or console entry points")
        entries = archive.read(entry_points).decode("utf-8")
        if "maintainer-defense = maintainer_defense_kit:main" not in entries:
            raise SystemExit("wheel is missing the maintainer-defense entry point")
        if f"Version: {PACKAGE_VERSION}" not in archive.read(metadata).decode("utf-8"):
            raise SystemExit("wheel metadata version is incorrect")

    formula = (ROOT / "Formula/maintainer-defense-kit.rb").read_text(encoding="utf-8")
    if f'/v{VERSION}/maintainer-defense-kit.py"' not in formula:
        raise SystemExit("Homebrew formula does not use the v1.1 release asset")
    match = re.search(r'^  sha256 "([0-9a-f]{64})"$', formula, re.MULTILINE)
    if not match or match.group(1) != digest:
        raise SystemExit("Homebrew formula checksum does not match the standalone artifact")
    print(f"OK standalone SHA256 {digest}")
    print(f"OK wheel {wheels[0].name}")
    print("OK Homebrew formula release URL and checksum")


if __name__ == "__main__":
    main()

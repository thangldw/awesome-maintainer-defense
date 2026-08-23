#!/usr/bin/env python3
"""Verify retained plugin identity assets and documentation diagrams."""

from __future__ import annotations

import hashlib
from pathlib import Path

from verify_diagrams import DIAGRAMS, verify

ROOT = Path(__file__).resolve().parents[1]
ICON_DIGESTS = {
    "assets/plugin-icon.png": "518944a11f4d9e62d2a60728e73698291e2c29ae9ccdd025b575beea691355bb",
    "assets/plugin-icon.svg": "dac8592e6cd607320f612d1f895037ed13bafac0bf52c8787883e459e7614603",
}


def main() -> None:
    errors: list[str] = []
    for relative, expected in ICON_DIGESTS.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing retained plugin icon: {relative}")
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            errors.append(f"plugin icon digest changed: {relative}")

    assets = {path.relative_to(ROOT).as_posix() for path in (ROOT / "assets").glob("*") if path.is_file()}
    if assets != set(ICON_DIGESTS):
        errors.append(
            f"release asset inventory differs: missing={sorted(set(ICON_DIGESTS) - assets)}, "
            f"extra={sorted(assets - set(ICON_DIGESTS))}"
        )

    for slug, budget in DIAGRAMS.items():
        path = ROOT / "docs/diagrams" / f"{slug}.html"
        if not path.is_file():
            errors.append(f"missing diagram: {path.relative_to(ROOT)}")
            continue
        errors.extend(f"{path.relative_to(ROOT)}: {error}" for error in verify(path, slug, budget))

    if errors:
        raise SystemExit("ERROR: " + "\nERROR: ".join(errors))
    print(f"OK: {len(ICON_DIGESTS)} retained plugin icons and {len(DIAGRAMS)} documentation diagrams")


if __name__ == "__main__":
    main()

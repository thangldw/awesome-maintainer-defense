#!/usr/bin/env python3
"""Build a deterministic, dependency-free Maintainer Defense Kit release CLI."""

from __future__ import annotations

import base64
import gzip
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "scripts/install_kit.py"
DIST = ROOT / "dist"
OUTPUT = DIST / "maintainer-defense-kit.py"
SENTINEL = "EMBEDDED_FILES: dict[str, str] = {}"


def asset_paths() -> list[str]:
    paths: list[str] = []
    for language in ("en", "vi", "ja"):
        base = f"kits/maintainer-defense-kit/locales/{language}"
        paths.extend(
            [
                f"{base}/pull_request_template.md",
                f"{base}/bug.yml",
                f"{base}/config.yml.tmpl",
                f"{base}/adoption-record.md",
            ]
        )
        suffix = "" if language == "en" else f".{language}"
        paths.extend(
            [
                f"policies/AI_CONTRIBUTIONS{suffix}.md",
                f"policies/UNSOLICITED_PULL_REQUESTS{suffix}.md",
                "docs/PLAYBOOK.md" if language == "en" else f"docs/{language}/PLAYBOOK.md",
            ]
        )
    paths.extend(
        [
            "kits/maintainer-defense-kit/profiles/observe/.github/workflows/pr-quality.yml",
            "kits/balanced/.github/workflows/pr-quality.yml",
            "kits/workflow-hardening/.github/workflows/dependency-review.yml",
            "kits/workflow-hardening/.github/workflows/zizmor.yml",
        ]
    )
    return sorted(set(paths))


def encoded_assets() -> str:
    rows = []
    for relative in asset_paths():
        path = ROOT / relative
        if not path.is_file():
            raise SystemExit(f"missing release asset: {relative}")
        packed = gzip.compress(path.read_bytes(), compresslevel=9, mtime=0)
        rows.append(f"    {relative!r}: {base64.b64encode(packed).decode('ascii')!r},")
    return "EMBEDDED_FILES: dict[str, str] = {\n" + "\n".join(rows) + "\n}"


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    if source.count(SENTINEL) != 1:
        raise SystemExit("installer embedding sentinel is missing or ambiguous")
    standalone = source.replace(SENTINEL, encoded_assets())
    DIST.mkdir(exist_ok=True)
    OUTPUT.write_text(standalone, encoding="utf-8")
    OUTPUT.chmod(0o755)
    checksum = hashlib.sha256(OUTPUT.read_bytes()).hexdigest()
    checksum_path = OUTPUT.with_suffix(OUTPUT.suffix + ".sha256")
    checksum_path.write_text(f"{checksum}  {OUTPUT.name}\n", encoding="ascii")
    print(f"BUILT {OUTPUT.relative_to(ROOT)} ({len(asset_paths())} embedded assets)")
    print(f"SHA256 {checksum}")


if __name__ == "__main__":
    main()

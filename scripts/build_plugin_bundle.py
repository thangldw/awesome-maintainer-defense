#!/usr/bin/env python3
"""Build a deterministic OpenAI skills-only plugin ZIP and release checksums."""

from __future__ import annotations

import hashlib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
VERSION = "1.1.0"
BUNDLE_NAME = f"awesome-maintainer-defense-openai-skills-v{VERSION}.zip"
FIXED_TIME = (1980, 1, 1, 0, 0, 0)
RELEASE_FILES = (
    "maintainer-defense-kit.py",
    "maintainer-defense-kit.py.sha256",
    "maintainer-defense.py",
    "maintainer-defense.py.sha256",
    f"maintainer_defense_kit-{VERSION}-py3-none-any.whl",
    f"maintainer_defense_kit-{VERSION}.tar.gz",
    BUNDLE_NAME,
)


def source_entries() -> dict[str, Path]:
    entries = {
        ".codex-plugin/plugin.json": ROOT / ".codex-plugin/plugin.json",
        "assets/plugin-icon.png": ROOT / "assets/plugin-icon.png",
        "LICENSE": ROOT / "LICENSE",
        "PRIVACY.md": ROOT / "PRIVACY.md",
        "SUPPORT.md": ROOT / "SUPPORT.md",
        "TERMS.md": ROOT / "TERMS.md",
    }
    skill_root = ROOT / "skills/audit-repository-workflows"
    for path in skill_root.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        relative = path.relative_to(ROOT).as_posix()
        entries[relative] = path
    return entries


def zip_info(name: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, FIXED_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    executable = name.endswith(".py") and "/scripts/" in name
    info.external_attr = ((0o755 if executable else 0o644) & 0xFFFF) << 16
    return info


def build_bundle() -> Path:
    standalone = DIST / "maintainer-defense-kit.py"
    if not standalone.is_file():
        raise SystemExit("missing standalone auditor; run make standalone")
    entries = source_entries()
    bundled_auditor = "skills/audit-repository-workflows/scripts/maintainer-defense.py"
    if bundled_auditor in entries:
        raise SystemExit(f"source tree unexpectedly contains generated {bundled_auditor}")
    payloads = {name: path.read_bytes() for name, path in entries.items()}
    payloads[bundled_auditor] = standalone.read_bytes()
    DIST.mkdir(exist_ok=True)
    output = DIST / BUNDLE_NAME
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in sorted(payloads):
            archive.writestr(zip_info(name), payloads[name], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return output


def build_checksums() -> Path:
    missing = [name for name in RELEASE_FILES if not (DIST / name).is_file()]
    if missing:
        raise SystemExit(f"missing release files: {missing}")
    rows = [
        f"{hashlib.sha256((DIST / name).read_bytes()).hexdigest()}  {name}"
        for name in sorted(RELEASE_FILES)
    ]
    output = DIST / "SHA256SUMS.txt"
    output.write_text("\n".join(rows) + "\n", encoding="ascii")
    return output


def main() -> None:
    bundle = build_bundle()
    checksums = build_checksums()
    print(f"BUILT {bundle.relative_to(ROOT)}")
    print(f"BUILT {checksums.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

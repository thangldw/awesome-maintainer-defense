#!/usr/bin/env python3
"""Preview, install, verify, and safely remove the Maintainer Defense Kit."""

from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KIT_VERSION = "1.0.0"
MANIFEST = ".maintainer-defense-kit.json"
PROFILES = ("observe", "balanced", "hardened")
LANGUAGES = ("en", "vi", "ja")
EMBEDDED_FILES: dict[str, str] = {}


class KitError(Exception):
    pass


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def read(path: str) -> bytes:
    if EMBEDDED_FILES:
        try:
            return gzip.decompress(base64.b64decode(EMBEDDED_FILES[path]))
        except KeyError as exc:
            raise KitError(f"standalone installer is missing embedded asset: {path}") from exc
    return (ROOT / path).read_bytes()


def detect_repository(target: Path) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(target), "remote", "get-url", "origin"],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        return None
    remote = result.stdout.strip()
    match = re.match(
        r"(?:https://github\.com/|ssh://git@github\.com/|git@github\.com:)([^/]+/[^/]+?)(?:\.git)?$",
        remote,
    )
    return match.group(1) if match else None


def valid_repository(value: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", value))


def localized_source(language: str, stem: str) -> str:
    return f"kits/maintainer-defense-kit/locales/{language}/{stem}"


def policy_source(language: str, name: str) -> str:
    suffix = "" if language == "en" else f".{language}"
    return f"policies/{name}{suffix}.md"


def playbook_source(language: str) -> str:
    return "docs/PLAYBOOK.md" if language == "en" else f"docs/{language}/PLAYBOOK.md"


def label_spec(language: str) -> bytes:
    descriptions = {
        "en": "Neutral queue for maintainer review; not an authorship or intent judgment.",
        "vi": "Hàng đợi trung lập để maintainer review; không kết luận về tác giả hay ý định.",
        "ja": "メンテナー確認用の中立的なキュー。作成者や意図を断定するものではありません。",
    }
    payload = {
        "labels": [
            {
                "name": "needs-human-review",
                "color": "D4C5F9",
                "description": descriptions[language],
                "optional_for_manual_triage": ["balanced", "hardened"],
            }
        ]
    }
    return (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode()


def desired_files(profile: str, language: str, repository: str) -> dict[str, bytes]:
    config = read(localized_source(language, "config.yml.tmpl")).replace(
        b"{{REPOSITORY}}", repository.encode()
    )
    files = {
        ".github/PULL_REQUEST_TEMPLATE.md": read(
            localized_source(language, "pull_request_template.md")
        ),
        ".github/ISSUE_TEMPLATE/bug.yml": read(localized_source(language, "bug.yml")),
        ".github/ISSUE_TEMPLATE/config.yml": config,
        ".github/maintainer-defense-labels.json": label_spec(language),
        "docs/maintainer-defense/AI_CONTRIBUTIONS.md": read(
            policy_source(language, "AI_CONTRIBUTIONS")
        ),
        "docs/maintainer-defense/UNSOLICITED_PULL_REQUESTS.md": read(
            policy_source(language, "UNSOLICITED_PULL_REQUESTS")
        ),
        "docs/maintainer-defense/PLAYBOOK.md": read(playbook_source(language)),
        "docs/maintainer-defense/ADOPTION_RECORD.md": read(
            localized_source(language, "adoption-record.md")
        ),
    }
    if profile == "observe":
        files[".github/workflows/pr-quality.yml"] = read(
            "kits/maintainer-defense-kit/profiles/observe/.github/workflows/pr-quality.yml"
        )
    else:
        files[".github/workflows/pr-quality.yml"] = read(
            "kits/balanced/.github/workflows/pr-quality.yml"
        )
    if profile == "hardened":
        files[".github/workflows/dependency-review.yml"] = read(
            "kits/workflow-hardening/.github/workflows/dependency-review.yml"
        )
        files[".github/workflows/zizmor.yml"] = read(
            "kits/workflow-hardening/.github/workflows/zizmor.yml"
        )
    return files


def destination(target: Path, relative: str) -> Path:
    candidate = Path(relative)
    if candidate.is_absolute() or ".." in candidate.parts or not candidate.parts:
        raise KitError(f"unsafe manifest path: {relative!r}")
    path = target.joinpath(*candidate.parts)
    current = target
    for part in candidate.parts:
        current = current / part
        if current.is_symlink():
            raise KitError(f"refusing to traverse symbolic link: {current}")
    return path


def load_manifest(target: Path) -> dict:
    path = target / MANIFEST
    if not path.is_file():
        raise KitError(f"no installation manifest found at {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise KitError(f"invalid installation manifest: {exc}") from exc
    if data.get("schema_version") != 1 or not isinstance(data.get("files"), list):
        raise KitError("unsupported or incomplete installation manifest")
    seen = set()
    for item in data["files"]:
        if not isinstance(item, dict) or set(item) != {"path", "sha256", "owned"}:
            raise KitError("installation manifest has an invalid file entry")
        if (
            not isinstance(item["path"], str)
            or not re.fullmatch(r"[0-9a-f]{64}", item["sha256"])
            or not isinstance(item["owned"], bool)
        ):
            raise KitError("installation manifest has invalid path, digest, or ownership data")
        destination(target, item["path"])
        if item["path"] in seen:
            raise KitError(f"duplicate installation manifest path: {item['path']}")
        seen.add(item["path"])
    return data


def check_manifest_files(target: Path, manifest: dict) -> list[str]:
    problems = []
    for item in manifest["files"]:
        path = destination(target, item["path"])
        if path.is_symlink() or not path.is_file():
            problems.append(f"MISSING  {item['path']}")
        elif digest(path.read_bytes()) != item["sha256"]:
            problems.append(f"MODIFIED {item['path']}")
    return problems


def install(target: Path, profile: str, language: str, repository: str, apply: bool) -> None:
    if (target / MANIFEST).exists():
        raise KitError(f"{MANIFEST} already exists; verify or uninstall the current kit")
    files = desired_files(profile, language, repository)
    conflicts = []
    entries = []
    for relative, content in sorted(files.items()):
        try:
            path = destination(target, relative)
        except KitError as exc:
            conflicts.append(f"CONFLICT {relative}: {exc}")
            continue
        if path.is_symlink() or (path.exists() and not path.is_file()):
            conflicts.append(f"CONFLICT {relative} is not a regular file")
        elif path.is_file() and path.read_bytes() != content:
            conflicts.append(f"CONFLICT {relative} already exists with different content")
        else:
            owned = not path.exists()
            print(f"{'CREATE' if owned else 'KEEP  '} {relative}")
            entries.append({"path": relative, "sha256": digest(content), "owned": owned})
    if conflicts:
        raise KitError("refusing to overwrite existing content:\n" + "\n".join(conflicts))
    if not apply:
        print("DRY RUN: no files written; add --apply to install")
        return

    created: list[Path] = []
    try:
        for relative, content in sorted(files.items()):
            path = destination(target, relative)
            if not path.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
                created.append(path)
        manifest = {
            "schema_version": 1,
            "kit_version": KIT_VERSION,
            "profile": profile,
            "language": language,
            "repository": repository,
            "installed_at": datetime.now(timezone.utc).isoformat(),
            "files": entries,
        }
        temporary_manifest = target / f"{MANIFEST}.tmp"
        temporary_manifest.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        os.replace(temporary_manifest, target / MANIFEST)
    except Exception:
        (target / f"{MANIFEST}.tmp").unlink(missing_ok=True)
        for path in reversed(created):
            path.unlink(missing_ok=True)
            remove_empty_parents(path, target)
        raise
    print(f"INSTALLED {profile}/{language}; manifest: {MANIFEST}")


def verify(target: Path) -> None:
    manifest = load_manifest(target)
    problems = check_manifest_files(target, manifest)
    if problems:
        raise KitError("installation verification failed:\n" + "\n".join(problems))
    print(
        f"VERIFIED {manifest['profile']}/{manifest['language']}: "
        f"{len(manifest['files'])} files match the manifest"
    )


def remove_empty_parents(path: Path, target: Path) -> None:
    current = path.parent
    while current != target and target in current.parents:
        try:
            current.rmdir()
        except OSError:
            break
        current = current.parent


def uninstall(target: Path) -> None:
    manifest = load_manifest(target)
    problems = check_manifest_files(target, manifest)
    owned_problems = [
        problem
        for problem in problems
        if next(
            item["owned"]
            for item in manifest["files"]
            if item["path"] == problem.split(maxsplit=1)[1]
        )
    ]
    if owned_problems:
        raise KitError(
            "refusing to remove modified or missing installer-owned files:\n"
            + "\n".join(owned_problems)
        )
    removed = []
    for item in reversed(manifest["files"]):
        if not item["owned"]:
            continue
        path = destination(target, item["path"])
        path.unlink()
        removed.append(path)
        remove_empty_parents(path, target)
    (target / MANIFEST).unlink()
    print(f"UNINSTALLED {len(removed)} installer-owned files; pre-existing files were kept")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, type=Path, help="target repository")
    parser.add_argument("--profile", choices=PROFILES, default="observe")
    parser.add_argument("--language", choices=LANGUAGES, default="en")
    parser.add_argument("--repo", help="GitHub OWNER/REPOSITORY (auto-detected when possible)")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true", help="write the previewed installation")
    mode.add_argument("--verify", action="store_true", help="verify files against the manifest")
    mode.add_argument("--uninstall", action="store_true", help="remove unmodified installer-owned files")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target = args.target.expanduser().resolve()
    try:
        if not target.is_dir():
            raise KitError(f"target is not a directory: {target}")
        if args.verify:
            verify(target)
            return
        if args.uninstall:
            uninstall(target)
            return
        repository = args.repo or detect_repository(target) or "OWNER/REPOSITORY"
        if not valid_repository(repository):
            raise KitError(f"invalid GitHub repository: {repository}")
        if args.apply and repository == "OWNER/REPOSITORY":
            raise KitError("--repo OWNER/REPOSITORY is required when no GitHub origin is detectable")
        install(target, args.profile, args.language, repository, args.apply)
    except (KitError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()

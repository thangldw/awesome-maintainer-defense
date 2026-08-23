#!/usr/bin/env python3
"""Verify checked-in pilot evidence against its pinned Git revisions."""

from __future__ import annotations

import hashlib
import io
import json
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
RUNTIME_PATHS = (
    "scripts/install_kit.py",
    "scripts/build_standalone.py",
    "auditor-rules.json",
    "maintainer-defense-config.schema.json",
    ":(glob)kits/maintainer-defense-kit/**",
    ":(glob)kits/balanced/.github/**",
    ":(glob)kits/workflow-hardening/.github/**",
    ":(glob)policies/**",
    "docs/PLAYBOOK.md",
    "docs/vi/PLAYBOOK.md",
    "docs/ja/PLAYBOOK.md",
)
INPUT_NAMES = ("metadata.json", "raw-report.json", "effective-report.json", "labels.json")


class PilotEvidenceError(Exception):
    pass


def load_canonical_json(path: Path) -> dict:
    try:
        text = path.read_text(encoding="utf-8")
        value = json.loads(text)
    except (OSError, json.JSONDecodeError) as exc:
        raise PilotEvidenceError(f"cannot read {path}: {exc}") from exc
    if json.dumps(value, ensure_ascii=False, indent=2) + "\n" != text:
        raise PilotEvidenceError(f"{path} is not canonical indented JSON")
    return value


def run_git(root: Path, *arguments: str, capture: bool = False) -> subprocess.CompletedProcess:
    result = subprocess.run(
        ["git", "-C", str(root), *arguments],
        capture_output=capture,
        check=False,
    )
    if result.returncode:
        detail = result.stderr.decode("utf-8", errors="replace").strip() if capture else ""
        raise PilotEvidenceError(f"git {' '.join(arguments)} failed{': ' + detail if detail else ''}")
    return result


def extract_commit(root: Path, revision: str, destination: Path) -> None:
    archive = run_git(root, "archive", "--format=tar", revision, capture=True).stdout
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as bundle:
        for member in bundle.getmembers():
            path = PurePosixPath(member.name)
            link = PurePosixPath(member.linkname) if member.linkname else None
            if path.is_absolute() or ".." in path.parts:
                raise PilotEvidenceError("git archive contains an unsafe path")
            if link and (link.is_absolute() or ".." in link.parts):
                raise PilotEvidenceError("git archive contains an unsafe link")
        bundle.extractall(destination)


def normalize_report_target(report: dict, expected: dict) -> dict:
    normalized = dict(report)
    normalized["target"] = expected["target"]
    return normalized


def verify_generated_outputs(root: Path, pilot_dir: Path) -> None:
    for name in INPUT_NAMES:
        load_canonical_json(pilot_dir / name)
    load_canonical_json(pilot_dir / "pilot.json")
    with tempfile.TemporaryDirectory() as tmp:
        temporary = Path(tmp)
        generated_json = temporary / "pilot.json"
        generated_markdown = temporary / "README.md"
        result = subprocess.run(
            [
                sys.executable,
                str(root / "scripts/build_pilot_bundle.py"),
                "--metadata", str(pilot_dir / "metadata.json"),
                "--raw-report", str(pilot_dir / "raw-report.json"),
                "--effective-report", str(pilot_dir / "effective-report.json"),
                "--labels", str(pilot_dir / "labels.json"),
                "--json-output", str(generated_json),
                "--markdown-output", str(generated_markdown),
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode:
            raise PilotEvidenceError(result.stderr.strip() or "pilot bundle regeneration failed")
        for expected, generated in (
            (pilot_dir / "pilot.json", generated_json),
            (pilot_dir / "README.md", generated_markdown),
        ):
            if expected.read_bytes() != generated.read_bytes():
                raise PilotEvidenceError(f"{expected} differs from regenerated evidence")


def verify_provenance(root: Path, pilot_dir: Path) -> None:
    metadata = load_canonical_json(pilot_dir / "metadata.json")
    if metadata["pilot_id"] != pilot_dir.name:
        raise PilotEvidenceError("pilot_id does not match its directory")
    if metadata["command"] != "python3 dist/maintainer-defense-kit.py audit . --format json":
        raise PilotEvidenceError("pilot command is not the reproducible dogfood command")
    source_commit = metadata["source_commit"]
    target_commit = metadata["target_commit"]
    for revision in (source_commit, target_commit):
        run_git(root, "cat-file", "-e", f"{revision}^{{commit}}", capture=True)
    diff = subprocess.run(
        ["git", "-C", str(root), "diff", "--quiet", source_commit, "--", *RUNTIME_PATHS],
        check=False,
    )
    if diff.returncode == 1:
        raise PilotEvidenceError("auditor runtime differs from the recorded source commit")
    if diff.returncode:
        raise PilotEvidenceError("cannot verify runtime-source provenance")
    raw_expected = load_canonical_json(pilot_dir / "raw-report.json")
    effective_expected = load_canonical_json(pilot_dir / "effective-report.json")
    with tempfile.TemporaryDirectory() as tmp:
        temporary = Path(tmp)
        source = temporary / "source"
        target = temporary / "target"
        source.mkdir()
        target.mkdir()
        extract_commit(root, source_commit, source)
        extract_commit(root, target_commit, target)
        build = subprocess.run(
            [sys.executable, str(source / "scripts/build_standalone.py")],
            cwd=source,
            text=True,
            capture_output=True,
            check=False,
        )
        if build.returncode:
            raise PilotEvidenceError(build.stderr.strip() or "pinned standalone build failed")
        standalone = source / "dist/maintainer-defense-kit.py"
        standalone_digest = hashlib.sha256(standalone.read_bytes()).hexdigest()
        if standalone_digest != metadata["standalone_sha256"]:
            raise PilotEvidenceError("pinned standalone digest differs from pilot metadata")
        audit = subprocess.run(
            [sys.executable, str(standalone), "audit", str(target), "--format", "json"],
            text=True,
            capture_output=True,
            check=False,
        )
        if audit.returncode:
            raise PilotEvidenceError(audit.stderr.strip() or "pinned target audit failed")
        try:
            regenerated = json.loads(audit.stdout)
        except json.JSONDecodeError as exc:
            raise PilotEvidenceError(f"pinned target audit emitted invalid JSON: {exc}") from exc
        for label, expected in (("raw", raw_expected), ("effective", effective_expected)):
            if normalize_report_target(regenerated, expected) != expected:
                raise PilotEvidenceError(f"{label} report differs from the pinned target audit")


def verify_pilot(root: Path, pilot_dir: Path) -> None:
    verify_generated_outputs(root, pilot_dir)
    verify_provenance(root, pilot_dir)


def main() -> None:
    pilot_dirs = sorted(path for path in (ROOT / "pilots").glob("20*") if path.is_dir())
    if not pilot_dirs:
        raise SystemExit("ERROR: no dated pilot evidence found")
    try:
        for pilot_dir in pilot_dirs:
            verify_pilot(ROOT, pilot_dir)
            print(f"OK {pilot_dir.relative_to(ROOT)}")
    except (OSError, PilotEvidenceError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()

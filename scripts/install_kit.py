#!/usr/bin/env python3
"""Audit repositories and preview, install, verify, or remove the Maintainer Defense Kit."""

from __future__ import annotations

import argparse
import base64
import difflib
import gzip
import hashlib
import io
import json
import os
import re
import shlex
import subprocess
import sys
import tarfile
import tempfile
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
KIT_VERSION = "1.1.0"
AUDITOR_VERSION = "1.1.0"
RULE_HELP_BASE = (
    "https://github.com/thangldw/awesome-maintainer-defense/"
    f"blob/v{AUDITOR_VERSION}/docs/AUDITOR_RULES.md"
)
MANIFEST = ".maintainer-defense-kit.json"
PROFILES = ("observe", "balanced", "hardened")
LANGUAGES = ("en", "vi", "ja")
EMBEDDED_FILES: dict[str, str] = {}
_RULE_CATALOG: dict[str, dict] | None = None


class KitError(Exception):
    pass


class UsageArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        self.print_usage(sys.stderr)
        self.exit(1, f"{self.prog}: error: {message}\n")


SEVERITY_ORDER = {"critical": 4, "high": 3, "medium": 2, "low": 1, "note": 0}
WORKFLOW_SUFFIXES = {".yml", ".yaml"}
PRIVILEGED_EVENTS = ("pull_request_target", "workflow_run", "issue_comment")
UNTRUSTED_EXPRESSION = re.compile(
    r"\$\{\{\s*github\.(?:event\.(?:issue|pull_request|comment|review|head_commit)(?:[^}]*)|head_ref|ref_name)\s*\}\}"
)
WRITE_PERMISSION_SCOPES = frozenset(
    {
        "actions",
        "artifact-metadata",
        "attestations",
        "checks",
        "code-quality",
        "contents",
        "deployments",
        "discussions",
        "id-token",
        "issues",
        "packages",
        "pages",
        "pull-requests",
        "security-events",
        "statuses",
    }
)
IDENTITY_PROXIES = {
    "detect-spam-usernames": "username pattern",
    "min-account-age": "account age",
    "max-daily-forks": "fork activity",
    "require-public-profile": "public-profile state",
    "min-profile-completeness": "profile completeness",
    "min-global-merge-ratio": "global merge history",
    "require-commit-author-match": "commit-author identity",
}


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def read(path: str) -> bytes:
    if EMBEDDED_FILES:
        try:
            return gzip.decompress(base64.b64decode(EMBEDDED_FILES[path]))
        except KeyError as exc:
            raise KitError(f"standalone installer is missing embedded asset: {path}") from exc
    return (ROOT / path).read_bytes()


def rule_catalog() -> dict[str, dict]:
    global _RULE_CATALOG
    if _RULE_CATALOG is not None:
        return _RULE_CATALOG
    try:
        data = json.loads(read("auditor-rules.json"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise KitError(f"invalid embedded auditor rule registry: {exc}") from exc
    if data.get("schema_version") != 1 or not isinstance(data.get("rules"), list):
        raise KitError("unsupported or incomplete auditor rule registry")
    catalog: dict[str, dict] = {}
    required = {
        "id", "title", "default_severity", "description", "safe_remediation",
        "help_anchor", "mappings",
    }
    for item in data["rules"]:
        if not isinstance(item, dict) or set(item) != required:
            raise KitError("auditor rule registry contains an invalid entry")
        rule_id = item["id"]
        if rule_id in catalog or not re.fullmatch(r"MD-(?:GOV|WF|MOD)-[0-9]{3}", rule_id):
            raise KitError(f"invalid or duplicate auditor rule ID: {rule_id!r}")
        if item["default_severity"] not in SEVERITY_ORDER:
            raise KitError(f"invalid severity for auditor rule {rule_id}")
        catalog[rule_id] = item
    _RULE_CATALOG = catalog
    return catalog


def rule_metadata(rule_id: str) -> dict:
    try:
        return rule_catalog()[rule_id]
    except KeyError as exc:
        raise KitError(f"finding uses undocumented rule ID: {rule_id}") from exc


def rule_help_uri(rule_id: str) -> str:
    return f"{RULE_HELP_BASE}#{rule_metadata(rule_id)['help_anchor']}"


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


def relative_path(target: Path, path: Path) -> str:
    return path.relative_to(target).as_posix()


def line_column(text: str, needle: str) -> tuple[int, int]:
    offset = text.find(needle)
    if offset < 0:
        return 1, 1
    line = text.count("\n", 0, offset) + 1
    previous = text.rfind("\n", 0, offset)
    return line, offset - previous


def unified_patch(path: str, before: str, after: str) -> str:
    return "".join(
        difflib.unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile=f"a/{path}",
            tofile=f"b/{path}",
        )
    )


def make_finding(
    rule_id: str,
    severity: str,
    confidence: str,
    path: str,
    line: int,
    column: int,
    message: str,
    threat_scenario: str,
    recommendation: str,
    *,
    before: str | None = None,
    after: str | None = None,
    fix_safety: str | None = None,
) -> dict:
    metadata = rule_metadata(rule_id)
    if severity != metadata["default_severity"]:
        raise KitError(
            f"finding severity {severity!r} does not match {rule_id} registry severity "
            f"{metadata['default_severity']!r}"
        )
    finding = {
        "rule_id": rule_id,
        "severity": severity,
        "confidence": confidence,
        "location": {"path": path, "line": line, "column": column},
        "message": message,
        "threat_scenario": threat_scenario,
        "recommendation": recommendation,
        "fingerprint": hashlib.sha256(
            f"{rule_id}:{path}:{message}".encode()
        ).hexdigest()[:24],
        "fix": {"available": False},
    }
    if before is not None and after is not None and before != after:
        finding["fix"] = {
            "available": True,
            "safety": fix_safety or "review-required",
            "patch": unified_patch(path, before, after),
        }
    return finding


def replace_line_value(text: str, line_index: int, value: str) -> str:
    lines = text.splitlines(keepends=True)
    ending = "\n" if lines[line_index].endswith("\n") else ""
    prefix = lines[line_index].split(":", 1)[0]
    comment = ""
    if " #" in lines[line_index]:
        comment = " #" + lines[line_index].split(" #", 1)[1].rstrip("\n")
    lines[line_index] = f"{prefix}: {value}{comment}{ending}"
    return "".join(lines)


def governance_findings(target: Path) -> list[dict]:
    findings: list[dict] = []
    security_candidates = (
        target / "SECURITY.md",
        target / ".github/SECURITY.md",
        target / "docs/SECURITY.md",
    )
    if not any(path.is_file() for path in security_candidates):
        findings.append(
            make_finding(
                "MD-GOV-001", "medium", "high", "SECURITY.md", 1, 1,
                "No repository security policy was found.",
                "A reporter may disclose a vulnerability publicly or abandon the report because no private, supported route is documented.",
                "Add SECURITY.md with supported versions, a private reporting route, response expectations, and a warning not to include secrets in public issues.",
            )
        )

    codeowners_candidates = (
        target / ".github/CODEOWNERS",
        target / "CODEOWNERS",
        target / "docs/CODEOWNERS",
    )
    codeowners = next((path for path in codeowners_candidates if path.is_file()), None)
    if codeowners is None:
        findings.append(
            make_finding(
                "MD-GOV-002", "medium", "high", ".github/CODEOWNERS", 1, 1,
                "No CODEOWNERS file protects repository control-plane files.",
                "A workflow, issue-template, or policy change can be merged without review from the people responsible for repository security and moderation.",
                "Add a real owner for .github/workflows/, .github/ISSUE_TEMPLATE/, SECURITY.md, and CODEOWNERS; do not use a placeholder account.",
            )
        )
    else:
        content = codeowners.read_text(encoding="utf-8", errors="replace")
        if not re.search(r"(?m)^\s*(?:/)?\.github(?:/|\s)", content):
            rel = relative_path(target, codeowners)
            findings.append(
                make_finding(
                    "MD-GOV-003", "medium", "medium", rel, 1, 1,
                    "CODEOWNERS does not explicitly cover .github/.",
                    "A broad ownership rule may be changed or bypassed without an explicit review boundary for workflows and repository automation.",
                    "Add an explicit /.github/ ownership rule naming the responsible team.",
                )
            )

    issue_dir = target / ".github/ISSUE_TEMPLATE"
    issue_forms = (
        [path for path in issue_dir.iterdir() if path.suffix in WORKFLOW_SUFFIXES and path.name != "config.yml"]
        if issue_dir.is_dir() else []
    )
    if not issue_forms:
        findings.append(
            make_finding(
                "MD-GOV-004", "low", "high", ".github/ISSUE_TEMPLATE", 1, 1,
                "No structured issue form was found.",
                "Unstructured reports can omit reproduction steps and expected behavior, increasing maintainer triage cost and security-report noise.",
                "Add at least one YAML issue form that requests reproducible evidence and directs vulnerabilities to a private reporting channel.",
            )
        )

    update_configs = (
        target / ".github/dependabot.yml",
        target / ".github/dependabot.yaml",
        target / "renovate.json",
        target / ".github/renovate.json",
        target / "renovate.json5",
    )
    if not any(path.is_file() for path in update_configs):
        findings.append(
            make_finding(
                "MD-GOV-005", "low", "high", ".github", 1, 1,
                "No machine-readable dependency update policy was found.",
                "Immutable Action and package pins can remain on vulnerable versions when no update mechanism or review cadence is configured.",
                "Configure Dependabot or Renovate for the ecosystems used by the repository, including github-actions where applicable.",
            )
        )

    local_expectation = any(
        pattern in path.read_text(encoding="utf-8", errors="replace").lower()
        for path in list(target.glob("*.md")) + list((target / "docs").glob("*.md") if (target / "docs").is_dir() else [])
        for pattern in ("branch protection", "ruleset", "required review", "protected branch")
    )
    settings_files = (target / ".github/settings.yml", target / ".github/repository.yml")
    if not local_expectation and not any(path.is_file() for path in settings_files):
        findings.append(
            make_finding(
                "MD-GOV-006", "note", "medium", ".github", 1, 1,
                "Branch-protection expectations are not documented in the checkout.",
                "Contributors and maintainers cannot tell which reviews, status checks, or force-push restrictions are intended, and local auditing cannot detect configuration drift.",
                "Document expected rulesets or branch protections and verify actual settings separately with a read-only GitHub API audit.",
            )
        )
    return findings


def yaml_block(lines: list[str], index: int, indentation: int) -> str:
    """Return the surrounding indentation-delimited YAML block."""
    start = index
    while start > 0:
        candidate = lines[start]
        stripped = candidate.lstrip()
        current = len(candidate) - len(stripped)
        if current == indentation and stripped and not stripped.startswith("#"):
            break
        start -= 1
    end = index + 1
    while end < len(lines):
        candidate = lines[end]
        stripped = candidate.lstrip()
        current = len(candidate) - len(stripped)
        if stripped and not stripped.startswith("#") and current <= indentation:
            break
        end += 1
    return "\n".join(lines[start:end])


def declared_write_scopes(lines: list[str], indentation: int) -> tuple[bool, set[str]]:
    prefix = " " * indentation
    for index, line in enumerate(lines):
        match = re.match(rf"^{re.escape(prefix)}permissions\s*:\s*(.*?)\s*$", line)
        if not match:
            continue
        value = match.group(1).split("#", 1)[0].strip()
        if value == "write-all":
            return True, set(WRITE_PERMISSION_SCOPES)
        if value in {"{}", "read-all"}:
            return True, set()
        scopes: set[str] = set()
        for candidate in lines[index + 1 :]:
            stripped = candidate.lstrip()
            current = len(candidate) - len(stripped)
            if stripped and not stripped.startswith("#") and current <= indentation:
                break
            permission = re.match(r"\s*([a-z-]+)\s*:\s*write\b", candidate)
            if permission and permission.group(1) in WRITE_PERMISSION_SCOPES:
                scopes.add(permission.group(1))
        return True, scopes
    return False, set()


def permission_scope(lines: list[str], evidence_index: int) -> set[str]:
    """Return effective write or credential-minting scopes for one job."""
    job_block = yaml_block(lines, evidence_index, 2).splitlines()
    job_declared, job_scopes = declared_write_scopes(job_block, 4)
    if job_declared:
        return job_scopes
    _, top_scopes = declared_write_scopes(lines, 0)
    return top_scopes


def permission_scope_writes(lines: list[str], evidence_index: int) -> bool:
    return bool(permission_scope(lines, evidence_index))


def run_block_injection(lines: list[str], run_index: int) -> tuple[int, int] | None:
    """Locate a direct untrusted expression in one run scalar or block."""
    line = lines[run_index]
    run_match = re.match(r"^(\s*)(?:-\s*)?run\s*:\s*(.*)$", line)
    if not run_match:
        return None
    value = run_match.group(2)
    inline = UNTRUSTED_EXPRESSION.search(value)
    if inline:
        value_column = line.find(value) if value else len(line)
        return run_index + 1, value_column + inline.start() + 1
    if value and not re.fullmatch(r"[|>][+-]?\d*", value.split("#", 1)[0].strip()):
        return None
    indentation = len(run_match.group(1))
    for index in range(run_index + 1, len(lines)):
        candidate = lines[index]
        stripped = candidate.lstrip()
        current = len(candidate) - len(stripped)
        if stripped and not stripped.startswith("#") and current <= indentation:
            break
        match = UNTRUSTED_EXPRESSION.search(candidate)
        if match:
            return index + 1, match.start() + 1
    return None


@dataclass(frozen=True)
class WorkflowRecord:
    path: Path
    name: str
    triggers: frozenset[str]
    workflow_run_names: frozenset[str]
    uploads_artifact: bool
    uploaded_artifact_names: frozenset[str]
    downloads_artifact: bool
    executes_downloaded_content: bool
    executed_artifact_names: frozenset[str]
    has_privileged_authority: bool


@dataclass(frozen=True)
class Suppression:
    rule_id: str
    reason: str
    owner: str
    expires_on: date
    fingerprint: str | None = None
    path: str | None = None
    expired: bool = False


def load_suppressions(path: Path, today: date) -> list[Suppression]:
    try:
        data = json.loads(path.expanduser().read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise KitError(f"invalid suppression JSON {path}: {exc}") from exc
    if not isinstance(data, dict) or set(data) != {"schema_version", "suppressions"}:
        raise KitError("suppression config must contain only schema_version and suppressions")
    if data["schema_version"] != 1 or not isinstance(data["suppressions"], list):
        raise KitError("suppression config must use schema_version 1 and a suppressions array")
    required = {"rule_id", "reason", "owner", "expires_on"}
    allowed = required | {"fingerprint", "path"}
    entries: list[Suppression] = []
    selectors: set[tuple[str, str | None, str | None]] = set()
    for index, item in enumerate(data["suppressions"]):
        label = f"suppression #{index + 1}"
        if not isinstance(item, dict) or not required <= set(item) or not set(item) <= allowed:
            raise KitError(f"{label} has missing or unknown fields")
        rule_id = item["rule_id"]
        if not isinstance(rule_id, str) or rule_id not in rule_catalog():
            raise KitError(f"{label} uses unknown rule_id: {rule_id!r}")
        reason = item["reason"]
        owner = item["owner"]
        if not isinstance(reason, str) or not reason.strip():
            raise KitError(f"{label} requires a non-empty reason")
        if not isinstance(owner, str) or not owner.strip():
            raise KitError(f"{label} requires a non-empty owner")
        raw_expiry = item["expires_on"]
        if not isinstance(raw_expiry, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw_expiry):
            raise KitError(f"{label} expires_on must use YYYY-MM-DD")
        try:
            expires_on = date.fromisoformat(raw_expiry)
        except ValueError as exc:
            raise KitError(f"{label} has invalid expires_on date: {raw_expiry}") from exc
        fingerprint = item.get("fingerprint")
        relative = item.get("path")
        if fingerprint is None and relative is None:
            raise KitError(f"{label} requires fingerprint or path")
        if fingerprint is not None and (
            not isinstance(fingerprint, str) or not re.fullmatch(r"[0-9a-f]{24}", fingerprint)
        ):
            raise KitError(f"{label} fingerprint must be 24 lowercase hexadecimal characters")
        if relative is not None:
            if not isinstance(relative, str) or not relative or "\\" in relative:
                raise KitError(f"{label} path must be a non-empty repository-relative POSIX path")
            normalized = PurePosixPath(relative)
            if normalized.is_absolute() or ".." in normalized.parts or str(normalized) != relative:
                raise KitError(f"{label} path must be a normalized repository-relative POSIX path")
        selector = (rule_id, fingerprint, relative)
        if selector in selectors:
            raise KitError(f"duplicate suppression selector for {rule_id}")
        selectors.add(selector)
        entries.append(
            Suppression(
                rule_id=rule_id,
                reason=reason.strip(),
                owner=owner.strip(),
                expires_on=expires_on,
                fingerprint=fingerprint,
                path=relative,
                expired=expires_on < today,
            )
        )
    return entries


def apply_suppressions(
    report: dict, entries: list[Suppression]
) -> tuple[dict, int, list[str]]:
    active = [(index, entry) for index, entry in enumerate(entries) if not entry.expired]
    warnings = [
        f"Suppression {entry.rule_id} owned by {entry.owner} expired on {entry.expires_on.isoformat()}"
        for entry in entries
        if entry.expired
    ]
    matched: set[int] = set()
    emitted: list[dict] = []
    suppressed = 0
    for finding in report["findings"]:
        matching = []
        for index, entry in active:
            if entry.rule_id != finding["rule_id"]:
                continue
            if entry.fingerprint is not None and entry.fingerprint != finding["fingerprint"]:
                continue
            if entry.path is not None and entry.path != finding["location"]["path"]:
                continue
            matching.append(index)
        if matching:
            matched.update(matching)
            suppressed += 1
        else:
            emitted.append(finding)
    unmatched = [entry for index, entry in active if index not in matched]
    if unmatched:
        entry = unmatched[0]
        selector = entry.fingerprint or entry.path
        raise KitError(
            f"active suppression {entry.rule_id} selector {selector!r} matches no finding"
        )
    return report_with_findings(report, emitted), suppressed, warnings


def inline_yaml_values(value: str) -> frozenset[str]:
    value = value.split("#", 1)[0].strip()
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]
    return frozenset(
        item.strip().strip("\"'")
        for item in value.split(",")
        if item.strip().strip("\"'")
    )


def workflow_triggers(lines: list[str]) -> frozenset[str]:
    for index, line in enumerate(lines):
        match = re.match(r"^on\s*:\s*(.*?)\s*$", line)
        if not match:
            continue
        value = match.group(1)
        if value:
            return inline_yaml_values(value)
        triggers: set[str] = set()
        for candidate in lines[index + 1 :]:
            stripped = candidate.lstrip()
            indentation = len(candidate) - len(stripped)
            if stripped and not stripped.startswith("#") and indentation == 0:
                break
            event = re.match(r"^  ([A-Za-z_][A-Za-z0-9_-]*)\s*:", candidate)
            if event:
                triggers.add(event.group(1))
        return frozenset(triggers)
    return frozenset()


def workflow_run_sources(lines: list[str]) -> frozenset[str]:
    for index, line in enumerate(lines):
        if not re.match(r"^  workflow_run\s*:\s*$", line):
            continue
        for source_index in range(index + 1, len(lines)):
            candidate = lines[source_index]
            stripped = candidate.lstrip()
            indentation = len(candidate) - len(stripped)
            if stripped and not stripped.startswith("#") and indentation <= 2:
                break
            match = re.match(r"^    workflows\s*:\s*(.*?)\s*$", candidate)
            if not match:
                continue
            value = match.group(1)
            if value:
                return inline_yaml_values(value)
            names: set[str] = set()
            for item in lines[source_index + 1 :]:
                item_stripped = item.lstrip()
                item_indentation = len(item) - len(item_stripped)
                if item_stripped and not item_stripped.startswith("#") and item_indentation <= 4:
                    break
                item_match = re.match(r"^\s+-\s*(.*?)\s*$", item)
                if item_match:
                    names.update(inline_yaml_values(item_match.group(1)))
            return frozenset(names)
    return frozenset()


def yaml_job_bounds(lines: list[str], evidence_index: int) -> tuple[int, int]:
    start = evidence_index
    while start >= 0 and not re.match(r"^  [A-Za-z0-9_.-]+\s*:\s*$", lines[start]):
        start -= 1
    if start < 0:
        return evidence_index, evidence_index + 1
    end = start + 1
    while end < len(lines):
        stripped = lines[end].lstrip()
        indentation = len(lines[end]) - len(stripped)
        if stripped and not stripped.startswith("#") and indentation <= 2:
            break
        end += 1
    return start, end


def run_scalar_text(lines: list[str], run_index: int) -> str:
    match = re.match(r"^(\s*)(?:-\s*)?run\s*:\s*(.*)$", lines[run_index])
    if not match:
        return ""
    chunks = [match.group(2)]
    indentation = len(match.group(1))
    for candidate in lines[run_index + 1 :]:
        stripped = candidate.lstrip()
        current = len(candidate) - len(stripped)
        if stripped and not stripped.startswith("#") and current <= indentation:
            break
        chunks.append(stripped)
    return "\n".join(chunks)


def action_inputs(lines: list[str], action_index: int) -> dict[str, str]:
    action_indent = len(lines[action_index]) - len(lines[action_index].lstrip())
    with_indent: int | None = None
    inputs: dict[str, str] = {}
    for candidate in lines[action_index + 1 :]:
        stripped = candidate.lstrip()
        indentation = len(candidate) - len(stripped)
        if stripped and indentation <= action_indent:
            break
        if re.match(r"^with\s*:\s*$", stripped):
            with_indent = indentation
            continue
        if with_indent is None:
            continue
        if stripped and indentation <= with_indent:
            break
        match = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*?)\s*$", stripped)
        if match:
            inputs[match.group(1)] = match.group(2).split(" #", 1)[0].strip().strip("\"'")
    return inputs


def literal_relative_path(value: str) -> PurePosixPath | None:
    if not value or "${{" in value or any(character in value for character in "`$<>\\"):
        return None
    path = PurePosixPath(value.removeprefix("./"))
    if path.is_absolute() or ".." in path.parts:
        return None
    return path


def executed_local_paths(command: str) -> frozenset[PurePosixPath]:
    paths: set[PurePosixPath] = set()
    interpreters = {"bash", "sh", "python", "python3", "node", "ruby", "perl"}
    for segment in re.split(r"(?:&&|\|\||[;|\n])", command):
        try:
            tokens = shlex.split(segment, comments=True, posix=True)
        except ValueError:
            continue
        while tokens and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", tokens[0]):
            tokens.pop(0)
        if not tokens:
            continue
        candidate: str | None = None
        executable = PurePosixPath(tokens[0]).name
        if executable in interpreters:
            for token in tokens[1:]:
                if token in {"-c", "-m"}:
                    candidate = None
                    break
                if not token.startswith("-"):
                    candidate = token
                    break
        elif tokens[0] in {"source", "."} and len(tokens) > 1:
            candidate = tokens[1]
        elif "/" in tokens[0] and not tokens[0].startswith("/"):
            candidate = tokens[0]
        if candidate:
            path = literal_relative_path(candidate)
            if path is not None:
                paths.add(path)
    return frozenset(paths)


def path_is_within(path: PurePosixPath, destination: PurePosixPath) -> bool:
    return destination == PurePosixPath(".") or path == destination or destination in path.parents


def index_workflows(target: Path) -> list[WorkflowRecord]:
    records: list[WorkflowRecord] = []
    workflow_dir = target / ".github/workflows"
    if not workflow_dir.is_dir():
        return records
    for path in sorted(workflow_dir.rglob("*")):
        if not path.is_file() or path.suffix not in WORKFLOW_SUFFIXES:
            continue
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        name_match = next((re.match(r"^name\s*:\s*(.*?)\s*$", line) for line in lines if re.match(r"^name\s*:", line)), None)
        name = name_match.group(1).strip("\"'") if name_match else path.stem
        upload_indexes = [
            index for index, line in enumerate(lines)
            if re.search(r"uses:\s*[\"']?actions/upload-artifact@", line)
        ]
        uploaded_names: set[str] = set()
        for upload_index in upload_indexes:
            upload_name = action_inputs(lines, upload_index).get("name", "artifact")
            if upload_name and "${{" not in upload_name:
                uploaded_names.add(upload_name)
        download_indexes = [
            index for index, line in enumerate(lines)
            if re.search(r"uses:\s*[\"']?actions/download-artifact@", line)
        ]
        executed_names: set[str] = set()
        privileged = False
        for download_index in download_indexes:
            inputs = action_inputs(lines, download_index)
            destination = literal_relative_path(inputs.get("path", "."))
            remote_run = "github.event.workflow_run.id" in inputs.get("run-id", "")
            authenticated = bool(inputs.get("github-token"))
            if destination is None or not remote_run or not authenticated:
                continue
            _, job_end = yaml_job_bounds(lines, download_index)
            for execution_index in range(download_index + 1, job_end):
                if re.match(r"^\s*(?:-\s*)?run\s*:", lines[execution_index]):
                    executed_paths = executed_local_paths(
                        run_scalar_text(lines, execution_index)
                    )
                else:
                    local_action = re.search(
                        r"uses:\s*[\"']?(\./[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*)",
                        lines[execution_index],
                    )
                    executed_path = (
                        literal_relative_path(local_action.group(1)) if local_action else None
                    )
                    executed_paths = (
                        frozenset({executed_path})
                        if executed_path is not None
                        else frozenset()
                    )
                if not any(
                    path_is_within(executed_path, destination)
                    for executed_path in executed_paths
                ):
                    continue
                job_start, _ = yaml_job_bounds(lines, execution_index)
                job_text = "\n".join(lines[job_start:job_end])
                execution_is_privileged = bool(
                    permission_scope(lines, execution_index)
                    or re.search(r"\$\{\{\s*secrets\.|secrets:\s*inherit", job_text)
                )
                if execution_is_privileged:
                    name = inputs.get("name")
                    if name and "${{" not in name:
                        executed_names.add(name)
                    elif not name:
                        executed_names.add("*")
                    privileged = True
                break
        records.append(
            WorkflowRecord(
                path=path,
                name=name,
                triggers=workflow_triggers(lines),
                workflow_run_names=workflow_run_sources(lines),
                uploads_artifact=bool(upload_indexes),
                uploaded_artifact_names=frozenset(uploaded_names),
                downloads_artifact=bool(download_indexes),
                executes_downloaded_content=bool(executed_names),
                executed_artifact_names=frozenset(executed_names),
                has_privileged_authority=privileged,
            )
        )
    return records


def artifact_trust_findings(target: Path, records: list[WorkflowRecord]) -> list[dict]:
    producers = [
        record for record in records
        if record.uploads_artifact and "pull_request" in record.triggers
    ]
    findings: list[dict] = []
    for consumer in records:
        if not (
            "workflow_run" in consumer.triggers
            and consumer.downloads_artifact
            and consumer.executes_downloaded_content
            and consumer.has_privileged_authority
        ):
            continue
        for producer in producers:
            if producer.name not in consumer.workflow_run_names:
                continue
            if not (
                "*" in consumer.executed_artifact_names
                or producer.uploaded_artifact_names & consumer.executed_artifact_names
            ):
                continue
            producer_rel = relative_path(target, producer.path)
            consumer_rel = relative_path(target, consumer.path)
            text = consumer.path.read_text(encoding="utf-8", errors="replace")
            line, column = line_column(text, "actions/download-artifact@")
            findings.append(
                make_finding(
                    "MD-WF-008", "critical", "high", consumer_rel, line, column,
                    f"Privileged workflow executes an artifact from pull-request workflow {producer_rel}.",
                    f"Untrusted pull-request code in {producer_rel} can alter an uploaded artifact that {consumer_rel} downloads and executes with secrets, OIDC, or repository write authority.",
                    "Treat the artifact as untrusted data: verify an immutable digest and parse it without execution, or rebuild it from trusted source in the privileged workflow.",
                )
            )
    return findings


def workflow_findings(target: Path, path: Path) -> list[dict]:
    findings: list[dict] = []
    rel = relative_path(target, path)
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    top_permissions = any(re.match(r"^permissions\s*:", line) for line in lines)
    if not top_permissions:
        insertion = "permissions: {}\n\n"
        insert_at = 0
        if lines and re.match(r"^name\s*:", lines[0]):
            first_end = text.find("\n") + 1
            insert_at = first_end if first_end > 0 else len(text)
        after = text[:insert_at] + insertion + text[insert_at:]
        findings.append(
            make_finding(
                "MD-WF-001", "medium", "high", rel, 1, 1,
                "Workflow has no top-level permissions boundary.",
                "A newly added job can silently inherit broader repository-default GITHUB_TOKEN permissions than its author intended.",
                "Declare top-level permissions: {} and grant the minimum permissions required by each job.",
                before=text, after=after, fix_safety="review-required",
            )
        )

    for index, line in enumerate(lines):
        if re.search(r"\bpermissions\s*:\s*write-all\b", line):
            after = replace_line_value(text, index, "{}")
            findings.append(
                make_finding(
                    "MD-WF-002", "high", "high", rel, index + 1, line.find("write-all") + 1,
                    "Workflow grants write-all token permissions.",
                    "Any compromised Action or command in this permission scope can modify repository content and other sensitive resources.",
                    "Replace write-all with an empty default and grant only the exact job-level write permissions required.",
                    before=text, after=after, fix_safety="review-required",
                )
            )

        uses = re.search(r"\buses:\s*[\"']?([^@\"'\s]+)@([^\"'\s#]+)[\"']?", line)
        if uses and not re.fullmatch(r"[0-9a-fA-F]{40}", uses.group(2)):
            findings.append(
                make_finding(
                    "MD-WF-003", "medium", "high", rel, index + 1, uses.start(2) + 1,
                    f"Action {uses.group(1)} is not pinned to a full commit SHA.",
                    "A mutable tag or branch can move to compromised code without a reviewed workflow change.",
                    "Resolve the reviewed release to a 40-character commit SHA, retain the release tag in a comment, and configure automated pin updates.",
                )
            )

    privileged = [event for event in PRIVILEGED_EVENTS if re.search(rf"(?m)^\s{{0,2}}{event}\s*:", text)]
    checkout_indexes = [
        index for index, line in enumerate(lines)
        if re.search(r"uses:\s*[\"']?actions/checkout@", line)
    ]
    checkout = bool(checkout_indexes)
    untrusted_ref = bool(re.search(r"github\.(?:event\.pull_request\.(?:head\.(?:sha|ref)|head)|head_ref)|refs/pull/", text))
    if privileged and checkout and untrusted_ref:
        needle = privileged[0]
        line, column = line_column(text, needle)
        findings.append(
            make_finding(
                "MD-WF-004", "high", "high", rel, line, column,
                f"Privileged event {needle} checks out an attacker-influenced revision.",
                "A fork or attacker-controlled event influences the checked-out revision inside a context that can receive base-repository authority.",
                "Split metadata handling from untrusted-code execution; use pull_request with read-only permissions for code execution and never check out a fork head in the privileged job.",
            )
        )
    if privileged:
        untrusted_pattern = re.compile(
            r"github\.(?:event\.pull_request\.(?:head\.(?:sha|ref)|head)|head_ref)|refs/pull/"
        )
        for evidence_index, evidence_line in enumerate(lines):
            if not untrusted_pattern.search(evidence_line):
                continue
            job_block = yaml_block(lines, evidence_index, 2)
            job_has_secrets = bool(
                re.search(r"\$\{\{\s*secrets\.|secrets:\s*inherit", job_block)
            )
            scopes = permission_scope(lines, evidence_index)
            if not job_has_secrets and not scopes:
                continue
            needle = "secrets." if "secrets." in job_block else evidence_line.strip()
            line, column = line_column(text, needle)
            findings.append(
                make_finding(
                    "MD-WF-005", "critical", "high", rel, line, column,
                    "Untrusted pull-request input can reach a privileged workflow with secrets or write authority.",
                    "An attacker can modify fork code or metadata so a privileged job executes attacker-controlled commands and exfiltrates credentials or changes the repository.",
                    "Remove the untrusted checkout/execution path from the privileged event and move it to an isolated pull_request workflow with no secrets and read-only permissions.",
                )
            )
            break
    for checkout_index in checkout_indexes:
        checkout_line = lines[checkout_index]
        indentation = len(checkout_line) - len(checkout_line.lstrip())
        step_block = yaml_block(lines, checkout_index, max(0, indentation - 2))
        if permission_scope_writes(lines, checkout_index) and "persist-credentials: false" not in step_block:
            column = checkout_line.find("actions/checkout@") + 1
            findings.append(
                make_finding(
                    "MD-WF-006", "medium", "medium", rel, checkout_index + 1, column,
                    "Checkout may persist a write-capable token in the workspace.",
                    "A later command or compromised build step can recover the credential from Git configuration and use its repository authority.",
                    "Set persist-credentials: false unless a reviewed step explicitly needs authenticated Git operations.",
                )
            )

    for run_index, run_line in enumerate(lines):
        if not re.match(r"^\s*(?:-\s*)?run\s*:", run_line):
            continue
        injection = run_block_injection(lines, run_index)
        if not injection:
            continue
        line, column = injection
        findings.append(
            make_finding(
                "MD-WF-007", "high", "high", rel, line, column,
                "Untrusted GitHub event data is interpolated directly into a shell command.",
                "An attacker can craft event text that changes the generated shell program and executes unintended commands in the job.",
                "Assign the expression to an environment variable or pass it as a reviewed action input, then quote the shell variable for the selected shell.",
            )
        )

    destructive_lines: list[int] = []
    for index, line in enumerate(lines):
        destructive = re.search(r"\b(close-pr|lock-pr|auto-close|delete-(?:issue|pr))\s*:\s*(true|yes)\b", line, re.IGNORECASE)
        if destructive:
            destructive_lines.append(index)
            after = replace_line_value(text, index, "false")
            findings.append(
                make_finding(
                    "MD-MOD-001", "high", "high", rel, index + 1, destructive.start(1) + 1,
                    f"Automation enables destructive operation {destructive.group(1)}.",
                    "A false positive, poisoned classifier input, or configuration mistake can close, lock, or delete legitimate contributor work without human review.",
                    "Start in report-only mode, require human review, publish an appeal path, and enable destructive behavior only after measuring false positives.",
                    before=text, after=after, fix_safety="safe",
                )
            )

        proxy = re.search(r"\b(" + "|".join(re.escape(key) for key in IDENTITY_PROXIES) + r")\s*:\s*([^\s#]+)", line)
        if proxy:
            key, raw = proxy.group(1), proxy.group(2).lower()
            enabled = raw in {"true", "yes"} or (raw.isdigit() and int(raw) > 0)
            if enabled:
                disabled = "false" if raw in {"true", "yes"} else "0"
                after = replace_line_value(text, index, disabled)
                findings.append(
                    make_finding(
                        "MD-MOD-002", "medium", "high", rel, index + 1, proxy.start(1) + 1,
                        f"Automated triage uses {IDENTITY_PROXIES[key]} as a contributor-risk proxy.",
                        "A legitimate newcomer can be penalized for identity or history characteristics unrelated to the quality and safety of the submitted change.",
                        "Disable the proxy and evaluate reproducibility, scope, tests, policy compliance, and contributor responsiveness instead.",
                        before=text, after=after, fix_safety="safe",
                    )
                )
    if destructive_lines:
        policy_text = "\n".join(
            path.read_text(encoding="utf-8", errors="replace")
            for path in list(target.glob("*.md")) + list((target / "docs").glob("*.md") if (target / "docs").is_dir() else [])
        ).lower()
        if not any(term in policy_text for term in ("appeal", "reopen", "kháng nghị", "異議")):
            first = destructive_lines[0]
            findings.append(
                make_finding(
                    "MD-MOD-003", "medium", "medium", rel, first + 1, 1,
                    "Destructive moderation is enabled without a discoverable appeal or reopening policy.",
                    "A false positive can become permanent because contributors have no documented path to request human reconsideration.",
                    "Document the appeal channel, review owner, response expectation, and process for reopening false positives before enabling enforcement.",
                )
            )
    return findings


def audit_repository(target: Path) -> dict:
    findings = governance_findings(target)
    records = index_workflows(target)
    for record in records:
        findings.extend(workflow_findings(target, record.path))
    findings.extend(artifact_trust_findings(target, records))
    findings.sort(
        key=lambda item: (
            -SEVERITY_ORDER[item["severity"]],
            item["location"]["path"],
            item["location"]["line"],
            item["rule_id"],
        )
    )
    counts = {severity: 0 for severity in SEVERITY_ORDER}
    for finding in findings:
        counts[finding["severity"]] += 1
    return {
        "schema_version": 1,
        "tool": {"name": "maintainer-defense", "version": AUDITOR_VERSION},
        "target": str(target),
        "summary": {"total": len(findings), "by_severity": counts},
        "findings": findings,
    }


def report_with_findings(report: dict, findings: list[dict]) -> dict:
    counts = {severity: 0 for severity in SEVERITY_ORDER}
    for finding in findings:
        counts[finding["severity"]] += 1
    updated = dict(report)
    updated["findings"] = findings
    updated["summary"] = {"total": len(findings), "by_severity": counts}
    return updated


def load_baseline(path: Path) -> set[str]:
    try:
        data = json.loads(path.expanduser().read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise KitError(f"invalid baseline JSON {path}: {exc}") from exc
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise KitError("baseline must be a schema-v1 maintainer-defense JSON report")
    findings = data.get("findings")
    if not isinstance(findings, list):
        raise KitError("baseline report must contain a findings array")
    fingerprints: set[str] = set()
    for finding in findings:
        fingerprint = finding.get("fingerprint") if isinstance(finding, dict) else None
        if not isinstance(fingerprint, str) or not fingerprint:
            raise KitError("every baseline finding must contain a non-empty fingerprint")
        fingerprints.add(fingerprint)
    return fingerprints


def filter_new(report: dict, baseline_fingerprints: set[str]) -> dict:
    findings = [
        finding for finding in report["findings"]
        if finding["fingerprint"] not in baseline_fingerprints
    ]
    return report_with_findings(report, findings)


def audit_git_ref(target: Path, ref: str) -> dict:
    """Archive and audit one local commit without executing repository code."""
    verify = subprocess.run(
        ["git", "-C", str(target), "rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}"],
        text=True,
        capture_output=True,
        check=False,
    )
    if verify.returncode != 0:
        raise KitError(f"unknown or non-commit Git ref: {ref}")
    commit = verify.stdout.strip()
    archived = subprocess.run(
        ["git", "-C", str(target), "archive", "--format=tar", commit],
        capture_output=True,
        check=False,
    )
    if archived.returncode != 0:
        detail = archived.stderr.decode(errors="replace").strip()
        raise KitError(f"cannot archive Git ref {ref}: {detail}")
    with tempfile.TemporaryDirectory(prefix="maintainer-defense-ref-") as tmp:
        snapshot = Path(tmp)
        with tarfile.open(fileobj=io.BytesIO(archived.stdout), mode="r:") as archive:
            for member in archive.getmembers():
                parts = Path(member.name).parts
                if member.name.startswith("/") or ".." in parts:
                    raise KitError(f"unsafe path in Git archive: {member.name}")
                if not member.isfile():
                    continue
                source = archive.extractfile(member)
                if source is None:
                    continue
                destination = snapshot.joinpath(*parts)
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(source.read())
        return audit_repository(snapshot)


def summary_headline(report: dict) -> str:
    summary = report["summary"]
    return " · ".join(
        [f"{summary['total']} finding{'s' if summary['total'] != 1 else ''}"]
        + [
            f"{count} {severity}"
            for severity, count in summary["by_severity"].items()
            if count
        ]
    )


def render_summary(report: dict) -> str:
    rows = [summary_headline(report)]
    if report["findings"]:
        rows.append("")
    for finding in report["findings"]:
        rows.append(
            f"{finding['severity'].upper():8} {finding['rule_id']}  {finding['message']}"
        )
    return "\n".join(rows) + "\n"


def render_human(report: dict) -> str:
    headline = summary_headline(report)
    if not report["findings"]:
        return headline + "\n"
    rows = [headline, ""]
    for finding in report["findings"]:
        location = finding["location"]
        rows.extend(
            [
                f"{finding['severity'].upper():8} {finding['rule_id']} {location['path']}:{location['line']}:{location['column']}",
                f"  Evidence: {finding['message']}",
                f"  Risk: {finding['threat_scenario']}",
                f"  Safe remediation: {finding['recommendation']}",
                f"  Rule: {rule_help_uri(finding['rule_id'])}",
            ]
        )
        if finding["fix"]["available"]:
            rows.append(f"  Patch: available ({finding['fix']['safety']})")
        rows.append("")
    return "\n".join(rows) + "\n"


def render_sarif(report: dict) -> dict:
    rules: dict[str, dict] = {}
    results = []
    levels = {"critical": "error", "high": "error", "medium": "warning", "low": "note", "note": "note"}
    for finding in report["findings"]:
        rule_id = finding["rule_id"]
        metadata = rule_metadata(rule_id)
        mappings = [f"{item['framework']}:{item['id']}" for item in metadata["mappings"]]
        rules.setdefault(
            rule_id,
            {
                "id": rule_id,
                "name": rule_id.replace("-", "_"),
                "shortDescription": {"text": metadata["title"]},
                "fullDescription": {"text": metadata["description"]},
                "help": {"text": metadata["safe_remediation"]},
                "helpUri": rule_help_uri(rule_id),
                "properties": {
                    "security-severity": str(SEVERITY_ORDER[metadata["default_severity"]] * 2.5),
                    "tags": mappings,
                },
            },
        )
        location = finding["location"]
        result = {
            "ruleId": rule_id,
            "level": levels[finding["severity"]],
            "message": {"text": finding["message"]},
            "partialFingerprints": {"maintainerDefenseFingerprint/v1": finding["fingerprint"]},
        }
        if (Path(report["target"]) / location["path"]).is_file():
            result["locations"] = [
                {
                    "physicalLocation": {
                        "artifactLocation": {"uri": location["path"]},
                        "region": {"startLine": location["line"], "startColumn": location["column"]},
                    }
                }
            ]
        results.append(result)
    return {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": report["tool"]["name"],
                        "version": report["tool"]["version"],
                        "informationUri": "https://github.com/thangldw/awesome-maintainer-defense",
                        "rules": list(rules.values()),
                    }
                },
                "results": results,
            }
        ],
    }


def combined_patch(report: dict, safe_only: bool) -> str:
    selected = [
        finding for finding in report["findings"]
        if finding["fix"]["available"]
        and (not safe_only or finding["fix"]["safety"] == "safe")
    ]
    by_path: dict[str, list[dict]] = {}
    for finding in selected:
        by_path.setdefault(finding["location"]["path"], []).append(finding)
    patches: list[str] = []
    target = Path(report["target"])
    for relative, file_findings in sorted(by_path.items()):
        path = target / relative
        before = path.read_text(encoding="utf-8", errors="replace")
        lines = before.splitlines(keepends=True)
        insert_permissions = any(item["rule_id"] == "MD-WF-001" for item in file_findings)
        for finding in sorted(file_findings, key=lambda item: item["location"]["line"], reverse=True):
            index = finding["location"]["line"] - 1
            if finding["rule_id"] == "MD-WF-002":
                ending = "\n" if lines[index].endswith("\n") else ""
                prefix = lines[index].split(":", 1)[0]
                lines[index] = f"{prefix}: {{}}{ending}"
            elif finding["rule_id"] in {"MD-MOD-001", "MD-MOD-002"}:
                ending = "\n" if lines[index].endswith("\n") else ""
                prefix = lines[index].split(":", 1)[0]
                current = lines[index].split(":", 1)[1].strip().split("#", 1)[0].strip().lower()
                disabled = "false" if current in {"true", "yes"} else "0"
                lines[index] = f"{prefix}: {disabled}{ending}"
        after = "".join(lines)
        if insert_permissions:
            first_end = after.find("\n") + 1 if re.match(r"^name\s*:", after) else 0
            after = after[:first_end] + "permissions: {}\n\n" + after[first_end:]
        if before != after:
            patches.append(unified_patch(relative, before, after))
    return "".join(patches)


def parse_install_args(arguments: list[str] | None = None) -> argparse.Namespace:
    parser = UsageArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, type=Path, help="target repository")
    parser.add_argument("--profile", choices=PROFILES, default="observe")
    parser.add_argument("--language", choices=LANGUAGES, default="en")
    parser.add_argument("--repo", help="GitHub OWNER/REPOSITORY (auto-detected when possible)")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true", help="write the previewed installation")
    mode.add_argument("--verify", action="store_true", help="verify files against the manifest")
    mode.add_argument("--uninstall", action="store_true", help="remove unmodified installer-owned files")
    return parser.parse_args(arguments)


def parse_audit_args(command: str, arguments: list[str]) -> argparse.Namespace:
    parser = UsageArgumentParser(prog=f"maintainer-defense {command}")
    parser.add_argument("target", nargs="?", default=".", type=Path, help="repository checkout")
    if command == "audit":
        parser.add_argument(
            "--format", choices=("human", "summary", "json", "sarif"), default="human"
        )
        parser.add_argument("--output", type=Path, help="write output to a file")
        parser.add_argument(
            "--fail-on", choices=("critical", "high", "medium", "low", "note"),
            help="exit 2 when a finding at or above this severity is present",
        )
        comparison = parser.add_mutually_exclusive_group()
        comparison.add_argument("--baseline", type=Path, help="schema-v1 JSON report")
        comparison.add_argument("--compare-ref", help="local Git commit to audit as baseline")
        parser.add_argument(
            "--config", type=Path,
            help="suppression config (default: TARGET/.maintainer-defense.json when present)",
        )
        parser.add_argument(
            "--new-only", action="store_true",
            help="emit only fingerprints absent from exactly one comparison source",
        )
    else:
        parser.add_argument("--output", type=Path, help="write unified diff to a file")
        parser.add_argument("--safe-only", action="store_true", help="exclude review-required patches")
        parser.add_argument(
            "--dry-run", action="store_true",
            help="compatibility flag; fix always emits a patch and never edits files",
        )
    args = parser.parse_args(arguments)
    if command == "audit":
        has_comparison = bool(args.baseline or args.compare_ref)
        if args.new_only and not has_comparison:
            parser.error("--new-only requires exactly one of --baseline or --compare-ref")
        if has_comparison and not args.new_only:
            parser.error("--baseline and --compare-ref require --new-only")
    return args


def emit_output(content: str, output: Path | None) -> None:
    if output is None:
        sys.stdout.write(content)
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{output.name}.", dir=output.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, output)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise
    print(f"WROTE {output}", file=sys.stderr)


def run_auditor(command: str, arguments: list[str]) -> None:
    args = parse_audit_args(command, arguments)
    target = args.target.expanduser().resolve()
    if not target.is_dir():
        raise KitError(f"target is not a directory: {target}")
    report = audit_repository(target)
    if command == "fix":
        patch = combined_patch(report, args.safe_only)
        emit_output(patch, args.output)
        return
    config_path = args.config.expanduser() if args.config else target / ".maintainer-defense.json"
    if args.config or config_path.is_file():
        entries = load_suppressions(config_path, date.today())
        report, suppressed, warnings = apply_suppressions(report, entries)
        for warning in warnings:
            print(f"WARNING: {warning}", file=sys.stderr)
        if suppressed:
            noun = "finding" if suppressed == 1 else "findings"
            print(f"Suppressed {suppressed} {noun} via {config_path}", file=sys.stderr)
    if args.new_only:
        if args.baseline:
            fingerprints = load_baseline(args.baseline)
        else:
            baseline_report = audit_git_ref(target, args.compare_ref)
            fingerprints = {item["fingerprint"] for item in baseline_report["findings"]}
        report = filter_new(report, fingerprints)
    if args.format == "human":
        content = render_human(report)
    elif args.format == "summary":
        content = render_summary(report)
    elif args.format == "json":
        content = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    else:
        content = json.dumps(render_sarif(report), ensure_ascii=False, indent=2) + "\n"
    emit_output(content, args.output)
    if args.fail_on:
        threshold = SEVERITY_ORDER[args.fail_on]
        if any(SEVERITY_ORDER[item["severity"]] >= threshold for item in report["findings"]):
            raise SystemExit(2)


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--version":
        print(f"maintainer-defense auditor {AUDITOR_VERSION}; kit {KIT_VERSION}")
        return
    if len(sys.argv) == 1:
        print(
            "usage: maintainer-defense {audit,fix,install} ...\n"
            "       maintainer-defense --target REPOSITORY [legacy installer options]\n\n"
            "commands:\n"
            "  audit    inspect local governance, workflows, and moderation automation\n"
            "  fix      emit a reviewable unified diff; never modify the target\n"
            "  install  preview or install a defense-kit profile\n\n"
            "Run a command with --help for details."
        )
        return
    if len(sys.argv) > 1 and sys.argv[1] in {"audit", "fix"}:
        try:
            run_auditor(sys.argv[1], sys.argv[2:])
        except (KitError, OSError) as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            raise SystemExit(1) from exc
        return
    install_arguments = sys.argv[2:] if len(sys.argv) > 1 and sys.argv[1] == "install" else None
    args = parse_install_args(install_arguments)
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

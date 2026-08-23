#!/usr/bin/env python3
"""Fail-closed inventory validation for public documentation artifacts."""

from __future__ import annotations

import json
from pathlib import Path, PurePosixPath


class DocumentationContractError(ValueError):
    """Raised when the checked-in documentation surface differs from its manifest."""


MANIFEST_KEYS = {
    "schema_version",
    "markdown",
    "generated_markdown",
    "diagrams",
    "retained_images",
    "forbidden_paths",
}
IMAGE_SUFFIXES = {".gif", ".jpeg", ".jpg", ".png", ".svg", ".webp"}


def _validated_paths(manifest: dict, key: str) -> list[str]:
    values = manifest.get(key)
    if not isinstance(values, list) or any(not isinstance(value, str) for value in values):
        raise DocumentationContractError(f"{key} must be a list of paths")
    for value in values:
        path = PurePosixPath(value)
        if (
            not value
            or "\\" in value
            or path.is_absolute()
            or value != path.as_posix()
            or any(part in {"", ".", ".."} for part in path.parts)
        ):
            raise DocumentationContractError("manifest requires normalized unique relative paths")
    if values != sorted(set(values)):
        raise DocumentationContractError("manifest requires normalized unique relative paths")
    return values


def repository_markdown(root: Path) -> set[str]:
    paths: set[str] = set()
    for path in root.rglob("*.md"):
        relative = path.relative_to(root)
        if ".git" in relative.parts or ".worktrees" in relative.parts:
            continue
        paths.add(relative.as_posix())
    return paths


def _repository_images(root: Path) -> set[str]:
    assets = root / "assets"
    if not assets.is_dir():
        return set()
    return {
        path.relative_to(root).as_posix()
        for path in assets.rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
    }


def validate_documentation_contract(root: Path) -> None:
    manifest_path = root / "documentation-manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise DocumentationContractError(f"cannot read documentation manifest: {exc}") from exc
    if not isinstance(manifest, dict) or set(manifest) != MANIFEST_KEYS:
        raise DocumentationContractError("documentation manifest has missing or unknown fields")
    if manifest["schema_version"] != 1:
        raise DocumentationContractError("unsupported documentation manifest schema")

    markdown = set(_validated_paths(manifest, "markdown"))
    generated = set(_validated_paths(manifest, "generated_markdown"))
    diagrams = set(_validated_paths(manifest, "diagrams"))
    retained_images = set(_validated_paths(manifest, "retained_images"))
    forbidden = set(_validated_paths(manifest, "forbidden_paths"))
    if not generated <= markdown:
        raise DocumentationContractError("generated Markdown must be listed in markdown")

    actual_markdown = repository_markdown(root)
    if missing := markdown - actual_markdown:
        raise DocumentationContractError(f"missing Markdown: {sorted(missing)}")
    if extra := actual_markdown - markdown:
        raise DocumentationContractError(f"unlisted Markdown: {sorted(extra)}")

    for relative in sorted(forbidden):
        if (root / relative).exists():
            raise DocumentationContractError(f"forbidden path exists: {relative}")
    for relative in sorted(diagrams):
        path = root / relative
        if not path.is_file() or path.is_symlink():
            raise DocumentationContractError(f"missing diagram: {relative}")
    for relative in sorted(retained_images):
        path = root / relative
        if not path.is_file() or path.is_symlink():
            raise DocumentationContractError(f"missing retained image: {relative}")
    if extra_images := _repository_images(root) - retained_images:
        raise DocumentationContractError(f"unlisted image: {sorted(extra_images)}")


if __name__ == "__main__":
    validate_documentation_contract(Path(__file__).resolve().parents[1])
    print("OK documentation contract")

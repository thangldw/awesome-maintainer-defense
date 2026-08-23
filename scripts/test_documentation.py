#!/usr/bin/env python3
"""Verify the repository documentation inventory and visual contract."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from documentation_contract import (
    DocumentationContractError,
    validate_documentation_contract,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads(ROOT.joinpath("documentation-manifest.json").read_text(encoding="utf-8"))


def write_manifest(
    root: Path,
    *,
    markdown: list[str] | None = None,
    generated_markdown: list[str] | None = None,
    diagrams: list[str] | None = None,
    retained_images: list[str] | None = None,
    forbidden_paths: list[str] | None = None,
) -> None:
    manifest = {
        "schema_version": 1,
        "markdown": markdown or [],
        "generated_markdown": generated_markdown or [],
        "diagrams": diagrams or [],
        "retained_images": retained_images or [],
        "forbidden_paths": forbidden_paths or [],
    }
    root.joinpath("documentation-manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )


class DocumentationContractTests(unittest.TestCase):
    def test_repository_root_may_live_below_dot_worktrees(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".worktrees" / "repository"
            root.mkdir(parents=True)
            write_manifest(root, markdown=["README.md"])
            root.joinpath("README.md").write_text("# Product\n", encoding="utf-8")

            validate_documentation_contract(root)

    def test_rejects_unlisted_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_manifest(root, markdown=["README.md"])
            root.joinpath("README.md").write_text("# Product\n", encoding="utf-8")
            root.joinpath("OLD.md").write_text("# Old\n", encoding="utf-8")

            with self.assertRaisesRegex(DocumentationContractError, "unlisted Markdown"):
                validate_documentation_contract(root)

    def test_rejects_forbidden_legacy_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_manifest(
                root,
                markdown=["README.md", "ROADMAP.md"],
                forbidden_paths=["ROADMAP.md"],
            )
            root.joinpath("README.md").write_text("# Product\n", encoding="utf-8")
            root.joinpath("ROADMAP.md").write_text("# Old roadmap\n", encoding="utf-8")

            with self.assertRaisesRegex(DocumentationContractError, "forbidden path"):
                validate_documentation_contract(root)

    def test_rejects_missing_diagram(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_manifest(root, diagrams=["docs/diagrams/trust.html"])

            with self.assertRaisesRegex(DocumentationContractError, "missing diagram"):
                validate_documentation_contract(root)

    def test_rejects_unlisted_image_but_accepts_retained_identity_assets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            assets = root / "assets"
            assets.mkdir()
            write_manifest(root, retained_images=["assets/plugin-icon.png"])
            assets.joinpath("plugin-icon.png").write_bytes(b"identity")
            validate_documentation_contract(root)

            assets.joinpath("old-preview.png").write_bytes(b"legacy")
            with self.assertRaisesRegex(DocumentationContractError, "unlisted image"):
                validate_documentation_contract(root)

    def test_rejects_unsafe_or_duplicate_manifest_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_manifest(root, markdown=["README.md", "README.md", "../outside.md"])

            with self.assertRaisesRegex(DocumentationContractError, "normalized unique relative paths"):
                validate_documentation_contract(root)


class RepositoryDocumentationTests(unittest.TestCase):
    def test_english_product_journey_paths_exist(self) -> None:
        for relative in (
            "docs/GETTING_STARTED.md",
            "docs/AUDITOR.md",
            "docs/CONFIGURATION.md",
            "docs/THREAT_MODEL.md",
            "docs/KIT_ASSURANCE.md",
            "docs/AUDITOR_PILOT_PROGRAM.md",
            "docs/DISTRIBUTION.md",
        ):
            with self.subTest(path=relative):
                self.assertTrue(ROOT.joinpath(relative).is_file(), relative)

    def test_approved_legacy_paths_are_absent(self) -> None:
        for relative in MANIFEST["forbidden_paths"]:
            with self.subTest(path=relative):
                self.assertFalse(ROOT.joinpath(relative).exists(), relative)


if __name__ == "__main__":
    unittest.main(verbosity=2)

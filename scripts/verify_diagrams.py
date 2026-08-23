#!/usr/bin/env python3
"""Verify the repository's accessible, self-contained Diagram Design outputs."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DIAGRAMS = {
    "audit-to-action": 6,
    "consent-to-evidence": 7,
    "trust-boundaries": 7,
}
GRID_ATTRIBUTES = ("x", "y", "cx", "cy", "width", "height", "x1", "y1", "x2", "y2")
TYPE_RAMP = {8, 12, 16, 20, 24, 28, 32, 40}


class DiagramParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.svgs: list[dict] = []
        self.references: list[tuple[str, str, str]] = []
        self.scripts = 0
        self.lines: list[dict[str, str]] = []
        self.nodes: list[dict[str, str]] = []
        self.legends: list[dict[str, str]] = []
        self.svg_elements: list[tuple[str, dict[str, str]]] = []
        self._svg_depth = 0
        self._current_svg: dict | None = None
        self._capture: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.casefold()
        data = {key.casefold(): value or "" for key, value in attrs}
        for key in ("href", "src", "xlink:href"):
            if key in data:
                self.references.append((tag, data.get("rel", ""), data[key]))
        if tag == "script":
            self.scripts += 1
        if tag == "line" and self._svg_depth:
            self.lines.append(data)
        if "data-node" in data:
            self.nodes.append(data)
        if data.get("data-legend-position") == "bottom":
            self.legends.append(data)
        if tag == "svg" and self._svg_depth == 0:
            self._svg_depth = 1
            self._current_svg = {"attrs": data, "first": None, "title": {}, "desc": {}}
            self.svgs.append(self._current_svg)
            return
        if self._svg_depth:
            self._svg_depth += 1
            self.svg_elements.append((tag, data))
            assert self._current_svg is not None
            if self._svg_depth == 2 and self._current_svg["first"] is None:
                self._current_svg["first"] = tag
            if self._svg_depth == 2 and tag in {"title", "desc"}:
                self._current_svg[tag] = {"attrs": data, "text": ""}
                self._capture = tag

    def handle_endtag(self, tag: str) -> None:
        tag = tag.casefold()
        if self._svg_depth:
            if tag in {"title", "desc"}:
                self._capture = None
            self._svg_depth -= 1
            if self._svg_depth == 0:
                self._current_svg = None

    def handle_data(self, data: str) -> None:
        if self._capture and self._current_svg:
            node = self._current_svg[self._capture]
            node["text"] = node.get("text", "") + data


def approved_reference(tag: str, rel: str, value: str) -> bool:
    if not value or value.startswith("#") or value.startswith("data:image/"):
        return True
    parsed = urlparse(value)
    if not parsed.scheme and not parsed.netloc:
        return True
    return (
        tag == "link"
        and "stylesheet" in rel.casefold().split()
        and parsed.scheme == "https"
        and parsed.hostname == "fonts.googleapis.com"
        and parsed.path == "/css2"
        and parsed.port is None
        and not parsed.fragment
    )


def verify(path: Path, slug: str, node_budget: int) -> list[str]:
    source = path.read_text(encoding="utf-8")
    parser = DiagramParser()
    parser.feed(source)
    parser.close()
    errors: list[str] = []
    if parser.scripts:
        errors.append("scripts are not allowed")
    for tag, rel, value in parser.references:
        if not approved_reference(tag, rel, value):
            errors.append(f"unapproved reference: {value}")
    if len(parser.svgs) != 1:
        errors.append(f"expected one SVG, found {len(parser.svgs)}")
    else:
        svg = parser.svgs[0]
        attrs = svg["attrs"]
        if attrs.get("role") != "img" or attrs.get("viewbox") != "0 0 1280 720":
            errors.append("SVG must be role=img with the doc-wide viewBox")
        if svg["first"] != "title":
            errors.append("SVG title must be the first child")
        title = svg["title"]
        desc = svg["desc"]
        title_id = title.get("attrs", {}).get("id", "")
        desc_id = desc.get("attrs", {}).get("id", "")
        if title_id != f"{slug}-title" or desc_id != f"{slug}-desc":
            errors.append("title and description IDs must use the diagram slug")
        if attrs.get("aria-labelledby", "").split() != [title_id, desc_id]:
            errors.append("aria-labelledby must reference title then description")
        if not title.get("text", "").strip() or not desc.get("text", "").strip():
            errors.append("title and description must not be empty")
    if len(parser.nodes) > node_budget:
        errors.append(f"node budget exceeded: {len(parser.nodes)} > {node_budget}")
    accent_nodes = sum("node--accent" in node.get("class", "").split() for node in parser.nodes)
    if accent_nodes > 2:
        errors.append(f"accent node budget exceeded: {accent_nodes} > 2")
    if len(parser.legends) != 1:
        errors.append("exactly one bottom legend is required")
    elif int(parser.legends[0].get("data-legend-y", "0")) < 640:
        errors.append("legend must occupy the bottom strip")
    for line in parser.lines:
        if line.get("x1") != line.get("x2") and line.get("y1") != line.get("y2"):
            errors.append("diagonal <line> connector is not allowed")
    for tag, attrs in parser.svg_elements:
        for attribute in GRID_ATTRIBUTES:
            value = attrs.get(attribute, "")
            if value.isdigit() and int(value) % 4:
                errors.append(f"{tag} {attribute}={value} is off the 4px grid")
    for size in re.findall(r"font:[^;}]*?\b(\d+)px(?:/|\s)", source):
        if int(size) not in TYPE_RAMP:
            errors.append(f"font size {size}px is outside the approved type ramp")
    lowered = source.casefold()
    for forbidden in ("writing-mode", "jetbrains mono", "box-shadow", "text-shadow", "drop-shadow", "<filter"):
        if forbidden in lowered:
            errors.append(f"forbidden visual treatment: {forbidden}")
    return errors


def main() -> None:
    directory = ROOT / "docs/diagrams"
    actual = {path.name for path in directory.glob("*.html")} if directory.is_dir() else set()
    expected = {f"{slug}.html" for slug in DIAGRAMS}
    errors = []
    if actual != expected:
        errors.append(f"diagram inventory differs: missing={sorted(expected - actual)}, extra={sorted(actual - expected)}")
    for slug, budget in DIAGRAMS.items():
        path = directory / f"{slug}.html"
        if path.is_file():
            errors.extend(f"{path.relative_to(ROOT)}: {error}" for error in verify(path, slug, budget))
    if errors:
        raise SystemExit("ERROR: " + "\nERROR: ".join(errors))
    print(f"OK: {len(DIAGRAMS)} accessible doc-wide diagrams")


if __name__ == "__main__":
    main()

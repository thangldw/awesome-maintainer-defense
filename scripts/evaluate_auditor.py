#!/usr/bin/env python3
"""Render deterministic measurements for the labeled synthetic auditor corpus."""

from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEST_HELPERS = ROOT / "scripts/test_auditor.py"
CORPUS = ROOT / "tests/fixtures/auditor/corpus.json"
OUTPUT = ROOT / "docs/AUDITOR_EVALUATION.md"

spec = importlib.util.spec_from_file_location("auditor_test_helpers", TEST_HELPERS)
assert spec and spec.loader
helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helpers)


def ratio(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 1.0


def main() -> None:
    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    rules = sorted({rule for case in corpus["cases"] for rule in case.get("expected", [])})
    counts = {rule: {"tp": 0, "fp": 0, "fn": 0} for rule in rules}
    exact = 0
    for case in corpus["cases"]:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            helpers.materialize(target, case)
            actual = {
                finding["rule_id"]
                for finding in helpers.module.audit_repository(target)["findings"]
            }
        expected = set(case.get("expected", []))
        exact += actual == expected
        for rule in rules:
            if rule in actual and rule in expected:
                counts[rule]["tp"] += 1
            elif rule in actual:
                counts[rule]["fp"] += 1
            elif rule in expected:
                counts[rule]["fn"] += 1

    total_tp = sum(item["tp"] for item in counts.values())
    total_fp = sum(item["fp"] for item in counts.values())
    total_fn = sum(item["fn"] for item in counts.values())
    lines = [
        "# Synthetic auditor evaluation",
        "",
        "> Generated from `tests/fixtures/auditor/corpus.json`. Edit fixtures and implementation, not this page.",
        "",
        "## Measured contract",
        "",
        f"The corpus contains **{len(corpus['cases'])}** small labeled fixtures designed to exercise known rule behavior.",
        "",
        f"- Exact fixture agreement: **{exact}/{len(corpus['cases'])}**",
        f"- Micro precision inside this corpus: **{ratio(total_tp, total_tp + total_fp):.3f}**",
        f"- Micro recall inside this corpus: **{ratio(total_tp, total_tp + total_fn):.3f}**",
        "",
        "| Rule | TP | FP | FN | Corpus precision | Corpus recall |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for rule, item in counts.items():
        lines.append(
            f"| `{rule}` | {item['tp']} | {item['fp']} | {item['fn']} | "
            f"{ratio(item['tp'], item['tp'] + item['fp']):.3f} | "
            f"{ratio(item['tp'], item['tp'] + item['fn']):.3f} |"
        )
    lines.extend(
        [
            "",
            "## Failure-injection check",
            "",
            "The suite injects four unsafe changes: remove the workflow permission boundary, add `write-all`, replace a full Action SHA with a tag, and persist credentials in a write-capable checkout. The expected result is **4/4 detected**.",
            "",
            "## Interpretation boundary",
            "",
            "These numbers are regression measurements for intentionally constructed fixtures. They are not prevalence-weighted field accuracy and do not measure arbitrary YAML semantics, live GitHub settings, maintainer time saved, contributor impact, or novel attack paths. Field claims require authorized, independently labeled repository pilots with explicit applicability decisions and adequate negative samples.",
            "",
            "Regenerate with `python3 scripts/evaluate_auditor.py`.",
            "",
        ]
    )
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"WROTE {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

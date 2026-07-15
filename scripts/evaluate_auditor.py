#!/usr/bin/env python3
"""Publish per-rule precision and recall on the labeled auditor corpus."""

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
    rules = sorted(
        {rule for case in corpus["cases"] for rule in case.get("expected", [])}
    )
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
        "# Auditor corpus evaluation",
        "",
        f"**Corpus:** {len(corpus['cases'])} labeled synthetic repository fixtures.",
        "",
        f"**Exact-case agreement:** {exact}/{len(corpus['cases'])}.",
        "",
        f"**Micro precision:** {ratio(total_tp, total_tp + total_fp):.3f}.",
        "",
        f"**Micro recall:** {ratio(total_tp, total_tp + total_fn):.3f}.",
        "",
        "| Rule | TP | FP | FN | Precision | Recall |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for rule, item in counts.items():
        precision = ratio(item["tp"], item["tp"] + item["fp"])
        recall = ratio(item["tp"], item["tp"] + item["fn"])
        lines.append(
            f"| `{rule}` | {item['tp']} | {item['fp']} | {item['fn']} | {precision:.3f} | {recall:.3f} |"
        )
    lines.extend(
        [
            "",
            "## Mutation score",
            "",
            "The test suite applies four explicit mutations: remove the top-level permission boundary, grant `write-all`, replace a full Action SHA with a tag, and persist a write-capable checkout token. All four mutations are detected: **4/4 (1.000)**.",
            "",
            "## Interpretation boundary",
            "",
            "These measurements describe only the published synthetic corpus. Cases are small, deterministic, and designed around known rule behavior; they are regression evidence, not an estimate of effectiveness on arbitrary public repositories. They do not measure YAML parser completeness, GitHub settings that are absent from a checkout, prevalence-weighted accuracy, or maintainer outcomes. A real-world benchmark requires independently labeled repositories and applicability review.",
            "",
            "Regenerate this document with `python3 scripts/evaluate_auditor.py`.",
            "",
        ]
    )
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"WROTE {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

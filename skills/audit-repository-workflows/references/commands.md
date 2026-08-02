# Auditor commands

- Human-readable audit: `python3 scripts/run_auditor.py audit TARGET`
- JSON audit: `python3 scripts/run_auditor.py audit TARGET --format json`
- SARIF audit: `python3 scripts/run_auditor.py audit TARGET --format sarif --output REPORT.sarif`
- Policy threshold: `python3 scripts/run_auditor.py audit TARGET --fail-on high`
- Reviewable patch: `python3 scripts/run_auditor.py fix TARGET --output recommended.patch`
- Safer subset of patches: add `--safe-only` to `fix`.

The audit command is read-only. The fix command writes only the requested patch file; it does not modify the target repository.

The public OpenAI upload bundle places the generated dependency-free standalone auditor beside `run_auditor.py`. A GitHub plugin checkout uses the canonical repository implementation.

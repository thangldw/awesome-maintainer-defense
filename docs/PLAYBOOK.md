# Maintainer defense playbook

## 1. Triage

Preserve the original URL, revision, workflow run, timestamp, and sanitized evidence. Separate security-sensitive reports from public intake. Classify the immediate risk: attention flood, unsafe workflow path, credential exposure, destructive automation, or governance gap. Do not infer authorship or intent from style, identity, or account history.

## 2. Review

Confirm the finding against the active file and repository context. Check whether external rulesets, organization policy, or service configuration changes applicability. For automation, trace untrusted input to its execution or authority sink. Record false positives and unresolved context explicitly.

## 3. Authorize

Assign a named owner. Document the proposed control, required permissions, data recipients, contributor-visible effects, exception criteria, appeal route, review date, and exact rollback. High-impact controls require repository-owner approval; an auditor recommendation is not authorization.

## 4. Roll out

Start with local audit and the `observe` profile. Run representative tests and sample both flagged and unflagged contributions. Prefer neutral routing and required status checks over public accusations. Enable close, lock, block, deletion, or broad interaction limits only for a measured need, with human review and an expiry.

## 5. Respond to an incident

Assign an incident owner and pause uncertain release or moderation automation. Preserve evidence without copying credentials or private reports into public logs. Isolate untrusted execution, revoke exposed credentials, invalidate suspect artifacts, and apply time-bounded platform controls. Communicate status without amplifying harassment or disclosing exploit details.

## 6. Roll back and recover

Disable the workflow or remove the required check using the recorded rollback. The installer may uninstall only unmodified files it owns; modified files require manual review. Reopen legitimate work, notify affected contributors when appropriate, remove temporary restrictions on schedule, and verify that credentials and release paths are restored safely.

## 7. Keep an adoption record

Record the repository and commit, control owner, measured problem, selected profile, permissions, data boundary, high-impact effects, evaluation window, false-positive budget, appeal path, review date, and rollback command. Keep aggregate evidence where possible; do not publish contributor identities or raw private content.

Controls without an active owner, current review date, and tested rollback should return to observation mode.

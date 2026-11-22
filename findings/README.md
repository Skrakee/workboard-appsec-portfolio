# Findings

This register contains validated security issues. Use the [threat model](../docs/threat-model.md) and [coverage register](../docs/security-testing.md#coverage-register) for scenarios still under investigation. Scanner observations are recorded in [scan reviews](../security/reviews/).

## Register

| ID | Issue | Severity | State | Traceability |
| --- | --- | --- | --- | --- |
| [F-01](F-01-BOLA-document-update.md) | Cross-tenant document modification | High, provisional | Verified fixed | TM-03; SR-02, SR-03, SR-04; [evidence](evidence/F-01/README.md) |

No additional finding IDs have been assigned. Suspicious code and scanner alerts have not been promoted to confirmed issues.

## Add a finding

Copy [TEMPLATE.md](TEMPLATE.md) when an investigation produces reproducible evidence. Assign the next unused `F-NN` identifier and a descriptive filename. Keep sanitized captures and supporting files under `evidence/F-NN/`; link them from the report.

A report states the violated requirement, affected version, preconditions, reproduction and impact. Add the finding to this register once confirmed. Link the fix and regression test when available, then record the actual retest before closing it.

| State | Meaning |
| --- | --- |
| Confirmed | Evidence establishes the issue; remediation is pending |
| In remediation | A fix is being developed or reviewed |
| Awaiting retest | A candidate fix exists; verification is incomplete |
| Verified fixed | Recorded regression and retest evidence support closure |

Keep the original evidence and chronology after closure. Record an explicit decision and reason if an issue is deferred or accepted; an untested scenario is not an accepted risk.

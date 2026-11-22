# Security checks

The [Security workflow](../.github/workflows/security.yml) runs on pull requests to `main`, pushes to `main` and manual dispatch. It uses open-source tools without paid scanning integrations.

| Check | Scope | Policy |
| --- | --- | --- |
| pytest | Functional behavior and F-01 requirements | Failed tests fail the check |
| Semgrep CE | Python/JavaScript under `app/`; two [local rules](../security/semgrep.yml) | Report candidates; scanner errors fail |
| pip-audit | Runtime requirements and resolved transitive Python dependencies | Report advisories; incomplete or invalid results fail |
| Gitleaks CLI | Full fetched Git history | Secret detections fail; only two exact synthetic JWT secret values are allowlisted |
| ZAP API scan, safe mode | OpenAPI routes on disposable Docker, with an Atlas admin token | Report passive alerts; startup/scanner errors fail |

SAST/SCA/DAST findings are **report only** for this intentionally vulnerable lab. A green scanner job means it completed and produced a report, not that the application is secure. This is not a production release gate.

## Verified results — 2026-11-22

Scanned source: [`594cda0`](https://github.com/Skrakee/workboard-appsec-portfolio/commit/594cda0f9129d4412cb4643f443ae52ad81ea470).

| Check | Observed result | Evidence |
| --- | --- | --- |
| pytest | 16 passed | [Test run](https://github.com/Skrakee/workboard-appsec-portfolio/actions/runs/45031798624) |
| Semgrep | 2 candidates: interpolated SQL and `innerHTML` | [SAST job](https://github.com/Skrakee/workboard-appsec-portfolio/actions/runs/45031798716/job/137236793405) |
| pip-audit | 24 advisory entries across PyJWT 2.10.1 and Starlette 0.46.2 | [SCA job](https://github.com/Skrakee/workboard-appsec-portfolio/actions/runs/45031798716/job/137236793052) |
| Gitleaks | 0 detections with the documented lab allowlist | [Secrets job](https://github.com/Skrakee/workboard-appsec-portfolio/actions/runs/45031798716/job/137236793219) |
| ZAP | 11 alert groups: 2 medium, 6 low, 3 informational | [DAST job](https://github.com/Skrakee/workboard-appsec-portfolio/actions/runs/45031798716/job/137236793275) |

## Triage

The two SAST matches correspond to unsafe code confirmed by source review. Their browser/API impact needs separate findings and retests; see the [open threats](security-design.md#threat-review).

The SCA count is scanner output, not 24 confirmed exploitable application bugs. Review each advisory's affected behavior and reachability before assigning application severity. Upgrade PyJWT and the FastAPI/Starlette stack in a separate change, preserving compatibility and rerunning the suite; do not force an incompatible Starlette version.

ZAP's medium alerts concern missing CSP and anti-clickjacking headers. Low alerts concern other headers and an unexpected content type; informational alerts include authentication detection, client errors and caching observations. Review responses against their expected contract: a 4xx alone is not a vulnerability. These deployment observations do not reopen F-01.

## Find reports and understand coverage

Open **Actions → Security → run**. The summary lists counts; **Artifacts** contains `sast-report`, `sca-report`, `secrets-report` and `dast-report`. Download the ZAP artifact and open `zap.html`. Artifacts expire after 30 days; this summary preserves the observed results.

Tool versions and container digests are saved with the reports. ZAP tokens are redacted before upload. Each run identifies its source commit; rerun to refresh dependency advisories.

The local SAST rules are narrow. ZAP safe mode runs no active attacks and does not execute the SPA like a full browser. Neither establishes tenant isolation or stored-XSS exploitability; F-01 relies on its regression suite and manual Burp retest.

Dependencies are resolved at scan time; transitives and the Docker base image are not fully locked. OS-package/image scanning and production hardening remain outside this exercise.

References: [Semgrep](https://semgrep.dev/docs/cli-reference), [pip-audit](https://github.com/pypa/pip-audit), [Gitleaks](https://github.com/gitleaks/gitleaks), [ZAP](https://www.zaproxy.org/docs/docker/api-scan/).

# Security checks

Workflows define executable commands. Their reports are generated during a run; installing a scanner locally is not required for GitHub CI.

## Configuration and execution

| Check | Source of truth | Execution |
| --- | --- | --- |
| Application tests | [tests/](../tests/), [tests.yml](../.github/workflows/tests.yml) | Python 3.12 installs development requirements and runs pytest against temporary databases |
| SAST | [security.yml](../.github/workflows/security.yml), [Semgrep rules](../security/semgrep.yml) | A versioned Semgrep container scans Python/JavaScript under `app/` using two local review rules |
| SCA | [security.yml](../.github/workflows/security.yml), [runtime requirements](../requirements.txt) | pip-audit resolves runtime/transitive Python dependencies and looks up known advisories |
| Secrets | [security.yml](../.github/workflows/security.yml), [.gitleaks.toml](../.gitleaks.toml) | Gitleaks scans fetched Git history; only two exact synthetic signing-secret values are allowlisted |
| DAST | [security.yml](../.github/workflows/security.yml), [compose.yaml](../compose.yaml) | Start a disposable Workboard container, authenticate as Atlas admin and run a passive ZAP OpenAPI scan |

Each job uses a temporary `ubuntu-latest` runner. Checkout supplies the proposed source. Docker images provide Semgrep, Gitleaks and ZAP; pip installs pip-audit. The workflow uploads reports with `actions/upload-artifact` and removes the disposable DAST application afterward.

Tests and Security run on PRs targeting `main` and pushes to `main`. Security also supports manual dispatch. Once the workflow is on the default branch, use **Actions → Security → Run workflow**, selecting the intended ref. This currently runs all four security jobs.

## Policy

Failed tests and detected non-allowlisted secrets fail their checks. SAST/SCA/DAST findings are **report only** while assessment of the seeded lab continues; scanner/startup errors and incomplete results still fail. Green means successful execution, not zero vulnerabilities or completed risk review.

## Read a run

1. Open **Actions → Security → run** or follow a PR's **Checks**.
2. Select a job and expand its scan step for commands, errors, rule/advisory IDs and file locations.
3. Read the run summary for counts. Download **Artifacts**: `sast-report`, `sca-report`, `secrets-report`, `dast-report`. Open `zap.html` for the readable DAST report.

A missing executable, invalid configuration or timeout is an execution failure. A source location, package advisory or HTTP alert is assessment evidence requiring triage. Record review outcomes in [security/reviews](../security/reviews/); promote validated issues to [findings](../findings/README.md).

Reports retain tool versions and container digests where applicable. ZAP tokens and secret matches are redacted before upload. Artifacts expire after 30 days; commit a concise review summary when preserving an assessment milestone. The [2026-11-22 review](../security/reviews/2026-11-22.md) preserves the initial observed results.

## Coverage limits

The two SAST rules are narrow. SCA reports package advisories, not demonstrated application exploitability. ZAP safe mode runs no active attacks, uses one account and does not execute the interface as a browser. Browser and multi-account authorization testing remain in the [assessment plan](security-testing.md).

Dependency resolution and advisory feeds can change between runs; transitives and the Docker base image are not fully locked. OS-package/image scanning and production deployment controls are not covered by this workflow.

Tool references: [Semgrep](https://semgrep.dev/docs/cli-reference), [pip-audit](https://github.com/pypa/pip-audit), [Gitleaks](https://github.com/gitleaks/gitleaks), [ZAP](https://www.zaproxy.org/docs/docker/api-scan/).

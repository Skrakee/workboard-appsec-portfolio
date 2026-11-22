# Tests and security scans

GitHub runs these checks on a temporary Linux computer. It downloads the project code, installs or starts the tools, runs them and saves their reports. Your own computer does not need to stay on.

## What runs?

| Check | What it does | Where it is set up |
| --- | --- | --- |
| App tests | Uses pytest to check login, documents, comments and edit permissions | [tests.yml](../.github/workflows/tests.yml) and [tests/](../tests/) |
| Code scan: Semgrep | Looks for two code patterns: SQL built from text, and assignment to `innerHTML` | [security.yml](../.github/workflows/security.yml) and [semgrep.yml](../security/semgrep.yml) |
| Library scan: pip-audit | Checks the app's Python libraries for known security problems | [security.yml](../.github/workflows/security.yml) and [requirements.txt](../requirements.txt) |
| Secret scan: Gitleaks | Checks current and old Git commits for exposed secrets | [security.yml](../.github/workflows/security.yml) and [.gitleaks.toml](../.gitleaks.toml) |
| Web scan: ZAP | Sends requests to a running copy of Workboard and checks the responses | [security.yml](../.github/workflows/security.yml) |

Semgrep, Gitleaks and ZAP run in Docker containers that contain the tools. The workflow installs pip-audit with `pip`.

For ZAP, GitHub also builds and starts Workboard, signs in as an Atlas admin and gives ZAP the sign-in token. This is a passive scan: it does not run active attack tests or test the page as a real browser.

App tests use a new temporary database for each test. They do not change your local Docker database. The [threat model](threat-model.md) lists checks that still need work.

## Where are the results?

Open **Actions**, select **Security checks**, then choose a run.

- Click a job and expand its scan step to read the output or an error.
- Read the summary for the number of warnings.
- Download the reports under **Artifacts**: `semgrep-report`, `pip-audit-report`, `gitleaks-report` and `zap-report`.
- Open `zap.html` from the ZAP report in a browser.

The reports stay available for 30 days. Tokens are hidden before reports are uploaded.

Tests and scans run when a pull request to `main` is opened or updated, and after a push to `main`. Once the workflow is merged, **Run workflow** also starts the four scans manually.

## What does a green check mean?

A failed app test or an unexpected secret makes its job fail. For Semgrep, pip-audit and ZAP, findings are currently reported without failing the job. Tool errors still fail.

A green scan means the tool finished. It does not mean the app has no security problems.

A message such as "command not found" is a tool setup problem. A file and line number, library warning or web alert is something to investigate.

## Recorded results — 2026-11-22

These results belong to [this code version](https://github.com/Skrakee/workboard-appsec-portfolio/commit/594cda0f9129d4412cb4643f443ae52ad81ea470).

| Check | Result | Details |
| --- | --- | --- |
| App tests | 16 passed | [Test run](https://github.com/Skrakee/workboard-appsec-portfolio/actions/runs/45031798624) |
| Semgrep | 2 code warnings: search SQL and comment HTML | [Code scan](https://github.com/Skrakee/workboard-appsec-portfolio/actions/runs/45031798716/job/137236793405) |
| pip-audit | 24 library warnings across PyJWT 2.10.1 and Starlette 0.46.2 | [Library scan](https://github.com/Skrakee/workboard-appsec-portfolio/actions/runs/45031798716/job/137236793052) |
| Gitleaks | No secrets found, with the two sample signing-secret exceptions | [Secret scan](https://github.com/Skrakee/workboard-appsec-portfolio/actions/runs/45031798716/job/137236793219) |
| ZAP | 11 alert groups: 2 medium, 6 low and 3 informational | [Web scan](https://github.com/Skrakee/workboard-appsec-portfolio/actions/runs/45031798716/job/137236793275) |

The library warnings still need review to see which affect Workboard. The web alerts include missing security headers and information about HTTP responses. A warning is not automatically a confirmed problem.

These tools do not cover every threat. The two Semgrep rules are limited, and the ZAP scan uses one account. Browser tests, checks between different users and full Docker-image checks need separate work.

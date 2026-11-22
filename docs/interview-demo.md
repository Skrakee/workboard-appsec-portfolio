# Reproduce the F-01 regression

This demo uses the actual commits in this repository. The lab is intentionally seeded; its review history was reconstructed from the preserved pre-fix source.

## Inspect without running code

- [Vulnerable implementation](https://github.com/Skrakee/workboard-appsec-portfolio/blob/78867096b84b577a8f471fafe32211eaf56b47bf/app/main.py#L119).
- [Regression-test commit](https://github.com/Skrakee/workboard-appsec-portfolio/commit/092c9b5c63814497720dc6594c2e13ec71b0c0aa).
- [Failed pre-fix CI run](https://github.com/Skrakee/workboard-appsec-portfolio/actions/runs/44939343951): **2 failed, 14 passed**. Both failures are cross-tenant administrator edits.
- [Remediation pull request](https://github.com/Skrakee/workboard-appsec-portfolio/pull/1): compare the test and fix commits, then open Checks for the recorded runs.

## Run the old and fixed versions

Clone this private repository using an account with access. Create a Python 3.12 virtual environment, activate it, and install the test dependencies.

```bash
git clone https://github.com/Skrakee/workboard-appsec-portfolio.git
cd workboard-appsec-portfolio
python -m venv .venv
# Activate .venv using the command appropriate for your OS.
python -m pip install -r requirements-dev.txt
```

Check out the pre-fix commit, which already contains the regression tests:

```bash
git switch --detach 092c9b5c63814497720dc6594c2e13ec71b0c0aa
python -m pytest tests/ -q
```

Expected: **2 failed, 14 passed**. The failing cases receive success for cross-tenant updates and observe modified stored data.

Check out the fixed commit to reproduce the post-fix result, including before the PR is merged:

```bash
git switch --detach 066e3affecfbf7bbb12909d6ff090858271403ac
python -m pytest tests/ -q
```

After the remediation PR is merged, `git switch main` followed by `git pull --ff-only` returns to the updated main branch.

Expected: **16 passed**. Before/after assertions also verify that denied edits leave the document unchanged.

Each test creates a temporary SQLite database. The tests do not require a running Docker instance and do not change the lab's persistent database.

## Review the policy separately from CI

The workflow runs automatically on pull requests targeting main and pushes to main. Required-check enforcement is not enabled: GitHub returned a plan restriction for protected branches in this private repository. A passing CI run and an enforced merge gate are different things.

## Manual post-fix evidence

The project owner performed the Atlas-to-Boreal retest on 2026-11-22. Read the [sanitized retest record](../findings/evidence/F-01/manual-retest-2026-11-22.md): `/api/me` identifies the Atlas administrator, the PATCH to document 201 returns 404, and the supplied screenshot plus the owner's observation support unchanged victim data. A separate manual successful same-tenant edit was not supplied.

To repeat the retest, check out the desired fixed revision, run `docker compose up --build -d workboard` from that checkout, obtain a fresh Atlas administrator token, repeat the captured PATCH and inspect the Boreal document after reloading it. Also verify that an administrator can still edit a document within their own tenant.

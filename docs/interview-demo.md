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

After the remediation PR is merged, switch back to the fixed main branch:

```bash
git switch main
git pull --ff-only
python -m pytest tests/ -q
```

Expected: **16 passed**. Before/after assertions also verify that denied edits leave the document unchanged.

Each test creates a temporary SQLite database. The tests do not require a running Docker instance and do not change the lab's persistent database.

## Review the policy separately from CI

The workflow runs automatically on pull requests targeting main and pushes to main. Required-check enforcement is not enabled: GitHub returned a plan restriction for protected branches in this private repository. A passing CI run and an enforced merge gate are different things.

Manual post-fix Burp verification remains a separate task: rebuild the local app, repeat the captured Atlas-to-Boreal PATCH with a fresh token, expect 404, and confirm the victim document is unchanged.

# Reproduce F-01

## Review

Read the [finding](../findings/F-01-BOLA-document-update.md), compare the [two-line fix](https://github.com/Skrakee/workboard-appsec-portfolio/commit/066e3affecfbf7bbb12909d6ff090858271403ac), then open the [before/after evidence](../findings/evidence/F-01/README.md).

## Run the regression tests

From a clone of this repository, use Python 3.12 in an activated virtual environment:

```bash
python -m pip install -r requirements-dev.txt
```

Run the same tests before and after the fix. Use a clean worktree before switching revisions.

```bash
git switch --detach 092c9b5c63814497720dc6594c2e13ec71b0c0aa
python -m pytest tests/ -q
# Expected: 2 failed, 14 passed

git switch --detach 066e3affecfbf7bbb12909d6ff090858271403ac
python -m pytest tests/ -q
# Expected: 16 passed
```

Each test uses a temporary SQLite database and leaves the Docker database unchanged.

Return to the working branch:

```bash
git switch fix/f-01-document-authorization
```

## Repeat the manual check

1. From the fixed checkout, run `docker compose up --build -d workboard`.
2. Sign in as `admin@atlas.test` and obtain a fresh token.
3. Replay the [post-fix capture](../findings/evidence/F-01/post-fix.http), replacing the token placeholder; expect `404 Document not found`.
4. Sign in as `admin@boreal.test`, reload document `201`, and confirm its contents did not change.
5. Also check that same-tenant administrator editing succeeds.

The [evidence index](../findings/evidence/F-01/README.md) records the checks already completed.

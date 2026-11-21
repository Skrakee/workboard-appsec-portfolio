# Workboard AppSec Portfolio

A small local document workspace used to demonstrate one AppSec finding from manual reproduction to a code fix and automated regression coverage.

**Educational lab:** the application and its weaknesses were intentionally seeded. The project owner reproduced F-01 manually with Burp Suite. The repository history is reconstructed from a preserved pre-fix source snapshot so the vulnerable code, regression test and remediation can be reviewed as separate commits; it is not an original chronological development record.

## Review in this order

1. [Security design and authorization policy](docs/security-design.md).
2. [F-01: cross-tenant document modification](findings/F-01-BOLA-document-update.md), including the sanitized request and response.
3. The baseline implementation of `update_doc` in the initial lab-source commit.
4. The regression-test commit and the remediation commit in the F-01 pull request.
5. [Actual CI results](docs/ci-evidence.md): the pre-fix regression produced **2 failed, 14 passed**; the fixed code produced **16 passed**. See [pull request #1](https://github.com/Skrakee/workboard-appsec-portfolio/pull/1) for the commit sequence.

## Run locally

The app contains additional intentional weaknesses. Use synthetic data and a local-only instance. Read [SECURITY_SCOPE.md](SECURITY_SCOPE.md).

```bash
docker compose up --build -d
```

Open `http://127.0.0.1:8085`. Compose publishes the app on loopback only.

| Organization | Role | Email | Demo password |
| --- | --- | --- | --- |
| Atlas | admin | admin@atlas.test | AtlasAdmin123! |
| Atlas | member | member@atlas.test | AtlasMember123! |
| Boreal | admin | admin@boreal.test | BorealAdmin123! |
| Boreal | member | member@boreal.test | BorealMember123! |

Atlas documents: `101`, `102`. Boreal documents: `201`, `202`.

## Run tests

With Python 3.12 and a virtual environment:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest tests/ -q
```

Tests run the FastAPI application through `TestClient` with a temporary SQLite database; a running Docker instance or Burp is not required.

The `Tests` workflow runs on pull requests targeting `main` and pushes to `main`. GitHub's current account plan does not support protected branches in this private repository, so required-check enforcement is not enabled. CI results remain visible in the pull request; the remediation was validated before merging.

## Scope

The demonstrated issue is BOLA in document editing. Other seeded weaknesses are outside the remediation scope. Passing these tests is not a claim that the entire application is secure. No deployment is configured.

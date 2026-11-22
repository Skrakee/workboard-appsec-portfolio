# Workboard AppSec Portfolio

A local FastAPI/SQLite document workspace demonstrating a cross-tenant authorization flaw: reproduction, regression tests, remediation and manual retesting.

## Start here

| Document | Purpose |
| --- | --- |
| [Security design](docs/security-design.md) | Data flow, trust boundaries, threats and test coverage |
| [F-01 finding](findings/F-01-BOLA-document-update.md) | Impact, root cause and fix |
| [F-01 evidence](findings/evidence/F-01/README.md) | Before/after HTTP captures and CI results |
| [Security checks](docs/security-checks.md) | Automated scans, reports, triage and limitations |
| [Remediation PR](https://github.com/Skrakee/workboard-appsec-portfolio/pull/1) | Review the test and fix commits |

This is an educational lab with intentionally seeded weaknesses. See [scope and provenance](SECURITY_SCOPE.md).

## Run locally

From the repository directory:

```bash
docker compose up --build -d workboard
```

Open `http://127.0.0.1:8085`. After changing application code, run the same command to rebuild and replace the container.

| Organization | Role | Email | Demo password |
| --- | --- | --- | --- |
| Atlas | admin | admin@atlas.test | AtlasAdmin123! |
| Atlas | member | member@atlas.test | AtlasMember123! |
| Boreal | admin | admin@boreal.test | BorealAdmin123! |
| Boreal | member | member@boreal.test | BorealMember123! |

Atlas documents: `101`, `102`. Boreal documents: `201`, `202`.

## Run tests

With Python 3.12 in an activated virtual environment:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest tests/ -q
```

Tests use FastAPI `TestClient` and isolated temporary databases. CI runs on pull requests targeting `main` and pushes to `main`; required-check enforcement is unavailable on the current private-repository plan.

## Project outcome

F-01 demonstrates a complete remediation cycle: threat and policy definition, manual reproduction, failing regression tests, a reviewed fix, passing CI and a manual post-fix retest. The [merged PR](https://github.com/Skrakee/workboard-appsec-portfolio/pull/1) preserves that history.

Additional seeded weaknesses remain in the [threat review](docs/security-design.md#threat-review). Automated scan completion does not mean the whole application is secure.

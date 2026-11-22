# Workboard

A document workspace for teams. Users sign in to their organization's workspace, find documents and discuss them through comments. Administrators can edit document titles and content.

Workboard uses FastAPI, SQLite and a browser interface built with HTML, CSS and JavaScript. Atlas and Boreal provide sample organizations, each with an administrator and a member.

This repository is a local security engineering lab with intentionally seeded weaknesses. Assessment and remediation are ongoing; see [scope and provenance](SECURITY_SCOPE.md).

## Run the application

Prerequisite: Docker Desktop with Docker Compose. From the repository directory:

```bash
docker compose up --build -d workboard
```

Open [the workspace](http://127.0.0.1:8085) or [the API reference](http://127.0.0.1:8085/docs).

| Organization | Role | Email | Demo password |
| --- | --- | --- | --- |
| Atlas | admin | admin@atlas.test | AtlasAdmin123! |
| Atlas | member | member@atlas.test | AtlasMember123! |
| Boreal | admin | admin@boreal.test | BorealAdmin123! |
| Boreal | member | member@boreal.test | BorealMember123! |

Atlas documents are `101` and `102`; Boreal documents are `201` and `202`.

The database persists in the `workboard_data` volume. Rebuilding the application keeps existing data. To update a checkout, switch to the intended branch, pull its changes and run the same Compose command. Compose rebuilds the image and replaces its service container when needed.

Use `docker compose logs --tail 100 workboard` for startup problems and `docker compose down` to stop the application. If port 8085 is occupied, stop the unrelated container using that port.

## Development and tests

With Python 3.12 and an activated virtual environment:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest tests/ -q
```

Tests create isolated temporary databases; they do not modify the running Docker workspace. See [contributing](CONTRIBUTING.md) for change and remediation workflows.

## Repository guide

| Area | Purpose |
| --- | --- |
| [Application](app/) | API, database setup and browser interface |
| [Architecture](docs/architecture.md) | Components, data flows, API surface and trust boundaries |
| [Security requirements](docs/security-requirements.md) | Intended authorization and security behavior |
| [Threat model](docs/threat-model.md) | Attack scenarios and required controls |
| [Security testing](docs/security-testing.md) | Current coverage and investigation queue |
| [Findings](findings/README.md) | Validated issues, remediation status and evidence |
| [Security checks](docs/security-checks.md) | CI tools, reports and scan policy |
| [Tests](tests/) | Functional checks and security regressions |

The [Tests](.github/workflows/tests.yml) and [Security](.github/workflows/security.yml) workflows run on pull requests to `main` and pushes to `main`. Passing CI is one input to review; assessment coverage is tracked separately.

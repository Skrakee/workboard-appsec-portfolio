# Workboard

Workboard is a small document-sharing app. Each user belongs to an organization. Members can read documents and add comments. Admins can also edit document titles and content.

The app uses FastAPI, SQLite, HTML, CSS and JavaScript. Atlas and Boreal are the two sample organizations.

This is a local security lab with known weaknesses. The work is to find, test and fix them. See [about this lab](SECURITY_SCOPE.md).

## Run the app

Install Docker Desktop, open a terminal in this repository and run:

```bash
docker compose up --build -d workboard
```

Open [Workboard](http://127.0.0.1:8085). The [API page](http://127.0.0.1:8085/docs) lists the available requests.

| Organization | Role | Email | Password |
| --- | --- | --- | --- |
| Atlas | Admin | admin@atlas.test | AtlasAdmin123! |
| Atlas | Member | member@atlas.test | AtlasMember123! |
| Boreal | Admin | admin@boreal.test | BorealAdmin123! |
| Boreal | Member | member@boreal.test | BorealMember123! |

Atlas owns documents `101` and `102`. Boreal owns `201` and `202`.

After pulling app changes, run the same Compose command to rebuild and restart the service. Existing documents stay in the Docker data volume. Pulling code alone does not update a running container.

Use `docker compose logs --tail 100 workboard` to check startup errors, or `docker compose down` to stop the app.

## Read the project

| File | What it explains |
| --- | --- |
| [Architecture](docs/architecture.md) | How the browser, server and database work together |
| [Security rules](docs/security-requirements.md) | Who should be allowed to do what |
| [Threat model](docs/threat-model.md) | What could go wrong, and what still needs testing |
| [Tests and scans](docs/security-checks.md) | How checks run and where to read their results |
| [Findings](findings/) | Confirmed problems; each finding has its own file |

## Work on a security problem

Choose a scenario from the threat model. Test it and record what happens. If it is a real problem, copy the [finding template](findings/TEMPLATE.md), add a test, fix the code and check it again.

Keep the before-and-after results in that finding's file. Planned tests and scanner warnings are not confirmed findings.

To run the existing tests, use Python 3.12 in an activated virtual environment:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest tests/ -q
```

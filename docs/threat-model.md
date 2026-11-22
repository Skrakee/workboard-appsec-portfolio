# Threat model

## Scope and assumptions

The subject is Workboard's login, document/search/edit and comment workflows, including browser rendering and persistent SQLite data. Components and flows F1–F5 are defined in the [architecture](architecture.md); expected behavior is defined by the [security requirements](security-requirements.md).

Assets are account identity, tenant-private documents, document/comment integrity, authentication secrets and service availability. Attackers may be unauthenticated clients, members, administrators of another tenant, or users placing content that another account later views.

Accounts, roles and organization membership are seeded by the application. The current product has no registration, file upload, export, background worker or outbound integration. Those features need new modeling if introduced. The local host, Docker daemon and source checkout are trusted for this assessment.

## Abuse scenarios and controls

These are scenarios to assess, not a list of confirmed vulnerabilities. An implemented control still needs verification. Current evidence and investigation status belong in the [coverage register](security-testing.md#coverage-register).

STRIDE shorthand: **S** spoofing, **T** tampering, **R** repudiation, **I** information disclosure, **D** denial of service, **E** elevation of privilege.

| Scenario | Preconditions and attack path | Security consequence | Required control |
| --- | --- | --- | --- |
| TM-01 · S/E | A client submits a modified, expired or malformed JWT on F1, or tries to make supplied role/tenant fields authoritative. | Another account's identity or authority is used. | Verify token validity and load identity from the account store; reject invalid credentials and accounts. SR-01, SR-03 |
| TM-02 · I | An authenticated account changes the document ID or search input on F2/F4 to address another tenant's data. | Private titles or content are disclosed. | Apply tenant scope to list, search and individual reads, including failure paths. SR-02 |
| TM-03 · T | An administrator of Atlas submits an update for a Boreal document, or vice versa. | Another tenant's document is modified. | Require both administrator role and matching organization before any write; preserve data on denial. SR-02, SR-04 |
| TM-04 · E/T | A member bypasses the hidden edit button and calls PATCH directly, possibly adding role/tenant fields. | A member gains administrative editing capability. | Enforce role on the API and ignore client assertions of authority. SR-01, SR-03, SR-04 |
| TM-05 · I/T | A member or admin uses another tenant's document ID to list comments or create a comment on F2/F5. | Private discussions leak or unauthorized content is persisted. | Authorize the target document for both GET and POST; rejected creation must leave no row. SR-02, SR-04 |
| TM-06 · I/T | A signed-in user supplies SQL syntax through the search query on F4. | The intended search predicate or tenant scope changes. | Bind input as parameters and test adversarial query values. SR-02, SR-05 |
| TM-07 · T/E | A member stores markup in a comment; another member or administrator later loads it through F5/F2. | Untrusted content executes or changes the victim's page/actions. | Treat stored text as untrusted at the DOM boundary; verify behavior in another account's browser. SR-06 |
| TM-08 · I/S | A token, signing secret or real credential is committed, attached as evidence or exposed by a report/session flow. | An observer can reuse credentials or impersonate an account. | Redact evidence, review token handling and scan history; production requires private, managed signing keys. SR-01, SR-07 |
| TM-09 · D | A client repeats password verification, search or large-input requests on F1/F2. | CPU, memory or database contention makes the service unavailable. | Bound inputs and resource use, assess rate limits and run controlled load tests. SR-08 |
| TM-10 · R | A user changes a document or submits a comment, but the service records insufficient actor/target/outcome context. | A disputed action cannot be investigated reliably. | Review security-event recording, attribution and secret-free log content. SR-07, SR-10 |
| TM-11 · S/T/D | A reachable runtime dependency contains an applicable vulnerability or changes behavior during an update. | The service's security properties or availability fail. | Review dependency versions and advisories, assess usage, and validate updates against regressions. SR-09 |

## Investigation approach

Start with unverified tenant boundaries and user-controlled data paths. For each scenario, identify the exact route, account and target; state the expected control; inspect the implementation; then collect reproducible evidence. Include allowed operations as well as denials so a fix does not simply disable the feature.

A scenario becomes a finding only when evidence supports a specific policy violation and impact. Scanner alerts and suspicious code are investigation inputs. Severity belongs to the validated finding; no numerical risk score is assigned to untested scenarios here.

When routes, identity, storage, rendering or dependencies change, review the affected flows and requirements, update the coverage register, and add regression tests for confirmed issues.

Method reference: [OWASP Threat Modeling](https://owasp.org/www-community/Threat_Modeling). The model describes what is being built, what can go wrong, intended controls and how those controls will be checked.

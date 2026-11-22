# Security requirements

These requirements describe intended Workboard behavior. They are acceptance criteria for implementation and assessment, not a declaration that the current application meets every requirement.

## Authorization policy

| Operation | Unauthenticated | Same-tenant member | Same-tenant admin | Other-tenant account |
| --- | --- | --- | --- | --- |
| List/search documents | Deny | Allow | Allow | No other-tenant results |
| Read a document | Deny | Allow | Allow | Deny |
| Read/add comments | Deny | Allow | Allow | Deny |
| Edit document title/content | Deny | Deny | Allow | Deny |

Login, static assets, health and API documentation are public. An admin's authority ends at the organization's boundary. Both roles may comment; neither role should read another organization's private documents.

For editing, missing authentication returns 401; an authenticated member receives 403; an administrator requesting a missing or other-tenant document receives 404. A rejected write must not change stored data. The policy above applies to both organizations; the [coverage register](security-testing.md#coverage-register) records which combinations are tested.

## Acceptance criteria

| ID | Requirement | Verification approach |
| --- | --- | --- |
| SR-01 | Protected endpoints require a valid, unexpired signed JWT for an existing account. Role and organization are loaded server-side. Invalid credentials/tokens must not disclose another identity. | Missing, expired, modified and malformed tokens; unknown accounts; invalid passwords |
| SR-02 | Document listing, search, individual reads, updates and comments enforce the caller's organization. Guessing an ID must not cross this boundary. | Repeat read/write operations across both tenants and roles |
| SR-03 | Only an administrator may change document title or content within their own tenant. Request fields and UI state cannot grant that role. | Direct API calls as members/admins; role-tampering attempts |
| SR-04 | Rejected writes preserve stored data. Valid writes persist the requested fields without altering tenant or ownership metadata. Missing objects are handled consistently. | Independent before/after database snapshots and response assertions |
| SR-05 | Search input is treated as SQL data through parameter binding; malformed input cannot change query scope or SQL structure. | Code review plus search tests with quotes and SQL syntax |
| SR-06 | Document and comment text is rendered as text. Any explicitly supported HTML must be sanitized against a defined policy. Stored input must not execute in another user's browser. | Source-to-DOM review and controlled browser verification |
| SR-07 | Real credentials, JWTs and signing secrets are excluded from repository evidence and reports. Authentication artifacts are handled for their lifetime without exposing them in logs. | Secret scan, sanitized captures and session-handling review |
| SR-08 | Input and resource use are bounded; repeated expensive requests must not exhaust the workspace service. | Boundary-value tests and controlled resource/rate-limit assessment |
| SR-09 | Runtime dependency advisories are reviewed for affected versions and application relevance; updates preserve compatibility and regression behavior. | SCA triage and tested dependency changes |
| SR-10 | Security-relevant actions can be attributed to an account, target, time and outcome without logging secrets. | Authentication/update/comment audit review |

The local lab deliberately uses published synthetic credentials and development signing secrets. Their exception is documented in [scope](../SECURITY_SCOPE.md) and narrowly reflected in [.gitleaks.toml](../.gitleaks.toml); it is not a production secret-management design.

Use the stable SR identifiers in [threat scenarios](threat-model.md), [test coverage](security-testing.md) and confirmed [findings](../findings/README.md). Record actual results in those assessment records rather than rewriting acceptance criteria to match current behavior.

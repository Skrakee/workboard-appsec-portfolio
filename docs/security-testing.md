# Security testing

This register connects [threat scenarios](threat-model.md) to assessment work. It is the starting point for the next investigation. Confirmed issue reports and their closure evidence belong in [findings](../findings/README.md).

## Test setup

Use the local Docker application and the four [sample accounts](../README.md#run-the-application). Record the tested commit, account/role/organization, target object, request and expected policy before testing. For stored data, capture a baseline and verify the stored result after the request; a response status alone is insufficient for write authorization.

Automated tests use FastAPI `TestClient` with a new temporary database for each test. The `login_as` fixture obtains a JWT through the login route. They do not test browser execution or the running Docker container.

## Coverage register

**Partial** means only the listed cases have evidence. **Candidate** means source/scanner evidence warrants investigation, without a completed exploit/retest. **Planned** means the validation has not been performed. **Verified** applies only to the specified scenario and accounts.

| Scenario | Existing evidence and status | Remaining assessment |
| --- | --- | --- |
| TM-01: authentication and identity | Partial: invalid-password login, profile lookup and missing-authentication tests exist. | Modified/expired/malformed tokens, unknown accounts and token-lifetime edge cases |
| TM-02: document read/search isolation | Partial: `test_list_docs_is_org_scoped` checks the Atlas member's list. Source review notes no tenant check in `read_doc`. | Individual reads and search across both organizations and roles; record a finding only after validation |
| TM-03: cross-tenant updates | Verified for administrator cross-tenant edits: automation covers both directions and unchanged database rows; manual Atlas-to-Boreal retest is recorded in [F-01](../findings/F-01-BOLA-document-update.md). | Extend coverage if the update interface or tenancy model changes |
| TM-04: member privilege boundary | Partial: automated Atlas-member edits to own/other-tenant documents are denied without changes; same-tenant admin updates succeed in both organizations. | Boreal-member cases and explicit client-field tampering |
| TM-05: comment isolation | Partial: an Atlas-member comment round trip and cross-tenant comment GET denial are tested. | Cross-tenant POST with unchanged row count, reverse direction and admin/member combinations |
| TM-06: search SQL handling | Candidate: interpolation in `search_docs` and a Semgrep match. | Reproduce impact using controlled search inputs; add positive/negative regression coverage with any fix |
| TM-07: stored content rendering | Candidate: comment body reaches `innerHTML`; Semgrep flags the sink. | Controlled browser verification with a second account; distinguish plain-text rendering from permitted HTML |
| TM-08: secret/session exposure | Partial: Gitleaks history scan and redacted HTTP/report evidence exist. | Review session handling and evidence exports; the documented synthetic-value exception remains |
| TM-09: resource exhaustion | Planned: input limits and container constraints are visible in configuration; no load result is recorded. | Boundary inputs and controlled repeated requests; assess application rate limits |
| TM-10: security-event attribution | Planned: no completed audit/logging assessment is recorded. | Check actor, target, time and outcome for login, edit and comment operations |
| TM-11: dependencies | Candidate: the [scan review](../security/reviews/2026-11-22.md) records package advisory entries. | Advisory-by-advisory applicability, reachable behavior and compatible update validation |

## Existing automated assertions

The current suite has 16 cases, including parametrized cases. These names refer to code that exists today:

| Behavior | Test source and assertions |
| --- | --- |
| Basic service behavior | [test_functional_baseline.py](../tests/test_functional_baseline.py): health, login/profile, tenant-scoped list, member edit denial, comment round trip, comment-read denial and missing authentication |
| Cross-tenant edits | [test_document_authorization.py](../tests/test_document_authorization.py): `test_admin_cannot_edit_another_organization` checks both tenant directions and compares full database snapshots |
| Allowed updates | Same file: `test_admin_can_edit_own_organization` checks response and persistence in both organizations |
| Rejected updates | Same file: `test_member_cannot_edit_documents`, `test_unauthenticated_edit_is_denied` and `test_admin_editing_missing_document_gets_not_found` |

Use [CONTRIBUTING.md](../CONTRIBUTING.md) for the investigation-to-fix workflow. Add real tests when performing that work; planned cases in this register are not implemented tests. Tool execution and report interpretation are documented separately in [security checks](security-checks.md).

Testing reference: [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/).

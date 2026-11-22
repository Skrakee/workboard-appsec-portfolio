# F-01: Cross-tenant document modification

| Field | Value |
| --- | --- |
| Status | Fixed; automated regression and manual Atlas-to-Boreal retest passed |
| Endpoint | `PATCH /api/docs/{doc_id}` |
| Classification | BOLA — OWASP API1:2023 |
| Severity | High (provisional; cross-tenant integrity impact) |
| Origin | Seeded educational lab |

## Finding

An authenticated Atlas administrator could change the title and content of a Boreal document by sending a PATCH request with its document ID. This violated tenant isolation and affected document integrity.

## Reproduce

1. Sign in as `admin@atlas.test`; confirm `org_id: 1` and `role: admin` through `GET /api/me`.
2. Send a PATCH to Boreal document `201` with the same bearer token.
3. Before the fix, the API returned `200 OK` and stored the submitted values.

See the [before/after HTTP captures and validation results](evidence/F-01/README.md).

## Root cause and fix

The `update_doc` route in [app/main.py](../app/main.py) checked the administrator role but not the document's organization. The [fix](https://github.com/Skrakee/workboard-appsec-portfolio/commit/066e3affecfbf7bbb12909d6ff090858271403ac) compares `doc["org_id"]` with `user["org_id"]` before any write and returns `404 Document not found` on a mismatch.

## Verification

The new regression tests failed before remediation and passed afterward. A manual retest on 2026-11-22 confirmed the Atlas-to-Boreal PATCH was rejected with `404`; the document retained its original title and content.

The [evidence index](evidence/F-01/README.md) separates manual observations from automated coverage.

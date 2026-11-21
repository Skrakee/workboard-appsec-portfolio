# F-01: Cross-tenant document modification (BOLA)

**Status:** Verified; vulnerable implementation retained in the baseline commit  
**Origin:** Seeded local AppSec training vulnerability  
**Endpoint:** `PATCH /api/docs/{doc_id}`  
**Classification:** OWASP API1:2023 — Broken Object Level Authorization  
**Severity:** High (provisional: cross-tenant integrity impact)

## Summary and impact

An authenticated Atlas administrator can modify a Boreal document by changing its ID in a PATCH request. The endpoint checks the administrator role but fails to verify the document's organization, allowing unauthorized changes to another tenant's title and content.

## Reproduction and evidence

1. Sign in as `admin@atlas.test`.
2. Send `GET /api/me` with the token; the captured response is:

```json
{"id":1,"email":"admin@atlas.test","org_id":1,"role":"admin"}
```

3. Using the same token, send:

```http
PATCH /api/docs/201 HTTP/1.1
Host: 127.0.0.1:8085
Authorization: Bearer <ATLAS_ADMIN_TOKEN>
Content-Type: application/json

{"title":"Atlas - Q4 Plan","content":"check"}
```

4. The vulnerable implementation returns:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{"id":201,"org_id":2,"owner_id":4,"title":"Atlas - Q4 Plan","content":"check"}
```

5. Open document `201` as `admin@boreal.test`; the project owner's supplied screenshot shows the submitted title and content.

**Expected:** Reject the edit and leave the document unchanged.  
**Actual:** An administrator from organization 1 updated a document in organization 2.

These HTTP exchanges were captured manually by the project owner on 2026-11-21. Tokens and unrelated headers are omitted.

## Root cause and remediation

In `app/main.py`, `update_doc` checks the role and loads the document by ID, then updates it without comparing the two organization IDs. The remediation must compare `doc["org_id"]` with `user["org_id"]` before any write and reject mismatches with `404 Document not found`, consistent with the cross-tenant comments policy.

## Verification

Add tests for cross-tenant rejection in both directions with unchanged stored data, successful same-tenant admin updates, member/unauthenticated denials, and missing documents. Record actual pre-fix and post-fix CI results in the pull request. Repeat the original Burp request against the rebuilt local app after remediation; this manual post-fix HTTP retest is still pending.

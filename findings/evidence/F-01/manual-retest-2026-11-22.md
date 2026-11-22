# F-01 manual post-fix retest — 2026-11-22

## Scope and provenance

The project owner performed this retest against the rebuilt local Docker application at `http://127.0.0.1:8085` and supplied the HTTP exchanges and a post-request screenshot. The HTTP requests were replayed by the project owner; this record preserves the supplied results.

The recorded source checkout is `fix/f-01-document-authorization` at `eef38c82aab17ed90e34d9c7e237123f73211795`, which includes the tenant-isolation fix `066e3affecfbf7bbb12909d6ff090858271403ac`. The checkout branch reference was read during documentation.

The original bearer token is replaced consistently with `<ATLAS_ADMIN_TOKEN>`. Browser-specific headers and Content-Length are omitted; request bodies, response status, identity, response bodies and server Date headers are preserved.

## 1. Confirm the caller's identity

Request:

```http
GET /api/me HTTP/1.1
Host: 127.0.0.1:8085
Authorization: Bearer <ATLAS_ADMIN_TOKEN>
```

Response supplied by the project owner:

```http
HTTP/1.1 200 OK
date: Sun, 22 Nov 2026 08:40:56 GMT
server: uvicorn
content-type: application/json

{"id":1,"email":"admin@atlas.test","org_id":1,"role":"admin"}
```

This identifies the caller as an Atlas administrator in organization 1. The same bearer token was used in the update attempt below.

## 2. Attempt to modify another tenant's document

Request:

```http
PATCH /api/docs/201 HTTP/1.1
Host: 127.0.0.1:8085
Authorization: Bearer <ATLAS_ADMIN_TOKEN>
Content-Type: application/json

{"title":"check","content":"BOLA check"}
```

Response supplied by the project owner:

```http
HTTP/1.1 404 Not Found
date: Sun, 22 Nov 2026 08:41:27 GMT
server: uvicorn
content-type: application/json

{"detail":"Document not found"}
```

The cross-tenant edit was rejected. The response was captured at 10:41:27 Israel time (UTC+02:00).

## 3. Check the victim document

The owner confirmed that document 201 remained unchanged. The supplied post-request screenshot shows:

| Field | Visible value after the rejected request | Attempted replacement |
| --- | --- | --- |
| Tenant/document | Boreal / Document #201 | Document 201 |
| Title | Boreal - Project Notes | check |
| Content | Boreal private notes | BOLA check |

The displayed title and content remain the original values, rather than the attempted replacements. The original screenshot was supplied by the project owner and is not embedded in this repository; its visible fields are transcribed above.

The supplied evidence does not include a separate before-and-after GET trace or database query; the unchanged-data observation is the owner's report supported by the screenshot.

## Result and remaining manual coverage

**Verified manually:** Atlas administrator identity, rejection of the Atlas-to-Boreal PATCH with `404 Document not found`, and owner-reported unchanged document contents corroborated by the supplied screenshot.

**Covered by the existing automated suite:** cross-tenant denial in both directions, unchanged stored data, allowed same-tenant administrator updates, member denials, unauthenticated denial and a missing document.

A separate manual same-tenant successful edit and a manual Boreal-to-Atlas attempt were not supplied and are not claimed here. This retest verifies the demonstrated F-01 attack path; it is not a security assessment of all application endpoints.

See the [finding report](../../F-01-BOLA-document-update.md) and [automated CI evidence](../../../docs/ci-evidence.md).

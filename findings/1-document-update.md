# Finding 1: An admin could edit another organization's document

**Status:** Fixed. **Severity:** High (initial rating).

An Atlas admin could change Boreal document `201` by sending its ID in an edit request. An admin should only be able to edit documents in their own organization.

Testing used the local app at `http://127.0.0.1:8085`. `GET /api/me` confirmed user `1` was `admin@atlas.test`, with `org_id: 1` and `role: admin`.

The examples below shorten the requests and responses. The sign-in token is replaced with a placeholder.

## Before the fix — 2026-11-21

```http
PATCH /api/docs/201 HTTP/1.1
Host: 127.0.0.1:8085
Authorization: Bearer <ATLAS_ADMIN_TOKEN>
Content-Type: application/json

{"title":"Atlas - Q4 Plan","content":"check"}

HTTP/1.1 200 OK

{"id":201,"org_id":2,"owner_id":4,"title":"Atlas - Q4 Plan","content":"check"}
```

The request succeeded and changed the Boreal document.

## The fix

The server checked the admin role but did not check the document's organization. The [fix](https://github.com/Skrakee/workboard-appsec-portfolio/commit/066e3affecfbf7bbb12909d6ff090858271403ac) compares the user's organization with the document's organization before saving changes.

## After the fix — 2026-11-22

```http
PATCH /api/docs/201 HTTP/1.1
Host: 127.0.0.1:8085
Authorization: Bearer <ATLAS_ADMIN_TOKEN>
Content-Type: application/json

{"title":"check","content":"BOLA check"}

HTTP/1.1 404 Not Found

{"detail":"Document not found"}
```

The manual browser check showed the original title, `Boreal - Project Notes`, and content, `Boreal private notes`, were unchanged. The retest used [this code version](https://github.com/Skrakee/workboard-appsec-portfolio/commit/eef38c82aab17ed90e34d9c7e237123f73211795).

## Automated tests

| Stage | Result |
| --- | --- |
| Original tests | [8 passed](https://github.com/Skrakee/workboard-appsec-portfolio/actions/runs/44939270429) |
| New tests before the fix | [2 failed, 14 passed](https://github.com/Skrakee/workboard-appsec-portfolio/actions/runs/44939343951) |
| After the fix | [16 passed](https://github.com/Skrakee/workboard-appsec-portfolio/actions/runs/44939617719) |

The [authorization tests](../tests/test_document_authorization.py) check edits in both organization directions, unchanged stored data after rejection, allowed admin edits and rejected member edits.

The manual retest checked Atlas-to-Boreal editing. The opposite direction and allowed edits were checked by automated tests.

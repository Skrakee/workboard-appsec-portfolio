# F-01 evidence

## Manual verification

Both captures target the local application at `http://127.0.0.1:8085`, using an Atlas administrator to edit Boreal document `201`. Tokens are replaced with `<ATLAS_ADMIN_TOKEN>`; unrelated headers are omitted.

| Stage | Capture | Observed result |
| --- | --- | --- |
| Before fix — 2026-11-21 | [pre-fix.http](pre-fix.http) | `200 OK`; submitted title and content were stored |
| After fix — 2026-11-22 | [post-fix.http](post-fix.http) | `404 Document not found`; original content remained |

After the rejected request, the manual UI check showed title `Boreal - Project Notes` and content `Boreal private notes`, rather than the attempted `check` / `BOLA check`. The supporting screenshot is not attached; these are the recorded visible values.

Post-fix checkout: `eef38c82aab17ed90e34d9c7e237123f73211795`, which includes fix `066e3af`.

## Automated verification

| Stage | Commit | Result | CI run |
| --- | --- | --- | --- |
| Baseline tests | [7886709](https://github.com/Skrakee/workboard-appsec-portfolio/commit/78867096b84b577a8f471fafe32211eaf56b47bf) | 8 passed | [Baseline](https://github.com/Skrakee/workboard-appsec-portfolio/actions/runs/44939270429) |
| Regression before fix | [092c9b5](https://github.com/Skrakee/workboard-appsec-portfolio/commit/092c9b5c63814497720dc6594c2e13ec71b0c0aa) | 2 failed, 14 passed | [Pre-fix](https://github.com/Skrakee/workboard-appsec-portfolio/actions/runs/44939343951) |
| After fix | [066e3af](https://github.com/Skrakee/workboard-appsec-portfolio/commit/066e3affecfbf7bbb12909d6ff090858271403ac) | 16 passed | [Post-fix](https://github.com/Skrakee/workboard-appsec-portfolio/actions/runs/44939617719) |

The two failures were cross-tenant administrator edits in opposite directions. Tests also verify unchanged stored data, allowed same-tenant edits, member denials, unauthenticated denial and missing documents through FastAPI routes and JWT authentication.

The manual retest covers Atlas-to-Boreal denial and unchanged content. Same-tenant success and reverse-direction denial are covered by automation; no additional manual result is claimed.

[Finding](../../F-01-BOLA-document-update.md)

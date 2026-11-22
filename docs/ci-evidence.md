# F-01 CI evidence

These results come from actual GitHub Actions jobs, not simulated assertions.

| Stage | Commit | Actual pytest result | Run |
| --- | --- | --- | --- |
| Baseline functional coverage | `7886709` | 8 passed | [Baseline run](https://github.com/Skrakee/workboard-appsec-portfolio/actions/runs/44939270429) |
| Regression before remediation | `092c9b5` | 2 failed, 14 passed | [Pre-fix run](https://github.com/Skrakee/workboard-appsec-portfolio/actions/runs/44939343951) |
| After remediation | `066e3af` | 16 passed | [Post-fix run](https://github.com/Skrakee/workboard-appsec-portfolio/actions/runs/44939617719) |

The two pre-fix failures were:

- `test_admin_cannot_edit_another_organization[atlas-cannot-edit-boreal]`
- `test_admin_cannot_edit_another_organization[boreal-cannot-edit-atlas]`

Both received `200` instead of the expected `404` and observed modified stored data. After the fix, the requests were rejected and data remained unchanged; same-tenant administrator edits still succeeded.

## Reproduce rather than rely on retained logs

Follow the [interview demo](interview-demo.md) to run the same test suite at the pre-fix commit and the fixed commit. Run links provide the original CI context; this summary preserves the observed counts, and the commits preserve the executable source and tests.

## Scope

Tests use the actual FastAPI routes, login/JWT path and temporary SQLite databases through `TestClient`. They do not establish that the entire intentionally vulnerable lab is secure.

## Manual post-fix verification

On 2026-11-22, the project owner supplied `/api/me` evidence confirming the Atlas administrator identity and a PATCH to Boreal document 201 with the same bearer token. The update was rejected with `404 Document not found`; the owner confirmed unchanged document contents, supported by a post-request screenshot. See the [sanitized manual retest record](../findings/evidence/F-01/manual-retest-2026-11-22.md) for the exact exchanges and evidence limits.

Manual same-tenant successful editing was not supplied; that positive control remains covered by the existing automated tests. The original automated CI counts above are unchanged.

GitHub rejected branch-protection configuration for this private repository with: "Upgrade to GitHub Pro or make this repository public to enable this feature." The repository remains private. CI is active; enforced required checks are not.

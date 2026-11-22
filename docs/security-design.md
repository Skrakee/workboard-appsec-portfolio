# Security design

Workboard is a local FastAPI/SQLite document workspace with two tenants, Atlas and Boreal, and two roles: `admin` and `member`. JWT authentication identifies the user; the API loads the role and organization from SQLite.

## Authorization policy

| Action | Own-tenant member | Own-tenant admin | Other-tenant user |
| --- | --- | --- | --- |
| Read a document | Allow | Allow | Deny |
| Read/add comments | Allow | Allow | Deny |
| Edit title/content | Deny | Allow | Deny |

This is the intended policy. F-01 verifies and fixes document editing.

## Threat and control

The browser is untrusted. Changing `/api/docs/101` to `/api/docs/201` must not let an Atlas administrator modify a Boreal document, regardless of which buttons the UI displays.

The API must enforce both `role == admin` and `user.org_id == doc.org_id` before writing. The vulnerable route checked only the role; the fix rejects a tenant mismatch with `404 Document not found`.

See the [finding](../findings/F-01-BOLA-document-update.md), [evidence](../findings/evidence/F-01/README.md) and [regression tests](../tests/test_document_authorization.py).

# Security design: document editing

Workboard is a local FastAPI/SQLite document workspace with two tenants, Atlas and Boreal. JWT authentication identifies a user; the API loads the user's role and organization from SQLite. Roles are `admin` and `member`.

## Authorization policy

| Action | Own-tenant member | Own-tenant admin | Other-tenant user |
| --- | --- | --- | --- |
| Read a document | Allow | Allow | Deny |
| Read/add comments | Allow | Allow | Deny |
| Edit title/content | Deny | Allow | Deny |

This is the intended policy, not a claim that every existing endpoint enforces it. This portfolio finding fixes document editing only.

## Threat and control

The browser is untrusted: an attacker can change the document ID regardless of which buttons the UI displays. For an edit, the server must enforce both `role == admin` and `user.org_id == doc.org_id`, using server-side data.

The concrete threat is cross-tenant tampering: an Atlas administrator changes `/api/docs/101` to `/api/docs/201` and modifies a Boreal document. The vulnerable version enforces the role check only. The remediation rejects a tenant mismatch before the database update.

Tests cover the denial and unchanged database state, allowed updates in each tenant, member denials, unauthenticated requests and a missing document. Each test uses an isolated temporary database.

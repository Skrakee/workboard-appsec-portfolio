# Security rules

These are the rules Workboard should follow. Some still need to be tested or fixed.

## Who can do what?

| Action | Member in the same organization | Admin in the same organization | User from another organization |
| --- | --- | --- | --- |
| Read or search documents | Allow | Allow | Deny access to the other organization's documents |
| Read or add comments | Allow | Allow | Deny |
| Edit document title and content | Deny | Allow | Deny |

Users must sign in before using these actions. Login, the home page, the health check and the API documentation are public.

An admin's permissions apply only to their own organization. Sending a different document ID must not change that rule.

## Other rules

- The server must reject invalid or expired sign-in tokens.
- The server must load the user's role and organization itself. It must not trust role or organization values sent by the browser.
- A rejected edit must leave the saved document unchanged.
- Search text must be passed as SQL data, not added directly to the SQL command.
- Comments and document text must not run as JavaScript in another user's browser.
- Real passwords and sign-in tokens must not appear in reports or Git history.
- Input limits and request controls should keep one user from overloading the app.
- Library security warnings need review, and updates need testing.
- Logs should help identify who performed important actions without recording passwords or tokens.

For document edits, a missing sign-in token returns `401`. A member trying to edit receives `403`. An admin trying to edit a missing document or another organization's document receives `404`.

See the [threat model](threat-model.md) for the current testing status.

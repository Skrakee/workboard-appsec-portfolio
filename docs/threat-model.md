# Threat model

This is a list of things that could go wrong in Workboard. Each scenario says what should happen and what has been checked. A scenario is not automatically a confirmed finding.

A JWT is the sign-in token sent with API requests. STRIDE is a way to name the type of threat; the letters below are written out.

## 1. Pretending to be another user

A user changes a sign-in token to pretend to be someone else. They may also try an expired or broken token.

**STRIDE:** S — Spoofing.

**Expected:** The server rejects the request. It loads the account, role and organization from the database.

**Status:** Basic login and missing-token tests exist. Changed, expired and broken tokens still need testing.

## 2. Reading another organization's document

A user changes the document ID, or uses search, to try to read another organization's documents.

**STRIDE:** I — Information disclosure.

**Expected:** The server returns only documents the user may read.

**Status:** The document list is tested for an Atlas member. Individual document reads and search need more testing.

## 3. Changing another organization's document

An Atlas admin sends an edit request for a Boreal document, or the other way around.

**STRIDE:** T — Tampering.

**Expected:** The server rejects the edit and leaves the document unchanged.

**Status:** Fixed and tested. See [finding 1](../findings/1-document-update.md).

## 4. Editing documents as a member

A member sends an edit request directly, even though the page hides the edit button.

**STRIDE:** E — Elevation of privilege.

**Expected:** The server rejects the edit. Sending extra role or organization fields must not help.

**Status:** Atlas-member edits are rejected in the existing tests. More account combinations and extra request fields still need testing.

## 5. Reading or posting comments in another organization

A user changes the document ID to read another organization's comments or add a comment there.

**STRIDE:** I — Information disclosure; T — Tampering.

**Expected:** Both requests are rejected. A rejected request must not save a comment.

**Status:** Some comment tests exist. Posting across organizations and checking both directions still need testing.

## 6. Changing a database query through search

A user puts SQL characters into the search box to change what the database query does.

**STRIDE:** I — Information disclosure; T — Tampering.

**Expected:** The server treats the search value as text and keeps results inside the user's organization.

**Status:** Code review and Semgrep flagged the query. Its actual effect still needs a separate test.

## 7. Running code through a saved comment

A user saves a comment containing HTML or JavaScript. Another user later opens that document.

**STRIDE:** T — Tampering; E — Elevation of privilege.

**Expected:** The page displays safe text rather than running the comment as code.

**Status:** Semgrep flagged the use of `innerHTML`. A browser test with another account is still needed.

## 8. Exposing a password or sign-in token

A real password, token or signing secret appears in a commit, log or report. Someone else may use it to sign in.

**STRIDE:** I — Information disclosure; S — Spoofing.

**Expected:** Sensitive values are kept out of reports and protected during use.

**Status:** Git history is scanned and recorded tokens are hidden. Browser token handling still needs review. The published sample passwords and signing secrets are only for this local lab.

## 9. Overloading the app

A user repeatedly sends login, search or large requests until the app stops responding.

**STRIDE:** D — Denial of service.

**Expected:** Input limits and request controls protect the app from excessive work.

**Status:** Some input and Docker limits exist. No load-test result is recorded.

## 10. Not knowing who changed something

A document changes, but the logs do not show enough information to identify the account and action.

**STRIDE:** R — Repudiation.

**Expected:** Important actions can be traced without logging passwords or tokens.

**Status:** Logging has not yet been assessed.

## 11. Using a library with a security problem

A library used by the app has a known bug that may affect Workboard.

**STRIDE:** The category depends on the bug. Examples include S — Spoofing, I — Information disclosure and D — Denial of service.

**Expected:** Check whether the app uses the affected feature, then test a suitable update.

**Status:** The library scan reported warnings. Their effect on Workboard still needs review.

# Scope and provenance

## Assessment scope

Workboard is an educational workspace with seeded weaknesses and an ongoing security assessment. The assessment includes authentication, tenant/role authorization, document search/editing, comments, browser rendering, dependency review and local runtime configuration.

Use synthetic accounts and data. Run the application and testing tools against the local instance at `http://127.0.0.1:8085`; preserve the loopback binding. Do not deploy this lab publicly.

The host and Docker administration environment are trusted. Third-party services, cloud infrastructure and production deployment are not part of this implementation. Requirements and threat scenarios describe the intended behavior; [coverage](docs/security-testing.md) distinguishes completed work from planned investigations.

## Development-only credentials

The published demo passwords and development `APP_SECRET` values are deliberate local fixtures. They are not evidence of production secret management. Gitleaks allows only the two exact documented signing-secret strings; real credentials and live JWTs must still be removed from evidence and reports.

## Provenance and evidence

The application contains intentionally seeded weaknesses. The historical F-01 demonstration commit sequence was reconstructed from a preserved vulnerable source snapshot; it is not the original development timeline. The recorded original proof of concept and post-fix retest were performed manually with Burp Suite.

Preserve those historical [captures and CI results](findings/evidence/F-01/README.md). They establish the documented finding's behavior at the recorded versions, not complete application security or unperformed tests. Later investigations receive their own evidence and status.

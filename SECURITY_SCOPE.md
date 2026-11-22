# Scope and provenance

## Scope

Workboard is an intentionally vulnerable educational lab. F-01 covers document editing across Atlas and Boreal; other weaknesses remain outside this fix. Passing the regression suite does not establish that all endpoints are secure.

Run the app and any active scans only against the local instance at `http://127.0.0.1:8085`. Keep the loopback port binding, use synthetic data, and do not deploy this lab publicly. Demo passwords and `APP_SECRET` are development-only values.

## Provenance

The application includes seeded weaknesses. The original F-01 proof of concept and post-fix retest were performed manually with Burp Suite. The demonstration commit sequence was reconstructed from a preserved vulnerable source snapshot; it is not the original development timeline.

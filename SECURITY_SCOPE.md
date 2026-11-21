# Security scope and disclosure

**This is intentionally vulnerable software for an isolated AppSec portfolio exercise.**
Some weaknesses were **seeded intentionally** by the project author. They are not vulnerabilities discovered in an unrelated upstream application. Never portray seeded findings as independent discoveries.

Run only on your own machine. Docker Compose binds the HTTP port to `127.0.0.1:8085`; do not change the binding to a public interface or deploy to the Internet. Use only synthetic demo data. Do not add real credentials, real customer information, or production services.

Run active DAST and proof-of-concept attacks **only** against the local instance (`http://127.0.0.1:8085`), never against arbitrary public hosts. Treat the app as untrusted code; Docker is not a perfect security boundary. Review dependency downloads and image contents prior to first build.

Vulnerability categories are intentionally not enumerated here to preserve a blind-testing component. Document each confirmed seeded finding with `Origin: seeded` in your final report. No finding is verified until it has a reproducible PoC.

The demo passwords and `APP_SECRET` are intentionally development-only. Do not reuse them anywhere.

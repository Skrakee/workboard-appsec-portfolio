# Security checks

The [Security workflow](../.github/workflows/security.yml) runs on pull requests to `main`, pushes to `main` and manual dispatch. It uses open-source tools without paid scanning integrations.

| Check | Scope | Policy |
| --- | --- | --- |
| Existing pytest workflow | Functional behavior and F-01 authorization requirements | Failed tests fail the check |
| Semgrep CE | Python and JavaScript under `app/`; two [local review rules](../security/semgrep.yml) | Report findings; fail on scanner errors |
| pip-audit | Runtime requirements and resolved transitive Python dependencies | Report advisories; fail on missing, incomplete or invalid results |
| Gitleaks CLI | Full fetched Git history | Fail on detected secrets; only two exact, documented lab secret values are allowlisted |
| ZAP API scan, safe mode | OpenAPI routes on a disposable Docker instance, using an Atlas admin token | Passive findings are reported; scanner/startup errors fail the check |

SAST, SCA and DAST are explicitly **report only for findings** while the intentionally vulnerable lab is retained. A green scanner job means that it completed and produced a report, not that the application has no vulnerabilities. These jobs do not enforce a production release policy.

## Read the results

Open the pull request's **Checks**, or the repository's **Actions → Security → run**. The run summary lists findings and the **Artifacts** section contains `sast-report`, `sca-report`, `secrets-report` and `dast-report`. Download the ZAP artifact and open `zap.html` for the readable report. Reports are retained for 30 days.

Each run records the source commit; Semgrep and pip-audit versions are pinned in the workflow. The ZAP image digest and Gitleaks version are saved with their reports. Re-run the workflow to refresh time-sensitive dependency advisories.

## Triage and limits

| Observation | Assessment | Next action |
| --- | --- | --- |
| Cross-tenant document update | Fixed and retested; [F-01 evidence](../findings/evidence/F-01/README.md) | Keep authorization regressions passing |
| Interpolated search SQL | Source confirms input reaches the query | Separate finding, bound parameters and regression tests |
| Stored comments assigned to HTML | Unsafe sink found in source; browser impact needs its own retest | Separate finding and safe rendering |
| Cross-tenant document read | Missing organization check in source | Separate authorization finding and tests |
| Dependency advisory | Package presence does not establish application exploitability | Review installed version, affected feature, reachability and fixed versions in the SCA report |
| Missing HTTP protection headers | Interpret in the local HTTP lab context | Review deployment controls before any production use |

The two local Semgrep rules detect review candidates, not all vulnerability classes. ZAP's safe mode does not run active attacks or execute the SPA like a full browser; it cannot establish cross-user authorization or stored-XSS exploitability. F-01 is validated by the dedicated tests and manual Burp retest.

Dependency results describe the requirements resolution at scan time; transitive dependencies and the Docker base image are not fully locked. OS-package/container-image scanning and production deployment hardening are outside this exercise.

References: [Semgrep CLI](https://semgrep.dev/docs/cli-reference), [pip-audit](https://github.com/pypa/pip-audit), [Gitleaks](https://github.com/gitleaks/gitleaks), [ZAP API scan](https://www.zaproxy.org/docs/docker/api-scan/).

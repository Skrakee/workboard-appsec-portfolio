# Contributing

Keep changes focused and describe observable behavior. Workboard's implementation, security requirements and assessment records evolve together.

## Development

Start from an up-to-date `main` and create a branch for the change. Edit the application and relevant tests, then run:

```bash
python -m pytest tests/ -q
docker compose up --build -d workboard
```

The first command tests isolated databases; the second builds the checked-out source and runs the local workspace. Verify the changed feature in the browser/API when applicable. Rebuild after application changes; pulling code alone does not update a running image.

Update [architecture](docs/architecture.md) for component/flow changes and [requirements](docs/security-requirements.md) for policy changes. Review affected [threat scenarios](docs/threat-model.md) when adding routes, inputs or identity decisions.

## Security investigation and remediation

1. Select a scenario from the [coverage register](docs/security-testing.md#coverage-register). Identify the actor, route/object, expected requirement and tested commit.
2. Investigate locally using code review and controlled requests/browser actions. Record expected and observed behavior; verify stored effects where relevant. A scanner match is a lead, not a completed finding.
3. If evidence confirms an issue, copy the [finding template](findings/TEMPLATE.md), add sanitized evidence and register the confirmed finding. Otherwise record the investigation's result without inventing a finding.
4. Add a regression that demonstrates the violation on the affected version. Implement the control and check that the regression passes while legitimate operations still work.
5. Rebuild the candidate fix and perform the relevant manual retest. Record the exact commit, account/target, response and persisted/browser effect. Do not extend the result to cases that were not tested.
6. Open a PR linking the finding, changed behavior and verification. Review [CI reports](docs/security-checks.md), update the coverage/register state, and mark the finding verified fixed only when the evidence supports it.

For ordinary feature/documentation changes, report the relevant validation; a manual security retest is not required for every edit.

## Review and merge

The [PR template](.github/pull_request_template.md) asks for the change, verification and security impact. Keep previous evidence intact, and label checks that were not run. Check workflow conclusions and reported findings separately: several scanner jobs intentionally report findings without failing.

After review and merge, update the local `main` checkout and rebuild the application when running the merged version. GitHub workflow configuration does not itself configure required-check enforcement or branch protection.

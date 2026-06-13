# Page 8: Release and CI Flow

Previous: [Troubleshooting](page-7-troubleshooting.md)

This page explains the release and CI flow in plain language.

It is a guide. The authoritative release rules live in
[docs/RELEASE.md](../RELEASE.md).

## Local Validation

Before a release candidate or final release, run the local gate:

```bash
python tools/horoji/validators/validate-all
python -m pytest
python tools/horoji/cli/horoji-check \
  --repo-root . \
  --auto-diff \
  --derived-policy committed
git diff --check
git status --short --branch
```

These commands check metadata, tests, generated artifacts, whitespace, and tree
state.

## CI Validation

The main CI workflow lives at:

```text
.github/workflows/horoji-ci.yml
```

CI installs the project, runs validators, runs `horoji-check`, and runs tests.

CI is an enforcement gate. It does not publish packages, deploy services, or
infer release approval.

## Committed Derived Policy

Horoji uses committed derived policy.

This means `.project_memory/derived/**` must be current when the gate runs. If
regeneration creates expected derived changes, those files should be committed
with the change that caused them.

## Release Decision Records

Release and release-candidate decisions live under:

```text
docs/releases/
```

Decision records explain what was reviewed, what was in scope, what was out of
scope, and which validation commands passed.

## Release Candidate Tags

A release candidate tag marks a validated review point.

It is not the final v1.0.0 release.

Example:

```text
v0.5.0-rc.1
```

## Final v1.0.0 Release Gate

The final v1.0.0 release should happen only after:

- the working tree is clean
- validators pass
- tests pass
- `horoji-check` passes with committed derived policy
- changelog is current
- a final decision record exists
- the final tag is created from a validated tree

Do not claim final production readiness before the final decision and tag.

For exact release rules, read [docs/RELEASE.md](../RELEASE.md).

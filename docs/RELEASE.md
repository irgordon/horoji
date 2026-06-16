# Horoji Release Gate

## Purpose

This document defines the release gate for Horoji release-candidate and release
work.

It does not create a release candidate, tag a release, publish a package, or
claim that Horoji is already production-ready.

## Release Gate

A release candidate must come from a validated, clean tree.

Required local checks:

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

Expected result:

- `validate-all` passes
- full `pytest` passes
- `horoji-check` passes with `--derived-policy committed`
- `.project_memory/derived/**` is clean after approved regeneration
- `git diff --check` reports no whitespace errors
- `git status --short --branch` shows a clean working tree

## CI Gate

The release-relevant CI workflow is `.github/workflows/horoji-ci.yml`.

It must:

- run on pull requests
- run on pushes to `main`
- allow manual dispatch
- install dependencies with `python -m pip install -e ".[test]"`
- run `python tools/horoji/validators/validate-all`
- run `python tools/horoji/cli/horoji-check --derived-policy committed`
- run the full pytest suite

The CI gate must not publish packages, tag releases, deploy services, or infer
approval. It is an enforcement gate only.

## Required Checks

The release gate includes:

- public CLI contract validation through `validate-cli-contract`
- authoritative contract validation through `validate-contracts`
- invariant validation through `validate-invariants`
- ownership validation through `validate-ownership`
- derived provenance validation through `validate-provenance`
- determinism and repository-locality validation through `validate-determinism`
- committed derived policy enforcement through `horoji-check`
- full regression tests through `pytest`

## Release Artifacts

Before a release candidate or final release tag, the repository must include:

- an up-to-date `CHANGELOG.md` entry
- a release or release-candidate decision record under `docs/releases/`
- committed derived artifacts required by committed derived policy
- a clean working tree

The release decision record must name the validation commands that were run and
their results.

Use `docs/VERSIONING.md` to decide whether a release should be patch, minor,
major, release-candidate, documentation-only, schema-impacting, or
CLI-impacting.

## Boundaries

Do not:

- tag from an unvalidated tree
- tag from a dirty working tree
- manually edit derived artifacts instead of using approved orchestration
- document public `horoji regenerate` or `horoji invalidate` commands
- expand the public CLI without contract, docs, parser, and validator alignment
- claim v1.0.0 production readiness before the final release decision
- use CI success as deployment, merge, promotion, or release approval

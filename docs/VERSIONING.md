# Horoji Version Policy

## Purpose

This document defines how Horoji uses release versions after v1.0.0.

The policy is practical. It helps decide whether a change belongs in a patch,
minor, major, release-candidate, or documentation-only release.

It does not create a release, tag a version, publish a package, or weaken the
release gate in `docs/RELEASE.md`.

## Baseline Rule

Every release must come from a clean, validated tree.

Before tagging, run:

```bash
python tools/horoji/validators/validate-all
python -m pytest
python tools/horoji/cli/horoji-check --repo-root . --auto-diff --derived-policy committed
git diff --check
git status --short --branch
```

The release tag should only be created when those checks pass.

## Patch Releases

Use a patch release for compatible fixes.

Examples:

- documentation corrections
- validator bug fixes that preserve the documented rule
- test fixes that preserve behavior
- packaging or CI fixes that do not change the public CLI or schema contract
- repairability improvements that preserve existing outputs

Patch releases must not introduce public CLI commands, remove fields from
governed metadata, or change schema compatibility expectations.

## Minor Releases

Use a minor release for compatible improvements.

Examples:

- new documentation or examples
- new tests that protect existing public behavior
- compatible public CLI output additions
- new validators for already-documented governance rules
- new governed metadata fields that are optional or backward-compatible
- usability improvements that preserve existing command names

Minor releases may add compatible behavior, but they must keep existing public
commands and governed metadata usable unless the release explicitly documents a
breaking change and becomes a major release.

## Major Releases

Use a major release for breaking changes.

Examples:

- removing or renaming a public CLI command
- changing required CLI arguments
- removing public output fields
- changing required metadata schema fields incompatibly
- changing authoritative versus derived trust boundaries
- changing release-gate expectations in a way older repositories cannot follow
- making public what was previously internal orchestration

Major releases require a release decision record that names the breaking
change, migration path, and validation evidence.

## Release Candidates

Use a release-candidate version when a release surface is frozen but final
release acceptance is still pending.

Examples:

- `v1.2.0-rc.1`
- `v2.0.0-rc.1`

Release candidates should:

- freeze the intended release surface
- run the normal release gate
- include a release-candidate decision record when the change is substantial
- avoid feature work unless it fixes a release blocker

## Documentation-Only Releases

A documentation-only release changes docs, examples, or decision records
without changing runtime behavior.

Documentation-only releases still need:

- changelog coverage
- committed derived artifacts when required
- normal validation
- a clean tag if a tag is created

Documentation-only does not mean validation can be skipped.

## Schema-Impacting Releases

A schema-impacting release changes governed metadata shape.

Compatible schema changes may be minor when they:

- add optional fields
- clarify existing field meaning
- add validator coverage for already-documented rules
- preserve existing valid metadata

Breaking schema changes require a major release when they:

- remove required fields
- rename required fields
- change field meaning incompatibly
- invalidate existing governed metadata without a migration path

Schema-impacting releases should update `docs/SCHEMAS.md`.

## CLI-Impacting Releases

A CLI-impacting release changes public command behavior, public output shape, or
help text.

Compatible CLI changes may be minor when they:

- improve help text
- add optional output fields
- improve repairable errors
- add tests for existing public commands
- preserve existing command names and required arguments

Breaking CLI changes require a major release when they:

- remove commands
- rename commands
- change required arguments
- remove output fields
- turn successful queries into failures for previously valid inputs

CLI-impacting releases must keep the parser, docs, authoritative CLI contract,
and tests aligned.

## Internal Orchestration

Regeneration and invalidation remain internal orchestration surfaces unless a
future release explicitly changes that boundary.

Making either one a public `horoji` command is a CLI-impacting change and may
be a major release depending on compatibility and migration impact.

## Choosing the Version

Use the highest-impact category touched by the release.

Examples:

- documentation typo only: patch
- new onboarding guide: minor or documentation-only tag
- compatible CLI output addition: minor
- optional metadata field: minor
- required schema field removal: major
- public CLI command removal: major

When unsure, document the compatibility decision in the release note or
decision record.

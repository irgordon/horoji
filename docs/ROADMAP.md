# Horoji v1.0.0 Roadmap

## Purpose

This roadmap describes the path from the accepted BASELINE-0.0.1 state to a
stable v1.0.0 production release.

It is a planning document. It does not claim that Horoji is already
production-ready, and it does not authorize runtime behavior, public CLI
expansion, schema changes, or weaker governance boundaries.

## Current Baseline

The accepted BASELINE-0.0.1 state establishes a coherent governed baseline:

- a governed baseline decision record exists
- the public CLI boundary is small and validated
- regeneration and invalidation are internal orchestration surfaces
- active tool ownership is enforced
- determinism and repository-locality boundaries are enforced
- derived artifact provenance is validated
- committed derived artifact policy passes
- README documents the current operator surface
- validation gates and regression tests pass for the baseline
- the committed-derived impact loop has been fixed
- validator exception and function-shape issues have been fixed

The baseline is not a production-readiness claim. It is the starting point for
release hardening.

## Production Release Definition

Horoji v1.0.0 is production-ready when a clean clone can install, validate,
query, and enforce repository memory boundaries reliably through documented
commands and CI gates.

Production-ready means:

- clean installation path
- stable public CLI contract
- stable metadata schemas
- documented validation gates
- reproducible derived artifacts
- CI-enforced governance
- clear operator and contributor workflows
- release decision record
- clean tag from a validated tree

Production-ready does not mean:

- autonomous reasoning
- probabilistic retrieval
- external services
- plugin marketplace
- network dependency
- source-of-truth replacement
- public regeneration or invalidation commands unless explicitly accepted
  before freeze

Canonical truth remains in repository source files and governance documents.
Horoji remains a deterministic, repository-resident projection and validation
system.

## Version Plan

### v0.1.0 — Baseline Packaging and Installability

Goal:

Make Horoji installable and runnable from a clean clone.

Expected work:

- document Python version
- document dependency setup
- document local validation commands
- confirm clean-clone validation path
- add packaging metadata if appropriate
- add CLI smoke tests if missing

Acceptance criteria:

- clean clone can run documented validation
- README setup commands work
- public CLI entrypoints work
- `validate-all` passes
- `pytest` passes
- committed derived policy passes

Non-goals:

- no daemon
- no network service
- no plugin system
- no public `horoji regenerate` command
- no public `horoji invalidate` command

### v0.2.0 — Schema Stability and Metadata Contracts

Goal:

Stabilize metadata schemas before v1.0.0.

Expected work:

- review authoritative contracts
- review invariant schemas
- review ownership metadata
- review derived artifact schemas
- add schema versioning where needed
- document compatibility rules

Acceptance criteria:

- every governed metadata type has a documented schema
- validators reject malformed metadata
- breaking changes are defined
- non-breaking changes are defined

Non-goals:

- no broad schema redesign without evidence
- no remote schema registry
- no runtime schema fetching

### v0.3.0 — Production Usability Pass

Goal:

Make the existing production-facing workflow clear and repairable without
expanding the public command surface.

Expected work:

- audit CLI help text
- improve error messages where they are not repairable
- document common query examples
- verify README setup and validation commands
- run clean-clone validation
- keep CLI contract, docs, and parser aligned

Acceptance criteria:

- CLI help output is clear
- unsupported commands fail clearly
- README commands match repository behavior
- clean clone can install, validate, and query
- query output is deterministic
- `validate-cli-contract` passes

Non-goals:

- do not add `horoji regenerate`
- do not add `horoji invalidate`
- no public CLI expansion unless required to fix a release blocker
- no interactive shell
- no natural-language query system

### v0.4.0 — Release Gate and CI Finalization

Goal:

Finalize the release gate so local and CI validation enforce the same
repository memory boundaries.

Expected work:

- confirm CI matches local validation
- confirm packaging install works in CI
- confirm committed derived policy is enforced
- align local and CI validation
- confirm release checklist exists

Acceptance criteria:

- CI runs the documented install path
- CI runs validators and tests
- CI fails on stale derived artifacts
- CI fails on governance drift
- release checklist is documented
- local and CI gates have no known drift

Non-goals:

- no deployment pipeline
- no external service dependency
- no cloud-only validation path
- no new public CLI commands

### v0.5.0-rc.1 — Release Candidate

Goal:

Tag and validate a v1.0.0 release candidate from a frozen public surface.

Expected work:

- freeze public CLI surface
- freeze schema surfaces
- run clean-clone validation
- create RC decision record
- tag release candidate

Acceptance criteria:

- public CLI freeze is documented
- schema freeze is documented
- RC decision record exists
- RC tag exists
- clean-clone validation passes
- full tests pass
- no known release-blocking governance drift

Non-goals:

- no feature work
- no schema changes unless release-blocking
- no CLI changes unless release-blocking
- no production v1.0.0 tag yet

### v0.6.0-docs — Developer and User Wiki

Goal:

Make Horoji understandable to a new developer or user before final v1.0.0.

Expected work:

- create a plain-language wiki landing page
- explain major Horoji components
- define key terms and command options
- add workflow diagrams
- add a first-hour walkthrough
- add troubleshooting guidance
- link the README to the wiki

Acceptance criteria:

- wiki landing page exists
- major components are explained
- key terms and command options are defined
- workflow diagrams are included
- first-hour walkthrough exists
- troubleshooting guide exists
- README points to the wiki
- no runtime behavior changes

Non-goals:

- no new product behavior
- no public CLI expansion
- no new validators unless required by existing checks
- no final v1.0.0 tag yet

### v1.0.0 — Production Baseline

Goal:

Publish Horoji v1.0.0 as a stable, governed, repository-resident project memory
subsystem.

Expected work:

- final release-readiness audit
- final changelog update
- final release decision document
- final tag
- clean-clone validation
- public CLI stability check
- schema stability check
- governance coherence check

Acceptance criteria:

- v1.0.0 tag exists
- final release decision exists
- full validation passes
- full tests pass
- clean-clone validation passes
- public CLI contract is stable
- metadata schemas are stable
- README accurately describes production baseline use
- no known release-blocking governance drift

Non-goals:

- no AI reasoning-system claim
- no source-of-truth replacement claim
- no probabilistic retrieval claim
- no public regenerate/invalidate commands unless accepted before freeze

## Post-v1.0.0 Work

These items are useful but not release blockers for v1.0.0:

- deeper query ergonomics
- expanded examples
- additional schema evolution work
- performance improvements
- broader invalidation confidence tests
- advanced documentation validation
- richer release automation
- optional troubleshooting expansion
- future security or boundary hardening that does not block the baseline

## Release Guardrails

- no public CLI expansion without contract, docs, parser, and validator alignment
- no derived artifact manual edits outside approved orchestration
- no weakening determinism or repository-locality enforcement
- no active tool surface without ownership metadata
- no undocumented runtime behavior
- no release tag without full validation

## Negative Patterns

- treating roadmap items as already implemented
- using marketing language as release evidence
- claiming production readiness early
- documenting commands that do not exist
- treating derived artifacts as authoritative
- expanding scope during release stabilization
- adding abstractions for hypothetical future features
- weakening validators to pass a release gate
- hiding caveats

## Follow-On Work

Each roadmap version should have its own task prompt, validation evidence,
changelog entry, and release or decision record as appropriate.

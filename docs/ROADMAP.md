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

### v0.3.0 — CLI Ergonomics and Query Reliability

Goal:

Improve usability of the existing small public CLI.

Expected work:

- audit CLI help text
- improve repairable error messages
- document common query examples
- test CLI output stability
- keep CLI contract, docs, and parser aligned

Acceptance criteria:

- help output is clear
- unsupported commands fail clearly
- query output is deterministic
- `validate-cli-contract` passes

Non-goals:

- do not add `horoji regenerate`
- do not add `horoji invalidate`
- no interactive shell
- no natural-language query system

### v0.4.0 — CI and Release Gate Hardening

Goal:

Make CI the reliable release gate.

Expected work:

- confirm CI runs validators
- confirm CI runs tests
- confirm CI checks committed derived artifacts
- align local and CI validation
- document required release gates
- pin toolchain behavior where needed

Acceptance criteria:

- CI fails on governance drift
- CI fails on stale derived artifacts
- CI fails on CLI contract drift
- CI fails on ownership gaps
- CI fails on determinism violations

Non-goals:

- no deployment pipeline
- no cloud-only validation path
- no external service dependency

### v0.5.0 — Documentation Completeness

Goal:

Bring operator, contributor, and release docs to release-candidate quality.

Expected work:

- expand contributor workflow
- add release process documentation
- add troubleshooting notes
- add examples for authoritative and derived artifacts
- add examples for agent workflow

Acceptance criteria:

- docs support first-time use
- docs explain authority boundaries
- docs explain release process
- docs avoid unsupported claims

Non-goals:

- no marketing rewrite
- no README replacement for governance docs
- no speculative feature promises

### v0.6.0 — Regeneration and Invalidation Confidence

Goal:

Strengthen confidence that derived artifacts are reproducible and invalidation
is correct.

Expected work:

- test incremental invalidation
- test full regeneration equivalence
- confirm stable ordering
- confirm provenance completeness
- document stale-derived recovery steps

Acceptance criteria:

- incremental invalidation tests pass
- regeneration equivalence tests pass
- derived artifacts are stable across repeated runs
- committed derived policy passes

Non-goals:

- no hidden regeneration behavior
- no caching layer unless governed and deterministic
- no performance work unless correctness requires it

### v0.7.0 — Security and Boundary Review

Goal:

Review repository-locality and safety boundaries before release-candidate work.

Expected work:

- audit path handling
- audit subprocess usage
- audit parser behavior
- audit generated write paths
- audit network prohibition
- audit environment input handling

Acceptance criteria:

- no host filesystem escape
- no network access
- no implicit environment dependency
- no unsafe path traversal
- boundary failures are explicit

Non-goals:

- no sandbox runtime
- no secrets system
- no remote execution
- no authorization framework

### v0.8.0 — Release Candidate Preparation

Goal:

Freeze the surfaces required for v1.0.0.

Expected work:

- freeze public CLI surface
- freeze metadata schemas
- freeze validation gate expectations
- resolve open caveats
- create release-candidate decision document

Acceptance criteria:

- public CLI freeze documented
- schema freeze documented
- release gates documented
- no unresolved P0/P1 findings
- full validation passes

Non-goals:

- no feature work after freeze
- no architecture expansion
- no unplanned validator additions unless release-blocking

### v0.9.0 — Release Candidate

Goal:

Tag and validate a v1.0.0 release candidate.

Expected work:

- create RC tag
- run clean-clone validation
- review README and release docs
- confirm changelog
- record RC decision

Acceptance criteria:

- RC tag exists
- clean-clone validation passes
- full tests pass
- release decision exists
- no governance drift

Non-goals:

- no feature work
- no schema changes unless release-blocking
- no CLI changes unless release-blocking

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

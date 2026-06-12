# Horoji v1.0.0 Production Roadmap

## Roadmap Goal

Move Horoji from a coherent governed baseline to a production-ready repository memory subsystem.

Production-ready means:

- documented installation and local operation
- stable public CLI contract
- stable authoritative metadata schema
- reliable validation in CI
- deterministic derived artifact behavior
- clear release/versioning rules
- clean operator guidance
- regression coverage for governance boundaries
- no undocumented runtime assumptions

Production-ready does not mean:

- autonomous reasoning
- probabilistic retrieval
- remote services
- plugin marketplaces
- external integrations
- replacing repository source files
- replacing governance documents
- broad AI-agent orchestration

Canonical truth remains in repository source files and governance documents.

Horoji remains a deterministic, repository-resident projection and validation system.

---

## v0.1.0 - Baseline Packaging and Installability

### Goal

Make Horoji easy to install, run, and validate in a clean clone.

### Scope

- Add documented local setup instructions.
- Add dependency installation guidance.
- Add a standard developer command path.
- Confirm clean-clone validation works.
- Document supported Python version.
- Document expected repository layout.
- Document how generated artifacts are handled.
- Add packaging metadata if appropriate.
- Add smoke tests for CLI entrypoints.

### Acceptance Criteria

- A new contributor can clone the repo and run validation from README instructions.
- Public CLI commands work from documented paths.
- `validate-all` passes in a clean setup.
- `pytest` passes in a clean setup.
- `horoji-check --derived-policy committed` passes.
- README setup instructions match actual commands.
- No new public CLI commands are added unless the CLI contract is updated and validated.

### Non-Goals

- No daemon.
- No network service.
- No plugin system.
- No external persistence layer.
- No speculative packaging for platforms not tested.

---

## v0.2.0 - Schema Stability and Metadata Contracts

### Goal

Define the metadata surfaces that must remain stable through v1.0.0.

### Scope

- Review authoritative contracts.
- Review invariant schemas.
- Review ownership metadata schemas.
- Review derived artifact schemas.
- Add schema version fields where needed.
- Define compatibility expectations.
- Add schema validation tests.
- Document allowed schema evolution rules.

### Acceptance Criteria

- Every authoritative metadata type has a documented schema.
- Every derived metadata type has a documented schema.
- Validators reject malformed metadata.
- Schema versions are explicit where needed.
- Breaking changes are defined.
- Non-breaking changes are defined.
- CHANGELOG records schema-surface changes clearly.

### Non-Goals

- No broad schema redesign without evidence.
- No migration framework unless required.
- No remote schema registry.
- No runtime schema fetching.

---

## v0.3.0 - CLI Ergonomics and Query Reliability

### Goal

Make the small public CLI easier to use without expanding it unnecessarily.

### Scope

- Audit current public CLI commands.
- Improve help text.
- Improve error messages.
- Add examples for common queries.
- Add stable output modes if needed.
- Add tests for CLI output stability.
- Confirm CLI contract, docs, and parser remain aligned.

### Acceptance Criteria

- `horoji --help` is clear.
- Public commands are documented.
- Unsupported commands fail clearly.
- CLI output is deterministic.
- CLI errors are repairable.
- `validate-cli-contract` passes.
- CLI tests cover command help and common query paths.

### Non-Goals

- Do not add `horoji regenerate` as a public command.
- Do not add `horoji invalidate` as a public command.
- Do not add an interactive shell.
- Do not add natural-language query behavior.
- Do not add probabilistic retrieval.

---

## v0.4.0 - CI and Release Gate Hardening

### Goal

Make CI the reliable production gate for Horoji.

### Scope

- Ensure CI runs validators.
- Ensure CI runs tests.
- Ensure CI checks committed derived artifacts.
- Ensure CI checks formatting or linting if already governed.
- Add a release-readiness workflow if appropriate.
- Document required gates before tagging.
- Ensure CI uses pinned tooling.

### Acceptance Criteria

- Pull requests fail on governance drift.
- Pull requests fail on stale derived artifacts.
- Pull requests fail on CLI contract drift.
- Pull requests fail on ownership gaps.
- Pull requests fail on determinism boundary violations.
- CI instructions are documented.
- Local validation and CI validation are aligned.

### Non-Goals

- No deployment pipeline.
- No external service dependency.
- No cloud-only workflow.
- No CI behavior that cannot be reproduced locally.

---

## v0.5.0 - Documentation Completeness

### Goal

Bring operator, contributor, and governance documentation to release-candidate quality.

### Scope

- Expand README where needed.
- Add contributor workflow documentation.
- Add release process documentation.
- Add troubleshooting notes.
- Add examples for authoritative and derived artifacts.
- Add examples for agent workflow.
- Ensure docs do not duplicate or contradict governance files.
- Add documentation drift checks only if needed.

### Acceptance Criteria

- README supports first-time use.
- Governance docs explain authority boundaries.
- Release process is documented.
- Agent workflow is documented.
- Operator commands are documented.
- Documentation avoids unsupported claims.
- Documentation does not present internal orchestration as public CLI.

### Non-Goals

- No marketing-heavy rewrite.
- No replacing governance docs with README prose.
- No broad speculative roadmap claims.
- No production-readiness claim before release gates support it.

---

## v0.6.0 - Deterministic Regeneration and Invalidation Confidence

### Goal

Strengthen confidence that derived artifacts are reproducible and invalidation is correct.

### Scope

- Add regression tests for incremental invalidation.
- Add regression tests for full regeneration equivalence.
- Confirm stable ordering in derived artifacts.
- Confirm provenance is complete.
- Confirm changed files map to expected impact artifacts.
- Document recovery steps for stale derived artifacts.

### Acceptance Criteria

- Incremental invalidation tests pass.
- Full regeneration equivalence tests pass.
- Derived artifacts are stable across repeated runs.
- Provenance validator passes.
- Committed derived policy passes.
- Stale derived artifact failure is clear and repairable.

### Non-Goals

- No performance optimization unless correctness requires it.
- No caching layer unless governed and deterministic.
- No hidden regeneration behavior.

---

## v0.7.0 - Security and Boundary Review

### Goal

Review Horoji's safety boundaries before release-candidate work.

### Scope

- Audit repository locality enforcement.
- Audit network prohibition.
- Audit environment input handling.
- Audit file path handling.
- Audit subprocess usage.
- Audit YAML/JSON parsing behavior.
- Audit generated artifact write paths.
- Add regression tests for boundary violations.

### Acceptance Criteria

- No host filesystem escape.
- No network access.
- No implicit environment dependency.
- No unsafe path traversal.
- No broad exception swallowing in critical validators.
- Boundary failures are explicit.
- Security review findings are documented.

### Non-Goals

- No sandbox runtime.
- No remote execution.
- No secrets handling system.
- No agent authorization system.

---

## v0.8.0 - Release Candidate Preparation

### Goal

Prepare Horoji for v1.0.0 release-candidate validation.

### Scope

- Freeze public CLI surface for v1.0.0.
- Freeze metadata schema surfaces for v1.0.0.
- Freeze validation gate expectations.
- Review all open TODOs and caveats.
- Update changelog.
- Create release-candidate decision document.
- Confirm clean clone validation.

### Acceptance Criteria

- Public CLI freeze documented.
- Metadata schema freeze documented.
- Release gate documented.
- No unresolved P0/P1 issues.
- Full validation passes.
- Full tests pass.
- Committed derived policy passes.
- Working tree clean.
- RC decision document exists.

### Non-Goals

- No new features after freeze.
- No architecture expansion.
- No unplanned validator additions unless fixing release-blocking defects.

---

## v0.9.0 - Release Candidate

### Goal

Cut a release candidate and validate it as if it were v1.0.0.

### Scope

- Tag release candidate.
- Run full validation from clean clone.
- Review README and release docs.
- Review changelog.
- Confirm version identifiers.
- Confirm no drift between docs, contracts, code, and derived artifacts.
- Record RC decision.

### Acceptance Criteria

- RC tag exists.
- Clean clone validation passes.
- Full tests pass.
- Release decision document exists.
- No governance drift.
- No unsupported production claims.
- No dirty working tree.

### Non-Goals

- No feature work.
- No schema changes unless release-blocking.
- No CLI changes unless release-blocking.
- No documentation rewrite unless correcting drift.

---

## v1.0.0 - Production Baseline

### Goal

Publish Horoji v1.0.0 as a stable, governed, repository-resident project memory subsystem.

### Scope

- Final release-readiness audit.
- Final changelog update.
- Final release decision document.
- Final tag.
- Confirm clean clone validation.
- Confirm public CLI stability.
- Confirm schema stability.
- Confirm governance coherence.
- Confirm deterministic artifact behavior.

### Acceptance Criteria

- v1.0.0 tag exists.
- Release decision document exists.
- Full validation passes.
- Full tests pass.
- Clean clone validation passes.
- Public CLI contract is stable.
- Metadata schema boundaries are stable.
- README accurately describes production baseline use.
- No known release-blocking governance drift.
- No unsupported runtime or maturity claims.

### Non-Goals

- No claim that Horoji is an AI reasoning system.
- No claim that Horoji replaces repository governance.
- No claim that Horoji performs probabilistic retrieval.
- No public regeneration/invalidation CLI unless explicitly accepted before freeze.

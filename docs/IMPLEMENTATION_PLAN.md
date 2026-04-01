HOROJI_IMPLEMENTATION_PLAN.md

Status: Canonical Implementation Plan
Applies To: Repository-local Horoji rollout
Scope: First-generation deterministic implementation only

⸻

1. Objective

Implement the first-generation Horoji project memory subsystem as a deterministic, repository-local, CI-enforced infrastructure layer.

This plan is limited to the following deliverables:
	•	authoritative metadata surfaces
	•	schema validation
	•	deterministic derived artifact generation
	•	invalidation-driven regeneration
	•	invariant and ownership validation
	•	stable CLI query surface
	•	CI enforcement

This plan does not authorize:
	•	non-deterministic analysis in enforcement paths
	•	freeform agent reasoning storage
	•	network-backed memory services
	•	probabilistic retrieval as a source of truth
	•	replacing canonical repository source with Horoji artifacts

⸻

2. Implementation Constraints

All work under this plan must satisfy the following constraints.

2.1 Repository locality

Horoji must operate strictly within the repository.

It must not:
	•	inspect host configuration
	•	read arbitrary filesystem locations outside the repository root
	•	perform network access
	•	download tools or metadata
	•	rely on environment discovery for correctness

2.2 Determinism

All enforcement and regeneration paths must be deterministic.

Given identical repository contents, pinned tools, and configuration, Horoji outputs must be identical.

2.3 Trust boundary enforcement

Horoji must preserve the distinction between:
	•	authoritative artifacts
	•	derived artifacts

Derived artifacts must never override or redefine authoritative artifacts.

2.4 Incremental correctness

Incremental regeneration is required, but correctness takes precedence over incremental performance.

If invalidation scope cannot be computed with confidence, Horoji must fall back to full regeneration of affected derived artifact classes.

⸻

3. Phase Structure

Implementation is divided into five bounded phases.

No later phase may weaken guarantees established by an earlier phase.

⸻

4. Phase 0 — Repository Skeleton and Control Surfaces

4.1 Objective

Create the Horoji directory layout, control files, and schema anchors required by the specification.

4.2 Allowed outputs

Create the following directories:

.project_memory/
    authoritative/
        contracts/
        invariants/
        ownership/
        architecture_manifest/
    derived/
        callgraphs/
        dependencies/
        impact_sets/
        summaries/
        embeddings/
    history/
        adr/
        decisions/
    schemas/
    config/

tools/
    horoji/
        cli/
        generators/
        validators/
        invalidation/

tests/
    horoji/

4.3 Required files

Create the following schema files:

.project_memory/schemas/contract.schema.json
.project_memory/schemas/invariant.schema.json
.project_memory/schemas/ownership.schema.json
.project_memory/schemas/provenance.schema.json

Create the following config files:

.project_memory/config/horoji.config.yaml
.project_memory/config/invalidation_rules.yaml

4.4 Requirements

The initial schema files may be minimal, but they must already enforce:
	•	required top-level keys
	•	artifact class identity
	•	trust-level identity where applicable
	•	schema version presence
	•	provenance structure

The initial config files must be explicit and versioned.

4.5 Acceptance criteria

Phase 0 is complete when:
	•	the canonical directory layout exists
	•	schema files exist and parse
	•	config files exist and parse
	•	repository tests can validate file presence and parseability
	•	no generator, validator, or CLI behavior is implied beyond structure existence

⸻

5. Phase 1 — Authoritative Layer

5.1 Objective

Establish the initial authoritative metadata surface for contracts, invariants, ownership, and architecture manifest data.

5.2 Deliverables

Populate:

.project_memory/authoritative/contracts/
.project_memory/authoritative/invariants/
.project_memory/authoritative/ownership/
.project_memory/authoritative/architecture_manifest/

5.3 Contracts

Create one contract file per subsystem.

Each contract must define at minimum:
	•	subsystem identifier
	•	exported surfaces
	•	allowed dependencies
	•	forbidden dependencies
	•	owner

Example shape:

subsystem: scheduler
exports:
  - schedule
  - enqueue
  - dequeue
forbidden_dependencies:
  - io
  - network
  - filesystem
allowed_dependencies:
  - memory
  - cpu
owner: core_runtime

Contracts are authoritative and human-reviewed.

5.4 Invariants

Create one file per invariant.

Each invariant must define at minimum:
	•	invariant identifier
	•	subsystem
	•	description
	•	deterministic enforcement definition

Example shape:

id: scheduler_non_blocking
subsystem: scheduler
description: scheduler must not perform blocking operations
enforcement:
  ast_query:
    forbidden_calls:
      - sleep
      - read_blocking
      - write_blocking

Invariants must be bounded and machine-verifiable.

5.5 Ownership

Create ownership mapping files defining:
	•	repository pattern
	•	owner
	•	required reviewers or review authority if used by governance

Example shape:

pattern: core/scheduler/**
owner: scheduler_subsystem
review_required:
  - scheduler_subsystem

Ownership must be explicit. Silent default ownership is forbidden.

5.6 Architecture manifest

Seed the architecture manifest with coarse subsystem-level structure only.

The initial architecture manifest must identify:
	•	subsystem names
	•	declared top-level dependencies
	•	major exported surfaces

Detailed graph data is not required in this phase.

5.7 Acceptance criteria

Phase 1 is complete when:
	•	authoritative artifacts exist for at least one real subsystem
	•	contracts validate against schema
	•	invariants validate against schema
	•	ownership maps validate against schema
	•	architecture manifest files validate against their initial expected structure
	•	no derived artifact generation is required yet

⸻

6. Phase 2 — Provenance and Derived Artifact Generators

6.1 Objective

Implement deterministic generation of derived artifacts with required provenance metadata.

6.2 Initial generator set

Implement under tools/horoji/generators/:
	•	horoji-callgraph
	•	horoji-deps
	•	horoji-impact

The following may exist but are non-blocking in the first generation:
	•	horoji-summarize
	•	horoji-embed

6.3 Generator requirements

Each generator must:
	•	read repository contents and authoritative Horoji artifacts only
	•	produce deterministic outputs
	•	write only to the corresponding .project_memory/derived/ subtree
	•	attach provenance metadata
	•	fail explicitly on malformed inputs

6.4 Required provenance fields

Every derived artifact must include:

artifact_type: <type>
trust_level: derived
generator: <generator-name>
schema_version: 1.0.0
input_commit: <git-sha-or-equivalent-revision-id>
generated_at: <timestamp>

generated_at may be recorded for traceability, but it must not affect logical output comparison rules in ways that break deterministic verification. If exact byte-for-byte comparison is required, provenance normalization rules must be defined explicitly.

6.5 Derived artifact restrictions

Derived artifacts are cacheable and disposable.

They must never:
	•	redefine contracts
	•	redefine ownership
	•	redefine invariants
	•	suppress authoritative validation outcomes

6.6 Acceptance criteria

Phase 2 is complete when:
	•	callgraph generation works deterministically for the initial target subsystem
	•	dependency generation works deterministically for the initial target subsystem
	•	impact-set generation works deterministically for the initial target subsystem
	•	all generated outputs include valid provenance
	•	tests verify that regenerating without repository changes produces equivalent logical outputs

⸻

7. Phase 3 — Invalidation Engine

7.1 Objective

Implement invalidation-driven regeneration for derived artifacts.

7.2 Deliverable

Implement:

tools/horoji/invalidation/horoji-invalidate

7.3 Required behavior

Input:
	•	list of changed files

Config input:
	•	.project_memory/config/invalidation_rules.yaml

Output:
	•	derived artifact classes requiring regeneration
	•	optionally, affected subsystem or surface identifiers if deterministically computable

7.4 Rule shape

Example:

- trigger:
    - include/**/*.h
  invalidate:
    - callgraphs
    - dependencies
    - impact_sets

7.5 Safety rule

If invalidation scope cannot be determined exactly enough to preserve correctness, the invalidation engine must widen scope, including full regeneration of relevant derived classes when necessary.

Under-invalidation is forbidden.

7.6 Acceptance criteria

Phase 3 is complete when:
	•	changed-file input produces deterministic invalidation output
	•	invalidation rules are schema-checked or structurally validated
	•	tests cover both narrow invalidation and conservative fallback behavior
	•	uncertain scope causes widening, not silent omission

⸻

8. Phase 4 — Validators

8.1 Objective

Implement deterministic validation of authoritative metadata and selected repository invariants.

8.2 Initial validator set

Implement under tools/horoji/validators/:
	•	validate-contracts
	•	validate-invariants
	•	validate-ownership
	•	at least one concrete invariant validator such as validate-scheduler_non_blocking

8.3 Validator requirements

Validators must:
	•	read repository contents and Horoji artifacts
	•	produce structured results
	•	return pass or fail deterministically
	•	never modify repository state

Validators must not:
	•	perform network access
	•	use randomness
	•	read external mutable configuration outside the repository
	•	silently downgrade failure to warning in enforcement mode

8.4 Output shape

Example:

validator: scheduler_non_blocking
status: FAIL
file: core/scheduler/schedule.c
line: 142
reason: blocking call detected

8.5 Required validation coverage

First-generation coverage must include:
	•	schema validity of authoritative artifacts
	•	ownership mapping consistency
	•	contract structure consistency
	•	at least one repository-backed invariant with real enforcement

8.6 Acceptance criteria

Phase 4 is complete when:
	•	validators run deterministically
	•	malformed authoritative artifacts fail validation
	•	at least one real invariant violation can be detected in tests
	•	structured validator output is stable and machine-readable

⸻

9. Phase 5 — CLI and CI Enforcement

9.1 Objective

Expose Horoji as a stable query surface and enforce it in CI.

9.2 CLI deliverable

Implement:

tools/horoji/cli/horoji

9.3 Required commands

The first-generation CLI must support:

horoji get-contract <subsystem>
horoji get-invariants <subsystem>
horoji get-owner <file>
horoji get-impact-set <file>
horoji validate
horoji regenerate
horoji invalidate

9.4 CLI behavior requirements

The CLI must:
	•	return deterministic machine-readable output
	•	fail explicitly on invalid inputs
	•	avoid implicit network or environment dependencies
	•	surface authoritative data distinctly from derived data

9.5 CI pipeline requirements

On pull requests, CI must:
	1.	determine changed files
	2.	run Horoji invalidation
	3.	regenerate required derived artifacts
	4.	run Horoji validation
	5.	verify schemas
	6.	verify provenance
	7.	fail on any violation

9.6 CI failure conditions

CI must fail when any of the following are detected:
	•	invariant violation
	•	contract violation
	•	ownership violation
	•	schema validation failure
	•	missing provenance metadata
	•	stale derived artifact
	•	invalidation/regeneration inconsistency

9.7 Acceptance criteria

Phase 5 is complete when:
	•	the CLI supports the required commands
	•	CI invokes Horoji deterministically
	•	CI fails on targeted negative test cases
	•	a clean repository state passes end-to-end

⸻

10. Phase 6 — Agent Integration Boundary

10.1 Objective

Define how external agents consume Horoji without making Horoji agent-dependent.

10.2 Rule

Horoji is the shared substrate. External agents are clients, not part of Horoji’s trust model.

Horoji must remain repository-local, deterministic, and usable without any model integration.

10.3 Standard context shape

Expose a stable machine-readable context shape equivalent to:

{
  "subsystem": "scheduler",
  "contract": {},
  "invariants": [],
  "ownership": [],
  "impact_set": [],
  "callgraph_slice": {},
  "history": []
}

The CLI may assemble this context, but the underlying authoritative and derived artifact boundaries must remain visible.

10.4 Restriction

Agents must not be allowed to treat advisory derived artifacts, including summaries or embeddings, as authoritative substitutes for contracts, invariants, or ownership.

10.5 Acceptance criteria

Phase 6 is complete when:
	•	an external tool can assemble subsystem context using only Horoji CLI calls
	•	the assembled context distinguishes authoritative from derived material
	•	agent workflows remain optional overlays, not required infrastructure

⸻

11. Deferred Work

The following are explicitly deferred from the first-generation rollout:
	•	embeddings as a required subsystem
	•	freeform reasoning history
	•	HTTP service mode
	•	cross-repository memory federation
	•	probabilistic ranking in enforcement paths
	•	broad natural-language retrieval as a correctness mechanism

These may be proposed later as separate scoped tasks.

⸻

12. Recommended Task Ordering

Recommended execution order:
	1.	Phase 0 — skeleton and schemas
	2.	Phase 1 — authoritative artifacts
	3.	Phase 2 — basic generators with provenance
	4.	Phase 3 — invalidation engine
	5.	Phase 4 — validators
	6.	Phase 5 — CLI and CI
	7.	Phase 6 — agent integration boundary

This order is binding for the first-generation implementation because validation and CI should not be built on unstable structure.

⸻

13. Final Edge Review

The following rules are locked for first-generation Horoji:
	•	authoritative artifacts are human-reviewed and never generator-defined
	•	derived artifacts are reproducible caches and never contract-defining
	•	under-invalidation is forbidden
	•	deterministic validation outranks convenience
	•	embeddings and summaries are advisory only
	•	Horoji is repository infrastructure, not an assistant
	•	external agents may consume Horoji, but Horoji must not depend on them

⸻

14. One-Sentence Definition

Horoji is a deterministic repository-local memory subsystem that exposes authoritative constraints and incrementally maintained derived structure for CI-enforced, invariant-safe development.

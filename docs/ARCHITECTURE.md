HOROJI — Project Memory Subsystem Specification

Status: Canonical
Version: 1.0.0
Scope: Repository-local structural knowledge system
Authority: Repository governance and CI verification pipeline

⸻

1. Purpose

Horoji is a repository-resident project memory subsystem that exposes:
	•	authoritative architectural facts
	•	machine-readable invariants
	•	ownership boundaries
	•	deterministically derived structural metadata

Horoji exists to:
	•	reduce repeated context derivation
	•	constrain implementation scope
	•	enforce architectural invariants
	•	enable deterministic agent and developer workflows

Horoji is not:
	•	a reasoning engine
	•	a documentation replacement
	•	a source-of-truth override
	•	a probabilistic retrieval system

All canonical truth remains in repository source files and governance documents.

Horoji provides structured, queryable projections of that truth.

⸻

2. Design Principles

2.1 Determinism

All derived artifacts must be reproducible from:
	•	repository content
	•	pinned toolchain
	•	explicit configuration

Given identical inputs, outputs must be identical.

No stochastic generation is permitted in enforcement paths.

⸻

2.2 Explicit Trust Boundaries

Every artifact is classified as:

Authoritative
or
Derived

Trust levels must never be ambiguous.

Derived artifacts must never override authoritative artifacts.

⸻

2.3 Incrementality

Horoji must update only what is invalidated.

Full regeneration is permitted but not required.

Incremental correctness takes precedence over performance.

⸻

2.4 Repository Locality

Horoji operates strictly within the repository.

It must not:
	•	inspect host filesystem state
	•	query system configuration
	•	download external artifacts
	•	rely on environment discovery

⸻

2.5 Verifiability

Every artifact must be:
	•	schema-validated
	•	provenance-tracked
	•	reproducible

Unverifiable artifacts are invalid.

⸻

3. System Model

Horoji is a repository subsystem consisting of:
	1.	authoritative metadata
	2.	derived structural metadata
	3.	invariant validators
	4.	invalidation engine
	5.	query interface

All components operate under CI governance.

⸻

4. Repository Layout

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
        contract.schema.json
        invariant.schema.json
        ownership.schema.json
        provenance.schema.json

    config/
        horoji.config.yaml
        invalidation_rules.yaml

tools/
    horoji/
        cli/
        generators/
        validators/
        invalidation/

tests/
    horoji/


⸻

5. Artifact Classes

5.1 Authoritative Artifacts

Authoritative artifacts define repository truth.

They are:
	•	human-reviewed
	•	version-controlled
	•	contract-binding

Examples:
	•	subsystem contracts
	•	invariants
	•	ownership maps
	•	architecture manifests

Authoritative artifacts must never be auto-generated.

⸻

5.2 Derived Artifacts

Derived artifacts are computed from authoritative data.

They are:
	•	reproducible
	•	cacheable
	•	disposable

Examples:
	•	call graphs
	•	dependency graphs
	•	impact sets
	•	structural summaries
	•	embeddings

Derived artifacts may be deleted and regenerated without loss of correctness.

⸻

6. Provenance Requirements

Every artifact must include provenance metadata.

Required fields:

artifact_type
trust_level
generator
schema_version
input_commit
generated_at

Example:

artifact_type: callgraph
trust_level: derived
generator: horoji-callgraph
schema_version: 1.0.0
input_commit: a1b2c3d4
generated_at: 2026-03-30T12:00:00Z

Artifacts missing provenance are invalid.

⸻

7. Contracts

Contracts define subsystem boundaries.

They describe:
	•	allowed dependencies
	•	forbidden dependencies
	•	exported interfaces
	•	ownership authority

Example:

subsystem: scheduler

exports:

    schedule()
    enqueue()
    dequeue()

forbidden_dependencies:

    io
    network
    filesystem

allowed_dependencies:

    memory
    cpu

owner:

    core_runtime

Contracts are authoritative.

Violations must fail CI.

⸻

8. Invariants

Invariants define non-negotiable behavioral constraints.

They must be:
	•	machine-verifiable
	•	deterministic
	•	bounded

Example:

invariant:

    id: scheduler_non_blocking

    description:

        scheduler must not perform blocking operations

    enforcement:

        ast_query:

            forbidden_calls:

                - sleep
                - read_blocking
                - write_blocking

Invariant violations must fail CI.

⸻

9. Ownership

Ownership defines authority over repository surfaces.

Ownership is exclusive unless explicitly shared.

Example:

file:

    core/scheduler/**

owner:

    scheduler_subsystem

review_required:

    scheduler_subsystem

Ownership conflicts must fail CI.

⸻

10. Invalidation Engine

The invalidation engine determines which derived artifacts must be regenerated.

This subsystem is mandatory.

⸻

10.1 Purpose

Prevent stale derived metadata.

Ensure incremental correctness.

⸻

10.2 Required Behavior

Given:

changed_files

The engine must compute:

affected_surfaces

Then regenerate only invalidated artifacts.

⸻

10.3 Example Rules

rule:

    trigger:

        include/**/*.h

    invalidate:

        callgraphs
        dependencies
        impact_sets

rule:

    trigger:

        contracts/**

    invalidate:

        validators
        summaries
        impact_sets


⸻

10.4 Safety Rule

If invalidation scope is uncertain:

full regeneration is required.

⸻

11. Validators

Validators enforce repository invariants.

They are deterministic programs.

Validators must:
	•	accept repository state
	•	return pass or fail
	•	produce structured output

⸻

11.1 Validator Requirements

Validators must not:
	•	modify repository state
	•	perform network access
	•	read external configuration
	•	use randomness

⸻

11.2 Output Format

validator: scheduler_non_blocking
status: FAIL
file: core/scheduler/schedule.c
line: 142
reason: blocking call detected


⸻

12. Impact Sets

Impact sets define the minimal affected surface of a change.

They are derived artifacts.

⸻

Example

change:

    core/scheduler/runqueue.c

impact_set:

    scheduler
    dispatch
    cpu_state

Impact sets drive incremental regeneration.

⸻

13. Embeddings

Embeddings are optional derived artifacts.

They are:
	•	non-authoritative
	•	non-enforcement
	•	advisory only

Embeddings must never determine pass/fail behavior.

⸻

14. Decision History

Decision history records architectural intent.

It exists to preserve reasoning context.

History entries must be structured.

⸻

Required Fields

decision_id
subsystem
problem
constraints
decision
rejected_alternatives
invariants_affected
files_changed
timestamp


⸻

Example

decision_id: ADR-014

subsystem: scheduler

problem:

    scheduler state ownership ambiguity

constraints:

    per-session ownership
    single writer

decision:

    scheduler state stored in session context

rejected_alternatives:

    global scheduler state

invariants_affected:

    scheduler_single_writer

files_changed:

    core/scheduler/state.c
    include/scheduler/state.h

timestamp:

    2026-03-30


⸻

15. Horoji CLI Interface

Horoji exposes a deterministic command interface.

The CLI is the primary query surface.

⸻

Required Commands

horoji get-contract <subsystem>
horoji get-invariants <subsystem>
horoji get-owner <file>
horoji get-impact-set <file>
horoji validate
horoji regenerate
horoji invalidate


⸻

Example

horoji get-contract scheduler

Returns:

contract:
    scheduler

exports:
    schedule
    enqueue
    dequeue

forbidden_dependencies:
    io


⸻

16. CI Integration

Horoji must run in CI.

⸻

Required Pipeline

on pull request:

    detect changed files

    run invalidation engine

    regenerate derived artifacts

    run validators

    verify schemas

    verify provenance

    fail if violations exist


⸻

CI Failure Conditions

CI must fail if:
	•	invariant violation detected
	•	contract violation detected
	•	ownership violation detected
	•	schema validation failure
	•	missing provenance metadata
	•	stale derived artifact detected

⸻

17. Determinism Requirements

Horoji execution must be deterministic.

⸻

Required Controls

Pinned:
	•	compiler
	•	parser
	•	analysis tools
	•	runtime versions

Explicit:
	•	configuration
	•	schema versions
	•	generator versions

⸻

Forbidden

Horoji must not depend on:
	•	system time for logic
	•	randomness
	•	environment discovery
	•	host filesystem inspection

⸻

18. Security Model

Horoji operates under a closed-world assumption.

⸻

Allowed Access

Repository files only.

⸻

Forbidden Access

/etc
/usr
/home
network
internet
external APIs


⸻

19. Failure Handling

Failure must be explicit.

Silent degradation is forbidden.

⸻

Required Behavior

On failure:

log structured error
halt execution
return non-zero status


⸻

20. Minimal Viable Implementation

A compliant first-generation Horoji system must implement:
	•	authoritative contracts
	•	invariant registry
	•	ownership map
	•	invalidation engine
	•	deterministic validators
	•	CLI interface
	•	CI enforcement

Optional components:
	•	embeddings
	•	summaries
	•	advanced dependency analysis

⸻

21. Acceptance Criteria

Horoji is considered operational when:
	•	contracts are machine-readable
	•	invariants are machine-verifiable
	•	ownership is enforced in CI
	•	derived artifacts regenerate incrementally
	•	invalidation rules function correctly
	•	CLI queries return deterministic results
	•	provenance metadata is present
	•	CI rejects invariant violations

⸻

22. One-Sentence Definition

Horoji is a deterministic repository subsystem that exposes authoritative architectural constraints and incrementally maintained structural metadata to enforce invariant-safe development workflows.

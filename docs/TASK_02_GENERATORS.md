TASK_02_GENERATORS.md

Status: Mandatory
Authority: Repository Governance
Phase: 2
Scope: Deterministic derived artifact generators and provenance attachment
Blocking: TASK_03_INVALIDATION_ENGINE.md and all downstream validation and CI enforcement

⸻

1. Task Title

Implement deterministic derived artifact generators for Horoji

⸻

2. Objective

Implement the first operational generation layer of Horoji by creating deterministic generators that compute derived structural metadata from repository source and authoritative artifacts.

This task establishes:
	•	reproducible derived artifact generation
	•	mandatory provenance metadata attachment
	•	deterministic output structure
	•	repository-local generation behavior

This task must not implement:
	•	invalidation engine behavior
	•	enforcement validators
	•	CI gating logic
	•	CLI orchestration beyond generator entrypoints
	•	probabilistic or non-deterministic analysis
	•	external network or host inspection

⸻

3. Rationale

Horoji requires derived structural metadata to support later invariant enforcement, impact analysis, and repository reasoning.

These artifacts must exist before invalidation logic and validation enforcement can operate.

Phase 2 establishes the generation capability.

Later phases will determine when generation runs and how outputs are validated.

⸻

4. Scope

Allowed paths:

tools/horoji/generators/**
.project_memory/derived/**
.project_memory/schemas/**
tests/horoji/**
CHANGELOG.md

All other paths are read-only.

⸻

5. Required Deliverables

This task must implement deterministic generators for the following derived artifact classes:
	•	callgraphs
	•	dependencies
	•	impact_sets

Optional (non-blocking):
	•	summaries
	•	embeddings

Optional generators must be implemented as advisory-only components and must not be required for correctness.

⸻

5.1 Generator Directory Layout

The following generator entrypoints must exist:

tools/horoji/generators/
    horoji-callgraph
    horoji-deps
    horoji-impact

Optional:

tools/horoji/generators/
    horoji-summarize
    horoji-embed

Each generator must be executable and repository-local.

⸻

5.2 Generator Responsibilities

Each generator must:
	•	read repository source files
	•	read authoritative artifacts
	•	compute deterministic derived metadata
	•	write outputs to the corresponding derived directory
	•	attach provenance metadata
	•	fail explicitly on malformed inputs

Each generator must operate independently.

Generators must not depend on each other unless explicitly declared in configuration.

⸻

5.3 Derived Artifact Output Locations

Outputs must be written only to:

.project_memory/derived/

Required structure:

.project_memory/derived/

callgraphs/
dependencies/
impact_sets/

summaries/      (optional)
embeddings/     (optional)

Generators must not write outside the derived subtree.

⸻

6. Determinism Requirements

All generators must produce deterministic outputs.

Given identical:
	•	repository contents
	•	authoritative metadata
	•	configuration
	•	toolchain

Outputs must be logically identical.

⸻

Deterministic Behavior Rules

Generators must:
	•	produce stable ordering of output elements
	•	avoid random identifiers
	•	avoid time-dependent logic
	•	avoid environment-dependent behavior
	•	avoid concurrency-dependent ordering

⸻

Timestamp Rule

Provenance metadata may include timestamps.

Timestamps must not affect logical output comparison.

If byte-level determinism is required, timestamp normalization must be applied.

⸻

7. Provenance Metadata

Every derived artifact must include provenance metadata.

⸻

Required Provenance Fields

artifact_type: <type>
trust_level: derived
generator: <generator_name>
schema_version: 1.0.0
input_commit: <repository_revision>
generated_at: <timestamp>


⸻

Provenance Requirements

Provenance metadata must:
	•	be present in every derived artifact
	•	validate against provenance schema
	•	reflect the generator identity
	•	reflect the repository revision used
	•	remain deterministic in structure

Provenance metadata must not:
	•	include environment-specific paths
	•	include host identifiers
	•	include runtime secrets

⸻

8. Callgraph Generator

Entry Point

tools/horoji/generators/horoji-callgraph


⸻

Purpose

Compute the function-level or interface-level call relationships within a subsystem.

⸻

Output Location

.project_memory/derived/callgraphs/


⸻

Required Behavior

The callgraph generator must:
	•	parse repository source files
	•	detect callable relationships
	•	produce deterministic call edge lists
	•	support subsystem-level granularity

⸻

Output Structure (example)

artifact_type: callgraph

subsystem: scheduler

nodes:

  - schedule
  - enqueue
  - dequeue

edges:

  - from: schedule
    to: enqueue

  - from: schedule
    to: dequeue


⸻

9. Dependency Generator

Entry Point

tools/horoji/generators/horoji-deps


⸻

Purpose

Compute subsystem or module dependency relationships.

⸻

Output Location

.project_memory/derived/dependencies/


⸻

Required Behavior

The dependency generator must:
	•	analyze import or include relationships
	•	compute declared dependencies
	•	produce deterministic dependency sets

⸻

Output Structure (example)

artifact_type: dependency

subsystem: scheduler

depends_on:

  - memory
  - cpu


⸻

10. Impact Set Generator

Entry Point

tools/horoji/generators/horoji-impact


⸻

Purpose

Compute the minimal affected subsystem set for a given file.

⸻

Output Location

.project_memory/derived/impact_sets/


⸻

Required Behavior

The impact generator must:
	•	map repository files to subsystems
	•	identify dependent subsystems
	•	produce deterministic impact sets

⸻

Output Structure (example)

artifact_type: impact_set

file: core/scheduler/runqueue.c

impacted_subsystems:

  - scheduler
  - dispatch


⸻

11. Generator Failure Behavior

Generators must fail explicitly when:
	•	required authoritative metadata is missing
	•	schema validation fails
	•	repository parsing fails
	•	output location is unavailable

Failure must:
	•	return non-zero status
	•	emit structured error output
	•	halt generation

Silent fallback is forbidden.

⸻

12. Bootstrap Tests

Add tests under:

tests/horoji/

Tests must verify:
	•	generator execution succeeds on valid repository state
	•	generator outputs are deterministic
	•	outputs include provenance metadata
	•	outputs validate against schema
	•	generator fails on malformed inputs

⸻

Determinism Test Requirement

Tests must confirm:

Repeated generator execution without repository changes produces logically identical outputs.

⸻

13. Non-Negotiable Guarantees

This task must ensure:

⸻

13.1 Derived artifacts are reproducible

Derived metadata must be fully regenerable from repository inputs.

⸻

13.2 Derived artifacts are disposable

Deleting derived artifacts must not affect repository correctness.

⸻

13.3 Derived artifacts never override authoritative data

Authoritative metadata always has precedence.

⸻

13.4 Generation is deterministic

Outputs must not vary across environments.

⸻

14. Forbidden Changes

The following actions are forbidden in this task:
	•	implementing invalidation engine behavior
	•	implementing validator enforcement logic
	•	implementing CI gating logic
	•	modifying authoritative artifacts automatically
	•	writing derived artifacts into authoritative directories
	•	performing network access
	•	using randomness
	•	relying on system configuration outside the repository
	•	modifying unrelated repository files

⸻

15. Acceptance Criteria

This task is complete when:
	1.	The callgraph generator exists
	2.	The dependency generator exists
	3.	The impact set generator exists
	4.	Generators produce deterministic outputs
	5.	All outputs include valid provenance metadata
	6.	Outputs validate against schema
	7.	Generators fail on malformed inputs
	8.	Repeated execution produces identical logical outputs
	9.	Derived artifacts are written only to the derived subtree
	10.	CHANGELOG records completion of generator implementation

⸻

16. Failure Conditions

This task fails if:
	•	generator outputs vary across identical runs
	•	provenance metadata is missing
	•	derived artifacts overwrite authoritative data
	•	generator execution depends on environment state
	•	outputs are written outside the derived directory
	•	generator silently ignores errors

⸻

17. Completion Statement

Upon completion of this task:

The repository contains deterministic generators capable of producing reproducible derived structural metadata from authoritative inputs.

Invalidation logic, enforcement validation, CI orchestration, and agent integration remain deferred.

⸻

18. One-Sentence Definition

TASK_02 establishes deterministic generation of reproducible derived structural metadata required for later invalidation, validation, and enforcement within the Horoji system.

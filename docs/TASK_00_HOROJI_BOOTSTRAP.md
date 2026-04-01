
TASK_00_HOROJI_BOOTSTRAP.md

Status: Mandatory
Authority: Repository Governance
Phase: 0
Scope: Horoji skeleton, schema anchors, config anchors, bootstrap verification
Blocking: All subsequent Horoji tasks

⸻

1. Task Title

Bootstrap the Horoji repository skeleton and verification anchors

⸻

2. Objective

Create the initial Horoji repository structure, schema anchors, config anchors, and bootstrap tests required to establish Horoji as a repository subsystem.

This task is strictly structural.

This task must only establish:
	•	the canonical Horoji directory layout
	•	parseable schema files
	•	parseable config files
	•	bootstrap verification tests for presence and parseability

This task does not authorize:
	•	derived artifact generation
	•	invalidation logic
	•	validator enforcement beyond bootstrap checks
	•	CLI query semantics
	•	CI policy for later-phase Horoji commands
	•	agent integration behavior
	•	PR rejection based on missing Horoji context queries

⸻

3. Rationale

Horoji cannot enforce contracts, invariants, ownership, or agent workflows until its structural surfaces exist.

Phase 0 exists to create those surfaces.

No later Horoji phase may assume a directory, schema, or config surface that was not established here.

⸻

4. Scope

Allowed paths:
	•	.project_memory/**
	•	tools/horoji/**
	•	tests/horoji/**
	•	CHANGELOG.md

All other paths are read-only.

⸻

5. Required Deliverables

5.1 Canonical directory layout

The following directory layout must be created exactly:

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

Directory names are contract surfaces.

Deletion, renaming, relocation, aliasing, or substitution is forbidden.

⸻

5.2 Schema anchors

The following files must be created:

.project_memory/schemas/contract.schema.json
.project_memory/schemas/invariant.schema.json
.project_memory/schemas/ownership.schema.json
.project_memory/schemas/provenance.schema.json

These schema files must:
	•	be syntactically valid JSON
	•	parse deterministically
	•	define required top-level keys for their artifact class
	•	include an explicit schema version field or equivalent required version key if that is the repository convention

The schemas may be minimal in this task, but they must not be empty placeholders.

⸻

5.3 Config anchors

The following files must be created:

.project_memory/config/horoji.config.yaml
.project_memory/config/invalidation_rules.yaml

These config files must:
	•	be syntactically valid YAML
	•	parse deterministically
	•	contain explicit versioned structure
	•	avoid implicit defaults that change meaning outside repository control

The invalidation rules file may be minimal in this task, but it must not imply implemented invalidation behavior beyond structural validity.

⸻

5.4 Bootstrap stubs for future surfaces

The following tool directories must exist:
	•	tools/horoji/cli/
	•	tools/horoji/generators/
	•	tools/horoji/validators/
	•	tools/horoji/invalidation/

This task may add minimal README, placeholder, or keep files only if required by repository rules, but must not implement later-phase behavior.

⸻

5.5 Bootstrap tests

Add tests under tests/horoji/ that verify:
	•	required directory existence
	•	required schema file existence
	•	required config file existence
	•	schema parseability
	•	config parseability
	•	failure on missing required anchor files

These tests must be deterministic and repository-local.

⸻

6. Non-Negotiable Guarantees

This task must ensure only the following guarantees.

6.1 Horoji structural presence

The .project_memory/ tree exists in canonical form.

6.2 Horoji parseable anchors

Schema and config anchors exist and are parseable.

6.3 Horoji bootstrap verifiability

Repository tests can detect missing or malformed bootstrap surfaces.

6.4 No premature semantics

This task must not claim that Horoji generation, invalidation, validation, CLI querying, CI enforcement, or agent enforcement already exists unless implemented in later tasks.

⸻

7. Forbidden Changes

The following are forbidden in this task:
	•	implementing derived artifact generators
	•	implementing invalidation engine logic
	•	implementing invariant validators beyond bootstrap surface checks
	•	implementing full CLI command semantics
	•	modifying general CI policy outside bootstrap verification wiring, if any
	•	adding agent-specific memory stores
	•	declaring agent workflows blocked on Horoji CLI before the CLI exists
	•	allowing derived artifacts to define or override authoritative artifacts
	•	writing authoritative contract, invariant, or ownership content beyond minimal anchor examples required for schema sanity, unless explicitly needed for parsing tests
	•	modifying unrelated repository structure

This is a bootstrap task, not a systems-integration task.

⸻

8. Acceptance Criteria

This task is complete when all of the following are true:
	1.	The full canonical Horoji directory skeleton exists.
	2.	All required schema files exist and parse as valid JSON.
	3.	All required config files exist and parse as valid YAML.
	4.	Bootstrap tests under tests/horoji/ verify required presence and parseability.
	5.	Negative tests or equivalent checks fail when required anchors are missing or malformed.
	6.	No later-phase Horoji behavior is claimed or required by this task.
	7.	The changelog records completion of Horoji bootstrap structure.

⸻

9. Completion Statement

On completion of this task, the repository has a valid Horoji bootstrap surface that later tasks may extend, but Horoji enforcement, regeneration, invalidation, CLI semantics, CI gating, and agent integration remain deferred.

⸻

10. Deferred To Later Tasks

The following are explicitly deferred:
	•	TASK_01_AUTHORITATIVE_SURFACES.md
	•	TASK_02_GENERATORS.md
	•	TASK_03_INVALIDATION_ENGINE.md
	•	TASK_04_VALIDATORS.md
	•	TASK_05_CI_ENFORCEMENT.md
	•	TASK_06_AGENT_INTEGRATION.md

Task 00 must not absorb work from those tasks.

⸻

11. One-Sentence Definition

TASK_00 establishes the canonical Horoji skeleton, schema anchors, config anchors, and bootstrap verification surfaces required for all later Horoji work.

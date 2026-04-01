TASK_01_AUTHORITATIVE_SURFACES.md

Status: Mandatory
Authority: Repository Governance
Phase: 1
Scope: Authoritative metadata surfaces only
Blocking: TASK_02_GENERATORS.md and all downstream Horoji functionality

⸻

1. Task Title

Establish the initial authoritative metadata layer for Horoji

⸻

2. Objective

Create the first operational authoritative surfaces for Horoji by defining:
	•	subsystem contracts
	•	invariant definitions
	•	ownership mappings
	•	architecture manifest structure

These artifacts must be machine-readable, schema-validated, and repository-local.

This task establishes the authoritative truth layer that all derived artifacts, validators, and agent workflows will rely on in later phases.

This task must not implement:
	•	derived artifact generation
	•	invalidation logic
	•	enforcement validators
	•	CLI semantics
	•	CI gating beyond schema validation
	•	agent workflow behavior

⸻

3. Rationale

Horoji cannot compute dependencies, enforce invariants, or validate ownership until authoritative metadata exists.

Phase 1 establishes the canonical metadata that defines repository structure and behavioral constraints.

All later phases assume these surfaces exist and are stable.

This task creates those surfaces.

⸻

4. Scope

Allowed paths:

.project_memory/authoritative/**
.project_memory/schemas/**
tests/horoji/**
CHANGELOG.md

All other paths are read-only.

⸻

5. Required Deliverables

This task must create valid authoritative artifacts for at least one real subsystem.

The subsystem used for initialization must represent an actual repository surface.

Synthetic placeholder subsystems are forbidden.

⸻

5.1 Contracts

Create subsystem contract files under:

.project_memory/authoritative/contracts/

Each contract must be stored in a separate file.

Filename rule:

<subsystem>.yaml

Example:

scheduler.yaml
filesystem.yaml
memory.yaml


⸻

Contract Structure

Each contract must define:

subsystem: <string>

exports:
  - <function_or_interface>

allowed_dependencies:
  - <subsystem>

forbidden_dependencies:
  - <subsystem>

owner: <subsystem_owner>


⸻

Contract Requirements

Contracts must:
	•	validate against contract.schema.json
	•	define at least one exported surface
	•	define explicit ownership
	•	define dependency boundaries
	•	be human-reviewable
	•	remain deterministic

Contracts must not:
	•	reference non-existent subsystems
	•	contain runtime logic
	•	contain environment-specific conditions
	•	include derived data

⸻

5.2 Invariants

Create invariant files under:

.project_memory/authoritative/invariants/

Each invariant must be stored in a separate file.

Filename rule:

<invariant_id>.yaml


⸻

Invariant Structure

Each invariant must define:

id: <string>

subsystem: <string>

description: <string>

enforcement:
  ast_query:
    forbidden_calls:
      - <function_name>


⸻

Invariant Requirements

Invariants must:
	•	validate against invariant.schema.json
	•	be deterministic
	•	be bounded
	•	be machine-verifiable
	•	reference an existing subsystem

Invariants must not:
	•	require runtime execution
	•	require network access
	•	depend on timing behavior
	•	rely on probabilistic logic
	•	reference external repositories

⸻

5.3 Ownership

Create ownership mapping files under:

.project_memory/authoritative/ownership/

Filename rule:

<subsystem>_ownership.yaml


⸻

Ownership Structure

Each ownership file must define:

pattern: <repository_path_pattern>

owner: <subsystem>

review_required:
  - <subsystem>


⸻

Ownership Requirements

Ownership mappings must:
	•	validate against ownership.schema.json
	•	define explicit path authority
	•	define responsible subsystem
	•	be deterministic

Ownership mappings must not:
	•	overlap without explicit shared ownership declaration
	•	rely on implicit defaults
	•	reference non-existent repository paths

⸻

5.4 Architecture Manifest

Create architecture manifest files under:

.project_memory/authoritative/architecture_manifest/


⸻

Architecture Manifest Purpose

The architecture manifest defines coarse structural boundaries between subsystems.

It is not a call graph.

It is not a dependency graph.

It is a declared architectural model.

⸻

Manifest Structure

Example:

subsystems:

  scheduler:
    depends_on:
      - cpu
      - memory

  filesystem:
    depends_on:
      - storage
      - memory


⸻

Manifest Requirements

Architecture manifest files must:
	•	define subsystem names
	•	define declared dependencies
	•	remain human-readable
	•	remain deterministic

Architecture manifest files must not:
	•	include derived relationships
	•	include runtime behavior
	•	include generated metadata

⸻

6. Schema Validation

All authoritative artifacts created in this task must validate against their schemas.

Required schemas:

contract.schema.json
invariant.schema.json
ownership.schema.json

Validation must confirm:
	•	required fields exist
	•	field types are correct
	•	schema version is present
	•	structure is deterministic

Schema validation must fail on:
	•	missing required fields
	•	invalid field types
	•	malformed structure
	•	unknown required keys

⸻

7. Bootstrap Tests

Add tests under:

tests/horoji/

These tests must verify:
	•	existence of at least one contract
	•	existence of at least one invariant
	•	existence of at least one ownership map
	•	existence of architecture manifest file
	•	schema validation success
	•	failure on malformed metadata

Tests must be:
	•	deterministic
	•	repository-local
	•	independent of network access

⸻

8. Non-Negotiable Guarantees

This task must ensure:

⸻

8.1 Authoritative metadata exists

The repository contains valid machine-readable authoritative artifacts.

⸻

8.2 Metadata is schema-validated

All authoritative artifacts conform to schema definitions.

⸻

8.3 Metadata is deterministic

Authoritative artifacts must produce identical validation results across environments.

⸻

8.4 Authoritative data precedes derived data

No derived artifact generation may occur before authoritative metadata exists.

⸻

9. Forbidden Changes

The following actions are forbidden in this task:
	•	implementing derived artifact generators
	•	implementing invalidation engine behavior
	•	implementing invariant enforcement logic
	•	implementing CLI commands
	•	implementing CI gating beyond schema validation
	•	modifying unrelated repository files
	•	introducing environment-dependent logic
	•	allowing authoritative artifacts to be auto-generated
	•	storing derived metadata in authoritative directories
	•	referencing external data sources

This task defines authoritative structure only.

⸻

10. Acceptance Criteria

This task is complete when:
	1.	At least one valid subsystem contract exists
	2.	At least one valid invariant exists
	3.	At least one valid ownership mapping exists
	4.	Architecture manifest files exist
	5.	All artifacts pass schema validation
	6.	Bootstrap tests pass
	7.	Tests fail when metadata is malformed
	8.	No derived artifact logic exists
	9.	No enforcement logic exists
	10.	CHANGELOG records completion of authoritative surface initialization

⸻

11. Failure Conditions

This task fails if:
	•	any authoritative artifact fails schema validation
	•	metadata references non-existent subsystems
	•	ownership mappings conflict without declaration
	•	architecture manifest is missing
	•	bootstrap tests are absent
	•	derived logic appears in authoritative directories

⸻

12. Completion Statement

Upon completion of this task:

The repository contains the first operational authoritative metadata layer defining subsystem contracts, invariants, ownership boundaries, and architecture structure.

Derived computation, invalidation, enforcement, and agent integration remain deferred.

⸻

13. One-Sentence Definition

TASK_01 establishes the machine-readable authoritative metadata that defines repository structure, behavioral constraints, and ownership boundaries for all subsequent Horoji operations.

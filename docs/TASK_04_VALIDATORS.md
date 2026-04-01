# TASK_04_VALIDATORS.md

Status: Mandatory  
Authority: Repository Governance  
Phase: 4  
Scope: Deterministic validator implementation for authoritative and derived Horoji surfaces  
Blocking: TASK_05_CI_ENFORCEMENT.md and all downstream enforcement workflows

---

# 1. Task Title

Implement deterministic validators for Horoji authoritative and derived artifacts

---

# 2. Objective

Implement the Horoji validation layer as a deterministic repository-local subsystem that verifies:

- authoritative artifact schema compliance
- authoritative artifact structural consistency
- ownership mapping integrity
- contract consistency
- invariant definition validity
- selected repository-backed invariant enforcement
- derived artifact provenance presence and validity
- generator output structural validity

This task establishes:

- deterministic validator entrypoints
- structured pass/fail output
- repository-local validation behavior
- explicit enforcement boundaries between schema validation, structural validation, and repository-backed invariant checks

This task must not implement:

- CI pipeline orchestration
- merge policy
- agent workflow gating
- automatic remediation
- network-backed validation
- non-deterministic heuristic enforcement

---

# 3. Rationale

Horoji cannot become an enforcement surface until repository facts can be validated deterministically.

Schemas alone are insufficient.

Several required rules cannot be expressed fully in JSON Schema, including:

- disjointness of allowed and forbidden dependencies
- identifier immutability across committed history
- ownership conflict detection
- repository-backed behavioral constraints
- provenance completeness on derived outputs

Phase 4 establishes the executable validation layer that turns Horoji from a descriptive metadata system into an enforceable governance subsystem.

---

# 4. Scope

Allowed paths:

```text
tools/horoji/validators/**
tests/horoji/**
.project_memory/schemas/**
.project_memory/authoritative/**
.project_memory/derived/**
.project_memory/config/**
CHANGELOG.md

All other paths are read-only.

⸻

5. Required Deliverables

This task must implement deterministic validators for the following classes:
	•	schema and structural validation of contracts
	•	schema and structural validation of invariants
	•	schema and structural validation of ownership mappings
	•	repository-backed ownership consistency checks
	•	contract dependency consistency checks
	•	invariant definition consistency checks
	•	provenance validation for derived artifacts
	•	at least one concrete repository-backed invariant validator

This task must also implement a stable validation entrypoint that can execute all validators together.

⸻

5.1 Validator Directory Layout

The following validator entrypoints must exist under:

tools/horoji/validators/

Required:

validate-contracts
validate-invariants
validate-ownership
validate-provenance
validate-scheduler_non_blocking
validate-all

Additional validators may be added only if they remain within Phase 4 scope.

⸻

5.2 Required Validator Responsibilities

Each validator must:
	•	read repository-local inputs only
	•	operate deterministically
	•	emit structured machine-readable output
	•	return explicit pass or fail status
	•	fail explicitly on malformed inputs
	•	avoid modifying repository state

Each validator must validate one bounded concern.

Monolithic multi-purpose validator logic is forbidden except for validate-all, which may orchestrate individual validators.

⸻

6. Validator Categories

⸻

6.1 Schema Validators

Schema validators verify that artifacts parse and conform to their declared schema structure.

They must validate:
	•	contracts against contract.schema.json
	•	invariants against invariant.schema.json
	•	ownership mappings against ownership.schema.json
	•	derived provenance blocks against provenance.schema.json

Schema validation must fail on:
	•	malformed YAML or JSON
	•	missing required fields
	•	wrong field types
	•	unknown fields where strict schemas forbid them

⸻

6.2 Structural Validators

Structural validators verify constraints that are not fully expressible in schema.

They must validate at minimum:
	•	allowed_dependencies and forbidden_dependencies are disjoint
	•	referenced subsystem names are non-empty and structurally valid
	•	ownership records do not conflict silently
	•	invariant predicate structures are internally consistent with declared predicate type
	•	architecture manifest entries remain structurally coherent where referenced

⸻

6.3 Repository-Backed Invariant Validators

Repository-backed validators verify actual repository behavior or structure against declared invariants.

At least one concrete validator must be implemented in this phase.

Required minimum:

validate-scheduler_non_blocking

This validator must verify that the scheduler surface does not invoke explicitly forbidden blocking operations in the targeted repository scope.

⸻

6.4 Derived Artifact Validators

Derived artifact validators verify generated output structure only.

They must validate:
	•	provenance presence
	•	provenance schema compliance
	•	artifact type and trust-level consistency, if present in generated artifacts
	•	output structural parseability

This task does not require semantic correctness proofs for derived artifacts, only deterministic structural validation.

⸻

7. Structured Output Requirements

All validators must emit structured output.

Required minimum shape:

validator: <validator_name>
status: PASS|FAIL
target: <artifact_or_surface>
reason: <short_reason>
details:
  - <optional_detail>

When a validator detects a file-local issue, it must include file location information where available.

Example:

validator: validate-scheduler_non_blocking
status: FAIL
target: core/scheduler/schedule.c
reason: blocking call detected
details:
  - line: 142
  - symbol: sleep

Output ordering must be deterministic.

Freeform prose-only validation output is forbidden.

⸻

8. Determinism Requirements

All validators must be deterministic.

Given identical:
	•	repository contents
	•	configuration
	•	authoritative artifacts
	•	derived artifacts
	•	toolchain

validation results must be identical.

Validators must not depend on:
	•	wall clock time
	•	randomness
	•	host environment discovery
	•	network access
	•	user-specific mutable state outside explicit repository inputs

⸻

9. Error Handling Requirements

Validators must fail explicitly.

Required behavior on failure:
	•	return non-zero exit status
	•	emit structured error output
	•	halt the failing validator cleanly

Silent pass, warning-only downgrade, or implicit fallback is forbidden.

Required error shape:

validator: <validator_name>
status: ERROR
target: <artifact_or_surface>
reason: <configuration_error_or_parse_error>
details:
  - <diagnostic>


⸻

10. Contract Validator Requirements

⸻

10.1 Entry Point

tools/horoji/validators/validate-contracts


⸻

10.2 Required Checks

The contract validator must verify:
	•	contract files exist and parse
	•	each contract validates against contract.schema.json
	•	subsystem identifiers are present and non-empty
	•	exports is an array of strings
	•	allowed_dependencies is an array of strings
	•	forbidden_dependencies is an array of strings
	•	owner is present and non-empty
	•	allowed_dependencies and forbidden_dependencies are disjoint
	•	duplicate dependency entries are rejected or normalized deterministically
	•	duplicate exported surface names within the same contract are rejected

⸻

10.3 Forbidden Behavior

The contract validator must not:
	•	infer missing fields
	•	auto-correct malformed contracts
	•	rewrite authoritative artifacts

⸻

11. Invariant Validator Requirements

⸻

11.1 Entry Point

tools/horoji/validators/validate-invariants


⸻

11.2 Required Checks

The invariant validator must verify:
	•	invariant files exist and parse
	•	each invariant validates against invariant.schema.json
	•	invariant_id is present and non-empty
	•	description is present and non-empty
	•	predicate.type is present
	•	predicate structure matches declared type
	•	optional subsystem field, if present, is structurally valid
	•	duplicate invariant identifiers are rejected
	•	invariant identifiers are stable within repository state under validation

If committed-history immutability validation is not yet available in this phase, the validator must at minimum enforce:
	•	no duplicate active invariant identifiers in repository state
	•	identifier structure remains stable within the current tree

Full historical immutability checks may be extended later, but this validator must preserve the lifecycle boundary.

⸻

12. Ownership Validator Requirements

⸻

12.1 Entry Point

tools/horoji/validators/validate-ownership


⸻

12.2 Required Checks

The ownership validator must verify:
	•	ownership files exist and parse
	•	each ownership record validates against ownership.schema.json
	•	ownership_id is present and non-empty
	•	resource.path is present and non-empty
	•	owner is present and non-empty
	•	duplicate ownership identifiers are rejected
	•	overlapping ownership patterns do not silently conflict
	•	review authorities, if present, are structurally valid

If overlapping ownership is allowed by repository policy, it must be explicit rather than inferred.

Silent overlap is forbidden.

⸻

13. Provenance Validator Requirements

⸻

13.1 Entry Point

tools/horoji/validators/validate-provenance


⸻

13.2 Required Checks

The provenance validator must verify all derived artifacts under:

.project_memory/derived/**

for:
	•	parseability
	•	provenance presence where required by artifact structure
	•	provenance validation against provenance.schema.json
	•	required provenance fields:
	•	schema_version
	•	provenance_id
	•	source_artifact
	•	generated_at
	•	absence of malformed provenance blocks

This validator must not require semantic correctness of generator outputs beyond provenance and structural validity.

⸻

14. Concrete Repository-Backed Invariant Validator

⸻

14.1 Required Entry Point

tools/horoji/validators/validate-scheduler_non_blocking


⸻

14.2 Purpose

Enforce the declared authoritative invariant:

scheduler_non_blocking


⸻

14.3 Required Behavior

This validator must:
	•	identify the scheduler-owned repository surface
	•	inspect relevant files deterministically
	•	detect explicitly forbidden blocking calls named in the invariant definition
	•	fail if any such call is present in the scheduler scope

The first-generation implementation may use:
	•	deterministic AST query execution
	•	deterministic token or symbol scanning
	•	deterministic syntax-aware scanning

The implementation chosen must be repository-local and reproducible.

⸻

14.4 Minimum Detection Targets

At minimum, the validator must detect the forbidden calls declared in the example invariant surface:
	•	sleep
	•	read_blocking
	•	write_blocking

If the authoritative invariant changes, this validator must derive its forbidden set from the authoritative artifact rather than hardcode a conflicting list.

⸻

15. Validation Orchestrator

⸻

15.1 Entry Point

tools/horoji/validators/validate-all


⸻

15.2 Purpose

Run all Phase 4 validators in deterministic order and produce an aggregate result.

⸻

15.3 Required Behavior

The orchestrator must:
	•	execute validators in explicit stable order
	•	aggregate structured results
	•	return non-zero status if any validator fails or errors
	•	preserve individual validator outputs
	•	avoid hiding failing validator details

Recommended order:
	1.	validate-contracts
	2.	validate-invariants
	3.	validate-ownership
	4.	validate-provenance
	5.	validate-scheduler_non_blocking

⸻

16. Bootstrap and Validation Tests

Add tests under:

tests/horoji/

These tests must verify:
	•	each validator executable exists
	•	validators succeed on valid repository state
	•	validators fail on malformed artifacts
	•	validators fail on structural conflicts
	•	output is machine-readable
	•	output ordering is deterministic
	•	repeated execution without repository changes produces identical logical results

⸻

16.1 Required Negative Test Cases

At minimum, include tests for:
	•	malformed contract artifact
	•	overlapping allowed and forbidden dependencies in a contract
	•	malformed invariant artifact
	•	duplicate invariant identifiers
	•	malformed ownership artifact
	•	overlapping ownership without explicit declaration
	•	derived artifact missing provenance
	•	scheduler scope containing a forbidden blocking call

⸻

17. Non-Negotiable Guarantees

This task must ensure:

⸻

17.1 Deterministic validation

Validation results must be reproducible from identical inputs.

⸻

17.2 Explicit enforcement boundaries

Validators must enforce only declared, bounded concerns.

⸻

17.3 No silent structural conflicts

Contract, invariant, ownership, and provenance conflicts must fail explicitly.

⸻

17.4 Repository-backed invariant enforcement exists

At least one actual repository-backed invariant must be executable and enforceable.

⸻

17.5 Validators do not mutate repository state

Validation is read-only.

⸻

18. Forbidden Changes

The following are forbidden in this task:
	•	implementing CI orchestration
	•	implementing merge gates
	•	implementing agent workflow blocking
	•	modifying authoritative artifacts automatically
	•	modifying derived artifacts automatically
	•	performing network access
	•	relying on randomness
	•	performing host-environment discovery beyond explicit repository inputs
	•	introducing non-deterministic validator ordering
	•	collapsing all validation into one opaque script without bounded validator entrypoints

⸻

19. Acceptance Criteria

This task is complete when:
	1.	validate-contracts exists and runs deterministically
	2.	validate-invariants exists and runs deterministically
	3.	validate-ownership exists and runs deterministically
	4.	validate-provenance exists and runs deterministically
	5.	validate-scheduler_non_blocking exists and enforces a real repository-backed invariant
	6.	validate-all exists and aggregates validator results deterministically
	7.	Validators emit structured machine-readable output
	8.	Validators fail explicitly on malformed inputs
	9.	Structural conflicts are detected and rejected
	10.	Tests verify deterministic pass/fail behavior
	11.	Repeated execution without repository changes produces identical logical results
	12.	CHANGELOG records completion of validator implementation

⸻

20. Failure Conditions

This task fails if:
	•	validators produce inconsistent results across identical runs
	•	schema-invalid artifacts pass validation
	•	structural conflicts are silently accepted
	•	repository-backed invariant enforcement is absent
	•	provenance issues in derived artifacts are ignored
	•	validators mutate repository state
	•	validator output is unstructured or ambiguous
	•	validate-all hides individual validator failures

⸻

21. Completion Statement

Upon completion of this task:

The repository contains a deterministic validation layer capable of enforcing authoritative artifact correctness, structural consistency, derived artifact provenance validity, and at least one concrete repository-backed invariant.

CI enforcement, merge policy, and agent gating remain deferred.

⸻

22. One-Sentence Definition

TASK_04 establishes the deterministic validation layer that turns Horoji from a descriptive metadata system into an enforceable repository governance subsystem.

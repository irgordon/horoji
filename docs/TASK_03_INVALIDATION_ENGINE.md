TASK_03_INVALIDATION_ENGINE.md

Status: Mandatory
Authority: Repository Governance
Phase: 3
Scope: Deterministic invalidation engine for derived artifacts
Blocking: TASK_04_VALIDATORS.md and all downstream regeneration workflows

⸻

1. Task Title

Implement the deterministic invalidation engine for Horoji derived artifacts

⸻

2. Objective

Implement the Horoji invalidation engine that determines which derived artifact classes must be regenerated based on repository changes.

This task establishes:
	•	deterministic change detection
	•	rule-driven invalidation decisions
	•	conservative regeneration safety behavior
	•	repository-local invalidation computation

This task must not implement:
	•	derived artifact generation logic
	•	validator enforcement logic
	•	CI pipeline orchestration
	•	agent workflow integration
	•	automatic regeneration execution
	•	policy enforcement outside invalidation scope

⸻

3. Rationale

Derived artifacts become stale when repository inputs change.

Regenerating everything on every change is safe but inefficient.

Regenerating nothing risks incorrect behavior.

The invalidation engine provides the deterministic mechanism that identifies the minimal set of derived artifacts that must be regenerated while guaranteeing correctness.

⸻

4. Scope

Allowed paths:

tools/horoji/invalidation/**
.project_memory/config/**
tests/horoji/**
CHANGELOG.md

All other paths are read-only.

⸻

5. Required Deliverables

This task must implement:
	•	the Horoji invalidation engine executable
	•	deterministic invalidation rule processing
	•	affected artifact class computation
	•	structured invalidation output
	•	conservative fallback behavior

⸻

5.1 Invalidation Engine Entry Point

The following executable must exist:

tools/horoji/invalidation/horoji-invalidate

The executable must be repository-local and deterministic.

⸻

5.2 Input

The invalidation engine must accept:

changed_files

This input represents repository file paths modified in a change set.

The input must be provided explicitly.

The engine must not compute changes implicitly.

⸻

Accepted Input Sources

Examples include:
	•	git diff output
	•	CI-provided change list
	•	explicit file list argument

⸻

5.3 Configuration Input

The invalidation engine must read:

.project_memory/config/invalidation_rules.yaml

This configuration defines deterministic invalidation rules.

The engine must not rely on implicit rules.

⸻

5.4 Output

The invalidation engine must produce structured output identifying:
	•	derived artifact classes requiring regeneration
	•	optionally affected subsystems

⸻

Required Output Structure

invalidation_result:

  affected_artifacts:

    - callgraphs
    - dependencies
    - impact_sets

  reason:

    - header_change_detected

  scope:

    conservative

Output must be deterministic and machine-readable.

⸻

6. Invalidation Rules

Invalidation behavior must be defined entirely through configuration.

The invalidation engine must not hardcode repository-specific rules.

⸻

Rule Structure

Each rule must define:

- trigger:

    - <path_pattern>

  invalidate:

    - <artifact_class>


⸻

Example Rule

- trigger:

    - include/**/*.h

  invalidate:

    - callgraphs
    - dependencies
    - impact_sets


⸻

Rule Requirements

Rules must:
	•	be deterministic
	•	be explicit
	•	be repository-local
	•	match file patterns predictably

Rules must not:
	•	depend on runtime conditions
	•	depend on network access
	•	depend on system configuration
	•	rely on timing behavior

⸻

7. Invalidation Algorithm

The invalidation engine must execute the following deterministic sequence.

⸻

Step 1 — Receive changed file list

Input:

changed_files


⸻

Step 2 — Load invalidation rules

Source:

.project_memory/config/invalidation_rules.yaml


⸻

Step 3 — Match triggers

For each changed file:
	•	evaluate pattern matches
	•	collect matching rules

⸻

Step 4 — Compute affected artifact classes

Combine:

invalidate sets from matching rules

Duplicates must be removed.

Ordering must be deterministic.

⸻

Step 5 — Apply safety rule

If any condition is uncertain:

expand invalidation scope


⸻

8. Safety Rule

The invalidation engine must never under-invalidate.

⸻

Required Behavior

If invalidation scope cannot be determined precisely:

invalidate all derived artifact classes


⸻

Example

scope: full_regeneration


⸻

Forbidden Behavior

The engine must never:
	•	silently ignore unmatched changes
	•	suppress invalidation when uncertainty exists
	•	assume safety without verification

⸻

9. Determinism Requirements

The invalidation engine must be deterministic.

⸻

Deterministic Behavior Rules

The engine must:
	•	produce stable ordering of artifact classes
	•	produce identical results for identical inputs
	•	avoid randomness
	•	avoid environment-dependent behavior
	•	avoid concurrency-dependent ordering

⸻

Input Ordering Rule

The engine must normalize:

changed_files

before processing.

⸻

10. Error Handling

The invalidation engine must fail explicitly when:
	•	invalidation_rules.yaml is missing
	•	invalidation_rules.yaml is malformed
	•	input file list is missing
	•	rule structure is invalid

⸻

Failure Output Structure

error:

  type: configuration_error

  message:

    invalidation rules file missing

The engine must return a non-zero exit code.

⸻

11. Bootstrap Tests

Add tests under:

tests/horoji/

These tests must verify:
	•	rule parsing success
	•	deterministic invalidation output
	•	correct rule matching
	•	conservative fallback behavior
	•	failure on malformed configuration

⸻

Required Test Cases

Case 1 — Single file change

core/scheduler/runqueue.c

Expected:

impact_sets invalidated


⸻

Case 2 — Header change

include/scheduler.h

Expected:

callgraphs invalidated
dependencies invalidated
impact_sets invalidated


⸻

Case 3 — Unknown file pattern

Expected:

full regeneration triggered


⸻

12. Non-Negotiable Guarantees

This task must ensure:

⸻

12.1 No under-invalidation

All required derived artifacts must be regenerated.

⸻

12.2 Deterministic invalidation

Identical inputs must produce identical invalidation results.

⸻

12.3 Repository-local operation

Invalidation must depend only on repository state and configuration.

⸻

12.4 Explicit rule authority

Invalidation behavior must be defined through configuration.

⸻

13. Forbidden Changes

The following actions are forbidden in this task:
	•	executing derived artifact generation
	•	implementing validator enforcement logic
	•	modifying authoritative artifacts
	•	performing CI orchestration
	•	performing network access
	•	inspecting host system configuration
	•	relying on runtime heuristics
	•	introducing probabilistic logic
	•	modifying unrelated repository files

⸻

14. Acceptance Criteria

This task is complete when:
	1.	The invalidation engine executable exists
	2.	Invalidation rules load successfully
	3.	Changed file input produces deterministic output
	4.	Unknown patterns trigger conservative fallback
	5.	Rule matching is deterministic
	6.	Output ordering is stable
	7.	Tests validate deterministic behavior
	8.	Tests verify fallback behavior
	9.	The engine fails explicitly on malformed configuration
	10.	CHANGELOG records completion of invalidation engine implementation

⸻

15. Failure Conditions

This task fails if:
	•	invalidation output varies across identical runs
	•	unmatched changes do not trigger fallback
	•	rule matching depends on environment state
	•	invalidation rules are ignored
	•	malformed configuration does not cause failure
	•	output is non-deterministic

⸻

16. Completion Statement

Upon completion of this task:

The repository contains a deterministic invalidation engine capable of computing which derived artifacts must be regenerated based on repository changes.

Validation enforcement, regeneration execution, CI gating, and agent integration remain deferred.

⸻

17. One-Sentence Definition

TASK_03 establishes the deterministic invalidation mechanism that identifies which derived artifacts must be regenerated to maintain correctness after repository changes.

# TASK_05_CI_ENFORCEMENT.md

Status: Mandatory  
Authority: Repository Governance  
Phase: 5  
Scope: Deterministic CI enforcement for Horoji initialization, regeneration, and validation  
Blocking: TASK_06_AGENT_INTEGRATION.md and all merge-gated Horoji workflows

---

# 1. Task Title

Implement deterministic CI enforcement for Horoji repository governance

---

# 2. Objective

Implement CI enforcement for Horoji so that repository changes are evaluated through a deterministic sequence that verifies:

- Horoji initialization is present
- required bootstrap anchors exist and parse
- invalidation is computed deterministically
- required derived artifacts are regenerated deterministically
- validators execute deterministically
- failing Horoji conditions block CI success

This task establishes:

- a CI entry workflow for Horoji
- deterministic ordering of Horoji checks
- explicit CI fail conditions
- artifact freshness enforcement
- read-only validation and controlled regeneration boundaries

This task must not implement:

- agent workflow orchestration
- model-specific integrations
- merge queue strategy outside Horoji gating
- automatic policy exceptions
- non-deterministic retry logic
- background or asynchronous out-of-band remediation

---

# 3. Rationale

Horoji is not enforceable at repository scale until its checks run automatically and consistently in CI.

Prior phases establish:

- bootstrap structure
- authoritative metadata
- derived generators
- invalidation engine
- validators

Phase 5 binds those subsystems into a deterministic enforcement pipeline.

Without CI enforcement, Horoji remains advisory.

With CI enforcement, malformed artifacts, stale derived outputs, missing provenance, invalid repository structure, and violated invariants become merge-blocking conditions.

---

# 4. Scope

Allowed paths:

```text
.github/workflows/**
tools/horoji/cli/**
tools/horoji/generators/**
tools/horoji/invalidation/**
tools/horoji/validators/**
tests/horoji/**
.project_memory/**
CHANGELOG.md

All other paths are read-only.

⸻

5. Required Deliverables

This task must implement:
	•	a CI workflow that runs Horoji checks on pull requests
	•	deterministic sequencing of bootstrap, invalidation, regeneration, and validation steps
	•	explicit non-zero failure behavior
	•	stale derived artifact detection
	•	repository-local execution rules
	•	machine-readable logs or outputs for Horoji steps

This task must also provide a stable CI entry command or script that can be run locally and in CI with identical logic.

⸻

5.1 Required CI Workflow

A repository CI workflow must exist under:

.github/workflows/

Recommended filename:

horoji-ci.yml

The workflow must execute on:
	•	pull_request
	•	optionally push to protected branches if repository policy requires it

The pull request path is mandatory.

⸻

5.2 Required CI Entry Point

A stable orchestrator entrypoint must exist for Horoji CI enforcement.

Recommended options:

tools/horoji/cli/horoji ci-check

or

tools/horoji/cli/horoji-check

or

tools/horoji/validators/validate-all

If an existing validator orchestrator is reused, it must still support the CI ordering defined in this task.

There must be one canonical CI entry path.

Multiple conflicting entrypoints are forbidden.

⸻

6. Required CI Execution Order

CI must execute Horoji steps in deterministic order.

Required minimum sequence:
	1.	verify Horoji bootstrap presence
	2.	verify schema/config parseability
	3.	compute changed files
	4.	run invalidation engine
	5.	regenerate required derived artifacts
	6.	validate authoritative artifacts
	7.	validate derived artifact provenance and structure
	8.	run repository-backed invariant validators
	9.	verify no stale derived artifact remains
	10.	fail or pass explicitly

This order is binding.

Validators must not run before required regeneration.

Regeneration must not run before invalidation.

⸻

7. Bootstrap Enforcement Requirements

CI must fail immediately if any required Horoji bootstrap surface is missing or malformed.

Required checks include:
	•	required .project_memory/ subtree presence
	•	required schema file presence
	•	required config file presence
	•	parseability of schema files
	•	parseability of config files

If bootstrap checks fail:
	•	CI must stop early
	•	later Horoji steps must not run
	•	failure output must identify the missing or malformed anchor

⸻

8. Changed File Resolution

CI must compute the repository change set deterministically.

The changed file list must be the sole input to invalidation for a given CI run.

Changed file resolution must:
	•	operate only on repository state available to CI
	•	avoid heuristic discovery outside repository history available in the checkout
	•	normalize ordering before passing to invalidation

If changed files cannot be computed reliably, CI must fail explicitly rather than silently widening or skipping checks.

⸻

9. Invalidation Execution Requirements

CI must invoke the Horoji invalidation engine using the normalized changed file list.

The invalidation engine output must determine which derived artifact classes require regeneration.

CI must not bypass invalidation by:
	•	always regenerating without recording invalidation scope, unless explicitly configured as a conservative repository policy
	•	selectively skipping invalidation for convenience
	•	inferring regeneration scope outside the invalidation engine

If the invalidation engine returns conservative full regeneration, CI must honor that result.

⸻

10. Regeneration Requirements

CI must regenerate all derived artifact classes identified by invalidation.

Regeneration must:
	•	be deterministic
	•	write only to the derived subtree
	•	attach provenance where required
	•	fail explicitly on malformed source inputs
	•	avoid modifying authoritative artifacts

If no derived artifacts require regeneration, CI may skip regeneration, but only if invalidation output explicitly permits that.

⸻

11. Validation Requirements

After regeneration, CI must run Horoji validators in deterministic order.

Required minimum validators:
	•	contract validator
	•	invariant validator
	•	ownership validator
	•	provenance validator
	•	at least one repository-backed invariant validator
	•	validation orchestrator or equivalent aggregate result

Validation must run on the post-regeneration repository state.

Validation must not consume stale pre-regeneration outputs.

⸻

12. Stale Derived Artifact Detection

CI must detect whether checked-in derived artifacts are stale relative to current authoritative inputs and generator outputs.

At minimum, stale detection must fail if:
	•	regenerated output differs logically from checked-in output
	•	required provenance metadata is missing
	•	invalidation required regeneration but repository state was not updated accordingly

CI must not silently overwrite stale outputs and pass.

Two acceptable repository policies exist:

Policy A — committed derived artifacts

If derived artifacts are committed, CI must fail when regeneration produces differences not included in the change set.

Policy B — non-committed derived artifacts

If derived artifacts are not committed, CI must still validate regenerated outputs during the CI run, but stale-check semantics must be defined accordingly.

The repository must choose one policy explicitly.

Implicit mixed policy is forbidden.

⸻

13. Structured CI Output Requirements

Each Horoji CI stage must emit machine-readable and human-readable output sufficient to diagnose failure.

Required minimum stage outputs:
	•	bootstrap check result
	•	invalidation result
	•	regeneration result
	•	validator results
	•	stale artifact check result

Output ordering must be deterministic.

Freeform log-only output without structured summaries is forbidden.

Recommended stage result shape:

stage: bootstrap
status: PASS|FAIL|ERROR
reason: <short_reason>
details:
  - <detail>

Equivalent JSON is acceptable.

⸻

14. Determinism Requirements

The full Horoji CI pipeline must be deterministic.

Given identical:
	•	repository state
	•	changed file list
	•	configuration
	•	toolchain
	•	workflow inputs

CI results must be logically identical.

The CI workflow must not depend on:
	•	current wall clock time for logical decisions
	•	random seeds
	•	host environment probing outside explicit workflow inputs
	•	network-fetched policy or schema content
	•	external mutable service state

Tool installation is permitted only if pinned and deterministic under repository policy.

Unpinned tool discovery is forbidden.

⸻

15. Error Handling Requirements

Each Horoji CI stage must fail explicitly.

Required behavior:
	•	non-zero exit on failure
	•	stage-local error identification
	•	no silent skip of required stages
	•	no downgrade of required failures to warnings

If a stage errors, CI must not continue as if the stage passed.

Where repository policy allows continued execution for diagnostic aggregation, the final job result must still fail.

⸻

16. Local Reproducibility Requirement

The same Horoji CI logic must be runnable locally.

The repository must provide a documented local command path that mirrors CI enforcement order.

Recommended:

tools/horoji/cli/horoji ci-check

The local path must:
	•	use the same invalidation logic
	•	use the same regeneration logic
	•	use the same validators
	•	produce logically equivalent results

CI-only hidden logic is forbidden.

⸻

17. Required Test Coverage

Add tests under:

tests/horoji/

These tests must verify:
	•	CI configuration file exists and parses
	•	Horoji CI stage ordering is stable
	•	missing bootstrap anchors fail CI entry checks
	•	invalidation output is consumed correctly
	•	regeneration is invoked when required
	•	validators run after regeneration
	•	stale derived artifact conditions fail
	•	repeated execution with unchanged inputs produces identical logical outcomes

If CI workflow semantics are difficult to test directly, a repository-local orchestration script must be tested instead.

⸻

18. Required Negative Test Cases

At minimum, include tests for:
	•	missing schema anchor in CI run
	•	malformed config anchor in CI run
	•	invalidation engine failure
	•	generator failure
	•	validator failure
	•	derived artifact missing provenance
	•	stale derived artifact after regeneration
	•	repository-backed invariant failure
	•	missing canonical CI entrypoint
	•	stage order violation

⸻

19. Non-Negotiable Guarantees

This task must ensure:

⸻

19.1 Horoji is enforced automatically

Repository changes are evaluated through Horoji in CI without manual invocation.

⸻

19.2 Horoji failures block success

Malformed or inconsistent Horoji state causes CI failure.

⸻

19.3 Regeneration precedes validation

Derived artifacts are regenerated before validators consume them.

⸻

19.4 Staleness is detected

CI rejects stale or missing required derived outputs under the chosen repository policy.

⸻

19.5 CI logic is reproducible locally

The same enforcement path can be executed outside CI using the canonical local entrypoint.

⸻

20. Forbidden Changes

The following are forbidden in this task:
	•	implementing agent orchestration
	•	hardcoding model-specific workflows
	•	allowing CI to pass when required Horoji stages fail
	•	silently skipping invalidation
	•	silently skipping regeneration when invalidation requires it
	•	silently skipping validators
	•	mutating authoritative artifacts during CI
	•	relying on non-deterministic tool selection
	•	introducing hidden CI-only enforcement logic not reproducible locally

⸻

21. Acceptance Criteria

This task is complete when:
	1.	a Horoji CI workflow exists for pull requests
	2.	CI executes Horoji stages in deterministic required order
	3.	bootstrap presence and parseability are enforced in CI
	4.	changed files are resolved deterministically
	5.	invalidation runs and determines regeneration scope
	6.	required derived artifacts are regenerated deterministically
	7.	validators run after regeneration
	8.	stale derived artifact conditions fail CI under the chosen repository policy
	9.	stage outputs are structured and diagnosable
	10.	local execution path mirrors CI logic
	11.	tests verify pass/fail behavior for required positive and negative cases
	12.	CHANGELOG records completion of CI enforcement implementation

⸻

22. Failure Conditions

This task fails if:
	•	CI does not run Horoji on pull requests
	•	required Horoji stages run in non-deterministic or incorrect order
	•	malformed bootstrap/config/schema state passes
	•	invalidation is skipped or ignored
	•	required regeneration is skipped
	•	validators consume stale outputs
	•	stale derived artifacts are not detected
	•	CI success is possible despite failing required Horoji checks
	•	local reproducibility path is absent
	•	CI logic differs materially from local enforcement logic

⸻

23. Completion Statement

Upon completion of this task:

The repository contains deterministic CI enforcement for Horoji bootstrap verification, invalidation-driven regeneration, validation, and stale artifact detection, making Horoji a mandatory automated governance path for repository changes.

Agent integration remains deferred.

⸻

24. One-Sentence Definition

TASK_05 establishes deterministic CI enforcement that makes Horoji initialization, regeneration, validation, and artifact freshness mandatory for repository changes.

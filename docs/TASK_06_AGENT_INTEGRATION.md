# TASK_06_AGENT_INTEGRATION.md

Status: Mandatory  
Authority: Repository Governance  
Phase: 6  
Scope: Deterministic integration of external agents with the Horoji memory and governance subsystem  
Blocking: None — This is the terminal integration phase for the first-generation Horoji workflow

---

# 1. Task Title

Integrate external agents as deterministic clients of the Horoji repository memory and governance system

---

# 2. Objective

Establish a deterministic, model-agnostic integration pattern so that all external agents:

- retrieve structured repository context from Horoji
- operate only within declared subsystem boundaries
- produce diffs constrained by contracts and invariants
- submit changes subject to CI enforcement
- remain external to the Horoji trust model

This task establishes:

- a stable Horoji context contract
- a deterministic agent interaction protocol
- CI-triggered agent workflows
- reproducible agent invocation semantics
- explicit boundaries between agent behavior and repository governance

This task must not implement:

- model-specific business logic
- dynamic learning behavior inside the repository
- persistent agent memory outside `.project_memory`
- runtime dependency on external model services
- automated code generation without CI validation

---

# 3. Rationale

Prior phases establish:

- repository memory structure
- authoritative metadata
- derived artifact generation
- invalidation logic
- validation enforcement
- CI governance

Phase 6 defines how external agents interact with that system.

The central rule is:

External agents are clients of Horoji.  
Horoji is not a client of agents.

This separation ensures:

- deterministic repository behavior
- reproducible enforcement
- model independence
- auditability of automated changes

---

# 4. Scope

Allowed paths:

```text
tools/horoji/cli/**
.github/workflows/**
docs/**
tests/horoji/**
.project_memory/**
CHANGELOG.md

All other paths are read-only.

⸻

5. Required Deliverables

This task must implement:
	•	a deterministic Horoji context retrieval interface
	•	a standard agent interaction contract
	•	CI-triggered agent workflow templates
	•	structured agent execution logging
	•	explicit failure handling for agent workflows
	•	repository documentation describing agent usage

⸻

5.1 Agent Definition

For the purposes of this repository, an agent is any automated system that:
	•	reads repository state
	•	proposes modifications
	•	generates diffs
	•	interacts with CI workflows

Examples include:
	•	ChatGPT
	•	Gemini
	•	Copilot
	•	scripted automation
	•	CI-triggered code generation tools

All such systems are treated identically.

⸻

6. Core Integration Rule

All agents must retrieve Horoji context before generating changes.

Required sequence:
	1.	request structured context from Horoji
	2.	analyze repository constraints
	3.	generate a plan or diff
	4.	submit changes through CI
	5.	allow Horoji validation to determine acceptance

Agents must never:
	•	modify repository state without CI validation
	•	bypass Horoji validation
	•	write authoritative artifacts directly
	•	persist private memory inside the repository

⸻

7. Horoji Context Contract

The repository must define a stable machine-readable context structure.

Required minimum format:

{
  "subsystem": "example_subsystem",
  "contract": { ... },
  "invariants": [ ... ],
  "ownership": [ ... ],
  "impact_set": [ ... ],
  "callgraph_slice": { ... },
  "history": [ ... ]
}

Fields may be empty if not yet generated.

Field presence must remain stable.

⸻

8. Required CLI Commands

The Horoji CLI must expose deterministic commands that return structured repository state.

Required minimum commands:

horoji get-contract <subsystem>
horoji get-invariants <subsystem>
horoji get-owner <file>
horoji get-impact-set <file>
horoji get-context <subsystem>
horoji validate

Each command must:
	•	operate deterministically
	•	read repository-local data only
	•	return structured output
	•	avoid side effects

⸻

9. Agent Workflow Templates

The repository must provide reusable workflow templates for agent interaction.

Templates must exist under:

.github/workflows/

Required template examples:

agent-modify-subsystem.yml
agent-generate-change.yml
agent-validate-change.yml

Templates may be minimal.

They must define:
	•	workflow trigger conditions
	•	Horoji context retrieval step
	•	agent invocation step
	•	validation step
	•	failure handling step

⸻

10. Agent Invocation Requirements

Agent execution must be:
	•	deterministic
	•	reproducible
	•	logged
	•	isolated from repository state mutation

Agent invocation must:
	•	read context from Horoji
	•	produce output as a proposed diff
	•	never commit changes directly
	•	return explicit success or failure status

⸻

11. CI Integration Requirements

All agent-generated changes must pass the existing CI enforcement pipeline.

Agent workflows must:
	•	trigger standard CI checks
	•	run validation after change generation
	•	block merge on validation failure
	•	produce audit logs

No separate CI bypass path may exist for agent-generated changes.

⸻

12. Logging Requirements

Agent execution must produce structured logs.

Required minimum fields:

agent:
  name: <agent_identifier>
  version: <agent_version>
execution:
  timestamp: <iso8601>
  subsystem: <target_subsystem>
  action: <operation>
result:
  status: SUCCESS|FAILURE
  details:
    - <message>

Logs must be:
	•	deterministic
	•	repository-local
	•	human-readable
	•	machine-readable

⸻

13. Determinism Requirements

Agent workflows must be deterministic.

Given identical:
	•	repository state
	•	Horoji context
	•	workflow configuration

agent execution must produce logically equivalent outcomes.

Non-deterministic behavior is forbidden.

Examples of forbidden dependencies:
	•	random number generation
	•	dynamic network configuration discovery
	•	environment-specific path assumptions
	•	time-based logic affecting repository state

⸻

14. Security Requirements

Agent workflows must not:
	•	execute arbitrary external code
	•	modify protected repository paths without validation
	•	store credentials inside the repository
	•	introduce persistent runtime services
	•	access network resources unless explicitly permitted by repository policy

All repository changes must remain auditable.

⸻

15. Local Reproducibility Requirement

Agent workflows must be reproducible outside CI.

The repository must provide documented steps for:
	•	retrieving Horoji context
	•	invoking an agent
	•	validating changes locally

Local execution must produce logically equivalent validation outcomes.

⸻

16. Required Documentation

The repository must include documentation describing:
	•	agent integration rules
	•	required workflow sequence
	•	failure handling behavior
	•	security constraints
	•	reproducibility requirements

Recommended location:

docs/AGENT_INTEGRATION.md


⸻

17. Required Tests

Add tests under:

tests/horoji/

Tests must verify:
	•	context retrieval commands execute successfully
	•	CLI outputs remain structured
	•	agent workflow templates exist
	•	CI validation runs after agent workflows
	•	agent-generated changes cannot bypass validation
	•	workflow logs are produced deterministically

⸻

18. Required Negative Test Cases

At minimum, include tests for:
	•	missing context retrieval command
	•	malformed context output
	•	agent attempting to modify repository without validation
	•	agent workflow skipping validation step
	•	invalid change submission
	•	unauthorized artifact modification
	•	missing workflow log output

Each failure must produce deterministic error output.

⸻

19. Non-Negotiable Guarantees

This task must ensure:

⸻

19.1 Agents are external clients

Agents interact with Horoji but do not control repository governance.

⸻

19.2 Horoji remains the canonical memory layer

All repository context is retrieved from Horoji.

⸻

19.3 All agent changes are validated

No automated change may bypass CI enforcement.

⸻

19.4 Agent behavior is auditable

All automated actions produce structured logs.

⸻

19.5 Integration remains model-agnostic

The repository does not depend on a specific AI system.

⸻

20. Forbidden Changes

The following are forbidden in this task:
	•	embedding model-specific logic into repository governance
	•	storing agent memory outside .project_memory
	•	bypassing CI enforcement
	•	allowing direct repository modification by agents
	•	introducing non-deterministic workflow behavior
	•	implementing hidden automation paths
	•	introducing runtime services not defined by repository policy

⸻

21. Acceptance Criteria

This task is complete when:
	1.	a deterministic Horoji context retrieval interface exists
	2.	required CLI commands return structured output
	3.	agent workflow templates exist
	4.	agent invocation produces structured logs
	5.	agent-generated changes trigger CI validation
	6.	validation failures block merge
	7.	repository documentation describes agent integration
	8.	tests verify agent workflow behavior
	9.	workflows are reproducible locally
	10.	CHANGELOG records completion of agent integration

⸻

22. Failure Conditions

This task fails if:
	•	agents can modify repository state without validation
	•	context retrieval is bypassed
	•	workflow logs are missing
	•	CI validation does not run after agent execution
	•	non-deterministic behavior affects repository state
	•	repository governance depends on a specific AI system
	•	integration cannot be reproduced locally

⸻

23. Completion Statement

Upon completion of this task:

External agents operate as deterministic clients of the Horoji memory and governance subsystem, and all automated repository changes are governed by CI validation and structured repository metadata.

⸻

24. One-Sentence Definition

TASK_06 establishes deterministic, model-agnostic integration of external agents as controlled clients of the Horoji repository memory and governance system.

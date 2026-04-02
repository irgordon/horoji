# AGENT_INTEGRATION.md

Status: Mandatory  
Authority: Repository Governance  
Scope: Deterministic external agent integration with Horoji (TASK_06)

---

## 1. Integration Rules

External agents are repository clients. They do not control repository governance.

Required sequence:

1. Retrieve structured Horoji context.
2. Analyze contracts, invariants, ownership, and impact.
3. Produce a proposed diff.
4. Run Horoji validation and CI enforcement.
5. Accept or reject through CI outcomes.

Agents must not:

- bypass Horoji validation
- commit or push directly from agent logic
- write authoritative artifacts directly
- persist memory outside `.project_memory`

---

## 2. Required CLI Commands

Use `tools/horoji/cli/horoji`:

- `get-contract <subsystem>`
- `get-invariants <subsystem>`
- `get-owner <file>`
- `get-impact-set <file>`
- `get-context <subsystem>`
- `validate`

All commands are deterministic, repository-local, and return structured YAML output.

---

## 3. Context Contract

`get-context <subsystem>` returns a stable shape:

- `subsystem`
- `contract`
- `invariants`
- `ownership`
- `impact_set`
- `callgraph_slice`
- `history`

Fields remain present even when empty.

---

## 4. Workflow Templates

Template workflows are provided under `.github/workflows/`:

- `agent-modify-subsystem.yml`
- `agent-generate-change.yml`
- `agent-validate-change.yml`

Each template defines:

- trigger conditions
- Horoji context retrieval
- agent invocation placeholder
- Horoji validation
- CI enforcement (`horoji-check`)
- structured log output
- explicit failure handling

---

## 5. Structured Agent Logs

Use:

`horoji log-agent-execution --agent-name ... --agent-version ... --timestamp ... --subsystem ... --action ... --status SUCCESS|FAILURE --detail ...`

Structured output shape:

- `agent.name`
- `agent.version`
- `execution.timestamp`
- `execution.subsystem`
- `execution.action`
- `result.status`
- `result.details`

---

## 6. Security and Determinism Constraints

Agent workflows must remain deterministic and auditable:

- no random or time-based state mutation logic
- no hidden automation path around validation
- no direct repository mutation commit path in agent invocation
- no external persistent runtime services
- no repository credential storage

All acceptance is controlled by repository CI and Horoji validators.

---

## 7. Local Reproducibility

From repository root:

1. Retrieve context:
   - `python tools/horoji/cli/horoji get-context horoji_cli`
2. Run deterministic validation:
   - `python tools/horoji/cli/horoji validate`
3. Run canonical CI-equivalent enforcement:
   - `python tools/horoji/cli/horoji-check --repo-root "$PWD" --changed-file tools/horoji/cli/horoji --derived-policy committed`
4. Emit a deterministic example agent log:
   - `python tools/horoji/cli/horoji log-agent-execution --agent-name example --agent-version 1.0.0 --timestamp 2026-01-01T00:00:00Z --subsystem horoji_cli --action validate_change --status SUCCESS --detail context_retrieved`

These steps mirror the workflow sequencing used by the agent templates.

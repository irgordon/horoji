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
- silently succeed after validation failure

Agent workflows must fail explicitly on validation failure.

---

## 2. Required CLI Commands

Use `tools/horoji/cli/horoji`.

The exported CLI command surface is governed by the authoritative contract:

`.project_memory/authoritative/contracts/horoji_cli.yaml`

Any change to the command surface requires a corresponding contract update.

Required commands:

- `get-contract <subsystem>`
- `get-invariants <subsystem>`
- `get-owner <file>`
- `get-impact-set <file>`
- `get-context <subsystem>`
- `validate`
- `log-agent-execution`

All commands are deterministic, repository-local, and return structured YAML output.

The CLI must not:

- modify authoritative artifacts
- rely on network access
- depend on host environment discovery
- introduce non-deterministic output

---

## 3. Context Contract

`get-context <subsystem>` returns a stable structure.

Fields:

- `subsystem`
- `contract`
- `invariants`
- `ownership`
- `impact_set`
- `callgraph_slice`
- `history`

Rules:

- Field names are stable.
- Field ordering is deterministic.
- Fields remain present even when empty.
- Output is reproducible for identical repository state.

This structure is the canonical agent input surface.

---

## 4. Workflow Templates

Template workflows are provided under:

`.github/workflows/`

Required templates:

- `agent-modify-subsystem.yml`
- `agent-generate-change.yml`
- `agent-validate-change.yml`

Each template defines the same deterministic execution phases:

1. Trigger conditions
2. Horoji context retrieval
3. Agent invocation placeholder
4. Horoji validation
5. CI enforcement (`horoji-check`)
6. Structured log emission
7. Explicit failure handling
8. Artifact preservation

Workflow sequencing rules:

- Context retrieval must occur before agent invocation.
- Validation must occur after agent invocation.
- CI enforcement must determine acceptance.
- No workflow may bypass validation.
- No workflow may commit directly.

---

## 5. Structured Agent Logs

Use:

```bash
tools/horoji/cli/horoji log-agent-execution \
  --agent-name <name> \
  --agent-version <version> \
  --timestamp <ISO8601> \
  --subsystem <subsystem> \
  --action <action> \
  --status SUCCESS|FAILURE \
  --detail <detail>
````

Required structured output fields:

* `agent.name`
* `agent.version`
* `execution.timestamp`
* `execution.subsystem`
* `execution.action`
* `result.status`
* `result.details`

Rules:

* Logs are deterministic.
* Logs are machine-readable.
* Logs are append-only or transient.
* Logs are not authoritative state.
* Logs must not alter repository behavior.

---

## 6. Security and Determinism Constraints

Agent workflows must remain deterministic and auditable.

Forbidden behaviors:

* random or time-dependent mutation logic
* hidden automation paths around validation
* direct repository mutation commits from agent logic
* external persistent runtime services
* repository credential storage
* network-dependent execution paths

All repository acceptance is controlled by:

* Horoji validators
* CI enforcement

Agents are advisory.

Validators are authoritative.

---

## 7. Local Reproducibility

All workflows must be reproducible locally from the repository root.

`horoji-check` is the deterministic CI enforcement entrypoint located at:

```
tools/horoji/cli/horoji-check
```

Required local validation sequence:

Retrieve deterministic context:

```bash
python3 tools/horoji/cli/horoji get-context horoji_cli
```

Run deterministic validation:

```bash
python3 tools/horoji/cli/horoji validate
```

Run canonical CI-equivalent enforcement:

```bash
python3 tools/horoji/cli/horoji-check \
  --repo-root "$PWD" \
  --changed-file tools/horoji/cli/horoji \
  --derived-policy committed
```

Emit deterministic example agent log:

```bash
python3 tools/horoji/cli/horoji log-agent-execution \
  --agent-name example \
  --agent-version 1.0.0 \
  --timestamp 2026-01-01T00:00:00Z \
  --subsystem horoji_cli \
  --action validate_change \
  --status SUCCESS \
  --detail context_retrieved
```

These steps mirror the workflow sequencing used by the agent templates.

---

## 8. Non-Negotiable Invariants

The following invariants define correct agent integration behavior.

Horoji must always remain the repository authority.

Agents must always consume Horoji context before producing changes.

Validation must always occur before acceptance.

CI must always determine repository acceptance.

All outputs must remain deterministic.

All failures must be explicit.

No alternate authority surface may exist outside Horoji.

<h1 align="center">Horoji</h1>

<p align="center">
  <img alt="Python 3.12+" src="https://img.shields.io/badge/python-3.12%2B-blue">
  <img alt="YAML metadata" src="https://img.shields.io/badge/metadata-YAML-green">
  <img alt="GitHub Actions" src="https://img.shields.io/badge/ci-GitHub%20Actions-black">
</p>

Horoji is a repository-resident project memory subsystem. It exposes
authoritative architectural facts, machine-readable invariants, ownership
boundaries, and deterministic structural metadata from files that live in this
repository.

Horoji is meant to reduce repeated context derivation, constrain implementation
scope, and give developers and agents a stable way to query repository
governance before making changes.

Canonical truth remains in source files and governance documents. Horoji
provides structured projections of that truth.

## What Horoji Is

Horoji is:

- a deterministic repository-local memory subsystem
- a structural projection layer over repository facts
- an invariant and ownership enforcement surface
- a machine-readable context source for developers, CI, and external agents

Horoji derives artifacts only from repository content, pinned tooling, explicit
repository configuration, and declared CI inputs passed through approved
entrypoints.

## What Horoji Is Not

Horoji is not:

- a reasoning engine
- a documentation replacement
- a source-of-truth override
- a probabilistic retrieval system
- an autonomous agent memory
- a deployment, merge, or release approval system

Derived Horoji artifacts must never override authoritative repository files or
governance documents.

## Current Status

The current repository contains the first-generation Horoji baseline:

- bounded public CLI query surface
- internal invalidation and regeneration orchestration
- authoritative ownership for active tool surfaces
- deterministic validators, including determinism and locality checks
- committed derived artifact policy support through `horoji-check`
- agent workflow templates that consume Horoji context and then run validation

The public CLI is intentionally small. Regeneration and invalidation are
internal orchestration surfaces, not public `horoji` commands.

## Repository Layout

```text
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
  schemas/
  config/

docs/
tools/
  horoji/
    cli/
    generators/
    invalidation/
    validators/
tests/
  horoji/
```

Root documentation orients contributors. Detailed governance lives in `docs/`.
Machine-readable memory artifacts live in `.project_memory/`.

## Clean-Clone Setup

Supported runtime:

- Python 3.12 or newer

Horoji is a repository-local toolset. From a clean clone, use a local virtual
environment and install the repository metadata with test dependencies:

```bash
git clone https://github.com/irgordon/horoji.git
cd horoji
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[test]"
```

Run the standard local validation path:

```bash
python tools/horoji/validators/validate-all
python -m pytest
python tools/horoji/cli/horoji-check \
  --repo-root . \
  --changed-file README.md \
  --derived-policy committed
```

After committing a change, run the same committed-derived policy from the last
commit:

```bash
python tools/horoji/cli/horoji-check \
  --repo-root . \
  --auto-diff \
  --derived-policy committed
```

Run a public CLI query example:

```bash
python tools/horoji/cli/horoji --repo-root . get-contract horoji_cli
python tools/horoji/cli/horoji --repo-root . get-context horoji_cli
python tools/horoji/cli/horoji --repo-root . get-owner tools/horoji/cli/horoji
```

## Authoritative vs Derived Artifacts

Authoritative artifacts define canonical repository memory facts. They are
human-reviewed and version-controlled.

Examples:

- `.project_memory/authoritative/contracts/`
- `.project_memory/authoritative/invariants/`
- `.project_memory/authoritative/ownership/`
- `.project_memory/authoritative/architecture_manifest/`

Derived artifacts are reproducible projections of authoritative repository
facts. They are cacheable, disposable, and must include provenance.

Examples:

- `.project_memory/derived/callgraphs/`
- `.project_memory/derived/dependencies/`
- `.project_memory/derived/impact_sets/`

Derived artifacts must be reproducible from repository content, pinned tooling,
explicit repository configuration, and declared CI inputs. They must never
redefine contracts, ownership, invariants, or review decisions.

## Public CLI Surface

Use the public CLI at:

```bash
python3 tools/horoji/cli/horoji <command>
```

Current public commands:

```text
get-contract <subsystem>
get-invariants <subsystem>
get-owner <file>
get-impact-set <file>
get-context <subsystem>
validate
log-agent-execution
```

The public CLI command set is governed by:

- `docs/ARCHITECTURE.md`
- `docs/IMPLEMENTATION_PLAN.md`
- `.project_memory/authoritative/contracts/horoji_cli.yaml`
- `tools/horoji/cli/horoji`
- `tools/horoji/validators/validate-cli-contract`

Do not add, rename, or document public CLI commands without updating those
surfaces together.

## Internal Orchestration Surfaces

These tools exist for generation, invalidation, validation, and CI
orchestration:

- `tools/horoji/cli/horoji-check`
- `tools/horoji/generators/horoji-callgraph`
- `tools/horoji/generators/horoji-deps`
- `tools/horoji/generators/horoji-impact`
- `tools/horoji/invalidation/horoji-invalidate`
- `tools/horoji/validators/*`

`horoji-check` may invoke invalidation and regeneration internally. There is no
public `horoji regenerate` or `horoji invalidate` command in the current command
surface.

## Validation

The core local validation path is:

```bash
python3 tools/horoji/validators/validate-all
python3 -m pytest
```

`validate-all` aggregates repository validators for contracts, CLI command-set
alignment, invariants, ownership, provenance, repository-backed invariants, and
determinism/locality boundaries.

`pytest` runs the Horoji regression test suite under `tests/horoji/`.

The CI-equivalent entrypoint is:

```bash
python3 tools/horoji/cli/horoji-check \
  --repo-root . \
  --changed-file README.md \
  --derived-policy committed
```

`horoji-check` verifies bootstrap anchors, computes invalidation from explicit
changed files, runs required regeneration, runs validators, and checks whether
committed derived artifacts are stale.

With `--derived-policy committed`, the check fails if `.project_memory/derived`
has uncommitted changes after regeneration. This is the repository policy used
to ensure checked-in derived artifacts match current authoritative inputs and
generator output.

If validation fails, read the structured `reason` and `details` fields first.
Repair the repository artifact or command input named there, then rerun the same
command. When committed derived policy reports stale artifacts, rerun
`horoji-check` for the changed primary files and commit the generated
`.project_memory/derived/**` changes if they are expected.

Do not manually edit derived artifacts as a substitute for regeneration. Do not
treat derived artifacts as authoritative.

## Operator Command Matrix

| Task | Command | Notes |
| --- | --- | --- |
| Run all Horoji validators | `python3 tools/horoji/validators/validate-all` | Validates authoritative, derived, invariant, ownership, CLI, and determinism surfaces. |
| Run the full test suite | `python3 -m pytest` | Runs tests configured in `pyproject.toml`. |
| Run CI-equivalent Horoji check for a file | `python3 tools/horoji/cli/horoji-check --repo-root . --changed-file README.md --derived-policy committed` | Uses committed derived policy. Replace `README.md` with the changed path. |
| Query a subsystem contract | `python3 tools/horoji/cli/horoji get-contract horoji_cli` | Reads authoritative contract data. |
| Query subsystem context | `python3 tools/horoji/cli/horoji get-context horoji_cli` | Combines authoritative and derived context while preserving trust boundaries. |
| Query file owner | `python3 tools/horoji/cli/horoji get-owner tools/horoji/cli/horoji` | Uses authoritative ownership metadata. |
| Query file impact set | `python3 tools/horoji/cli/horoji get-impact-set README.md` | Reads the committed derived impact artifact if present. |
| Run public CLI validation wrapper | `python3 tools/horoji/cli/horoji validate` | Delegates to `validate-all`. |
| Run one validator | `python3 tools/horoji/validators/validate-determinism` | Example targeted validator. |
| Emit an agent execution log | `python3 tools/horoji/cli/horoji log-agent-execution --agent-name example --agent-version 1.0.0 --timestamp 2026-01-01T00:00:00Z --subsystem horoji_cli --action validate_change --status SUCCESS --detail context_retrieved` | Emits deterministic YAML; it is not authoritative state. |

## Agent Workflow

Agents are repository clients. They do not control repository governance.

Before editing, agents should read `AGENTS.md` and the relevant files in
`docs/`. The expected workflow is:

1. Retrieve Horoji context with `get-context` or the narrower query commands.
2. Read the governing contract, invariants, ownership, and impact information.
3. Produce a proposed change within the declared boundary.
4. Run Horoji validation and tests.
5. Report completed task, summary, files changed, commands run, validation, and
   notes or deviations.

Agent workflow templates live in `.github/workflows/`. They retrieve Horoji
context, invoke an external agent placeholder, run validation, run
`horoji-check`, and preserve logs as workflow artifacts.

Agents must not bypass validation, treat derived artifacts as authoritative, or
commit directly from workflow logic.

## Governance Documents

Primary governance and implementation documents:

- `AGENTS.md`
- `docs/ARCHITECTURE.md`
- `docs/CODING_STYLE.md`
- `docs/IMPLEMENTATION_PLAN.md`
- `docs/AGENT_INTEGRATION.md`
- `docs/ROADMAP.md`
- `docs/SCHEMAS.md`
- `docs/TASK_00_HOROJI_BOOTSTRAP.md`
- `docs/TASK_01_AUTHORITATIVE_SURFACES.md`
- `docs/TASK_02_GENERATORS.md`
- `docs/TASK_03_INVALIDATION_ENGINE.md`
- `docs/TASK_04_VALIDATORS.md`
- `docs/TASK_05_CI_ENFORCEMENT.md`
- `docs/TASK_06_AGENT_INTEGRATION.md`

Use governance documents for authority rules and design constraints. Use
`CHANGELOG.md` for completed work history.

## Development Rules

- Keep changes narrow and repository-local.
- Preserve authoritative versus derived boundaries.
- Keep public CLI behavior aligned with the CLI contract.
- Do not document unsupported commands.
- Do not use environment discovery, network access, random values, or wall-clock
  reads as hidden authority for derived output.
- Regenerate and commit derived artifacts when committed derived policy requires
  them.

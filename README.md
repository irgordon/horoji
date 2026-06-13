<h1 align="center">Horoji</h1>

<p align="center">
  <img alt="Python 3.12+" src="https://img.shields.io/badge/python-3.12%2B-blue">
  <img alt="YAML metadata" src="https://img.shields.io/badge/metadata-YAML-green">
  <img alt="GitHub Actions" src="https://img.shields.io/badge/ci-GitHub%20Actions-black">
</p>

Horoji helps developers and AI coding agents understand a repository before they change it.

It keeps important project facts in one place, such as:

* how the project is organized
* which files own which parts of the system
* which rules must not be broken
* which generated files need to stay in sync

The goal is simple: reduce guesswork.

Before a developer or agent edits code, Horoji gives them a structured way to check the project’s rules, ownership boundaries, and affected files. That helps keep changes smaller, safer, and easier to review.

Horoji does not replace the repository’s source files or documentation. Those remain the source of truth. Horoji reads those facts, organizes them, and checks that generated project memory stays current.

New to Horoji? Start with the [Horoji Wiki](docs/wiki/introduction.md) for a plain-language walkthrough of the major components, terms, workflows, and diagrams.

## Why Use Horoji?

Large repositories are hard to understand quickly.

A developer may need to answer:

* What part of the project owns this file?
* What rules apply before I change it?
* What other files may be affected?
* Did generated project memory get updated correctly?
* Did an AI agent stay inside the right scope?

Horoji gives the repository a local memory layer for those answers.

It is designed for teams that want AI-assisted development without letting agents guess how the project works.

## What Horoji Does

Horoji can:

* store reviewed project facts in `.project_memory/authoritative/`
* generate derived project maps in `.project_memory/derived/`
* validate contracts, ownership, invariants, and provenance
* check whether generated memory files are stale
* give developers and agents a small command-line interface for project context
* support CI checks so drift is caught before merge

In plain terms: Horoji helps the repository explain itself.

## What Horoji Does Not Do

Horoji is not:

* an AI reasoning engine
* a chatbot
* a documentation replacement
* a release approval system
* a deployment tool
* a source-of-truth override
* a probabilistic search system

It does not decide whether a change is good.

It helps developers and agents see the rules before they make or review a change.

## Current Status

Horoji currently provides a stable governed baseline.

It includes:

* a small public CLI for querying project memory
* validation for contracts, ownership, invariants, provenance, and determinism
* committed generated-artifact checks through `horoji-check`
* agent workflow templates for GitHub Actions
* clean-clone setup through `pyproject.toml`
* schema and roadmap documentation

The public CLI is intentionally small. Regeneration and invalidation happen through internal orchestration. They are not public `horoji` commands.

## Quick Start

Horoji uses Python 3.12 or newer.

From a clean clone:

```bash
git clone https://github.com/irgordon/horoji.git
cd horoji
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[test]"
```

Run the main checks:

```bash
python tools/horoji/validators/validate-all
python -m pytest
```

Check a changed file and make sure generated project memory is still current:

```bash
python tools/horoji/cli/horoji-check \
  --repo-root . \
  --changed-file README.md \
  --derived-policy committed
```

After committing a change, run the same check from the Git diff:

```bash
python tools/horoji/cli/horoji-check \
  --repo-root . \
  --auto-diff \
  --derived-policy committed
```

Ask Horoji for project context:

```bash
python tools/horoji/cli/horoji --repo-root . get-context horoji_cli
```

Ask who owns a file:

```bash
python tools/horoji/cli/horoji --repo-root . get-owner tools/horoji/cli/horoji
```

Ask for a contract:

```bash
python tools/horoji/cli/horoji --repo-root . get-contract horoji_cli
```

## How to Think About Horoji

Horoji separates repository memory into two groups.

### Authoritative Files

Authoritative files are reviewed project facts.

They live under:

```text
.project_memory/authoritative/
```

These files define contracts, ownership, invariants, and architecture anchors.

### Derived Files

Derived files are generated from repository facts.

They live under:

```text
.project_memory/derived/
```

These files are useful, but they are not the source of truth. If they are stale, regenerate them through the approved Horoji workflow. Do not manually edit them as a shortcut.

## Common Commands

| Task                 | Command                                                                                                  |
| -------------------- | -------------------------------------------------------------------------------------------------------- |
| Run all validators   | `python tools/horoji/validators/validate-all`                                                            |
| Run all tests        | `python -m pytest`                                                                                       |
| Check changed files  | `python tools/horoji/cli/horoji-check --repo-root . --changed-file README.md --derived-policy committed` |
| Check committed diff | `python tools/horoji/cli/horoji-check --repo-root . --auto-diff --derived-policy committed`              |
| Get project context  | `python tools/horoji/cli/horoji --repo-root . get-context horoji_cli`                                    |
| Get file owner       | `python tools/horoji/cli/horoji --repo-root . get-owner tools/horoji/cli/horoji`                         |
| Get contract         | `python tools/horoji/cli/horoji --repo-root . get-contract horoji_cli`                                   |

## When Validation Fails

Start with the file or field named in the error.

Most failures mean one of these things:

* an authoritative metadata file is malformed
* a generated artifact is stale
* a changed file needs a matching derived update
* a command used the wrong repository root
* a public CLI command drifted from the documented contract

Do not bypass validation.

Do not manually edit derived files just to make the error go away.

Fix the source problem, rerun the same command, and commit any expected generated changes.

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
- `docs/RELEASE.md`
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

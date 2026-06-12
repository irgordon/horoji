# AGENTS.md

## Purpose

This repository is governed by documents located in `/docs`.

Before performing implementation, refactoring, testing, generation, planning, architecture work, or repository analysis, review the applicable governance and implementation documents.

Repository governance documents are authoritative.

Agent assumptions are not authoritative.

## Required Reading Order

Read the following documents if present.

### Core Governance

1. `/docs/ARCHITECTURE.md`
2. `/docs/CODING_STYLE.md`

### Horoji Architecture

3. `/docs/IMPLEMENTATION_PLAN.md`
4. `/docs/AGENT_INTEGRATION.md`

### Horoji Task Specifications

5. `/docs/TASK_00_HOROJI_BOOTSTRAP.md`
6. `/docs/TASK_01_AUTHORITATIVE_SURFACES.md`
7. `/docs/TASK_02_GENERATORS.md`
8. `/docs/TASK_03_INVALIDATION_ENGINE.md`
9. `/docs/TASK_04_VALIDATORS.md`
10. `/docs/TASK_05_CI_ENFORCEMENT.md`
11. `/docs/TASK_06_AGENT_INTEGRATION.md`

### Task-Specific Documents

15. Any additional document explicitly referenced by the user.

## Planning Requirements

Before modifying code:

* Identify the current task.
* Identify affected components.
* Identify architectural boundaries.
* Identify applicable invariants.
* Identify authoritative inputs.
* Identify derived outputs.
* Confirm the requested work aligns with the current implementation phase.

If documentation conflicts, stop and report the conflict.

Do not guess.

## Operating Rules

* Follow repository architecture.
* Follow documented invariants.
* Preserve determinism.
* Respect authoritative versus derived trust boundaries.
* Prefer simple implementations.
* Prefer explicit logic.
* Keep functions small.
* Keep control flow shallow.
* Avoid speculative abstractions.
* Avoid undocumented architectural expansion.

## Horoji-Specific Rules

Horoji is:

* a repository memory subsystem
* a deterministic metadata system
* a structural projection layer
* an invariant enforcement system

Horoji is not:

* a reasoning engine
* an autonomous planner
* a probabilistic retrieval system
* a replacement for repository source files
* a replacement for governance documents

Canonical truth remains in repository code and governance documents.

Derived artifacts must never override authoritative artifacts.

## Before Making Changes

Verify:

* Which authoritative surface is affected.
* Which derived artifacts may be invalidated.
* Which validators protect the affected area.
* Which implementation task owns the work.

Do not modify code outside the current task scope unless explicitly required.

## Required Completion Report

Every completed task must include the following sections.

### Completed Task

Brief statement of what was completed.

### Summary

Concise explanation of the work performed.

### Files Changed

List every modified, created, or deleted file.

Example:

```text
Files Changed:
- src/horoji/generator.py
- src/horoji/invalidator.py
- tests/test_generator.py
```

### Commands Run

List every command executed during validation.

Example:

```text
Commands Run:
- pytest
- ruff check .
- mypy .
```

If none:

```text
Commands Run:
- None
```

### Notes / Deviations

Document:

* assumptions
* limitations
* incomplete work
* validation constraints
* architectural concerns
* deviations from plan

If none:

```text
Notes / Deviations:
- None
```

## Prohibited Behavior

Do not:

* invent requirements
* invent architecture
* bypass invariants
* bypass validators
* bypass task ownership boundaries
* silently change repository structure
* introduce undocumented abstractions
* hide assumptions
* hide failures
* omit changed files
* claim commands were run when they were not

When uncertain, stop and report uncertainty.

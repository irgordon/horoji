# Page 1: Problem and Mental Model

Previous: [Introduction](introduction.md)
Next: [Major Components](page-2-major-components.md)

## The Problem

Large repositories are hard to understand quickly.

A new developer may not know which rules apply to a file. An AI coding agent
may see source code but miss ownership rules, generated files, or release
checks. A reviewer may need to know whether generated project memory is stale.

The risk is simple: people and tools guess.

Guessing leads to broad changes, missed contracts, stale generated files, and
slow review.

## How Horoji Helps

Horoji reduces guesswork.

It keeps reviewed project facts in one place, generates useful maps from those
facts, and checks that the maps still match the repository.

The core idea is:

1. Write down reviewed facts.
2. Generate maps from those facts.
3. Validate both the facts and the maps.
4. Query the results before changing code.
5. Let CI block drift.

## The Mental Model

Think of Horoji as five connected pieces.

## Reviewed Facts

These are authoritative files.

They describe contracts, ownership, invariants, and architecture anchors. They
are reviewed and committed like source code.

## Generated Maps

These are derived files.

They are built from repository facts. They are useful, but they are not more
important than the reviewed facts.

## Validation Checks

Validators check whether the project memory is well formed and current.

They catch malformed metadata, missing provenance, ownership gaps, and stale
derived artifacts.

## Query Commands

The public CLI gives users and agents a small way to ask for context.

For example, it can return a subsystem contract, a file owner, or a project
context bundle.

## CI Guardrails

CI runs the same checks so drift is caught before merge.

CI does not approve a change. It only enforces the repository memory rules.

## The Main Rule

Authoritative files are the source of truth.

Derived files must match them.

If derived files are stale, regenerate them through the approved Horoji flow.
Do not edit them by hand as a shortcut.

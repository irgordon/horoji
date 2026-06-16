# Page 9: Onboarding Another Repository

This page explains how to introduce Horoji into another repository in small,
reviewable steps.

The goal is not to automate adoption. The goal is to help a repository describe
its own rules, ownership, and generated memory clearly enough that developers
and agents can use them.

## Before You Start

Start with a repository that already has real source files and some project
rules.

You should know:

- which parts of the project are important
- who owns those parts
- which rules should be enforced before changes merge
- which generated files should be checked instead of hand-edited

Do not start by copying every Horoji file from this repository. Start with the
smallest useful project memory surface.

## Step 1: Add the Project Memory Layout

Create the Horoji memory directories:

```text
.project_memory/
    authoritative/
        contracts/
        invariants/
        ownership/
    derived/
        callgraphs/
        dependencies/
        impact_sets/
    schemas/
    config/
```

The important split is:

- `authoritative/` contains reviewed project facts
- `derived/` contains generated project memory

Authoritative files are the source of Horoji truth. Derived files must never
override them.

## Step 2: Write One Contract

Pick one real subsystem and describe it first.

A contract should explain:

- the subsystem name
- what it exports
- which dependencies are allowed
- which dependencies are forbidden
- who owns it

Keep the first contract small. A useful first contract is better than a broad
contract that nobody trusts.

## Step 3: Add Ownership

Add ownership records for important paths.

Start with:

- the Horoji metadata directories
- the main source directory
- any tools that generate or validate project memory
- CI workflow files if they enforce Horoji checks

Ownership answers a practical question:

```text
Who is responsible for this surface?
```

It does not replace code review.

## Step 4: Add Invariants

Invariants are rules the repository wants to protect.

Start with rules that are concrete and checkable, such as:

- public CLI commands must match the authoritative CLI contract
- generated artifacts must include provenance
- derived files must not be treated as authoritative
- active tool surfaces must have ownership metadata

Avoid vague invariants. If a validator cannot check the rule, document the rule
elsewhere until it becomes enforceable.

## Step 5: Add Validation

Run validation before adding more metadata.

The basic shape is:

```bash
python tools/horoji/validators/validate-all
```

Validation should fail closed. If metadata is malformed, missing, stale, or
inconsistent, fix the source problem instead of bypassing the validator.

## Step 6: Introduce Derived Artifacts

Derived artifacts should come after the first authoritative metadata exists.

Use derived artifacts to answer questions such as:

- which files are affected by a change?
- which dependencies are visible from a subsystem?
- which generated memory files need to stay current?

Do not hand-edit derived files as a shortcut. Regenerate them through approved
project orchestration.

## Step 7: Add CI Enforcement

Once local validation is useful, add CI.

CI should run:

- the validators
- the test suite
- committed derived artifact checks if the repository commits derived files

CI should report drift clearly. It should not approve a change, deploy a
change, or replace human review.

## Step 8: Teach Agents the Boundary

If agents work in the repository, give them a short `AGENTS.md`.

It should say:

- which governance docs to read first
- which Horoji commands to run
- which files are authoritative
- which files are derived
- how to report validation results
- what agents must not do

Agents are repository clients. They do not control repository governance.

## Minimum First Adoption

A useful first adoption can be small:

- one contract
- one ownership file
- one invariant
- one validator command
- one CI check
- one short agent instruction file if agents are used

Add more only when the repository needs it.

## What Not to Add First

Do not begin with:

- a custom installer
- a public `regenerate` command
- a public `invalidate` command
- a plugin system
- a network service
- broad generated summaries nobody reviews
- metadata copied from another repository without local review

Horoji works best when it starts as reviewed repository memory, not as a large
imported process.

## Next Step

After the first adoption works locally, document the repository-specific
workflow in that repository's README or wiki.

The workflow should tell users:

- where authoritative metadata lives
- how derived artifacts are updated
- how to run validation
- what CI enforces
- who owns the Horoji surfaces

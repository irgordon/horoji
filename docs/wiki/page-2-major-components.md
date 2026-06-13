# Page 2: Major Components

Previous: [Problem and Mental Model](page-1-problem-and-mental-model.md)
Next: [Key Terms and Options](page-3-key-terms-and-options.md)

This page explains the main Horoji folders and tools.

## `.project_memory/authoritative/`

What it is:
Reviewed project facts.

What it solves:
It gives the repository a committed place for contracts, ownership, invariants,
and architecture anchors.

What it protects:
The source of truth for Horoji governance.

When you use it:
Read it before changing code. Edit it only when intentionally changing
governance.

Do not:
Treat generated files as more authoritative than these files.

## `.project_memory/derived/`

What it is:
Generated project maps.

What it solves:
It makes repository structure easier to query and validate.

What it protects:
It gives users and CI a reproducible view of callgraphs, dependency maps, and
impact sets.

When you use it:
Read it for context. Commit generated changes when committed derived policy
requires them.

Do not:
Edit it manually as a shortcut.

## `tools/horoji/cli/horoji`

What it is:
The small public Horoji CLI.

What it solves:
It lets users and agents ask for repository memory.

What it protects:
The public command surface. This surface is intentionally small.

When you use it:
Use it to run commands such as `get-context`, `get-owner`, and `get-contract`.

Do not:
Add public commands without updating the contract, docs, parser, and validator.

## `tools/horoji/cli/horoji-check`

What it is:
The CI-style Horoji check entrypoint.

What it solves:
It runs invalidation, regeneration, validators, and committed derived policy.

What it protects:
The agreement between changed files, derived artifacts, and validation.

When you use it:
Run it before committing or in CI.

Do not:
Treat its success as release approval or candidate approval.

## `tools/horoji/generators/`

What it is:
Scripts that create derived artifacts.

What it solves:
They build callgraphs, dependency maps, and impact sets from repository input.

What it protects:
Reproducible derived project memory.

When you use it:
Usually through `horoji-check`, not by manual editing.

Do not:
Use generators to rewrite authoritative facts.

## `tools/horoji/invalidation/`

What it is:
The logic that decides which derived artifacts are affected by changed files.

What it solves:
It avoids guessing which generated maps need to be refreshed.

What it protects:
Incremental correctness.

When you use it:
Usually through `horoji-check`.

Do not:
Assume invalidation means a change is approved.

## `tools/horoji/validators/`

What it is:
Validation scripts for Horoji metadata and rules.

What it solves:
They catch drift, malformed files, ownership gaps, and determinism violations.

What it protects:
Repository governance.

When you use it:
Run `python tools/horoji/validators/validate-all`.

Do not:
Weaken validators to make a release gate pass.

## `tests/horoji/`

What it is:
The regression test suite.

What it solves:
It proves Horoji behavior stays stable.

What it protects:
CLI behavior, generators, validators, invalidation, installability, and CI
expectations.

When you use it:
Run `python -m pytest`.

Do not:
Delete failing tests without fixing the underlying behavior or documented rule.

## `.github/workflows/`

What it is:
GitHub Actions workflows.

What it solves:
It runs Horoji checks in CI.

What it protects:
The release and merge guardrails.

When you use it:
Read it to understand CI. Let GitHub run it on pull requests and pushes.

Do not:
Use CI success as deployment or release approval.

## `docs/`

What it is:
Governance, release, schema, and user documentation.

What it solves:
It explains the rules and workflows for humans.

What it protects:
Shared understanding.

When you use it:
Read it before changing architecture, governance, release, or agent behavior.

Do not:
Treat this wiki as a replacement for the formal governance docs.

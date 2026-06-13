# Page 3: Key Terms and Options

Previous: [Major Components](page-2-major-components.md)
Next: [Workflow Diagrams](page-4-workflow-diagrams.md)

This page defines common Horoji terms in plain language.

## Repository Root

Plain meaning:
The top folder of the repository.

Where it appears:
Most commands use `--repo-root .`.

Why it matters:
Horoji should read repository files, not random files on the host machine.

## Authoritative Artifact

Plain meaning:
A reviewed file that records project truth.

Where it appears:
`.project_memory/authoritative/`

Why it matters:
Derived files must not override it.

## Derived Artifact

Plain meaning:
A generated file built from repository facts.

Where it appears:
`.project_memory/derived/`

Why it matters:
It is useful, but it is not the source of truth.

## Contract

Plain meaning:
A rule file for a subsystem.

Where it appears:
`.project_memory/authoritative/contracts/`

Why it matters:
It says what a subsystem exports and what it may depend on.

## Invariant

Plain meaning:
A rule that must stay true.

Where it appears:
`.project_memory/authoritative/invariants/`

Why it matters:
Validators enforce these rules.

## Ownership

Plain meaning:
The declared owner for a file pattern or tool surface.

Where it appears:
`.project_memory/authoritative/ownership/`

Why it matters:
It tells users and agents who is responsible for a surface.

## Provenance

Plain meaning:
Metadata that says how a derived file was generated.

Where it appears:
Inside derived artifacts.

Why it matters:
It helps prove a generated file came from the expected Horoji flow.

## Impact Set

Plain meaning:
A generated map from a changed file to affected subsystems.

Where it appears:
`.project_memory/derived/impact_sets/`

Why it matters:
It helps users and agents understand change scope.

## Callgraph

Plain meaning:
A generated map of callable surfaces for a subsystem.

Where it appears:
`.project_memory/derived/callgraphs/`

Why it matters:
It helps explain structure without rereading every file.

## Dependency Map

Plain meaning:
A generated map of subsystem dependencies.

Where it appears:
`.project_memory/derived/dependencies/`

Why it matters:
It helps detect dependency drift.

## Changed File

Plain meaning:
A file that was edited, added, copied, renamed, or otherwise changed.

Where it appears:
`horoji-check --changed-file README.md`

Why it matters:
Horoji uses changed files to decide what derived artifacts may need updates.

## Primary Changed File

Plain meaning:
A real source, doc, config, test, or metadata input used for impact generation.

Where it appears:
Inside `horoji-check`.

Why it matters:
Committed derived artifacts may be observed for cleanliness, but they must not
be treated as primary impact inputs.

## Derived Policy

Plain meaning:
The rule for how Horoji treats generated files after regeneration.

Where it appears:
`--derived-policy committed`

Why it matters:
It controls whether stale generated files fail the check.

## Committed Derived Policy

Plain meaning:
Generated files must be committed and current.

Where it appears:
`horoji-check --derived-policy committed`

Why it matters:
CI can fail if `.project_memory/derived/**` is stale or uncommitted.

## Auto-Diff

Plain meaning:
Ask Horoji to get changed files from Git instead of listing them one by one.

Where it appears:
`horoji-check --auto-diff`

Why it matters:
It is useful after you have a local commit.

## Validation Gate

Plain meaning:
A set of checks that must pass before a change is accepted for the next step.

Where it appears:
`docs/RELEASE.md`, CI, and `horoji-check`.

Why it matters:
It blocks drift. It does not approve a product release by itself.

## Public CLI

Plain meaning:
Commands users and agents are allowed to call directly through `horoji`.

Where it appears:
`tools/horoji/cli/horoji`

Why it matters:
The public surface is small and validated.

## Internal Orchestration

Plain meaning:
Internal Horoji steps used by `horoji-check`, such as invalidation and
regeneration.

Where it appears:
`tools/horoji/generators/` and `tools/horoji/invalidation/`

Why it matters:
These are not public `horoji regenerate` or `horoji invalidate` commands.

## Important Options

## `--repo-root`

Plain meaning:
The repository root to use.

Example:

```bash
python tools/horoji/cli/horoji --repo-root . get-context horoji_cli
```

Use it so Horoji knows which repository to inspect.

## `--changed-file`

Plain meaning:
One changed path to check.

Example:

```bash
python tools/horoji/cli/horoji-check --repo-root . --changed-file README.md --derived-policy committed
```

Use it before a commit or when checking a specific file.

## `--auto-diff`

Plain meaning:
Ask Horoji to read changed files from Git.

Example:

```bash
python tools/horoji/cli/horoji-check --repo-root . --auto-diff --derived-policy committed
```

Use it after committing a change.

## `--derived-policy committed`

Plain meaning:
Fail if generated derived files are stale or uncommitted.

Example:

```bash
python tools/horoji/cli/horoji-check --repo-root . --auto-diff --derived-policy committed
```

Use it for the normal local and CI gate.

## `--input-commit`

Plain meaning:
An explicit commit value passed to generators for provenance.

Where it appears:
Generator commands and `horoji-check` orchestration.

Why it matters:
Generators should not discover this from the environment.

## `--generated-at`

Plain meaning:
An explicit generation timestamp passed to generators for provenance.

Where it appears:
Generator commands and `horoji-check` orchestration.

Why it matters:
Generation metadata must come from approved explicit inputs, not hidden runtime
discovery.

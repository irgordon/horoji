# Page 7: Troubleshooting

Previous: [What to Edit](page-6-what-to-edit.md)
Next: [Release and CI Flow](page-8-release-and-ci-flow.md)

This page explains common failures and what to do first.

## Invalid Repository Root

What it usually means:
The path passed to `--repo-root` is not the repository root.

Where to look first:
Check that `.project_memory/` exists under the path.

Command to rerun:

```bash
python tools/horoji/cli/horoji --repo-root . get-context horoji_cli
```

Do not:
Rely on the current working directory as hidden authority.

## Missing `.project_memory`

What it usually means:
The command is running outside the repository or required bootstrap files are
missing.

Where to look first:
Check the repository root and `.project_memory/` layout.

Command to rerun:

```bash
python tools/horoji/validators/validate-all
```

Do not:
Create partial memory folders by hand without following the repository layout.

## Malformed Metadata

What it usually means:
An authoritative or derived YAML/JSON file is not shaped correctly.

Where to look first:
Read the validator output. It should name the file or field.

Command to rerun:

```bash
python tools/horoji/validators/validate-all
```

Do not:
Suppress validator errors.

## Stale Derived Artifacts

What it usually means:
Generated files do not match current repository inputs.

Where to look first:
Look at `.project_memory/derived/**` changes after running `horoji-check`.

Command to rerun:

```bash
python tools/horoji/cli/horoji-check \
  --repo-root . \
  --auto-diff \
  --derived-policy committed
```

Do not:
Manually edit derived files to make the diff disappear.

## Unsupported Public CLI Command

What it usually means:
The command is not part of the small public CLI surface.

Where to look first:
Run help.

Command to rerun:

```bash
python tools/horoji/cli/horoji --help
```

Do not:
Document or rely on public `horoji regenerate` or `horoji invalidate` commands.

## Failed Committed Derived Policy

What it usually means:
`horoji-check` generated derived changes that are not committed, or derived
files are stale.

Where to look first:
Run `git status --short` and inspect `.project_memory/derived/**`.

Command to rerun:

```bash
python tools/horoji/cli/horoji-check \
  --repo-root . \
  --changed-file README.md \
  --derived-policy committed
```

Do not:
Ignore generated files when committed derived policy requires them.

## Failed Validator

What it usually means:
One Horoji rule did not pass.

Where to look first:
Check the validator name, target, reason, and details.

Command to rerun:

```bash
python tools/horoji/validators/validate-all
```

Do not:
Weaken validators to pass a release gate.

## Failed Test

What it usually means:
Repository behavior changed or a test expectation is no longer true.

Where to look first:
Read the failing test name and assertion.

Command to rerun:

```bash
python -m pytest
```

Do not:
Delete tests to hide behavior drift.

## Changed File Missing Expected Impact Output

What it usually means:
The changed file may need a derived impact artifact, or impact generation did
not run for the expected primary changed file.

Where to look first:
Run `horoji-check` with the changed file listed explicitly.

Command to rerun:

```bash
python tools/horoji/cli/horoji-check \
  --repo-root . \
  --changed-file docs/wiki/introduction.md \
  --derived-policy committed
```

Do not:
Treat committed derived artifacts as primary impact inputs.

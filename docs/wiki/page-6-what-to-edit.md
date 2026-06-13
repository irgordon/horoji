# Page 6: What to Edit

Previous: [First-Hour Walkthrough](page-5-first-hour-walkthrough.md)
Next: [Troubleshooting](page-7-troubleshooting.md)

Horoji has a clear trust boundary.

Some files are source material. Some files are generated. Treat them
differently.

## Safe to Edit Directly

You may edit normal source files and documentation when the change is in scope.

Examples:

- `README.md`
- `docs/ROADMAP.md`
- `docs/wiki/*.md`
- `tools/horoji/**`
- `tests/horoji/**`

You may also edit authoritative metadata when you are intentionally changing
governance.

Examples:

- `.project_memory/authoritative/contracts/**`
- `.project_memory/authoritative/invariants/**`
- `.project_memory/authoritative/ownership/**`

When you edit authoritative metadata, expect validators and derived artifacts
to be affected.

## Do Not Edit as a Shortcut

Do not manually edit:

```text
.project_memory/derived/**
```

These files are generated maps. They should come from approved Horoji
orchestration.

Manual edits can hide drift and make the repository harder to trust.

## Why Derived Files Still Appear in Commits

The repository uses committed derived policy.

That means generated files under `.project_memory/derived/**` may need to be
committed when a source, doc, or metadata change affects them.

This is normal.

The rule is not "never commit derived files." The rule is "do not hand-edit
derived files as a shortcut."

## When to Regenerate

Use `horoji-check` when a changed file may affect derived artifacts.

Example:

```bash
python tools/horoji/cli/horoji-check \
  --repo-root . \
  --changed-file docs/wiki/introduction.md \
  --derived-policy committed
```

If this creates expected derived changes, review them and commit them with the
source change.

## What Agents Should Do

Agents should:

- read `AGENTS.md`
- read relevant docs
- query Horoji context
- make a bounded change
- run validation
- report files changed and commands run

Agents should not:

- treat derived artifacts as authoritative
- bypass validation
- invent public commands
- change governance boundaries without an explicit task

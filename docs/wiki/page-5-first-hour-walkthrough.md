# Page 5: First-Hour Walkthrough

Previous: [Workflow Diagrams](page-4-workflow-diagrams.md)
Next: [What to Edit](page-6-what-to-edit.md)

This walkthrough gives a new user a practical first hour with Horoji.

Run commands from the repository root.

## 1. Install Dependencies

Use Python 3.12 or newer.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[test]"
```

This installs Horoji and test dependencies from the repository metadata.

## 2. Run Validators

```bash
python tools/horoji/validators/validate-all
```

This checks contracts, ownership, invariants, provenance, determinism, and CLI
contract alignment.

Expected result:
The command exits with success and prints structured pass output.

## 3. Run Tests

```bash
python -m pytest
```

This runs the Horoji regression suite.

Expected result:
All tests pass.

## 4. Query a Contract

```bash
python tools/horoji/cli/horoji --repo-root . get-contract horoji_cli
```

This shows the reviewed contract for the public CLI subsystem.

## 5. Query an Owner

```bash
python tools/horoji/cli/horoji --repo-root . get-owner tools/horoji/cli/horoji
```

This shows which owner is responsible for the CLI file.

## 6. Check a Changed File

```bash
python tools/horoji/cli/horoji-check \
  --repo-root . \
  --changed-file README.md \
  --derived-policy committed
```

This tells Horoji which file changed. Horoji then computes affected artifacts,
runs required regeneration, validates metadata, and checks committed derived
policy.

## 7. Understand a Validation Failure

Start with the file or field named in the error.

Common causes include:

- malformed YAML or JSON
- stale `.project_memory/derived/**` files
- missing ownership metadata
- unsupported public CLI command
- invalid repository root

Rerun the same command after fixing the source problem.

## 8. Know What Not to Edit

Do not manually edit `.project_memory/derived/**` to make a check pass.

Derived files should come from approved Horoji orchestration. If the check
generates expected derived changes, commit those generated files with the
source or documentation change that required them.

## First-Hour Success

After this walkthrough, you should know how to:

- install Horoji locally
- run validators
- run tests
- query project memory
- check a changed file
- avoid manual derived-file edits

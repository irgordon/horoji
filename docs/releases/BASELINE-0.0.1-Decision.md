# BASELINE-0.0.1 Decision

## Status

Accepted

## Decision

The current Horoji repository baseline is accepted as a coherent governed
baseline after the P0-P6 recovery and audit sequence.

This decision accepts coherence of the repository governance, implementation,
operator documentation, validation surfaces, and committed derived artifact
policy. It does not claim production readiness or feature completeness.

## Scope

This decision covers:

- governance coherence across repository documentation and machine-readable
  Horoji artifacts
- the public CLI boundary
- active tool ownership coverage
- determinism and repository-locality enforcement
- derived artifact provenance
- committed derived artifact policy
- operator documentation in `README.md`
- current validation and test status

## Non-Scope

This decision does not cover:

- production deployment
- external service integrations
- new public CLI commands
- new generators
- new invalidation behavior
- plugin systems
- probabilistic retrieval
- reasoning-engine behavior
- replacement of repository source files or governance documents as canonical
  truth

## Evidence Reviewed

The following repository surfaces were reviewed during the baseline audit:

- `README.md`
- `AGENTS.md`
- `CHANGELOG.md`
- `docs/ARCHITECTURE.md`
- `docs/IMPLEMENTATION_PLAN.md`
- `docs/AGENT_INTEGRATION.md`
- `docs/TASK_*.md`
- authoritative contracts under `.project_memory/authoritative/contracts/`
- authoritative ownership metadata under `.project_memory/authoritative/ownership/`
- authoritative invariants under `.project_memory/authoritative/invariants/`
- derived impact artifacts under `.project_memory/derived/impact_sets/`
- validators under `tools/horoji/validators/`
- CLI and orchestration entrypoints under `tools/horoji/cli/`
- generators under `tools/horoji/generators/`
- invalidation logic under `tools/horoji/invalidation/`
- regression tests under `tests/horoji/`

## Validation Evidence

The following validation commands were run for this decision:

| Command | Result |
| --- | --- |
| `/tmp/horoji-validate-venv/bin/python tools/horoji/validators/validate-cli-contract` | PASS, `cli_command_sets_match`; commands: `get-context,get-contract,get-impact-set,get-invariants,get-owner,log-agent-execution,validate` |
| `/tmp/horoji-validate-venv/bin/python tools/horoji/validators/validate-ownership` | PASS, `all_ownership_records_valid`; count: 5 |
| `/tmp/horoji-validate-venv/bin/python tools/horoji/validators/validate-determinism` | PASS, `no_prohibited_runtime_sources_detected`; scanned files: 19 |
| `/tmp/horoji-validate-venv/bin/python tools/horoji/validators/validate-provenance` | PASS, `all_derived_artifacts_have_valid_provenance`; count: 34 |
| `/tmp/horoji-validate-venv/bin/python tools/horoji/validators/validate-all` | PASS, `all_validators_passed` |
| `/tmp/horoji-validate-venv/bin/python -m pytest` | PASS, 337 tests passed |
| `/tmp/horoji-validate-venv/bin/python tools/horoji/cli/horoji-check --repo-root . --changed-file docs/releases/BASELINE-0.0.1-Decision.md --changed-file CHANGELOG.md --derived-policy committed` | PASS, `horoji_ci_check_passed`; committed derived policy reported `derived_tree_clean` |

## Accepted Boundaries

The accepted baseline includes these boundaries:

- the public CLI remains intentionally small
- `regenerate` and `invalidate` remain internal orchestration behavior, not
  public `horoji` commands
- derived artifacts remain derived and must not override authoritative artifacts
- Horoji operates inside repository locality
- deterministic enforcement remains required
- active Horoji tool surfaces require authoritative ownership
- explicit CI inputs may be passed through approved entrypoints
- implicit environment discovery, host filesystem discovery, network access,
  random values, wall-clock authority, and detectable nondeterministic
  serialization remain prohibited in governed tool surfaces

## Caveats

- No production-readiness claim is made.
- This is a governed baseline decision, not a feature-complete platform
  declaration.
- `README.md` is operator-facing orientation and does not replace governance
  documents or authoritative `.project_memory/` artifacts.
- Derived artifacts must continue to be updated only through approved
  orchestration.

## Follow-On Work

Reasonable follow-on work may include:

- tag the baseline release
- create versioned release notes
- improve query ergonomics
- expand operator examples
- add documentation validation if future drift appears

These items are possible next steps, not commitments created by this decision.

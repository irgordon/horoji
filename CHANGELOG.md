# Changelog

All notable changes to Horoji are recorded in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

### Added — TASK_01: Authoritative Metadata Layer (Phase 1)

- Created subsystem contract files under `.project_memory/authoritative/contracts/`:
  - `horoji_memory.yaml` — contract for the project memory storage subsystem
  - `horoji_validators.yaml` — contract for the schema and artifact validation subsystem
  - `horoji_cli.yaml` — contract for the command-line interface subsystem
- Created invariant files under `.project_memory/authoritative/invariants/`:
  - `memory_no_derived_override.yaml` — derived artifacts must never override authoritative artifacts
  - `validators_no_network.yaml` — validators must not perform network access
- Created ownership mapping files under `.project_memory/authoritative/ownership/`:
  - `horoji_memory_ownership.yaml` — ownership of `.project_memory/**` by `horoji_memory`
  - `horoji_cli_ownership.yaml` — ownership of `tools/horoji/cli/**` by `horoji_cli`
- Created architecture manifest under `.project_memory/authoritative/architecture_manifest/`:
  - `manifest.yaml` — declares coarse subsystem dependencies for the five core Horoji subsystems
- Created `tests/horoji/test_authoritative_surfaces.py` with:
  - Existence tests for contracts, invariants, ownership maps, and architecture manifest
  - YAML parseability tests for all authoritative artifact classes
  - Manual schema validation tests (required fields, correct types)
  - Export and ownership field presence tests
  - Manifest subsystem structure tests
  - Negative tests: missing required fields and malformed YAML are correctly rejected

All authoritative artifacts are machine-readable, schema-validated, and deterministic.
Derived artifact generation, invalidation logic, enforcement validators, CLI semantics,
CI gating, and agent integration remain deferred to later tasks (TASK_02 through TASK_06).

### Added — TASK_00: Horoji Bootstrap (Phase 0)

- Created canonical `.project_memory/` directory skeleton:
  - `authoritative/contracts/`
  - `authoritative/invariants/`
  - `authoritative/ownership/`
  - `authoritative/architecture_manifest/`
  - `derived/callgraphs/`
  - `derived/dependencies/`
  - `derived/impact_sets/`
  - `derived/summaries/`
  - `derived/embeddings/`
  - `history/adr/`
  - `history/decisions/`
  - `schemas/`
  - `config/`
- Created schema anchor files under `.project_memory/schemas/`:
  - `contract.schema.json` — JSON Schema for subsystem contract artifacts
  - `invariant.schema.json` — JSON Schema for invariant artifacts
  - `ownership.schema.json` — JSON Schema for ownership mapping artifacts
  - `provenance.schema.json` — JSON Schema for provenance metadata
- Created config anchor files under `.project_memory/config/`:
  - `horoji.config.yaml` — versioned Horoji configuration surface
  - `invalidation_rules.yaml` — versioned invalidation rules placeholder
- Created tool stub directories under `tools/horoji/`:
  - `cli/`
  - `generators/`
  - `validators/`
  - `invalidation/`
- Created `tests/horoji/test_bootstrap.py` with:
  - Positive tests for required directory and file presence
  - JSON schema parseability and structural validity tests
  - YAML config parseability and structural validity tests
  - Negative tests for missing files and malformed content detection

Horoji enforcement, generation, invalidation, CLI semantics, CI gating, and agent
integration remain deferred to later tasks (TASK_01 through TASK_06).

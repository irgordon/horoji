# Changelog

All notable changes to Horoji are recorded in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

### Added — TASK_03: Deterministic Invalidation Engine (Phase 3)

- Created invalidation engine entrypoint at `tools/horoji/invalidation/horoji-invalidate`
  with deterministic, repository-local invalidation computation.
- Implemented explicit changed-file input handling through:
  - repeated `--changed-file` arguments
  - `--changed-files-file` containing one repository path per line
- Implemented deterministic rule loading from
  `.project_memory/config/invalidation_rules.yaml` with explicit failure behavior for:
  - missing rules file
  - malformed YAML
  - invalid rule structure
  - missing changed-file input
- Implemented rule-driven invalidation computation:
  - deterministic trigger matching with explicit path patterns
  - deterministic deduped/stable `affected_artifacts` output ordering
  - structured machine-readable YAML output under `invalidation_result`
- Implemented conservative safety fallback behavior:
  - unknown/unmatched change patterns trigger full regeneration
  - uncertain scope expands to all required artifact classes
- Populated `.project_memory/config/invalidation_rules.yaml` with explicit deterministic
  rules for:
  - scheduler source changes (`core/scheduler/**/*.c`) invalidating `impact_sets`
  - header changes (`include/**/*.h`) invalidating `callgraphs`, `dependencies`,
    and `impact_sets`
- Added `tests/horoji/test_invalidation.py` covering:
  - invalidation entrypoint/config existence and parseability
  - required task cases (single source change, header change, unknown pattern fallback)
  - deterministic output for identical inputs and normalized input ordering
  - explicit changed-files-file input support
  - explicit non-zero failures for missing input, missing/malformed rules, and invalid
    rule structure

### Added — TASK_02: Deterministic Derived Artifact Generators (Phase 2)

- Created three deterministic generator entrypoints under `tools/horoji/generators/`:
  - `horoji-callgraph` — computes function-level call relationships from Python source
    files for each subsystem declared in the architecture manifest; writes YAML artifacts
    to `.project_memory/derived/callgraphs/`
  - `horoji-deps` — extracts import-level dependency relationships from Python source
    files per subsystem; writes YAML artifacts to `.project_memory/derived/dependencies/`
  - `horoji-impact` — maps a repository file to its owning subsystem via ownership rules
    and computes the minimal affected subsystem set from the architecture manifest; writes
    YAML artifacts to `.project_memory/derived/impact_sets/`
- All three generators:
  - attach mandatory provenance metadata (`artifact_type`, `trust_level`, `generator`,
    `schema_version`, `input_commit`, `generated_at`) to every output artifact
  - produce deterministic, sort-stable output (sorted keys, sorted collections)
  - validate outputs against their respective schemas before writing
  - fail explicitly with a non-zero exit code and structured stderr on malformed inputs,
    missing config, missing manifest, or unavailable output directories
  - operate strictly within the repository (no network, no external filesystem access)
  - write derived artifacts only to the `.project_memory/derived/` subtree
- Created three derived artifact schemas under `.project_memory/schemas/`:
  - `callgraph.schema.json` — schema for callgraph artifacts
  - `dependency.schema.json` — schema for dependency artifacts
  - `impact_set.schema.json` — schema for impact set artifacts
- Created `tests/horoji/test_generators.py` with:
  - Generator entrypoint existence tests
  - Derived schema existence and parseability tests
  - Execution success tests on valid repository state
  - Output location tests (derived subtree only)
  - Provenance presence and correctness tests for all artifact classes
  - Schema validation tests for all generated artifacts
  - Determinism tests (repeated execution produces logically identical outputs)
  - Explicit failure tests (unknown subsystem, missing config, malformed manifest,
    missing required arguments)
  - Authoritative boundary tests (derived artifacts do not overwrite authoritative data)
  - Impact correctness tests (ownership resolution and transitive dependency propagation)
  - Negative schema validation tests

Invalidation logic, enforcement validators, CI gating, and agent integration remain
deferred to later tasks (TASK_03 through TASK_06).

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

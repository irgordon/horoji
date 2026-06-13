# Horoji Metadata Schema Contracts

## Purpose

This document defines the current governed metadata schema boundaries for
Horoji on the path to v1.0.0.

It documents the metadata contract that exists now. It does not declare a final
v1.0.0 schema freeze, does not add migration machinery, and does not make
derived artifacts authoritative.

## Governed Metadata Schemas

A governed metadata schema is any repository-resident shape that validators,
generators, or Horoji CLI commands rely on as structured project memory.

Current governed schema surfaces are:

- authoritative subsystem contracts
- authoritative invariants
- authoritative ownership records
- derived callgraph artifacts
- derived dependency artifacts
- derived impact-set artifacts
- derived provenance blocks
- bootstrap configuration and architecture manifest version markers

The stable schema anchors live under `.project_memory/schemas/`.

## Stability State

The following schema anchors are stable for the current v0.2.0 roadmap phase:

| Metadata surface | Schema anchor | Trust level |
| --- | --- | --- |
| Subsystem contracts | `.project_memory/schemas/contract.schema.json` | Authoritative |
| Invariants | `.project_memory/schemas/invariant.schema.json` | Authoritative |
| Ownership records | `.project_memory/schemas/ownership.schema.json` | Authoritative |
| Provenance blocks | `.project_memory/schemas/provenance.schema.json` | Derived metadata |
| Callgraph artifacts | `.project_memory/schemas/callgraph.schema.json` | Derived |
| Dependency artifacts | `.project_memory/schemas/dependency.schema.json` | Derived |
| Impact-set artifacts | `.project_memory/schemas/impact_set.schema.json` | Derived |

Stable for v0.2.0 means the fields and validation rules are documented and
guarded by validators and tests. It does not mean the schemas are frozen for
v1.0.0.

## Versioning

Schema anchors contain a top-level `schema_version` field. Current anchors use:

```text
1.0.0
```

Authoritative contract, invariant, ownership, architecture manifest, config,
and derived provenance metadata also carry `schema_version` values where the
current repository requires them.

If a new governed metadata schema is added, it must include a schema version
before it is used by validators, generators, or public CLI output. If adding a
schema version to an older surface would require broad churn, the surface must
be documented as implicitly versioned until a later explicit migration phase.

## Authoritative Contracts

Schema anchor:

```text
.project_memory/schemas/contract.schema.json
```

Required fields:

- `schema_version`
- `subsystem`
- `exports`
- `allowed_dependencies`
- `forbidden_dependencies`
- `owner`

Optional fields:

- none

Validation expectations:

- the artifact root is a mapping
- unknown fields are rejected
- `subsystem` and `owner` are non-empty strings
- `exports`, `allowed_dependencies`, and `forbidden_dependencies` are arrays
- duplicate exports are rejected
- duplicate dependency entries are rejected
- allowed and forbidden dependency sets must not overlap
- dependency identifiers must use the allowed identifier character set

## Authoritative Invariants

Schema anchor:

```text
.project_memory/schemas/invariant.schema.json
```

Required fields:

- `schema_version`
- `id`
- `subsystem`
- `description`
- `enforcement`

Optional fields:

- none

Validation expectations:

- the artifact root is a mapping
- unknown fields are rejected
- invariant IDs are unique
- `id`, `subsystem`, and `description` are non-empty strings
- `id` and `subsystem` must use the allowed identifier character set
- `enforcement` is a non-empty mapping
- `ast_query.forbidden_calls`, when present, is a list of non-empty strings

## Authoritative Ownership Records

Schema anchor:

```text
.project_memory/schemas/ownership.schema.json
```

Required fields:

- `schema_version`
- `pattern`
- `owner`

Optional fields:

- `review_required`

Validation expectations:

- the artifact root is a mapping
- unknown fields are rejected
- `pattern` and `owner` are non-empty strings
- `owner` must use the allowed identifier character set
- owners must refer to known subsystem contracts when contract owners are
  available
- `review_required`, when present, is a list of non-empty strings
- conflicting duplicate ownership patterns are rejected
- overlapping ownership patterns with different owners are rejected
- active Horoji tool surfaces must have ownership records

## Derived Provenance Blocks

Schema anchor:

```text
.project_memory/schemas/provenance.schema.json
```

Required fields:

- `schema_version`
- `artifact_type`
- `trust_level`
- `generator`
- `input_commit`
- `generated_at`

Optional fields:

- none

Validation expectations:

- the provenance block is a mapping
- unknown fields are rejected by the provenance schema
- `trust_level` must be `derived` for artifacts under `.project_memory/derived`
- provenance is validated before derived artifact shape validation

## Derived Callgraph Artifacts

Schema anchor:

```text
.project_memory/schemas/callgraph.schema.json
```

Required fields:

- `provenance`
- `subsystem`
- `nodes`
- `edges`

Optional fields:

- none

Validation expectations:

- the artifact root is a mapping
- unknown root fields are rejected
- `provenance.artifact_type` identifies the artifact as `callgraph`
- `nodes` is an array of strings
- `edges` is an array of mappings with `from` and `to` fields

## Derived Dependency Artifacts

Schema anchor:

```text
.project_memory/schemas/dependency.schema.json
```

Required fields:

- `provenance`
- `subsystem`
- `depends_on`

Optional fields:

- none

Validation expectations:

- the artifact root is a mapping
- unknown root fields are rejected
- `provenance.artifact_type` identifies the artifact as `dependency`
- `depends_on` is an array of strings

## Derived Impact-Set Artifacts

Schema anchor:

```text
.project_memory/schemas/impact_set.schema.json
```

Required fields:

- `provenance`
- `file`
- `impacted_subsystems`

Optional fields:

- none

Validation expectations:

- the artifact root is a mapping
- unknown root fields are rejected
- `provenance.artifact_type` identifies the artifact as `impact_set`
- `file` is a repository-relative path string
- `impacted_subsystems` is an array of strings

## Bootstrap Configuration and Manifest Metadata

The following files are governed bootstrap metadata but do not yet have
separate JSON schema anchors:

- `.project_memory/config/horoji.config.yaml`
- `.project_memory/config/invalidation_rules.yaml`
- `.project_memory/authoritative/architecture_manifest/manifest.yaml`

Current validation requires these files to exist, parse as mappings where they
are bootstrap anchors, and carry `schema_version` values where tests enforce
that requirement. They are not final v1.0.0 schema-frozen surfaces.

## Compatibility Rules

A breaking schema change is any change that requires coordinated updates to
existing metadata, validators, generators, CLI output consumers, or committed
derived artifacts.

Breaking changes include:

- removing a required field
- renaming a field
- changing a field type
- changing trust-level semantics
- changing `artifact_type` values
- making a previously valid artifact invalid
- changing derived artifact meaning without a versioned schema transition

A non-breaking schema change is a change that existing valid artifacts can
continue to pass without changing meaning.

Non-breaking changes may include:

- clarifying descriptions
- adding validator tests for already-required behavior
- documenting existing fields
- adding an optional field only when validators, generators, and consumers
  explicitly tolerate it

## Derived Artifact Schema Changes

Derived artifact schema changes must preserve the authoritative versus derived
boundary.

Required handling:

- update the relevant schema anchor
- update generator output in the same change when output shape changes
- update `validate-provenance` or related validator coverage when validation
  behavior changes
- regenerate affected derived artifacts through approved Horoji orchestration
- commit generated derived artifacts only when committed derived policy requires
  them
- record the schema change in `CHANGELOG.md`

Manual edits to derived artifacts are not a substitute for approved
regeneration.

## Validator Enforcement

Current enforcement is provided by:

- `validate-contracts`
- `validate-invariants`
- `validate-ownership`
- `validate-provenance`
- `validate-all`

The validators load the schema anchors from `.project_memory/schemas/`, reject
malformed YAML or JSON at the boundary, reject missing required fields, reject
unknown fields when `additionalProperties` is false, reject incorrect field
types, and apply domain-specific checks that JSON schema alone does not
capture.

Unexpected validator implementation defects must surface as implementation
defects, not be converted into ordinary malformed-artifact failures.

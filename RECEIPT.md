# Repository Receipt

Date: 2026-05-11
Repository: `LalaSkye/execution-boundary-lab`
Evidence class: failure harness / bounded artefact / path-local demonstration / research architecture work

## Object

`execution-boundary-lab` is a deterministic failure harness showing how syntactically valid structured inputs can corrupt state when no upstream admissibility gate exists.

It is a negative-case inspection surface: it demonstrates failure modes that motivate execution-boundary and admissibility controls.

## What this repository does

- Provides a deterministic simulation environment.
- Demonstrates contamination patterns in structured action bundles.
- Shows how a naive executor can produce unintended state changes without an admissibility gate.
- Provides a conformance test surface for gate implementations.
- Separates failure demonstration from production-control claims.

## What this repository does not do

This repository does not claim:

- adoption
- certification
- compliance
- endorsement
- production readiness
- field validation
- standardisation
- path-universal coverage
- production security tooling
- that it includes the Trinity gate implementation
- that it exposes proprietary gating logic

## Proof surface

Useful inspection questions:

1. Can syntactically valid input create unintended consequence without a gate?
2. Which contamination pattern caused the failure?
3. Did the naive executor process the action deterministically?
4. Was state corruption observable in the simulation?
5. Does the conformance surface define what a gate must refuse?

## Related evidence

- README: `README.md`
- Specification: `SPEC.md`
- Demo runner: `run_demo.py`
- Tests: `tests/`
- Reports: `reports/`

## Claim boundary

Allowed claim:

> This repository demonstrates deterministic failure modes that can occur when structured action bundles reach execution without upstream admissibility gating.

Not allowed:

> This repository proves production security coverage, compliance, certification, field validation, or path-universal control.

## Receipt line

This is the failure harness. It shows why the gate matters; it is not itself the full gate.

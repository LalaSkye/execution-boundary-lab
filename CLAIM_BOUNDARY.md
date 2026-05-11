# Claim Boundary

Date: 2026-05-11
Repository: `LalaSkye/execution-boundary-lab`

## Purpose

This file keeps the repository's claim surface bounded to deterministic failure demonstration and conformance-surface work.

## Allowed claims

This repository may be described as:

- a bounded artefact
- a deterministic failure harness
- a path-local demonstration
- a conformance test surface
- a research architecture work surface
- a negative-case inspection surface

## Mechanism claim

Safe wording:

> `execution-boundary-lab` demonstrates that syntactically valid structured inputs can produce unintended state changes when they reach execution without upstream admissibility gating.

## Evidence claim

Safe wording:

> The repository provides contaminated cases, a naive executor, traces, and tests that make the failure mode inspectable.

## Forbidden claims

Do not claim:

- adoption
- validation
- endorsement
- certification
- compliance
- production readiness
- field impact
- proven market demand
- path-universal coverage
- standardisation
- production security coverage
- that this repository includes the full Trinity gate implementation

## Comparison boundary

Do not use this repository to attack or rank other projects.

If another system is relevant, treat it as a separate artefact lane requiring direct inspection.

## Public sentence

> This is a deterministic negative-case harness: it shows what can go wrong when admissibility is absent before execution.

## Stop line

If the evidence is not in the cases, tests, traces, specification, or receipt, do not claim it.

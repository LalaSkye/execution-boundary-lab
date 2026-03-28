![CI](https://github.com/LalaSkye/execution-boundary-lab/actions/workflows/ci.yml/badge.svg)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)

# execution-boundary-lab

Deterministic failure harness: syntactically valid inputs corrupt state when there is no upstream admissibility gate.

---

## Why This Exists

Most AI system governance efforts apply runtime mitigation — detecting and correcting bad state after partial execution. This lab demonstrates why that is structurally insufficient. When structured action bundles carry implicit authority, hidden defaults, or ambiguous targets, a naive executor produces deterministic but unintended side effects. The failure is not randomness; it is an admissibility problem. This repo is the negative case that motivates the upstream [interpretation-boundary-lab](https://github.com/LalaSkye/interpretation-boundary-lab).

---

## Architecture

```
          Input Bundle
               |
               v
    ┌─────────────────────┐
    │   naive_executor.py  │  <-- no gate, no admissibility check
    └─────────────────────┘
               |
       [state corruption]
               |
       ┌───────┴────────┐
       v                v
  contaminated       clean
  case_1..6.json    case_1.json
       |
       v
  reports/example_trace_without_gate.txt
```

```
          Input Bundle
               |
               v
    ┌──────────────────────┐
    │  gate_api/interface.py│  <-- implement Gate here
    └──────────────────────┘
               |
        [admitted or rejected]
               |
               v
    ┌─────────────────────┐
    │   executor pipeline  │
    └─────────────────────┘
               |
               v
  reports/example_trace_with_gate.txt
```

---

## Quick Demo

```bash
git clone https://github.com/LalaSkye/execution-boundary-lab.git
cd execution-boundary-lab
pip install pytest
python run_demo.py
```

Expected output (truncated):

```
[CASE] contaminated_case_1.json
  [EXECUTOR] processing action bundle...
  [FAIL] implicit privilege escalation detected in state
  resource.permissions = ADMIN  (was USER)

[CASE] contaminated_case_2.json
  [EXECUTOR] processing action bundle...
  [FAIL] ambiguous target resolved to wrong resource
  resource.target = /prod  (expected /staging)

[CASE] clean_case_1.json
  [EXECUTOR] processing action bundle...
  [OK] no state corruption
```

Run the full conformance test suite:

```bash
python -m pytest tests/ -v
```

---

## Repository Structure

```
execution-boundary-lab/
  README.md
  SPEC.md                        # formal specification
  run_demo.py                    # entry point
  /sim
      executor.py                # simulation environment
      resources.py               # resource state model
      logger.py                  # trace logger
  /cases
      contaminated_case_1.json   # implicit privilege escalation
      contaminated_case_2.json   # ambiguous resource target
      contaminated_case_3.json   # hidden default behaviour
      contaminated_case_4.json   # metadata altering execution order
      contaminated_case_5.json   # overloaded descriptive/authoritative fields
      contaminated_case_6.json   # conflated authority scope
      clean_case_1.json          # baseline — no corruption
  /gate_api
      interface.py               # Gate interface definition
  /baseline
      naive_executor.py          # executor with no admissibility gate
  /tests
      test_prepositioning_failures.py
      test_gate_contract.py
  /reports
      example_trace_without_gate.txt
      example_trace_with_gate.txt
```

---

## Core Concept: Information Pre-Positioning

Information pre-positioning occurs when structured data embeds executable consequences that are not explicit at the point of execution. Examples:

- Implicit privilege escalation fields
- Hidden default behaviours
- Ambiguous resource targets
- Metadata that alters execution ordering
- Conflation of descriptive and authoritative fields

A naive executor processes these structures deterministically, yet produces state corruption. The failure is not randomness. The failure is **admissibility**.

---

## Architectural Distinction

| Approach | Mechanism | Consequence |
|---|---|---|
| Runtime mitigation | Detects and handles problematic states *after* they form | Ongoing operational burden; failure surface grows with system complexity |
| Pre-execution admissibility gating | Prevents problematic state categories from *entering* the system | Reduces mitigation workload downstream; failure surface is bounded upstream |

> If a system requires mitigation logic at runtime, it has already admitted instability. Admissibility is upstream of enforcement.

---

## What This Repository Is

- A deterministic simulation environment
- A failure harness for six contamination patterns
- A conformance test surface for gate implementations
- A behavioural contract for admissibility gating

## What This Repository Is Not

- It does **not** include the Trinity gate implementation
- It does **not** expose gating logic
- It does **not** implement scoring heuristics
- It does **not** provide production security tooling

This is a boundary demonstration only.

---

## Extending with a Real Gate

To test an admissibility gate against the conformance suite:

1. Implement the `Gate` interface defined in `gate_api/interface.py`
2. Inject it into the executor pipeline
3. Ensure all conformance tests pass

---

## Part of the Execution Boundary Series

| Repo | Layer | What It Does |
|---|---|---|
| [interpretation-boundary-lab](https://github.com/LalaSkye/interpretation-boundary-lab) | Upstream boundary | 10-rule admissibility gate for interpretations |
| [dual-boundary-admissibility-lab](https://github.com/LalaSkye/dual-boundary-admissibility-lab) | Full corridor | Dual-boundary model with pressure monitoring and C-sector rotation |
| [execution-boundary-lab](https://github.com/LalaSkye/execution-boundary-lab) | Execution boundary | Demonstrates cascading failures without upstream governance |
| [stop-machine](https://github.com/LalaSkye/stop-machine) | Control primitive | Deterministic three-state stop controller |
| [constraint-workshop](https://github.com/LalaSkye/constraint-workshop) | Control primitives | Execution gate, invariant litmus, stop machine |
| [csgr-lab](https://github.com/LalaSkye/csgr-lab) | Measurement | Contracted stability and drift measurement |
| [invariant-lock](https://github.com/LalaSkye/invariant-lock) | Drift prevention | Refuse execution unless version increments |
| [policy-lint](https://github.com/LalaSkye/policy-lint) | Policy validation | Deterministic linter for governance statements |
| [deterministic-lexicon](https://github.com/LalaSkye/deterministic-lexicon) | Vocabulary | Fixed terms, exact matches, no inference |

---

## License

Apache 2.0. See `LICENSE`.

---

## Authorship & Rights

All architecture, methods, and system designs in this repository are the original work of **Ricky Dean Jones** unless otherwise stated.
No rights to use, reproduce, or implement are granted without explicit permission beyond the terms of the repository licence.

**Author:** Ricky Dean Jones
**Repository owner:** [LalaSkye](https://github.com/LalaSkye)
**Status:** Active research / architecture work
**Part of:** [Execution Boundary Series](https://github.com/LalaSkye) — TrinityOS / AlvianTech

---

This repository demonstrates deterministic control using standard engineering techniques. No proprietary frameworks or external implementations are used.


# execution_boundary_lab

## Purpose

This repository demonstrates a structural phenomenon:

**Information pre-positioning causes cascading execution failures in naive systems.**

When structured action bundles contain implicit authority, hidden defaults, ambiguous targets, or overloaded metadata, downstream execution engines can produce deterministic but unintended side effects.

This lab shows:

1. How syntactically valid inputs can corrupt state under naive execution.
2. Why runtime mitigation is insufficient.
3. Why a pre-execution admissibility gate is structurally necessary.

---

## Why This Matters

Modern AI-integrated systems increasingly execute structured actions proposed by probabilistic models.

Most governance efforts focus on runtime mitigation — detecting and correcting undesirable states after partial execution.

This lab demonstrates a different architectural claim:

> If a system permits certain categories of state to form, mitigation becomes an ongoing operational burden.

Reducing admissibility upstream reduces mitigation workload downstream.

This is not an alignment argument. It is a systems design argument.

---

## What This Repository Is

- A deterministic simulation environment.
- A failure harness.
- A conformance test surface.
- A behavioural contract for admissibility gating.

---

## What This Repository Is Not

- It does **NOT** include the Trinity gate implementation.
- It does **NOT** expose gating logic.
- It does **NOT** implement scoring heuristics.
- It does **NOT** provide production security tooling.

This is a boundary demonstration only.

---

## Core Concept

### Information Pre-Positioning

Information pre-positioning occurs when structured data embeds executable consequences that are not explicit at the point of execution.

Examples include:

- Implicit privilege escalation fields.
- Hidden default behaviours.
- Ambiguous resource targets.
- Metadata that alters execution ordering.
- Conflation of descriptive and authoritative fields.

A naive executor processes these structures deterministically, yet produces state corruption.

The failure is not randomness. The failure is **admissibility**.

---

## Architectural Distinction

**Runtime mitigation:**
- Detects and handles problematic states *after* they form.

**Pre-execution admissibility gating:**
- Prevents problematic state categories from *entering* the system.

This repository illustrates why the latter reduces systemic workload and failure surface.

---

## Repository Structure

```
/execution_boundary_lab
  README.md
  SPEC.md
  /sim
      __init__.py
      executor.py
      resources.py
      logger.py
  /cases
      contaminated_case_1.json
      contaminated_case_2.json
      contaminated_case_3.json
      contaminated_case_4.json
      contaminated_case_5.json
      contaminated_case_6.json
      clean_case_1.json
  /gate_api
      __init__.py
      interface.py
  /baseline
      __init__.py
      naive_executor.py
  /tests
      __init__.py
      conftest.py
      test_prepositioning_failures.py
      test_gate_contract.py
  /reports
      example_trace_without_gate.txt
      example_trace_with_gate.txt
```

---

## Running Tests

```bash
pip install pytest
python -m pytest
```

---

## Extension

To test a real admissibility gate:

1. Implement the `Gate` interface defined in `gate_api/interface.py`.
2. Inject it into the executor pipeline.
3. Ensure all conformance tests pass.

---

## Position

> If a system requires mitigation logic at runtime, it has already admitted instability.
> Admissibility is upstream of enforcement.

---

## Licence

Apache 2.0. See `LICENSE`.

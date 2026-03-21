# Core Invariants

## INV-01 — Execution Dependency
Execution requires a resolved decision.

## INV-02 — Authority Separation
Authority determines what can happen.
Governance describes what should happen.

## INV-03 — Non-Bypassability
All irreversible actions must pass through a single, explicit decision point.

## INV-04 — Test of Control
If execution remains reachable without a decision → control is invalid.

## INV-05 — Capability vs Permission
System capability does not imply execution permission.

## INV-06 — Continuity vs Constraint
Reconstructing or preserving state does not constrain execution.

---

## Canonical Test

Remove decision.

IF system still executes:
→ Not governed

ELSE:
→ Governed

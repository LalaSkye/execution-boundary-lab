# Invariant: Authority Must Be Current at Bind Time

## Statement
A consequence **should not bind** unless the authority that permits it is **current**, **scoped**, **valid**, and **checkable** at the moment of binding.

This distinguishes:

- **Issue-time authority** — when the authority was created or granted.
- **Bind-time authority** — when a consequence would take effect.

The invariant asserts that bind-time is the relevant moment for evaluating authority freshness.

---

## Motivation
Relying solely on the existence of an authority record risks:

- binding consequences after authority has expired,
- binding consequences outside the intended scope,
- binding consequences when the authority cannot be revalidated,
- binding consequences based on stale or revoked permissions.

This invariant prevents the assumption that “an authority record exists” implies “authority is still valid.”

---

## Expected Behaviour (Design-Level)
At bind time:

1. Authority should still be within its validity window.
2. Authority should still match the required scope.
3. Authority should still be checkable (i.e., not orphaned, revoked, or unverifiable).
4. If authority cannot be revalidated, binding should not proceed.

These expectations are **design-level only**.
They do **not** imply runtime enforcement.

---

## Non-Goals
This invariant does **not**:

- guarantee that any system enforces authority checks,
- specify how authority is stored, validated, or revoked,
- define a runtime mechanism,
- imply compliance, certification, or production readiness,
- modify or constrain `commit-gate-core`.

---

## Relation to Other Invariants
This invariant complements any rule requiring:

- explicit authority,
- scoped authority,
- revocation awareness,
- time-bounded permissions.

It does not replace or override them.

---

## Claim Boundary
This document asserts only a **design requirement** and a **testable expectation**.
It does **not** assert that any implementation exists or that any system currently satisfies it.

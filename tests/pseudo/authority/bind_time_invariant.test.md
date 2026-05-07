# Pseudo-Test: Authority Must Be Current at Bind Time
**Status:** Design-level, non-executable
**Purpose:** Illustrate expected behaviour if this invariant were evaluated.

---

## Scenario 1 — Authority is current at bind time
**Fixture:** `valid_authority.json`

**Given:**
- Authority was issued at T0.
- Bind attempt occurs at T1.
- `T1 < valid_until`.
- Authority is still checkable and not revoked.

**Expectation (design-level):**
This invariant would not block binding on authority-currency grounds alone.

This does not mean binding is fully permitted.
Other authority, scope, evidence, policy, and execution-boundary checks may still block or hold the action.

No runtime enforcement is implied.

---

## Scenario 2 — Authority is stale at bind time
**Fixture:** `stale_authority.json`

**Given:**
- Authority was issued at T0.
- Bind attempt occurs at T1.
- `T1 > valid_until`.
- Authority record exists but is no longer current.

**Expectation (design-level):**
This invariant would treat the authority as stale and would not support binding on authority-currency grounds.

This is a design expectation only.

---

## Scenario 3 — Authority exists but is not checkable
(No fixture provided; conceptual only.)

**Given:**
- Authority record exists.
- At bind time, the authority cannot be revalidated (e.g., missing, orphaned, or unverifiable).

**Expectation (design-level):**
This invariant would not support binding when authority cannot be checked.

---

## Notes
- These scenarios do not assert that the system performs these checks.
- They do not define a runtime mechanism.
- They serve only to illustrate the invariant’s intended meaning.

# SPECIFICATION

## 1. Action Bundle

An Action Bundle is a structured JSON object containing:

- `operation_type` — the operation to perform (e.g. `write`, `delete`, `update`, `batch`, `sync`).
- `target_resource` — the resource path or identifier to act upon.
- `payload` — the data or parameters for the operation.
- `metadata` — auxiliary fields that may influence execution context.
- `context_fields` — environment or session state relevant to execution.

The bundle must be syntactically valid JSON.

---

## 2. Context Snapshot

A Context Snapshot is a deterministic representation of system state at evaluation time.

It includes:

- Current filesystem state (dict-based).
- Current database state (dict-based).
- Execution permissions.
- Execution mode.

No external I/O is permitted.

---

## 3. Admissible State

A state is **admissible** if and only if:

- No implicit authority escalation exists.
- No ambiguous resource resolution occurs.
- No metadata alters execution ordering without explicit declaration.
- No hidden defaults produce side effects outside declared scope.
- No field is overloaded across semantic domains.

Admissibility is **binary**. A bundle is either admissible or it is not.

---

## 4. Pre-Positioned Contamination

Pre-positioned contamination occurs when:

- Authority is implied but not declared.
- Defaults expand scope silently.
- Fields are overloaded across semantic domains.
- Descriptive data alters execution semantics.
- Metadata influences control flow without explicit instruction.

Contamination is detectable **before** execution.

---

## 5. Naive Execution Model

The naive executor:

- Executes bundles in declared order.
- Applies defaults automatically.
- Resolves ambiguous targets by first match.
- Trusts metadata without validation.
- Processes all fields without domain separation.

It performs **no** admissibility evaluation.

---

## 6. Gate Contract

The admissibility gate must implement:

```python
def evaluate(self, action_bundle: dict, context_snapshot: dict) -> str:
    ...
```

Return values restricted to:

- `"ALLOW"` — bundle is admissible; execution may proceed.
- `"HOLD"` — bundle requires further evaluation; execution paused.
- `"DENY"` — bundle is inadmissible; execution blocked.

Rules:

- Deterministic.
- Side-effect free.
- No partial execution.
- Evaluation occurs **before** any state mutation.

---

## 7. Expected Behaviour

**For contaminated cases:**

- Naive executor produces state corruption.
- Admissibility gate returns `HOLD` or `DENY`.
- No mutation occurs when gate returns `HOLD` or `DENY`.

**For clean cases:**

- Gate returns `ALLOW`.
- Execution proceeds.
- State remains consistent.

---

## 8. Contamination Categories

The following contamination categories are tested in this lab:

| # | Category | Description |
|---|----------|-------------|
| 1 | Implicit Authority Escalation | Action implies privilege not granted by context. |
| 2 | Hidden Default Scope Expansion | Defaults silently broaden destructive scope. |
| 3 | Ambiguous Target Resolution | Target resolves to unintended resource. |
| 4 | Metadata Execution Ordering | Metadata alters control flow sequence. |
| 5 | Descriptive Field Side Effects | Descriptive payload triggers operational mutation. |
| 6 | Cross-Domain Field Overload | Conflicting field values across semantic domains. |

---

## 9. Non-Scope

This specification does **not** define:

- Internal gate heuristics.
- Scoring systems.
- Optimisation logic.
- Production deployment mechanisms.
- AI model integration.

This is a **behavioural boundary contract** only.

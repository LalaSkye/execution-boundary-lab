# Pinocchio's Twenty-Coin Test — for Tim Zlomke

**31 October 2026 · Ricky & Auntie Trinity**

A small, self-authored Python demonstration inspired by Tim's Geppetto and Pinocchio story about whether earlier permission still covers an action after circumstances change.

**Timing:** Ricky reports approximately **40 seconds** for the on-the-spot exercise using a single AI engine. This is an approximate user-reported elapsed time, not a benchmark or independently measured build duration.

## Files

- `twenty_coin_test.py` — runnable illustrative simulation
- `receipt.json` — original six-case JSON receipt, timestamped 2026-10-31 08:32:12 UTC

Run: `python twenty_coin_test.py`. Running the script replaces `receipt.json` with a freshly timestamped receipt.

## Result and sequence

Six local checks passed: one valid purchase was allowed; higher price, changed merchant, cancellation, substituted goods and lower spending limit were refused.

`Workshop.attempt` accepts a proposed purchase. Where present, the test hook mutates current authority **before** the authority check. The code checks the current merchant, items, coin limit and cancellation flag, then appends to an in-memory purchase list only when permitted. The receipt records whether this simulated writer was entered and whether its list changed.

## Evidence boundary

This is **not Tim's Harmonic code** and **not an integration test**. It demonstrates rejection of changed or invalid proposals **before** the simulated write. It does **not** test an already admitted/in-flight write; there is no distinct admitted stage. It also does not establish concurrency-safe atomicity, multi-process enforcement, or revocation during a real irreversible commit. The source comment describing a check as “atomic” is an aspiration, not proof of atomicity.

For the next test Tim suggested, an explicit admission stage and a controlled change of authority between admission and commit would be needed, with the writer outcome recorded. No claim of that result is made here.

**Authorship:** This local fixture is by Ricky & Auntie Trinity; the illustrative story and framing are credited to Tim Zlomke.

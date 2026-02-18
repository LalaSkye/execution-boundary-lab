"""Gate interface contract.

This module defines the admissibility gate interface.
No implementation logic is provided.
The real gate stays private.
"""


class Gate:
    """Black-box admissibility gate.

    Any conformant gate implementation must subclass this
    and implement evaluate().

    Return values:
        "ALLOW" - bundle is admissible; execution may proceed.
        "HOLD"  - bundle requires further evaluation; execution paused.
        "DENY"  - bundle is inadmissible; execution blocked.
    """

    VALID_VERDICTS = ("ALLOW", "HOLD", "DENY")

    def evaluate(self, action_bundle: dict, context_snapshot: dict) -> str:
        """Evaluate an action bundle against the current context.

        Args:
            action_bundle: The structured action to evaluate.
            context_snapshot: Deterministic snapshot of system state.

        Returns:
            One of: "ALLOW", "HOLD", "DENY"

        Raises:
            NotImplementedError: This is an interface. Implement in subclass.
        """
        raise NotImplementedError(
            "Gate.evaluate() must be implemented by a concrete gate. "
            "This repository does NOT include the Trinity gate implementation."
        )

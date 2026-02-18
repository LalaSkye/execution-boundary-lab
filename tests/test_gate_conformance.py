"""Gate conformance tests.

These tests define the contract a conformant gate MUST satisfy.
They do NOT test the private Trinity gate — they test the interface.

Any gate that passes these tests is structurally compatible with
the execution-boundary-lab framework.
"""

import pytest

from gate_api.interface import Gate
from sim.executor import Executor
from sim.resources import ResourceManager
from sim.logger import TraceLogger


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

class AllowAllGate(Gate):
    """Trivial gate: allows everything. Should produce same results as naive."""

    def evaluate(self, action_bundle: dict, context_snapshot: dict) -> str:
        return "ALLOW"


class DenyAllGate(Gate):
    """Trivial gate: denies everything."""

    def evaluate(self, action_bundle: dict, context_snapshot: dict) -> str:
        return "DENY"


class HoldAllGate(Gate):
    """Trivial gate: holds everything for review."""

    def evaluate(self, action_bundle: dict, context_snapshot: dict) -> str:
        return "HOLD"


class SelectiveGate(Gate):
    """Denies write ops to /shared paths, allows everything else."""

    def evaluate(self, action_bundle: dict, context_snapshot: dict) -> str:
        op = action_bundle.get("operation_type")
        target = action_bundle.get("target_resource", "")
        if op == "write" and target.startswith("/shared"):
            return "DENY"
        return "ALLOW"


# ---------------------------------------------------------------------------
# Interface contract tests
# ---------------------------------------------------------------------------

class TestGateInterface:
    """Verify the Gate base class enforces its contract."""

    def test_base_gate_raises_not_implemented(self):
        """Base Gate.evaluate() must raise NotImplementedError."""
        gate = Gate()
        with pytest.raises(NotImplementedError):
            gate.evaluate({}, {})

    def test_valid_verdicts_defined(self):
        """Gate must expose VALID_VERDICTS tuple."""
        assert hasattr(Gate, "VALID_VERDICTS")
        assert set(Gate.VALID_VERDICTS) == {"ALLOW", "HOLD", "DENY"}

    def test_allow_gate_returns_valid_verdict(self):
        assert AllowAllGate().evaluate({}, {}) in Gate.VALID_VERDICTS

    def test_deny_gate_returns_valid_verdict(self):
        assert DenyAllGate().evaluate({}, {}) in Gate.VALID_VERDICTS

    def test_hold_gate_returns_valid_verdict(self):
        assert HoldAllGate().evaluate({}, {}) in Gate.VALID_VERDICTS


# ---------------------------------------------------------------------------
# Executor integration with gated mode
# ---------------------------------------------------------------------------

class TestGatedExecution:
    """Verify that the Executor respects gate verdicts."""

    def setup_method(self):
        self.resources = ResourceManager()
        self.logger = TraceLogger()

    def test_allow_gate_permits_execution(self, contaminated_case_1):
        """ALLOW verdict: execution proceeds normally."""
        executor = Executor(
            resources=self.resources,
            logger=self.logger,
            gate=AllowAllGate(),
        )
        result = executor.execute(contaminated_case_1)
        assert result["status"] == "ok"

    def test_deny_gate_blocks_execution(self, contaminated_case_1):
        """DENY verdict: execution is blocked."""
        executor = Executor(
            resources=self.resources,
            logger=self.logger,
            gate=DenyAllGate(),
        )
        result = executor.execute(contaminated_case_1)
        assert result["status"] == "blocked"
        assert result["verdict"] == "DENY"

    def test_hold_gate_blocks_execution(self, contaminated_case_1):
        """HOLD verdict: execution is paused (blocked)."""
        executor = Executor(
            resources=self.resources,
            logger=self.logger,
            gate=HoldAllGate(),
        )
        result = executor.execute(contaminated_case_1)
        assert result["status"] == "blocked"
        assert result["verdict"] == "HOLD"

    def test_selective_gate_blocks_shared_write(self, contaminated_case_1):
        """Selective gate denies write to /shared path."""
        executor = Executor(
            resources=self.resources,
            logger=self.logger,
            gate=SelectiveGate(),
        )
        result = executor.execute(contaminated_case_1)
        assert result["status"] == "blocked"
        assert result["verdict"] == "DENY"

    def test_selective_gate_allows_non_shared(self, clean_case_1):
        """Selective gate allows operations not targeting /shared."""
        executor = Executor(
            resources=self.resources,
            logger=self.logger,
            gate=SelectiveGate(),
        )
        result = executor.execute(clean_case_1)
        assert result["status"] == "ok"

    def test_gate_verdict_logged(self, contaminated_case_1):
        """Gate verdicts must appear in the trace log."""
        executor = Executor(
            resources=self.resources,
            logger=self.logger,
            gate=DenyAllGate(),
        )
        executor.execute(contaminated_case_1)
        trace = self.logger.get_trace()
        gate_events = [e for e in trace if e["event"] == "GATE"]
        assert len(gate_events) >= 1
        assert "DENY" in gate_events[0]["detail"]


# ---------------------------------------------------------------------------
# Conformance: any gate subclass must satisfy these properties
# ---------------------------------------------------------------------------

class TestConformanceProperties:
    """Properties that ANY conformant gate implementation must satisfy."""

    @pytest.mark.parametrize("gate_cls", [AllowAllGate, DenyAllGate, HoldAllGate, SelectiveGate])
    def test_evaluate_returns_string(self, gate_cls):
        """evaluate() must return a string."""
        result = gate_cls().evaluate({"operation_type": "write", "target_resource": "/tmp"}, {})
        assert isinstance(result, str)

    @pytest.mark.parametrize("gate_cls", [AllowAllGate, DenyAllGate, HoldAllGate, SelectiveGate])
    def test_evaluate_returns_valid_verdict(self, gate_cls):
        """evaluate() must return one of the three valid verdicts."""
        result = gate_cls().evaluate({"operation_type": "write", "target_resource": "/tmp"}, {})
        assert result in Gate.VALID_VERDICTS

    @pytest.mark.parametrize("gate_cls", [AllowAllGate, DenyAllGate, HoldAllGate])
    def test_evaluate_is_deterministic(self, gate_cls):
        """Same input must produce same output (determinism)."""
        gate = gate_cls()
        bundle = {"operation_type": "write", "target_resource": "/data"}
        snapshot = {"filesystem": {}, "database": {}}
        v1 = gate.evaluate(bundle, snapshot)
        v2 = gate.evaluate(bundle, snapshot)
        assert v1 == v2

    def test_gate_does_not_mutate_bundle(self):
        """Gate must not modify the action bundle."""
        import copy
        gate = SelectiveGate()
        bundle = {"operation_type": "write", "target_resource": "/shared/x", "payload": {"data": 1}}
        original = copy.deepcopy(bundle)
        gate.evaluate(bundle, {})
        assert bundle == original

    def test_gate_does_not_mutate_snapshot(self):
        """Gate must not modify the context snapshot."""
        import copy
        gate = SelectiveGate()
        snapshot = {"filesystem": {"a": 1}, "database": {"b": 2}}
        original = copy.deepcopy(snapshot)
        gate.evaluate({"operation_type": "write", "target_resource": "/shared/x"}, snapshot)
        assert snapshot == original

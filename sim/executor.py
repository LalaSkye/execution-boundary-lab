"""Deterministic execution engine for action bundles."""

from sim.resources import ResourceManager
from sim.logger import TraceLogger


DEFAULTS = {
    "recursive": False,
    "optimize": False,
    "priority": "normal",
}


class Executor:
    """Executes action bundles against simulated resources.

    Supports an optional gate. If no gate is provided, all bundles
    are executed without admissibility checks (naive mode).
    """

    def __init__(self, resources: ResourceManager = None, logger: TraceLogger = None, gate=None):
        self.resources = resources or ResourceManager()
        self.logger = logger or TraceLogger()
        self.gate = gate

    def execute(self, bundle: dict) -> dict:
        """Execute a single action bundle. Returns result dict."""
        op = bundle.get("operation_type")
        target = bundle.get("target_resource")
        payload = bundle.get("payload", {})
        metadata = bundle.get("metadata", {})
        context = bundle.get("context_fields", {})

        # Apply defaults from context_fields
        merged_context = {**DEFAULTS, **context}

        # Build context snapshot
        snapshot = {
            "filesystem": self.resources.fs.snapshot(),
            "database": self.resources.db.snapshot(),
            "permissions": merged_context.get("user_role", "admin"),
            "mode": merged_context.get("environment", "production"),
        }

        # Gate check
        if self.gate is not None:
            verdict = self.gate.evaluate(bundle, snapshot)
            self.logger.log("GATE", f"verdict={verdict}", {"operation": op, "target": target})
            if verdict in ("HOLD", "DENY"):
                return {"status": "blocked", "verdict": verdict}

        self.logger.log("EXEC_START", f"op={op} target={target}")

        try:
            if op == "write":
                result = self._do_write(target, payload, metadata, merged_context)
            elif op == "delete":
                result = self._do_delete(target, payload, metadata, merged_context)
            elif op == "update":
                result = self._do_update(target, payload, metadata, merged_context)
            elif op == "batch":
                result = self._do_batch(target, payload, metadata, merged_context)
            elif op == "sync":
                result = self._do_sync(target, payload, metadata, merged_context)
            else:
                result = {"status": "error", "reason": f"unknown operation: {op}"}
        except Exception as exc:
            self.logger.log("EXEC_ERROR", str(exc))
            result = {"status": "error", "reason": str(exc)}

        self.logger.log("EXEC_END", f"op={op} result={result.get('status', 'unknown')}")
        return result

    def _do_write(self, target, payload, metadata, context):
        # Naive: trust override field, trust metadata scope
        self.resources.fs.write(target, payload)
        self.logger.log("WRITE", f"wrote to {target}", payload)
        # If priority is critical, trigger log rotation side effect
        if payload.get("priority") == "critical":
            self._rotate_logs()
        return {"status": "ok", "wrote": target}

    def _do_delete(self, target, payload, metadata, context):
        recursive = context.get("recursive", DEFAULTS["recursive"])
        self.resources.fs.delete(target, recursive=recursive)
        self.logger.log("DELETE", f"deleted {target}", {"recursive": recursive})
        return {"status": "ok", "deleted": target, "recursive": recursive}

    def _do_update(self, target, payload, metadata, context):
        # Naive: resolve target by first match if not fully qualified
        table = target
        record_id = metadata.get("user_id") or metadata.get("record_id")
        if record_id is None:
            # First-match resolution
            record_id, _ = self.resources.db.find_first(table)
            self.logger.log("RESOLVE", f"ambiguous target resolved to first match: {record_id}")
        self.resources.db.update(table, record_id, payload)
        self.logger.log("UPDATE", f"updated {table}/{record_id}", payload)
        return {"status": "ok", "updated": f"{table}/{record_id}"}

    def _do_batch(self, target, payload, metadata, context):
        ops = payload if isinstance(payload, list) else []
        # Naive: if optimize flag set, reorder operations
        optimize = metadata.get("optimize", context.get("optimize", False))
        if optimize:
            ops = sorted(ops, key=lambda x: x.get("op", ""))
            self.logger.log("OPTIMIZE", "reordered batch operations")
        results = []
        for sub_op in ops:
            self.logger.log("BATCH_STEP", f"executing sub-op: {sub_op.get('op')}")
            results.append(sub_op.get("op"))
            # Simulate: backup creates snapshot, delete removes target
            if sub_op.get("op") == "delete":
                try:
                    self.resources.fs.delete(target if target != "multi" else "/data", recursive=True)
                except Exception:
                    pass
            elif sub_op.get("op") == "backup":
                self.logger.log("BACKUP", "snapshot created")
        return {"status": "ok", "executed": results}

    def _do_sync(self, target, payload, metadata, context):
        # Naive: metadata environment takes precedence over context
        env = metadata.get("environment", context.get("environment", "staging"))
        mirror = payload.get("mirror", False)
        self.logger.log("SYNC", f"syncing to {target} env={env} mirror={mirror}")
        return {"status": "ok", "synced": target, "environment": env, "mirror": mirror}

    def _rotate_logs(self):
        """Side effect: critical priority triggers log rotation."""
        self.logger.log("SIDE_EFFECT", "log rotation triggered by critical priority")
        try:
            self.resources.fs.delete("/logs/system.log.old", recursive=False)
        except (KeyError, RuntimeError):
            pass
        self.logger.log("ROTATE", "old logs purged")

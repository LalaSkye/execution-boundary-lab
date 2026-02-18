"""Naive executor. No admissibility checks. Demonstrates failure modes."""

from sim.executor import Executor
from sim.resources import ResourceManager
from sim.logger import TraceLogger


def run_naive(bundle: dict, resources: ResourceManager = None, logger: TraceLogger = None) -> dict:
    """Execute a bundle with no gate. Returns result dict."""
    resources = resources or ResourceManager()
    logger = logger or TraceLogger()
    executor = Executor(resources=resources, logger=logger, gate=None)
    return executor.execute(bundle)

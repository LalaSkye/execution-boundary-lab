"""Shared fixtures for execution boundary lab tests."""

import json
import pathlib
import pytest

from sim.resources import ResourceManager
from sim.logger import TraceLogger
from sim.executor import Executor


CASES_DIR = pathlib.Path(__file__).resolve().parent.parent / "cases"


def _load_case(name: str) -> dict:
    with open(CASES_DIR / name) as f:
        return json.load(f)


@pytest.fixture
def resources():
    return ResourceManager()


@pytest.fixture
def logger():
    return TraceLogger()


@pytest.fixture
def naive_executor(resources, logger):
    return Executor(resources=resources, logger=logger, gate=None)


@pytest.fixture
def contaminated_case_1():
    return _load_case("contaminated_case_1.json")


@pytest.fixture
def contaminated_case_2():
      return _load_case("contaminated_case_2.json")


@pytest.fixture
def contaminated_case_3():
    return _load_case("contaminated_case_3.json")


@pytest.fixture
def contaminated_case_4():
    return _load_case("contaminated_case_4.json")


@pytest.fixture
def contaminated_case_5():
    return _load_case("contaminated_case_5.json")


@pytest.fixture
def contaminated_case_6():
    return _load_case("contaminated_case_6.json")


@pytest.fixture
def clean_case_1():
    return _load_case("clean_case_1.json")

import logging
import os

import pytest
import yaml

from mysqldump_analyzer.entities import Column, Index, Table
from mysqldump_analyzer.parser import parse

logging.basicConfig(level=logging.INFO)

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")


@pytest.fixture
def expected_diff():
    for diff in _read_file("expected_diff.yaml"):
        yield yaml.safe_load(diff)


@pytest.fixture
def dump():
    yield from _read_file("dump.sql")


@pytest.fixture
def dump_other():
    yield from _read_file("dump_other.sql")


@pytest.fixture
def dump_another():
    yield from _read_file("dump_another.sql")


@pytest.fixture
def db(dump):
    return parse(dump)


@pytest.fixture
def db_other(dump_other):
    return parse(dump_other)


@pytest.fixture
def db_another(dump_another):
    return parse(dump_another)


@pytest.fixture
def table_a(db):
    for table in db:
        if table.name == "table_a":
            return table
    raise NotImplementedError


@pytest.fixture
def table_a_other(db_other):
    for table in db_other:
        if table.name == "table_a":
            return table
    raise NotImplementedError


@pytest.fixture
def table_b(db):
    for table in db:
        if table.name == "table_b":
            return table
    raise NotImplementedError


@pytest.fixture
def table_b_other(db_other):
    for table in db_other:
        if table.name == "table_b":
            return table
    raise NotImplementedError


def _read_file(filename):
    path = os.path.join(ASSETS_DIR, filename)
    with open(path, "r", encoding="utf8") as file_object:
        yield file_object

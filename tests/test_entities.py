import pytest

from mysqldump_analyzer.entities import Index, Options


def test_primary_key_is_unique_index():
    with pytest.raises(ValueError):
        Index(name="primary key", columns=("foo",), primary_key=True, unique=False)

    # sanity check: nominal case
    Index(name="primary key", columns=("foo",), primary_key=True, unique=True)


def test_primary_key_has_no_name():
    with pytest.raises(ValueError):
        Index(name="foo", columns=("foo",), primary_key=True, unique=True)
    with pytest.raises(ValueError):
        Index(name="", columns=("foo",), primary_key=True, unique=True)
    with pytest.raises(ValueError):
        Index(name=None, columns=("foo",), primary_key=True, unique=True)

    # sanity check: nominal case
    Index(name="primary key", columns=("foo",), primary_key=True, unique=True)


def test_options_bool_values():
    assert Options(values="foo=bar")
    assert not Options(values="")


def test_index_covers():
    index1 = Index(name="1", columns=("a", "b"))
    assert index1.covers(index1)

    index2 = Index(name="2", columns=("b", "a"))
    assert not index1.covers(index2)
    assert not index2.covers(index1)

    index3 = Index(name="3", columns=("a", "b", "c"))
    assert index3.covers(index1)
    assert not index1.covers(index3)
    assert not index2.covers(index3)
    assert not index3.covers(index2)

    primary_key1 = Index(name="primary key", columns=("a", "b"), primary_key=True, unique=True)
    assert primary_key1.covers(index1)
    assert not index1.covers(primary_key1)
    assert not index3.covers(primary_key1)

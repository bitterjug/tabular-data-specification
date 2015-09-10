from __future__ import absolute_import
import pytest
from colspec import ColumnSpecification, Column


@pytest.fixture
def colspec():
    return ColumnSpecification(
        Column("One"),
        Column("a", header="Two"),
        Column("b", "c", header="Three", reduce=sum),
        Column('d', 'e', header="Four", reduce=" ".join)
    )


def inc(x):
    return x + 1


def test_headers(colspec):
    assert colspec.headers() == ["One", "Two", "Three", "Four"]


def test_inputs(colspec):
    assert colspec.inputs() == ["One", "a", "b", "c", "d", "e"]


def test_values(colspec):
    context = {
        'a': 1,
        'b': 2,
        'c': 3,
        'd': "foo",
        'e': "bar",
        'One': 6,
    }
    assert colspec.values(context) == [6, 1, 5, "foo bar"]


def test_fn_with_single_value():
    colspec = ColumnSpecification(
        Column('key', function=inc),
    )
    assert colspec.values({'key': 1}) == [2]


def test_fn_with_multiple_values():
    colspec = ColumnSpecification(
        Column('a', 'b', 'c', function=lambda a, b, c: a + b - c),
    )
    row = {
        'a': 4,
        'b': 6,
        'c': 2,
    }
    assert colspec.values(row) == [8]


def test_reduce_before_fn():
    colspec = ColumnSpecification(
        Column('a', 'b', reduce=sum, function=inc),
    )
    assert colspec.values({'a': 4, 'b': 6}) == [11]


def test_default():
    colspec = ColumnSpecification(
        Column('key', default=7),
    )
    assert colspec.values({}) == [7]


def test_default_and_fn():
    colspec = ColumnSpecification(
        Column('key', function=inc, default=4),
    )
    assert colspec.values({}) == [5]


def test_default_rx_with_multiple_values():
    colspec = ColumnSpecification(
        Column('a', 'b', 'c')
    )
    row = {
        'a': 4,
        'b': 6,
        'c': 2,
    }
    assert colspec.values(row) == [4]


def test_related():
    colspec = ColumnSpecification(
        Column("0", 'q'),
        Column("Aa", 'a__x'),
        Column("Ab", 'b__x'),
        Column("Ac", 'c__x', 'c__y'),
        Column("Aa2", 'a__y'),
    )
    expected = set(['a', 'b', 'c'])
    assert expected.symmetric_difference(colspec.related()) == set()

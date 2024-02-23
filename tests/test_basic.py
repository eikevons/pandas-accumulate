import operator

from pandas_accumulate import accumulate

import pandas as pd
import pytest

@pytest.fixture
def int_series():
    return pd.Series(range(5))


def test_int_cumsum(int_series):
    expected = pd.Series([0, 1, 3, 6, 10])
    pd.testing.assert_series_equal(
        accumulate(int_series, operator.add),
        expected,
    )

def test_int_cumsum_initial(int_series):
    expected = pd.Series([3, 4, 6, 9, 13])
    pd.testing.assert_series_equal(
        accumulate(int_series, operator.add, initial=3),
        expected,
    )

def test_int_xor(int_series):
    expected = pd.Series([0, 0^1, 0^1^2, 0^1^2^3, 0^1^2^3^4])
    pd.testing.assert_series_equal(
        accumulate(int_series, operator.xor),
        expected,
    )

def test_length_1_series():
    s = pd.Series([1])
    pd.testing.assert_series_equal(
        accumulate(s, operator.add),
        s,
    )

def test_length_1_series_with_initial():
    s = pd.Series([1])
    pd.testing.assert_series_equal(
        accumulate(s, operator.add, initial=42),
        s + 42,
    )

def test_cumulative_uniques_use_case():
    inp = pd.Series([1, 2, 1, 3, 1, 2])
    expected = pd.Series([1, 2, 2, 3, 3, 3])
    expected = pd.Series([{1}, {1, 2}, {1, 2}] + 3 * [{1, 2, 3}])

    test = accumulate(inp, lambda a, b: a | {b}, initial=set())
    pd.testing.assert_series_equal(test, expected)

def test_length_0_series():
    s = pd.Series([])
    pd.testing.assert_series_equal(
        accumulate(s, operator.add),
        s,
    )

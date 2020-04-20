"""Tests for typing helpers"""

import pytest

from pytiled_parser import typing_helpers as TH

TEST_IS_FLOAT_PARAMS = [
    (1, True),
    ("1", True),
    (1.1, True),
    ("1.1", True),
    ("one", False),
    (None, False),
]


@pytest.mark.parametrize("string,expected", TEST_IS_FLOAT_PARAMS)
def test_is_float(string, expected):
    assert TH.is_float(string) == expected

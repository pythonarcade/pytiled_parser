"""Tests for maps"""
import importlib.util
import os
from pathlib import Path

import pytest

from pytiled_parser import tiled_map

TESTS_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
TEST_DATA = TESTS_DIR / "test_data"
MAP_TESTS = TEST_DATA / "map_tests"

ALL_MAP_TESTS = [
    MAP_TESTS / "no_layers",
    MAP_TESTS / "no_background_color",
    MAP_TESTS / "hexagonal",
    MAP_TESTS / "embedded_tileset",
]


@pytest.mark.parametrize("map_test", ALL_MAP_TESTS)
def test_map_integration(map_test):
    # it's a PITA to import like this, don't do it
    # https://stackoverflow.com/a/67692/1342874
    spec = importlib.util.spec_from_file_location("expected", map_test / "expected.py")
    expected = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(expected)

    raw_maps_path = map_test / "map.json"

    casted_map = tiled_map.cast(raw_maps_path)

    assert casted_map == expected.EXPECTED

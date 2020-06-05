"""Tests for tilesets"""
import json
import os
from pathlib import Path

import pytest

from pytiled_parser import tileset

TESTS_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
TEST_DATA = TESTS_DIR / "test_data"
TILE_SETS = TEST_DATA / "tilesets"


ALL_TILESETS = TILE_SETS.glob("*.json")


@pytest.mark.parametrize("raw_tileset", ALL_TILESETS)
def test_tilesets_integration(raw_tileset):
    """ This could be redundant, but it is useful just to ensure that anything in there
    is at least sanity checked"""
    tileset_ = tileset.cast(json.loads(raw_tileset))
    assert tileset_ is not None

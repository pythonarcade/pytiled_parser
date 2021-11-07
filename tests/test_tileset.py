"""Tests for tilesets"""
import importlib.util
import json
import os
from pathlib import Path

import pytest

from pytiled_parser.parsers.json.tileset import parse

TESTS_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
TEST_DATA = TESTS_DIR / "test_data"
TILE_SETS = TEST_DATA / "tilesets"


ALL_TILESET_DIRS = [
    TILE_SETS / "image",
    TILE_SETS / "image_background_color",
    TILE_SETS / "image_grid",
    TILE_SETS / "image_properties",
    TILE_SETS / "image_transparent_color",
    TILE_SETS / "image_tile_offset",
    TILE_SETS / "image_transformations",
    TILE_SETS / "individual_images",
    TILE_SETS / "terrain",
]


@pytest.mark.parametrize("tileset_dir", ALL_TILESET_DIRS)
def test_tilesets_integration(tileset_dir):
    # it's a PITA to import like this, don't do it
    # https://stackoverflow.com/a/67692/1342874
    spec = importlib.util.spec_from_file_location(
        "expected", tileset_dir / "expected.py"
    )
    expected = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(expected)

    raw_tileset_path = tileset_dir / "tileset.json"

    with open(raw_tileset_path) as raw_tileset:
        tileset_ = parse(json.loads(raw_tileset.read()), 1)

    assert tileset_ == expected.EXPECTED

"""Tests for tilesets"""
import importlib.util
import json
import os
from pathlib import Path

import pytest

from pytiled_parser.parsers.json.layer import parse

TESTS_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
TEST_DATA = TESTS_DIR / "test_data"
LAYER_TESTS = TEST_DATA / "layer_tests"


ALL_LAYER_TESTS = [
    LAYER_TESTS / "all_layer_types",
    LAYER_TESTS / "b64",
    LAYER_TESTS / "b64_gzip",
    LAYER_TESTS / "b64_zlib",
    # LAYER_TESTS / "b64_zstd",
    LAYER_TESTS / "no_layers",
    LAYER_TESTS / "infinite_map",
    LAYER_TESTS / "infinite_map_b64",
]


@pytest.mark.parametrize("layer_test", ALL_LAYER_TESTS)
def test_layer_integration(layer_test):
    # it's a PITA to import like this, don't do it
    # https://stackoverflow.com/a/67692/1342874
    spec = importlib.util.spec_from_file_location(
        "expected", layer_test / "expected.py"
    )
    expected = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(expected)

    raw_layers_path = layer_test / "map.json"

    with open(raw_layers_path) as raw_layers_file:
        raw_layers = json.load(raw_layers_file)["layers"]
        layers = [parse(raw_layer) for raw_layer in raw_layers]

    assert layers == expected.EXPECTED

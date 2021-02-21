"""test test_map_simple_offset.tmx"""
import os
from pathlib import Path

import pytiled_parser

TESTS_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
TEST_DATA = TESTS_DIR / "test_data"


def test_map_simple():
    """
    TMX with a very simple spritesheet tile set and some properties.
    """

    test_map = pytiled_parser.parse_tile_map(TEST_DATA / "test_map_simple_offset.tmx")

    # map
    # unsure how to get paths to compare propperly
    assert test_map.parent_dir == TEST_DATA
    assert test_map.version == "1.2"
    assert test_map.tiled_version == "1.3.1"
    assert test_map.orientation == "orthogonal"
    assert test_map.render_order == "right-down"
    assert test_map.map_size == (8, 6)
    assert test_map.tile_size == (32, 32)
    assert test_map.infinite == False
    assert test_map.next_layer_id == 2
    assert test_map.next_object_id == 1

    # optional, not for orthogonal maps
    assert test_map.hex_side_length == None
    assert test_map.stagger_axis == None
    assert test_map.stagger_index == None
    assert test_map.background_color == None

    assert test_map.properties == {
        "bool property - false": False,
        "bool property - true": True,
        "color property": "#ff49fcff",
        "float property": 1.23456789,
        "int property": 13,
        "string property": "Hello, World!!",
    }

    # tileset
    assert test_map.tile_sets[1].name == "tile_set_image"
    assert test_map.tile_sets[1].max_tile_size == (32, 32)
    assert test_map.tile_sets[1].spacing == 1
    assert test_map.tile_sets[1].margin == 1
    assert test_map.tile_sets[1].tile_count == 48
    assert test_map.tile_sets[1].columns == 8
    assert test_map.tile_sets[1].tile_offset == None
    assert test_map.tile_sets[1].grid == None
    assert test_map.tile_sets[1].properties == None

    # unsure how to get paths to compare propperly
    assert str(test_map.tile_sets[1].image.source) == ("images/tmw_desert_spacing.png")
    assert test_map.tile_sets[1].image.trans == None
    assert test_map.tile_sets[1].image.size == (265, 199)

    assert test_map.tile_sets[1].terrain_types == None
    assert test_map.tile_sets[1].tiles == {}

    # layers
    assert test_map.layers[0].layer_data == [
        [1, 2, 3, 4, 5, 6, 7, 8],
        [9, 10, 11, 12, 13, 14, 15, 16],
        [17, 18, 19, 20, 21, 22, 23, 24],
        [25, 26, 27, 28, 29, 30, 31, 32],
        [33, 34, 35, 36, 37, 38, 39, 40],
        [41, 42, 43, 44, 45, 46, 47, 48],
    ]
    assert test_map.layers[0].id_ == 1
    assert test_map.layers[0].name == "Tile Layer 1"
    assert test_map.layers[0].offset == pytiled_parser.objects.OrderedPair(
        x=16.0, y=-16.42
    )
    assert test_map.layers[0].opacity == None
    assert test_map.layers[0].properties == None
    assert test_map.layers[0].size == (8, 6)

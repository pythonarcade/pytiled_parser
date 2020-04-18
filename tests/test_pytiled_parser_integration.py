import os
from pathlib import Path

import pytest

import pytiled_parser

TESTS_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
TEST_DATA = TESTS_DIR / "test_data"


def test_map_simple():
    """
    TMX with a very simple spritesheet tile set and some properties.
    """

    test_map = pytiled_parser.parse_tile_map(TEST_DATA / "test_map_simple.tmx")

    # map
    # unsure how to get paths to compare propperly
    assert str(map.parent_dir) == "test_data"
    assert map.version == "1.2"
    assert map.tiled_version == "1.2.3"
    assert map.orientation == "orthogonal"
    assert map.render_order == "right-down"
    assert map.map_size == (8, 6)
    assert map.tile_size == (32, 32)
    assert map.infinite == False
    assert map.next_layer_id == 2
    assert map.next_object_id == 1

    # optional, not for orthogonal maps
    assert map.hex_side_length == None
    assert map.stagger_axis == None
    assert map.stagger_index == None
    assert map.background_color == None

    assert map.properties == {
        "bool property - false": False,
        "bool property - true": True,
        "color property": "#ff49fcff",
        "file property": Path("/var/log/syslog"),
        "float property": 1.23456789,
        "int property": 13,
        "string property": "Hello, World!!",
    }

    # tileset
    assert map.tile_sets[1].name == "tile_set_image"
    assert map.tile_sets[1].max_tile_size == (32, 32)
    assert map.tile_sets[1].spacing == 1
    assert map.tile_sets[1].margin == 1
    assert map.tile_sets[1].tile_count == 48
    assert map.tile_sets[1].columns == 8
    assert map.tile_sets[1].tile_offset == None
    assert map.tile_sets[1].grid == None
    assert map.tile_sets[1].properties == None

    # unsure how to get paths to compare propperly
    assert str(map.tile_sets[1].image.source) == ("images/tmw_desert_spacing.png")
    assert map.tile_sets[1].image.trans == None
    assert map.tile_sets[1].image.size == (265, 199)

    assert map.tile_sets[1].terrain_types == None
    assert map.tile_sets[1].tiles == {}

    # layers
    assert map.layers[0].data == [
        [1, 2, 3, 4, 5, 6, 7, 8],
        [9, 10, 11, 12, 13, 14, 15, 16],
        [17, 18, 19, 20, 21, 22, 23, 24],
        [25, 26, 27, 28, 29, 30, 31, 32],
        [33, 34, 35, 36, 37, 38, 39, 40],
        [41, 42, 43, 44, 45, 46, 47, 48],
    ]
    assert map.layers[0].id_ == 1
    assert map.layers[0].name == "Tile Layer 1"
    assert map.layers[0].offset == None
    assert map.layers[0].opacity == None
    assert map.layers[0].properties == None
    assert map.layers[0].size == (8, 6)


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("#001122", (0x00, 0x11, 0x22, 0xFF)),
        ("001122", (0x00, 0x11, 0x22, 0xFF)),
        ("#FF001122", (0x00, 0x11, 0x22, 0xFF)),
        ("FF001122", (0x00, 0x11, 0x22, 0xFF)),
        ("FF001122", (0x00, 0x11, 0x22, 0xFF)),
    ],
)
def test_color_parsing(test_input, expected):
    """
    Tiled has a few different types of color representations.
    """
    assert pytiled_parser.utilities.parse_color(test_input) == expected

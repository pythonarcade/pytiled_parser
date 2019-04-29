import os

from pathlib import Path

import pytest

import pytiled_parser

print(os.path.dirname(os.path.abspath(__file__)))

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def test_map_simple():
    """
    TMX with a very simple tileset and some properties.
    """
    map = pytiled_parser.parse_tile_map(Path("../test_data/test_map_simple.tmx"))

    properties = {
        "bool property - false": False,
        "bool property - true": True,
        "color property": (0x49, 0xfc, 0xff, 0xff),
        "file property": Path("/var/log/syslog"),
        "float property": 1.23456789,
        "int property": 13,
        "string property": "Hello, World!!"
    }

    assert map.version == "1.2"
    assert map.tiled_version == "1.2.3"
    assert map.orientation == "orthogonal"
    assert map.render_order == "right-down"
    assert map.width == 8
    assert map.height == 6
    assert map.tile_width == 32
    assert map.tile_height == 32
    assert map.infinite == False
    assert map.hex_side_length == None
    assert map.stagger_axis == None
    assert map.stagger_index == None
    assert map.background_color == None
    assert map.next_layer_id == 2
    assert map.next_object_id == 1
    assert map.properties == properties

    assert map.tile_sets[1].name == "tile_set_image"
    assert map.tile_sets[1].tilewidth == 32
    assert map.tile_sets[1].tileheight == 32
    assert map.tile_sets[1].spacing == 1
    assert map.tile_sets[1].margin == 1
    assert map.tile_sets[1].tilecount == 48
    assert map.tile_sets[1].columns == 8
    assert map.tile_sets[1].tileoffset == None
    assert map.tile_sets[1].grid == None
    assert map.tile_sets[1].properties == None
    assert map.tile_sets[1].terraintypes == None
    assert map.tile_sets[1].tiles == {}

    # unsure how to get paths to compare propperly
    assert str(map.tile_sets[1].image.source) == (
        "images/tmw_desert_spacing.png")
    assert map.tile_sets[1].image.trans == None
    assert map.tile_sets[1].image.width == 265
    assert map.tile_sets[1].image.height == 199

    # assert map.layers ==


@pytest.mark.parametrize(
    "test_input,expected", [
        ("#001122", (0x00, 0x11, 0x22, 0xff)),
        ("001122", (0x00, 0x11, 0x22, 0xff)),
        ("#FF001122", (0x00, 0x11, 0x22, 0xff)),
        ("FF001122", (0x00, 0x11, 0x22, 0xff)),
        ("FF001122", (0x00, 0x11, 0x22, 0xff)),
    ]
)
def test_color_parsing(test_input, expected):
    """
    Tiled has a few different types of color representations.
    """
    assert pytiled_parser._parse_color(test_input) == expected

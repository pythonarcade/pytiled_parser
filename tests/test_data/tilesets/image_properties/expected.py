from pathlib import Path

from pytiled_parser import tileset
from pytiled_parser.common_types import Color

EXPECTED = tileset.TileSet(
    columns=8,
    image=Path(r"..\/..\/maps\/images\/tmw_desert_spacing.png"),
    image_height=199,
    image_width=265,
    margin=1,
    spacing=1,
    name="tile_set_image",
    tile_count=48,
    tiled_version="1.3.1",
    tile_height=32,
    tile_width=32,
    version=1.2,
    properties={
        "bool property": True,
        "color property": Color("#ff0000ff"),
        "float property": 5.6,
        "int property": 5,
        "string property": "testing",
    },
)

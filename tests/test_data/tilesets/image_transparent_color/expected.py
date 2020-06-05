from pathlib import Path

from pytiled_parser import tileset
from pytiled_parser.common_types import Color

EXPECTED = tileset.TileSet(
    columns=8,
    image=Path("../../maps/images/tmw_desert_spacing.png"),
    image_height=199,
    image_width=265,
    margin=1,
    spacing=1,
    name="tileset",
    tile_count=48,
    tiled_version="1.3.5",
    tile_height=32,
    tile_width=32,
    version=1.2,
    transparent_color=Color("#ff00ff"),
)

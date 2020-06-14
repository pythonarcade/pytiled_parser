from pathlib import Path

from pytiled_parser import common_types, layer, tileset

EXPECTED = tileset.TileSet(
    columns=8,
    margin=1,
    spacing=1,
    name="tileset",
    image=Path("../../images/tmw_desert_spacing.png"),
    image_height=199,
    image_width=265,
    tile_count=48,
    tiled_version="1.3.5",
    tile_height=32,
    tile_width=32,
    version=1.2,
    type="tileset",
    terrain_types=[
        tileset.Terrain(name="Sand", tile=29),
        tileset.Terrain(name="Cobblestone", tile=29),
        tileset.Terrain(name="Pavement", tile=29),
        tileset.Terrain(name="Dirt", tile=29),
    ],
    tiles=[
        tileset.Tile(
            id=0,
            terrain=tileset.TileTerrain(
                top_left=0, top_right=0, bottom_left=0, bottom_right=1
            ),
        ),
        tileset.Tile(
            id=1,
            terrain=tileset.TileTerrain(
                top_left=0, top_right=0, bottom_left=1, bottom_right=1
            ),
        ),
        tileset.Tile(
            id=2,
            terrain=tileset.TileTerrain(
                top_left=0, top_right=0, bottom_left=1, bottom_right=0
            ),
        ),
        tileset.Tile(
            id=3,
            terrain=tileset.TileTerrain(
                top_left=3, top_right=3, bottom_left=3, bottom_right=0
            ),
        ),
        tileset.Tile(
            id=4,
            terrain=tileset.TileTerrain(
                top_left=3, top_right=3, bottom_left=0, bottom_right=3
            ),
        ),
        tileset.Tile(
            id=5,
            terrain=tileset.TileTerrain(
                top_left=0, top_right=0, bottom_left=0, bottom_right=3
            ),
        ),
        tileset.Tile(
            id=6,
            terrain=tileset.TileTerrain(
                top_left=0, top_right=0, bottom_left=3, bottom_right=3
            ),
        ),
        tileset.Tile(
            id=7,
            terrain=tileset.TileTerrain(
                top_left=0, top_right=0, bottom_left=3, bottom_right=0
            ),
        ),
        tileset.Tile(
            id=8,
            terrain=tileset.TileTerrain(
                top_left=0, top_right=1, bottom_left=0, bottom_right=1
            ),
        ),
        tileset.Tile(
            id=9,
            terrain=tileset.TileTerrain(
                top_left=1, top_right=1, bottom_left=1, bottom_right=1
            ),
        ),
        tileset.Tile(
            id=10,
            terrain=tileset.TileTerrain(
                top_left=1, top_right=0, bottom_left=1, bottom_right=0
            ),
        ),
        tileset.Tile(
            id=11,
            terrain=tileset.TileTerrain(
                top_left=3, top_right=0, bottom_left=3, bottom_right=3
            ),
        ),
        tileset.Tile(
            id=12,
            terrain=tileset.TileTerrain(
                top_left=0, top_right=3, bottom_left=3, bottom_right=3
            ),
        ),
        tileset.Tile(
            id=13,
            terrain=tileset.TileTerrain(
                top_left=0, top_right=3, bottom_left=0, bottom_right=3
            ),
        ),
        tileset.Tile(
            id=14,
            terrain=tileset.TileTerrain(
                top_left=3, top_right=3, bottom_left=3, bottom_right=3
            ),
        ),
        tileset.Tile(
            id=15,
            terrain=tileset.TileTerrain(
                top_left=3, top_right=0, bottom_left=3, bottom_right=0
            ),
        ),
        tileset.Tile(
            id=16,
            terrain=tileset.TileTerrain(
                top_left=0, top_right=1, bottom_left=0, bottom_right=0
            ),
        ),
        tileset.Tile(
            id=17,
            terrain=tileset.TileTerrain(
                top_left=1, top_right=1, bottom_left=0, bottom_right=0
            ),
        ),
        tileset.Tile(
            id=18,
            terrain=tileset.TileTerrain(
                top_left=1, top_right=0, bottom_left=0, bottom_right=0
            ),
        ),
        tileset.Tile(
            id=19,
            terrain=tileset.TileTerrain(
                top_left=1, top_right=1, bottom_left=1, bottom_right=0
            ),
        ),
        tileset.Tile(
            id=20,
            terrain=tileset.TileTerrain(
                top_left=1, top_right=1, bottom_left=0, bottom_right=1
            ),
        ),
        tileset.Tile(
            id=21,
            terrain=tileset.TileTerrain(
                top_left=0, top_right=3, bottom_left=0, bottom_right=0
            ),
        ),
        tileset.Tile(
            id=22,
            terrain=tileset.TileTerrain(
                top_left=3, top_right=3, bottom_left=0, bottom_right=0
            ),
        ),
        tileset.Tile(
            id=23,
            terrain=tileset.TileTerrain(
                top_left=3, top_right=0, bottom_left=0, bottom_right=0
            ),
        ),
        tileset.Tile(
            id=24,
            terrain=tileset.TileTerrain(
                top_left=0, top_right=0, bottom_left=0, bottom_right=2
            ),
        ),
        tileset.Tile(
            id=25,
            terrain=tileset.TileTerrain(
                top_left=0, top_right=0, bottom_left=2, bottom_right=2
            ),
        ),
        tileset.Tile(
            id=26,
            terrain=tileset.TileTerrain(
                top_left=0, top_right=0, bottom_left=2, bottom_right=0
            ),
        ),
        tileset.Tile(
            id=27,
            terrain=tileset.TileTerrain(
                top_left=1, top_right=0, bottom_left=1, bottom_right=1
            ),
        ),
        tileset.Tile(
            id=28,
            terrain=tileset.TileTerrain(
                top_left=0, top_right=1, bottom_left=1, bottom_right=1
            ),
        ),
        tileset.Tile(
            id=29,
            terrain=tileset.TileTerrain(
                top_left=0, top_right=0, bottom_left=0, bottom_right=0
            ),
        ),
        tileset.Tile(
            id=32,
            terrain=tileset.TileTerrain(
                top_left=0, top_right=2, bottom_left=0, bottom_right=2
            ),
        ),
        tileset.Tile(
            id=33,
            terrain=tileset.TileTerrain(
                top_left=2, top_right=2, bottom_left=2, bottom_right=2
            ),
        ),
        tileset.Tile(
            id=34,
            terrain=tileset.TileTerrain(
                top_left=2, top_right=0, bottom_left=2, bottom_right=0
            ),
        ),
        tileset.Tile(
            id=35,
            terrain=tileset.TileTerrain(
                top_left=2, top_right=2, bottom_left=2, bottom_right=0
            ),
        ),
        tileset.Tile(
            id=36,
            terrain=tileset.TileTerrain(
                top_left=2, top_right=2, bottom_left=0, bottom_right=2
            ),
        ),
        tileset.Tile(
            id=40,
            terrain=tileset.TileTerrain(
                top_left=0, top_right=2, bottom_left=0, bottom_right=0
            ),
        ),
        tileset.Tile(
            id=41,
            terrain=tileset.TileTerrain(
                top_left=2, top_right=2, bottom_left=0, bottom_right=0
            ),
        ),
        tileset.Tile(
            id=42,
            terrain=tileset.TileTerrain(
                top_left=2, top_right=0, bottom_left=0, bottom_right=0
            ),
        ),
        tileset.Tile(
            id=43,
            terrain=tileset.TileTerrain(
                top_left=2, top_right=0, bottom_left=2, bottom_right=2
            ),
        ),
        tileset.Tile(
            id=44,
            terrain=tileset.TileTerrain(
                top_left=0, top_right=2, bottom_left=2, bottom_right=2
            ),
        ),
    ],
)

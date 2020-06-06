from pathlib import Path

from pytiled_parser import common_types, tiled_object, tileset

EXPECTED = tileset.TileSet(
    columns=0,
    margin=0,
    spacing=0,
    name="tileset",
    tile_count=4,
    tiled_version="1.3.5",
    tile_height=32,
    tile_width=32,
    version=1.2,
    type="tileset",
    tiles=[
        tileset.Tile(
            animation=[
                tileset.Frame(duration=100, tile_id=0),
                tileset.Frame(duration=100, tile_id=1),
                tileset.Frame(duration=100, tile_id=2),
                tileset.Frame(duration=100, tile_id=3),
            ],
            id=0,
            image=Path("../../images/tile_01.png"),
            image_height=32,
            image_width=32,
            properties={"float property": 2.2},
            type="tile",
        ),
        tileset.Tile(
            id=1,
            image=Path("../../images/tile_02.png"),
            image_height=32,
            image_width=32,
            objects=[
                tiled_object.Rectangle(
                    id=2,
                    size=common_types.Size(14.4766410408043, 13.7196924896511),
                    name="",
                    rotation=0,
                    type="",
                    visible=True,
                    coordinates=common_types.OrderedPair(
                        13.4358367829687, 13.5304553518628
                    ),
                ),
                tiled_object.Ellipse(
                    id=3,
                    size=common_types.Size(14.287403903016, 11.070372560615),
                    name="",
                    rotation=0,
                    type="",
                    visible=True,
                    coordinates=common_types.OrderedPair(
                        13.8143110585452, 1.98698994677705
                    ),
                ),
            ],
        ),
    ],
)

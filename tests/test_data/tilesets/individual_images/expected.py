from pathlib import Path

from pytiled_parser import common_types, layer, tiled_object, tileset

EXPECTED = tileset.Tileset(
    columns=0,
    margin=0,
    spacing=0,
    name="tileset",
    tile_count=5,
    tiled_version="1.9.1",
    tile_height=32,
    tile_width=32,
    firstgid=1,
    version="1.9",
    type="tileset",
    grid=tileset.Grid(orientation="orthogonal", width=1, height=1),
    tiles={
        0: tileset.Tile(
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
            class_="tile",
            width=32,
            height=32,
        ),
        1: tileset.Tile(
            id=1,
            image=Path("../../images/tile_02.png"),
            image_height=32,
            image_width=32,
            objects=layer.ObjectLayer(
                name="",
                opacity=1,
                visible=True,
                draw_order="index",
                tiled_objects=[
                    tiled_object.Rectangle(
                        id=2,
                        name="",
                        size=common_types.Size(14.4766410408043, 13.7196924896511),
                        rotation=0,
                        class_="",
                        visible=True,
                        coordinates=common_types.OrderedPair(
                            13.4358367829687, 13.5304553518628
                        ),
                    ),
                    tiled_object.Ellipse(
                        id=3,
                        name="",
                        size=common_types.Size(14.287403903016, 11.070372560615),
                        rotation=0,
                        class_="",
                        visible=True,
                        coordinates=common_types.OrderedPair(
                            13.8143110585452, 1.98698994677705
                        ),
                    ),
                ],
            ),
            properties={"string property": "testing"},
            class_="tile",
            width=32,
            height=32,
        ),
        2: tileset.Tile(
            id=2,
            image=Path("../../images/tile_03.png"),
            image_height=32,
            image_width=32,
            properties={"bool property": True},
            class_="tile",
            width=32,
            height=32,
        ),
        3: tileset.Tile(
            id=3,
            image=Path("../../images/tile_04.png"),
            image_height=32,
            image_width=32,
            class_="tile",
            width=32,
            height=32,
        ),
        4: tileset.Tile(
            id=4,
            image=Path("../../images/tile_05.png"),
            image_height=32,
            image_width=64,
            x=32,
            y=0,
            width=32,
            height=32
        )
    },
)

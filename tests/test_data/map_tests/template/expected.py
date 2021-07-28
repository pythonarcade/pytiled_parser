from pathlib import Path

from pytiled_parser import common_types, layer, tiled_map, tiled_object, tileset

EXPECTED = tiled_map.TiledMap(
    infinite=False,
    layers=[
        layer.ObjectLayer(
            name="Object Layer 1",
            opacity=1,
            visible=True,
            id=2,
            draw_order="topdown",
            tiled_objects=[
                tiled_object.Rectangle(
                    id=2,
                    name="",
                    rotation=0,
                    size=common_types.Size(63.6585878103079, 38.2811778048473),
                    coordinates=common_types.OrderedPair(
                        98.4987608686521, 46.2385012811358
                    ),
                    visible=True,
                    type="",
                ),
                tiled_object.Tile(
                    id=3,
                    coordinates=common_types.OrderedPair(
                        46.3682110303692, 112.993321292057
                    ),
                    name="",
                    rotation=0,
                    type="",
                    visible=True,
                    size=common_types.Size(32, 32),
                    gid=30,
                ),
                tiled_object.Tile(
                    id=5,
                    coordinates=common_types.OrderedPair(116, 145),
                    name="",
                    rotation=0,
                    type="",
                    visible=True,
                    size=common_types.Size(32, 32),
                    gid=1,
                ),
            ],
        )
    ],
    map_size=common_types.Size(8, 6),
    next_layer_id=3,
    next_object_id=6,
    orientation="orthogonal",
    render_order="right-down",
    tiled_version="1.7.1",
    tile_size=common_types.Size(32, 32),
    version="1.6",
    background_color=common_types.Color(255, 0, 4, 255),
    tilesets={
        1: tileset.Tileset(
            columns=8,
            image=Path(Path(__file__).parent / "../../images/tmw_desert_spacing.png")
            .absolute()
            .resolve(),
            image_width=265,
            image_height=199,
            margin=1,
            spacing=1,
            name="tile_set_image",
            tile_count=48,
            tiled_version="1.6.0",
            tile_height=32,
            tile_width=32,
            version="1.6",
            type="tileset",
        ),
        49: tileset.Tileset(
            columns=0,
            margin=0,
            spacing=0,
            name="tileset_single_image",
            grid=tileset.Grid(orientation="orthogonal", width=1, height=1),
            tiles={
                0: tileset.Tile(
                    id=0,
                    image=Path(Path(__file__).parent / "../../images/tile_01.png")
                    .absolute()
                    .resolve(),
                    image_height=32,
                    image_width=32,
                )
            },
            tile_count=1,
            tiled_version="1.7.1",
            tile_height=32,
            tile_width=32,
            type="tileset",
            version="1.6",
        ),
    },
    properties={
        "bool property - true": True,
        "color property": common_types.Color(73, 252, 255, 255),
        "file property": Path("../../../../../../var/log/syslog"),
        "float property": 1.23456789,
        "int property": 13,
        "string property": "Hello, World!!",
    },
)

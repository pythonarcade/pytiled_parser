{
    "parent_dir": PosixPath(
        "/home/ben/Projects/pytiled_parser/pytiled_parser-venv/pytiled_parser/tests/test_data"
    ),
    "version": "1.2",
    "tiled_version": "1.2.3",
    "orientation": "orthogonal",
    "render_order": "right-down",
    "map_size": Size(width=8, height=6),
    "tile_size": Size(width=32, height=32),
    "infinite": False,
    "next_layer_id": 2,
    "next_object_id": 1,
    "tile_sets": {
        1: TileSet(
            name="tile_set_image",
            max_tile_size=Size(width=32, height=32),
            spacing=1,
            margin=1,
            tile_count=48,
            columns=8,
            tile_offset=None,
            grid=None,
            properties=None,
            image=Image(
                source="images/tmw_desert_spacing.png",
                size=Size(width=265, height=199),
                trans=None,
            ),
            terrain_types=None,
            tiles={
                9: Tile(
                    id=9,
                    type=None,
                    terrain=None,
                    animation=None,
                    image=None,
                    hitboxes=[
                        TiledObject(
                            id=2,
                            location=OrderedPair(x=1.0, y=1.0),
                            size=Size(width=32.0, height=32.0),
                            rotation=1,
                            opacity=1,
                            name="wall",
                            type="rectangle type",
                            properties=None,
                            template=None,
                        )
                    ],
                ),
                19: Tile(
                    id=19,
                    type=None,
                    terrain=None,
                    animation=None,
                    image=None,
                    hitboxes=[
                        TiledObject(
                            id=1,
                            location=OrderedPair(x=32.0, y=1.0),
                            size=Size(width=0, height=0),
                            rotation=1,
                            opacity=1,
                            name="wall corner",
                            type="polygon type",
                            properties=None,
                            template=None,
                        )
                    ],
                ),
                20: Tile(
                    id=20,
                    type=None,
                    terrain=None,
                    animation=None,
                    image=None,
                    hitboxes=[
                        TiledObject(
                            id=1,
                            location=OrderedPair(x=1.45455, y=1.45455),
                            size=Size(width=0, height=0),
                            rotation=1,
                            opacity=1,
                            name="polyline",
                            type="polyline type",
                            properties=None,
                            template=None,
                        )
                    ],
                ),
                31: Tile(
                    id=31,
                    type=None,
                    terrain=None,
                    animation=None,
                    image=None,
                    hitboxes=[
                        TiledObject(
                            id=1,
                            location=OrderedPair(x=5.09091, y=2.54545),
                            size=Size(width=19.6364, height=19.2727),
                            rotation=1,
                            opacity=1,
                            name="rock 1",
                            type="elipse type",
                            properties=None,
                            template=None,
                        ),
                        TiledObject(
                            id=2,
                            location=OrderedPair(x=16.1818, y=22.0),
                            size=Size(width=8.54545, height=8.36364),
                            rotation=-1,
                            opacity=1,
                            name="rock 2",
                            type="elipse type",
                            properties=None,
                            template=None,
                        ),
                    ],
                ),
                45: Tile(
                    id=45,
                    type=None,
                    terrain=None,
                    animation=None,
                    image=None,
                    hitboxes=[
                        TiledObject(
                            id=1,
                            location=OrderedPair(x=14.7273, y=26.3636),
                            size=Size(width=0, height=0),
                            rotation=0,
                            opacity=1,
                            name="sign",
                            type="point type",
                            properties=None,
                            template=None,
                        )
                    ],
                ),
            },
        )
    },
    "layers": [
        TileLayer(
            id=1,
            name="Tile Layer 1",
            offset=None,
            opacity=None,
            properties=None,
            size=Size(width=8, height=6),
            data=[
                [1, 2, 3, 4, 5, 6, 7, 8],
                [9, 10, 11, 12, 13, 14, 15, 16],
                [17, 18, 19, 20, 21, 22, 23, 24],
                [25, 26, 27, 28, 29, 30, 31, 32],
                [33, 34, 35, 36, 37, 38, 39, 40],
                [41, 42, 43, 44, 45, 46, 47, 48],
            ],
        )
    ],
    "hex_side_length": None,
    "stagger_axis": None,
    "stagger_index": None,
    "background_color": None,
    "properties": {
        "bool property - false": False,
        "bool property - true": True,
        "color property": "#ff49fcff",
        "file property": PosixPath("../../../../../../../../var/log/syslog"),
        "float property": 1.23456789,
        "int property": 13,
        "string property": "Hello, World!!",
    },
}
e

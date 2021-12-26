from pathlib import Path

from pytiled_parser import common_types, layer, tiled_map, tileset, world

EXPECTED = world.World(
    only_show_adjacent=False,
    maps=[
        world.WorldMap(
            size=common_types.Size(160, 160),
            coordinates=common_types.OrderedPair(0, 0),
            map_file=Path(Path(__file__).parent / "map_01.json").absolute().resolve(),
        ),
        world.WorldMap(
            size=common_types.Size(160, 160),
            coordinates=common_types.OrderedPair(160, 0),
            map_file=Path(Path(__file__).parent / "map_02.json").absolute().resolve(),
        ),
    ],
)

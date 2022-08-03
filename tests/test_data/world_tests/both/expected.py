from pathlib import Path

from pytiled_parser import common_types, world

EXPECTED = world.World(
    only_show_adjacent=False,
    maps=[
        world.WorldMap(
            size=common_types.Size(160, 160),
            coordinates=common_types.OrderedPair(-160, 0),
            map_file=Path(Path(__file__).parent / "map_manual_one.json")
            .absolute()
            .resolve(),
        ),
        world.WorldMap(
            size=common_types.Size(160, 160),
            coordinates=common_types.OrderedPair(0, 0),
            map_file=Path(Path(__file__).parent / "map_p0-n0.json")
            .absolute()
            .resolve(),
        ),
        world.WorldMap(
            size=common_types.Size(160, 160),
            coordinates=common_types.OrderedPair(0, 160),
            map_file=Path(Path(__file__).parent / "map_p0-n1.json")
            .absolute()
            .resolve(),
        ),
    ],
)

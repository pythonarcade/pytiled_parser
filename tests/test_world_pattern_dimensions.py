import json

import pytest

from pytiled_parser import parse_world
from pytiled_parser.common_types import OrderedPair, Size


@pytest.mark.parametrize(
    "dimensions, expected",
    [
        ({}, Size(100, 200)),
        ({"mapWidth": 80}, Size(80, 200)),
        ({"mapHeight": 160}, Size(100, 160)),
        ({"mapWidth": 80, "mapHeight": 160}, Size(80, 160)),
        ({"mapWidth": 0}, Size(0, 200)),
        ({"mapHeight": 0}, Size(100, 0)),
    ],
)
def test_world_pattern_dimensions(tmp_path, dimensions, expected):
    map_file = tmp_path / "map_-2_3.tmx"
    map_file.touch()
    (tmp_path / "unrelated.txt").touch()
    pattern = {
        "regexp": r"^map_(-?\d+)_(-?\d+)\.tmx$",
        "multiplierX": 100,
        "multiplierY": 200,
        "offsetX": 7,
        "offsetY": 11,
    }
    pattern.update(dimensions)
    world_file = tmp_path / "maps.world"
    world_data = {"patterns": [pattern], "type": "world"}
    world_data["onlyShowAdjacentMaps"] = True
    world_file.write_text(
        json.dumps(world_data),
        encoding="utf-8",
    )

    parsed = parse_world(world_file)
    assert parsed.only_show_adjacent
    assert len(parsed.maps) == 1
    parsed_map = parsed.maps[0]
    assert parsed_map.map_file == map_file
    assert parsed_map.size == expected
    assert parsed_map.coordinates == OrderedPair(-193, 611)

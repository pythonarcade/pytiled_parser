import json
import xml.etree.ElementTree as etree
from pathlib import Path

import pytest

from pytiled_parser import parse_tileset

TERRAIN = Path(__file__).parent / "test_data" / "tilesets" / "terrain"


@pytest.mark.parametrize("parser_type", ["json", "tmx"])
@pytest.mark.parametrize(
    "set_class,color_class",
    [
        (None, None),
        ("TerrainSet", None),
        (None, "Ground"),
        ("", None),
        (None, ""),
        ("TerrainSet", "Ground"),
        ("", ""),
    ],
)
def test_tileset_wang_classes(tmp_path, parser_type, set_class, color_class):
    if parser_type == "json":
        source = json.loads((TERRAIN / "tileset.json").read_text())
        wang_set = source["wangsets"][0]
        if set_class is not None:
            wang_set["class"] = set_class
        if color_class is not None:
            wang_set["colors"][0]["class"] = color_class
        path = tmp_path / "tileset.json"
        path.write_text(json.dumps(source))
    else:
        source = etree.parse(TERRAIN / "tileset.tsx")
        wang_set = source.find("./wangsets/wangset")
        if set_class is not None:
            wang_set.set("class", set_class)
        if color_class is not None:
            wang_set.find("./wangcolor").set("class", color_class)
        path = tmp_path / "tileset.tsx"
        source.write(path)

    parsed = parse_tileset(path).wang_sets[0]
    assert parsed.class_ == set_class
    assert parsed.wang_colors[0].class_ == color_class
    assert all(color.class_ is None for color in parsed.wang_colors[1:])
    assert parsed.name == "Terrains"
    assert parsed.wang_type == "mixed"
    assert parsed.tile == -1
    assert parsed.properties == {"test": "this is a test"}
    assert parsed.wang_colors[3].properties == {"test": "this is a test"}
    assert parsed.wang_colors[0].probability == 1
    assert parsed.wang_tiles[0].wang_id == [1, 1, 0, 2, 0, 1, 1, 1]

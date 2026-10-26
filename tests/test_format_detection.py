import json

import pytest

from pytiled_parser import UnknownFormat, parse_map
from pytiled_parser.common_types import Size

MAP = {
    "version": "1.9",
    "tiledversion": "1.9.1",
    "orientation": "orthogonal",
    "renderorder": "right-down",
    "width": 1,
    "height": 1,
    "tilewidth": 16,
    "tileheight": 16,
    "infinite": False,
    "nextlayerid": 1,
    "nextobjectid": 1,
    "layers": [],
    "tilesets": [],
}

TMX = (
    '<map version="1.9" tiledversion="1.9.1" orientation="orthogonal" '
    'renderorder="right-down" width="1" height="1" tilewidth="16" '
    'tileheight="16" infinite="0" nextlayerid="1" nextobjectid="1"/>'
)


@pytest.mark.parametrize("prefix", ["", "\n", "\r\n\r\n", " \t\n\n"])
@pytest.mark.parametrize("format_", ["json", "tmx"])
def test_leading_blank_lines(tmp_path, prefix, format_):
    map_file = tmp_path / ("map." + format_)
    content = json.dumps(MAP) if format_ == "json" else TMX
    map_file.write_text(prefix + content, encoding="utf-8")
    parsed = parse_map(map_file)
    assert parsed.map_size == Size(1, 1)
    assert parsed.tile_size == Size(16, 16)
    assert parsed.layers == []


@pytest.mark.parametrize("content", ["", "\n", " \t\n\r\n"])
def test_empty_map_has_format_error(tmp_path, content):
    map_file = tmp_path / "map.json"
    map_file.write_text(content, encoding="utf-8")
    with pytest.raises(UnknownFormat):
        parse_map(map_file)

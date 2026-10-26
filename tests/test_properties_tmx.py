import xml.etree.ElementTree as etree

import pytest

from pytiled_parser import parse_map
from pytiled_parser.layer import ObjectLayer
from pytiled_parser.parsers.json.properties import parse as parse_json
from pytiled_parser.parsers.tmx.properties import parse as parse_tmx
from pytiled_parser.properties import ClassProperty


@pytest.mark.parametrize("object_id", [0, 1, 42, 2147483647])
def test_object_reference_ids(object_id):
    properties = etree.fromstring(
        '<properties><property name="target" type="object" '
        f'value="{object_id}"/></properties>'
    )
    parsed = parse_tmx(properties)
    raw_property = {"name": "target", "type": "object", "value": object_id}
    expected = parse_json([raw_property])
    assert parsed == expected
    assert type(parsed["target"]) is int


def test_object_reference_in_class():
    properties = etree.fromstring(
        '<properties><property name="spawn" type="class" propertytype="Spawn">'
        '<properties><property name="target" type="object" value="42"/>'
        "</properties></property></properties>"
    )
    parsed = parse_tmx(properties)["spawn"]
    assert isinstance(parsed, ClassProperty)
    assert parsed.propertytype == "Spawn"
    assert parsed["target"] == 42


def test_map_object_reference_lookup(tmp_path):
    map_file = tmp_path / "objects.tmx"
    map_file.write_text(
        '<map version="1.10" tiledversion="1.10.2" orientation="orthogonal" '
        'renderorder="right-down" width="1" height="1" tilewidth="16" '
        'tileheight="16" infinite="0" nextlayerid="2" nextobjectid="3">'
        '<objectgroup id="1" name="objects"><object id="1" x="0" y="0">'
        '<properties><property name="target" type="object" value="2"/>'
        '<property name="unset" type="object" value="0"/></properties>'
        '</object><object id="2" x="16" y="0"/></objectgroup></map>',
        encoding="utf-8",
    )
    layer = parse_map(map_file).layers[0]
    assert isinstance(layer, ObjectLayer)
    source, target = layer.tiled_objects
    objects_by_id = {obj.id: obj for obj in layer.tiled_objects}
    assert objects_by_id[source.properties["target"]] is target
    assert source.properties["unset"] == 0

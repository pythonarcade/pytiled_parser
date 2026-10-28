"""Layer offset axes are independently optional in both map formats."""

import xml.etree.ElementTree as etree

import pytest

from pytiled_parser.common_types import OrderedPair
from pytiled_parser.parsers.json.layer import parse as parse_json
from pytiled_parser.parsers.tmx.layer import parse as parse_tmx


@pytest.mark.parametrize("parser_type", ["json", "tmx"])
@pytest.mark.parametrize(
    "layer_type", ["tilelayer", "objectgroup", "imagelayer", "group"]
)
@pytest.mark.parametrize(
    "offsets,expected",
    [
        ({}, (0, 0)),
        ({"offsetx": 17.5}, (17.5, 0)),
        ({"offsety": -6.25}, (0, -6.25)),
        ({"offsetx": 0}, (0, 0)),
        ({"offsety": 0}, (0, 0)),
        ({"offsetx": 0, "offsety": -6.25}, (0, -6.25)),
        ({"offsetx": -17.5, "offsety": 6.25}, (-17.5, 6.25)),
    ],
)
def test_independent_layer_offsets(parser_type, layer_type, offsets, expected):
    if parser_type == "json":
        raw = {
            "name": "test",
            "type": layer_type,
            "opacity": 1,
            "visible": True,
            **offsets,
        }
        if layer_type == "tilelayer":
            raw.update(width=1, height=1, data=[0])
        elif layer_type == "objectgroup":
            raw.update(objects=[], draworder="topdown")
        elif layer_type == "imagelayer":
            raw["image"] = "background.png"
        else:
            raw["layers"] = []
        # Exercise recursive parsing as well as each concrete layer parser.
        group = parse_json(
            {
                "name": "parent",
                "type": "group",
                "opacity": 1,
                "visible": True,
                "layers": [raw],
            },
            encoding="utf-8",
        )
    else:
        parent = etree.Element("group", name="parent")
        tag = "layer" if layer_type == "tilelayer" else layer_type
        raw = etree.SubElement(parent, tag, name="test")
        raw.attrib.update({key: str(value) for key, value in offsets.items()})
        if layer_type == "tilelayer":
            raw.attrib.update(width="1", height="1")
            etree.SubElement(raw, "data", encoding="csv").text = "0"
        elif layer_type == "imagelayer":
            etree.SubElement(raw, "image", source="background.png")
        group = parse_tmx(parent, encoding="utf-8")

    assert group.offset == OrderedPair(0, 0)
    assert group.layers[0].offset == OrderedPair(*expected)

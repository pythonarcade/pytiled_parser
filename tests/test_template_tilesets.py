"""Tilesets supplied by object templates must also work without map tilesets."""

import copy
import json
import xml.etree.ElementTree as etree
from pathlib import Path

import pytest

from pytiled_parser import parse_map

TEMPLATE_DATA = Path(__file__).parent / "test_data" / "map_tests" / "template"


@pytest.mark.parametrize("group_depth", [0, 1, 3])
@pytest.mark.parametrize("format_", ["json", "tmx"])
@pytest.mark.parametrize("with_map_tilesets", [False, True])
def test_template_tileset_allocation(tmp_path, format_, with_map_tilesets, group_depth):
    source = TEMPLATE_DATA / ("map." + format_)
    destination = tmp_path / source.name
    if format_ == "json":
        document = json.loads(source.read_text())
        if with_map_tilesets:
            for tileset in document["tilesets"]:
                tileset["source"] = str((TEMPLATE_DATA / tileset["source"]).resolve())
        else:
            document["tilesets"] = []
        document["nextobjectid"] = 9
        objects = document["layers"][0]["objects"]
        objects.append(copy.deepcopy(objects[1]))
        objects[-1]["id"] = 8
        for object_ in objects:
            object_["template"] = str((TEMPLATE_DATA / object_["template"]).resolve())
        for depth in range(group_depth):
            document["layers"] = [
                {
                    "id": 3 + depth,
                    "name": "group",
                    "type": "group",
                    "opacity": 1,
                    "visible": True,
                    "x": 0,
                    "y": 0,
                    "layers": document["layers"],
                }
            ]
        document["nextlayerid"] = 3 + group_depth
        destination.write_text(json.dumps(document))
    else:
        document = etree.parse(source)
        for tileset in document.findall("tileset"):
            if with_map_tilesets:
                tileset.set(
                    "source", str((TEMPLATE_DATA / tileset.get("source")).resolve())
                )
            else:
                document.getroot().remove(tileset)
        document.getroot().set("nextobjectid", "9")
        layer = document.find("objectgroup")
        repeated = copy.deepcopy(layer.findall("object")[1])
        repeated.set("id", "8")
        layer.append(repeated)
        for object_ in layer.findall("object"):
            object_.set(
                "template", str((TEMPLATE_DATA / object_.get("template")).resolve())
            )
        document.getroot().remove(layer)
        for depth in range(group_depth):
            group = etree.Element("group", id=str(3 + depth), name="group")
            group.append(layer)
            layer = group
        document.getroot().append(layer)
        document.getroot().set("nextlayerid", str(3 + group_depth))
        document.write(destination, encoding="utf-8")

    parsed = parse_map(destination)
    layer = parsed.layers[0]
    for _ in range(group_depth):
        layer = layer.layers[0]
    objects = layer.tiled_objects
    expected_gids = [49, 50, 49] if with_map_tilesets else [1, 2, 1]
    assert [object_.gid for object_ in objects[1:]] == expected_gids
    assert sorted(parsed.tilesets) == ([1, 49, 50] if with_map_tilesets else [1, 2])
    for gid, name in zip(
        expected_gids,
        [
            "tile_set_image_for_template",
            "tile_set_single_image",
            "tile_set_image_for_template",
        ],
    ):
        assert parsed.tilesets[gid].name == name
        assert parsed.tilesets[gid].firstgid == gid
        assert (
            parsed.tilesets[gid].image is not None
            or parsed.tilesets[gid].tiles[0].image is not None
        )
    assert all(object_.new_tileset is None for object_ in objects[1:])

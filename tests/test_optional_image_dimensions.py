"""Image dimensions are optional in TSX, just as in JSON tilesets."""

import json
import xml.etree.ElementTree as etree
from pathlib import Path

import pytest

from pytiled_parser import parse_tileset


@pytest.mark.parametrize("format_", ["json", "tsx"])
@pytest.mark.parametrize("collection", [False, True])
@pytest.mark.parametrize(
    "dimensions", [{}, {"width": 32}, {"height": 16}, {"width": 32, "height": 16}]
)
def test_optional_image_dimensions(tmp_path, format_, collection, dimensions):
    attributes = {
        "name": "test",
        "spacing": 0,
        "margin": 0,
        "tilecount": 1,
        "tilewidth": 32,
        "tileheight": 16,
        "columns": 0 if collection else 1,
    }
    filename = tmp_path / ("tileset." + format_)
    if format_ == "json":
        image = {"image": "tile.png"}
        image.update({"image" + key: value for key, value in dimensions.items()})
        if collection:
            attributes["tiles"] = [dict(image, id=0)]
        else:
            attributes.update(image)
        filename.write_text(json.dumps(attributes), encoding="utf-8")
    else:
        root = etree.Element(
            "tileset", {key: str(value) for key, value in attributes.items()}
        )
        parent = etree.SubElement(root, "tile", id="0") if collection else root
        etree.SubElement(
            parent,
            "image",
            source="tile.png",
            **{key: str(value) for key, value in dimensions.items()},
        )
        etree.ElementTree(root).write(filename, encoding="utf-8")

    tileset = parse_tileset(filename)
    image = tileset.tiles[0] if collection else tileset
    assert image.image == Path("tile.png")
    assert image.image_width == dimensions.get("width")
    assert image.image_height == dimensions.get("height")
    if collection:
        assert image.width == dimensions.get("width", 0)
        assert image.height == dimensions.get("height", 0)
    assert tileset.tile_width == 32
    assert tileset.tile_height == 16

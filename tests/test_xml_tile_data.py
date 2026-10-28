"""Read XML tile elements and retain parity with encoded layer data."""

import base64
import gzip
import struct
import xml.etree.ElementTree as etree
import zlib

import pytest

from pytiled_parser import parse_map
from pytiled_parser.common_types import OrderedPair, Size


def add_data(parent, gids, encoding):
    if encoding.startswith("xml"):
        if encoding == "xml_pretty":
            parent.text = "\n  "
        for gid in gids:
            # The documented default for a missing gid is an empty cell.
            tile = etree.SubElement(parent, "tile", {"gid": str(gid)} if gid else {})
            if encoding == "xml_pretty":
                tile.tail = "\n  "
    elif encoding == "csv":
        parent.text = ",".join(str(gid) for gid in gids)
    else:
        data = struct.pack(f"<{len(gids)}I", *gids)
        if encoding == "gzip":
            data = gzip.compress(data)
        elif encoding == "zlib":
            data = zlib.compress(data)
        parent.text = base64.b64encode(data).decode("ascii")


@pytest.mark.parametrize(
    "encoding", ["xml", "xml_pretty", "csv", "base64", "gzip", "zlib"]
)
@pytest.mark.parametrize("infinite", [False, True])
def test_tile_data_formats(tmp_path, encoding, infinite):
    root = etree.Element(
        "map",
        version="1.9",
        tiledversion="1.9.0",
        orientation="orthogonal",
        renderorder="right-down",
        width="2",
        height="2",
        tilewidth="32",
        tileheight="32",
        infinite=str(int(infinite)),
        nextlayerid="2",
        nextobjectid="1",
    )
    tileset = etree.SubElement(
        root,
        "tileset",
        firstgid="1",
        name="tiles",
        tilewidth="32",
        tileheight="32",
        tilecount="1",
        columns="1",
    )
    etree.SubElement(tileset, "image", source="tiles.png", width="32", height="32")
    layer = etree.SubElement(
        root, "layer", id="1", name="ground", width="2", height="2"
    )
    data = etree.SubElement(layer, "data")
    if not encoding.startswith("xml"):
        data.set("encoding", "csv" if encoding == "csv" else "base64")
        if encoding in ("gzip", "zlib"):
            data.set("compression", encoding)

    # Keep zero cells and every high GID flag bit intact, including the fourth flag.
    gids = [0, 0, 0x80000001, 0xF0000001]
    if infinite:
        first = etree.SubElement(data, "chunk", x="-2", y="3", width="2", height="2")
        second = etree.SubElement(data, "chunk", x="4", y="-5", width="1", height="3")
        add_data(first, gids, encoding)
        add_data(second, [1, 0, 0x40000001], encoding)
    else:
        add_data(data, gids, encoding)

    path = tmp_path / "map.tmx"
    path.write_bytes(etree.tostring(root))
    parsed = parse_map(path)
    result = parsed.layers[0]
    expected = [[0, 0], [0x80000001, 0xF0000001]]
    assert parsed.infinite == infinite
    assert result.name == "ground"
    if infinite:
        assert result.data is None
        assert len(result.chunks) == 2
        assert result.chunks[0].coordinates == OrderedPair(-2, 3)
        assert result.chunks[0].size == Size(2, 2)
        assert result.chunks[0].data == expected
        assert result.chunks[1].coordinates == OrderedPair(4, -5)
        assert result.chunks[1].size == Size(1, 3)
        assert result.chunks[1].data == [[1], [0], [0x40000001]]
    else:
        assert result.chunks is None
        assert result.data == expected

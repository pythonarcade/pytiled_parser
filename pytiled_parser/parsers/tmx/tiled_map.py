import xml.etree.ElementTree as etree
from pathlib import Path

from pytiled_parser.common_types import OrderedPair, Size
from pytiled_parser.parsers.tmx.tileset import parse as parse_tileset
from pytiled_parser.tiled_map import TiledMap, TilesetDict


def parse(file: Path) -> TiledMap:
    """Parse the raw Tiled map into a pytiled_parser type.

    Args:
        file: Path to the map file.

    Returns:
        TiledMap: A parsed TiledMap.
    """
    with open(file) as map_file:
        raw_map = etree.parse(map_file).getroot()

    parent_dir = file.parent

    raw_tilesets = raw_map.findall("./tileset")
    tilesets: TilesetDict = {}

    for raw_tileset in raw_tilesets:
        if raw_tileset.attrib.get("source") is not None:
            # Is an external Tileset
            tileset_path = Path(parent_dir / raw_tileset.attrib["source"])
            with open(tileset_path) as tileset_file:
                raw_tileset = etree.parse(tileset_file).getroot()

            tilesets[int(raw_tileset.attrib["firstgid"])] = parse_tileset(
                raw_tileset,
                int(raw_tileset.attrib["firstgid"]),
                external_path=tileset_path.parent,
            )
        else:
            # Is an embedded Tileset
            tilesets[int(raw_tileset.attrib["firstgid"])] = parse_tileset(
                raw_tileset, int(raw_tileset.attrib["firstgid"])
            )

    map_ = TiledMap(
        map_file=file,
        infinite=bool(int(raw_map.attrib["infinite"])),
        layers=[parse_layer(layer_, parent_dir) for layer_ in raw_tiled_map["layers"]],
        map_size=Size(int(raw_map.attrib["width"]), int(raw_map.attrib["height"])),
        next_layer_id=int(raw_map.attrib["nextlayerid"]),
        next_object_id=int(raw_map.attrib["nextobjectid"]),
        orientation=raw_map.attrib["orientation"],
        render_order=raw_map.attrib["renderorder"],
        tiled_version=raw_map.attrib["tiledversion"],
        tile_size=Size(
            int(raw_map.attrib["tilewidth"]), int(raw_map.attrib["tileheight"])
        ),
        tilesets=tilesets,
        version=raw_map.attrib["version"],
    )

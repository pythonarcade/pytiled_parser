# pylint: disable=too-few-public-methods

import json
from pathlib import Path
from typing import Dict, List, Optional, Union
from typing import cast as typing_cast

import attr
from typing_extensions import TypedDict

from . import layer, properties, tileset
from .common_types import Color, Size
from .layer import Layer, RawLayer
from .properties import Properties, RawProperty
from .tileset import RawTileSet, Tileset
from .util import parse_color

TilesetDict = Dict[int, Tileset]


@attr.s(auto_attribs=True)
class TiledMap:
    """Object for storing a TMX with all associated layers and properties.

    See: https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#map

    Attributes:
        infinite: If the map is infinite or not.
        layers: List of layer objects by draw order.
        map_size: The map width in tiles.
        next_layer_id: Stores the next available ID for new layers.
        next_object_id: Stores the next available ID for new objects.
        orientation: Map orientation. Tiled supports "orthogonal", "isometric",
            "staggered" and "hexagonal"
        render_order: The order in which tiles on tile layers are rendered. Valid values
            are right-down, right-up, left-down and left-up. In all cases, the map is
        tiled_version: The Tiled version used to save the file. May be a date (for
            snapshot builds).
            drawn row-by-row. (only supported for orthogonal maps at the moment)
        tile_size: The size of a tile.
        tilesets: Dict of Tileset where Key is the firstgid and the value is the Tileset
        version: The JSON format version.
        background_color: The background color of the map.
        properties: The properties of the Map.
        hex_side_length: Only for hexagonal maps. Determines the width or height
            (depending on the staggered axis) of the tile's edge, in pixels.
        stagger_axis: For staggered and hexagonal maps, determines which axis ("x" or
            "y") is staggered.
        stagger_index: For staggered and hexagonal maps, determines whether the "even"
            or "odd" indexes along the staggered axis are shifted.
    """

    infinite: bool
    layers: List[Layer]
    map_size: Size
    next_layer_id: Optional[int]
    next_object_id: int
    orientation: str
    render_order: str
    tiled_version: str
    tile_size: Size
    tilesets: TilesetDict
    version: str

    map_file: Optional[Path] = None
    background_color: Optional[Color] = None
    properties: Optional[Properties] = None
    hex_side_length: Optional[int] = None
    stagger_axis: Optional[str] = None
    stagger_index: Optional[str] = None


class _RawTilesetMapping(TypedDict):
    """ The way that tilesets are stored in the Tiled JSON formatted map."""

    firstgid: int
    source: str


class _RawTiledMap(TypedDict):
    """The keys and their types that appear in a Tiled JSON Map.

    Keys:
        compressionlevel: not documented - https://github.com/bjorn/tiled/issues/2815
    """

    backgroundcolor: str
    compressionlevel: int
    height: int
    hexsidelength: int
    infinite: bool
    layers: List[RawLayer]
    nextlayerid: int
    nextobjectid: int
    orientation: str
    properties: List[RawProperty]
    renderorder: str
    staggeraxis: str
    staggerindex: str
    tiledversion: str
    tileheight: int
    tilesets: List[_RawTilesetMapping]
    tilewidth: int
    type: str
    version: Union[str, float]
    width: int


def parse_map(file: Path) -> TiledMap:
    """Parse the raw Tiled map into a pytiled_parser type

    Args:
        file: Path to the map's JSON file

    Returns:
        TileSet: a properly typed TileSet.
    """

    with open(file) as map_file:
        raw_tiled_map = json.load(map_file)

    parent_dir = file.parent

    raw_tilesets: List[Union[RawTileSet, _RawTilesetMapping]] = raw_tiled_map[
        "tilesets"
    ]
    tilesets: TilesetDict = {}

    for raw_tileset in raw_tilesets:
        if raw_tileset.get("source") is not None:
            # Is an external Tileset
            tileset_path = Path(parent_dir / raw_tileset["source"])
            with open(tileset_path) as raw_tileset_file:
                tilesets[raw_tileset["firstgid"]] = tileset.cast(
                    json.load(raw_tileset_file),
                    raw_tileset["firstgid"],
                    external_path=tileset_path.parent,
                )
        else:
            # Is an embedded Tileset
            raw_tileset = typing_cast(RawTileSet, raw_tileset)
            tilesets[raw_tileset["firstgid"]] = tileset.cast(
                raw_tileset, raw_tileset["firstgid"]
            )

    if isinstance(raw_tiled_map["version"], float):
        version = str(raw_tiled_map["version"])
    else:
        version = raw_tiled_map["version"]

    # `map` is a built-in function
    map_ = TiledMap(
        map_file=file,
        infinite=raw_tiled_map["infinite"],
        layers=[layer.cast(layer_, parent_dir) for layer_ in raw_tiled_map["layers"]],
        map_size=Size(raw_tiled_map["width"], raw_tiled_map["height"]),
        next_layer_id=raw_tiled_map["nextlayerid"],
        next_object_id=raw_tiled_map["nextobjectid"],
        orientation=raw_tiled_map["orientation"],
        render_order=raw_tiled_map["renderorder"],
        tiled_version=raw_tiled_map["tiledversion"],
        tile_size=Size(raw_tiled_map["tilewidth"], raw_tiled_map["tileheight"]),
        tilesets=tilesets,
        version=version,
    )

    layers = [layer for layer in map_.layers if hasattr(layer, "tiled_objects")]

    for my_layer in layers:
        for tiled_object in my_layer.tiled_objects:  # type: ignore
            if hasattr(tiled_object, "new_tileset"):
                if tiled_object.new_tileset:
                    already_loaded = None
                    for val in map_.tilesets.values():
                        if val.name == tiled_object.new_tileset["name"]:
                            already_loaded = val
                            break

                    if not already_loaded:
                        highest_firstgid = max(map_.tilesets.keys())
                        last_tileset_count = map_.tilesets[highest_firstgid].tile_count
                        new_firstgid = highest_firstgid + last_tileset_count
                        map_.tilesets[new_firstgid] = tileset.cast(
                            tiled_object.new_tileset,
                            new_firstgid,
                            tiled_object.new_tileset_path,
                        )
                        tiled_object.gid = tiled_object.gid + (new_firstgid - 1)

                    else:
                        tiled_object.gid = tiled_object.gid + (
                            already_loaded.firstgid - 1
                        )

                    tiled_object.new_tileset = None
                    tiled_object.new_tileset_path = None

    if raw_tiled_map.get("backgroundcolor") is not None:
        map_.background_color = parse_color(raw_tiled_map["backgroundcolor"])

    if raw_tiled_map.get("hexsidelength") is not None:
        map_.hex_side_length = raw_tiled_map["hexsidelength"]

    if raw_tiled_map.get("properties") is not None:
        map_.properties = properties.cast(raw_tiled_map["properties"])

    if raw_tiled_map.get("staggeraxis") is not None:
        map_.stagger_axis = raw_tiled_map["staggeraxis"]

    if raw_tiled_map.get("staggerindex") is not None:
        map_.stagger_index = raw_tiled_map["staggerindex"]

    return map_

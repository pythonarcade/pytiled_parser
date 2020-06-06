# pylint: disable=too-few-public-methods

from pathlib import Path
from typing import Dict, List, NamedTuple, Optional, Union

import attr
from typing_extensions import TypedDict

from .common_types import Color, Size
from .layer import Layer, RawLayer
from .properties import Properties, RawProperty
from .tileset import RawTileSet, TileSet

TileSetDict = Dict[int, TileSet]


@attr.s(auto_attribs=True)
class Map:
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
        tile_size: The width of a tile.
        tile_sets: Tilesets used in this map.
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
    tile_sets: List[TileSet]
    version: str

    background_color: Optional[Color] = None
    properties: Optional[Properties] = None
    hex_side_length: Optional[int] = None
    stagger_axis: Optional[int] = None
    stagger_index: Optional[int] = None


class _RawTiledMap(TypedDict):
    """ The keys and their types that appear in a Tiled JSON Map.
    
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
    tilesets: List[RawTileSet]
    tilewidth: int
    type: str
    version: str
    width: int


def cast(raw_tiled_map: _RawTiledMap) -> Map:
    """ Cast the raw Tiled map into a pytiled_parser type

    Args:
        raw_tiled_map: Raw JSON Formatted Tiled Map to be cast.

    Returns:
        TileSet: a properly typed TileSet.
    """

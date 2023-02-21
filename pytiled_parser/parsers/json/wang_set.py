from typing import List, Optional

from typing_extensions import NotRequired, TypedDict

from pytiled_parser.parsers.json.properties import RawProperty
from pytiled_parser.parsers.json.properties import parse as parse_properties
from pytiled_parser.parsers.json.properties import serialize as serialize_properties
from pytiled_parser.util import parse_color, serialize_color
from pytiled_parser.wang_set import WangColor, WangSet, WangTile

RawWangTile = TypedDict(
    "RawWangTile",
    {
        "tileid": int,
        # Tiled stores these IDs as a list represented like so:
        # [top, top_right, right, bottom_right, bottom, bottom_left, left, top_left]
        "wangid": List[int],
    },
)
RawWangTile.__doc__ = """
    The keys and their types that appear in a Wang Tile JSON Object.
"""


RawWangColor = TypedDict(
    "RawWangColor",
    {
        "color": str,
        "class": Optional[str],
        "name": str,
        "probability": float,
        "tile": int,
        "properties": List[RawProperty],
    },
)
RawWangColor.__doc__ = """
    The keys and their types that appear in a Wang Color JSON Object.
"""


RawWangSet = TypedDict(
    "RawWangSet",
    {
        "colors": List[RawWangColor],
        "class": Optional[str],
        "name": str,
        "properties": List[RawProperty],
        "tile": int,
        "type": NotRequired[str],
        "wangtiles": List[RawWangTile],
    },
)
RawWangSet.__doc__ = """
    The keys and their types that appear in a Wang Set JSON Object.
"""


def _parse_wang_tile(raw_wang_tile: RawWangTile) -> WangTile:
    """Parse the raw wang tile into a pytiled_parser type

    Args:
        raw_wang_tile: RawWangTile to be parsed.

    Returns:
        WangTile: A properly typed WangTile.
    """
    return WangTile(tile_id=raw_wang_tile["tileid"], wang_id=raw_wang_tile["wangid"])


def _serialize_wang_tile(wang_tile: WangTile) -> RawWangTile:
    """Serialize the pytiled_parser WangTile into a RawWangTile

    Args:
        wang_tile: WangTile to be serialized.

    Returns:
        RawWangTile: The serialized WangTile.
    """
    return {"tileid": wang_tile.tile_id, "wangid": wang_tile.wang_id}


def _parse_wang_color(raw_wang_color: RawWangColor) -> WangColor:
    """Parse the raw wang color into a pytiled_parser type

    Args:
        raw_wang_color: RawWangColor to be parsed.

    Returns:
        WangColor: A properly typed WangColor.
    """
    wang_color = WangColor(
        name=raw_wang_color["name"],
        color=parse_color(raw_wang_color["color"]),
        tile=raw_wang_color["tile"],
        probability=raw_wang_color["probability"],
    )

    if raw_wang_color.get("properties") is not None:
        wang_color.properties = parse_properties(raw_wang_color["properties"])

    return wang_color


def _serialize_wang_color(wang_color: WangColor) -> RawWangColor:
    """Serialize the WangColor into a RawWangColor

    Args:
        wang_color: WangColor to be serialized.

    Returns:
        RawWangColor: The serialized WangColor.
    """
    if wang_color.properties:
        properties = serialize_properties(wang_color.properties)
    else:
        properties = None

    return {
        "color": serialize_color(wang_color.color),
        "class": wang_color.class_,
        "name": wang_color.name,
        "probability": wang_color.probability,
        "tile": wang_color.tile,
        "properties": properties,
    }


def parse(raw_wangset: RawWangSet) -> WangSet:
    """Parse the raw wangset into a pytiled_parser type

    Args:
        raw_wangset: Raw Wangset to be parsed.

    Returns:
        WangSet: A properly typed WangSet.
    """

    colors = []
    for raw_wang_color in raw_wangset["colors"]:
        colors.append(_parse_wang_color(raw_wang_color))

    tiles = {}
    for raw_wang_tile in raw_wangset["wangtiles"]:
        tiles[raw_wang_tile["tileid"]] = _parse_wang_tile(raw_wang_tile)

    wangset = WangSet(
        name=raw_wangset["name"],
        tile=raw_wangset["tile"],
        wang_type=raw_wangset["type"],
        wang_colors=colors,
        wang_tiles=tiles,
    )

    if raw_wangset.get("properties") is not None:
        wangset.properties = parse_properties(raw_wangset["properties"])

    return wangset


def serialize(wangset: WangSet) -> RawWangSet:
    raw_wang_colors: List[RawWangColor] = []

    for color in wangset.wang_colors:
        raw_wang_colors.append(_serialize_wang_color(color))

    raw_wang_tiles: List[RawWangTile] = []

    for tile in wangset.wang_tiles.values():
        raw_wang_tiles.append(_serialize_wang_tile(tile))

    if wangset.properties:
        properties = serialize_properties(wangset.properties)
    else:
        properties = None

    raw_wang_set: RawWangSet = {
        "colors": raw_wang_colors,
        "class": wangset.class_,
        "name": wangset.name,
        "properties": properties,
        "tile": wangset.tile,
        "wangtiles": raw_wang_tiles,
    }

    return raw_wang_set

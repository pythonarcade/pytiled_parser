from typing import List, Optional

import attr
from typing_extensions import TypedDict

from . import properties as properties_
from .common_types import Color
from .util import parse_color


@attr.s(auto_attribs=True)
class WangTile:

    tile_id: int
    wang_id: List[int]


@attr.s(auto_attribs=True)
class WangColor:

    color: Color
    name: str
    probability: float
    tile: int
    properties: Optional[properties_.Properties] = None


@attr.s(auto_attribs=True)
class WangSet:

    name: str
    tile: int
    wang_tiles: List[WangTile]
    wang_colors: List[WangColor]
    properties: Optional[properties_.Properties] = None


class RawWangTile(TypedDict):
    """ The keys and their types that appear in a Wang Tile JSON Object."""

    tileid: int
    wangid: List[int]


class RawWangColor(TypedDict):
    """ The keys and their types that appear in a Wang Color JSON Object."""

    color: str
    name: str
    probability: float
    tile: int
    properties: List[properties_.RawProperty]


class RawWangSet(TypedDict):
    """ The keys and their types that appear in a Wang Set JSON Object."""

    colors: List[RawWangColor]
    name: str
    properties: List[properties_.RawProperty]
    tile: int
    wangtiles: List[RawWangTile]


def _cast_wang_tile(raw_wang_tile: RawWangTile) -> WangTile:
    """Cast the raw wang tile into a pytiled_parser type

    Args:
        raw_wang_tile: RawWangTile to be cast.

    Returns:
        WangTile: A properly typed WangTile.
    """
    return WangTile(tile_id=raw_wang_tile["tileid"], wang_id=raw_wang_tile["wangid"])


def _cast_wang_color(raw_wang_color: RawWangColor) -> WangColor:
    """Cast the raw wang color into a pytiled_parser type

    Args:
        raw_wang_color: RawWangColor to be cast.

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
        wang_color.properties = properties_.cast(raw_wang_color["properties"])

    return wang_color


def cast(raw_wangset: RawWangSet) -> WangSet:
    """Cast the raw wangset into a pytiled_parser type

    Args:
        raw_wangset: Raw Wangset to be cast.

    Returns:
        WangSet: A properly typed WangSet.
    """

    colors = []
    for raw_wang_color in raw_wangset["colors"]:
        colors.append(_cast_wang_color(raw_wang_color))

    tiles = []
    for raw_wang_tile in raw_wangset["wangtiles"]:
        tiles.append(_cast_wang_tile(raw_wang_tile))

    wangset = WangSet(
        name=raw_wangset["name"],
        tile=raw_wangset["tile"],
        wang_colors=colors,
        wang_tiles=tiles,
    )

    if raw_wangset.get("properties") is not None:
        wangset.properties = properties_.cast(raw_wangset["properties"])

    return wangset

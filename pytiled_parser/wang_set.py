from typing import List, NamedTuple, Optional

import attr
from typing_extensions import TypedDict

from . import properties as properties_
from .common_types import Color, OrderedPair


class WangTile(NamedTuple):

    id: int
    dflip: bool = False
    hflip: bool = False
    vflip: bool = False
    wang_ids: List[int] = []


class WangColor(NamedTuple):

    color: Color
    name: str
    probability: float
    tile: int


class WangSet(NamedTuple):

    cornercolors: List[WangColor]
    edgecolors: List[WangColor]
    name: str
    tile: int
    wang_tiles: List[WangTile]
    properties: Optional[properties_.Properties] = None


class RawWangTile(TypedDict):
    """ The keys and their types that appear in a Wang Tile JSON Object."""

    tileid: int
    dflip: bool
    hflip: bool
    vflip: bool
    wangid: List[int]


class RawWangColor(TypedDict):
    """ The keys and their types that appear in a Wang Color JSON Object."""

    color: str
    name: str
    probability: float
    tile: int


class RawWangSet(TypedDict):
    """ The keys and their types that appear in a Wang Set JSON Object."""

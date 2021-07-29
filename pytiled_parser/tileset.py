# pylint: disable=too-few-public-methods
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional, Union

import attr
from typing_extensions import TypedDict

from . import layer
from . import properties as properties_
from .common_types import Color, OrderedPair
from .util import parse_color
from .wang_set import RawWangSet, WangSet
from .wang_set import cast as cast_wangset


class Grid(NamedTuple):
    """Contains info for isometric maps.

    This element is only used in case of isometric orientation, and determines how tile
        overlays for terrain and collision information are rendered.

    Args:
        orientation: Orientation of the grid for the tiles in this tileset (orthogonal
            or isometric).
        width: Width of a grid cell.
        height: Height of a grid cell.
    """

    orientation: str
    width: int
    height: int


class Frame(NamedTuple):
    """Animation Frame object.

    This is only used as a part of an animation for Tile objects.

    Args:
        tile_id: The local ID of a tile within the parent tile set object.
        duration: How long in milliseconds this frame should be displayed before
            advancing to the next frame.
    """

    tile_id: int
    duration: int


@attr.s(auto_attribs=True, kw_only=True)
class Transformations:
    """Transformations Object.

    This is used to store what transformations may be performed on Tiles
    within a tileset. (This is primarily used with wang sets, however could
    be used for any means a game wants really.)

    Args:
        hflip: Allow horizontal flip?
        vflip: Allow vertical flip?
        rotate: Allow rotation?
        prefer_untransformed: Should untransformed tiles be preferred?
    """

    hflip: Optional[bool] = None
    vflip: Optional[bool] = None
    rotate: Optional[bool] = None
    prefer_untransformed: Optional[bool] = None


@attr.s(auto_attribs=True, kw_only=True)
class Tile:
    # FIXME: args
    """Individual tile object.

    See: https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#tile

    Args:
        id: The local tile ID within its tileset.
        type: The type of the tile. Refers to an object type and is used by tile
            objects.
        terrain: Defines the terrain type of each corner of the tile.
        animation: Each tile can have exactly one animation associated with it.
    """

    id: int
    opacity: int = 1
    type: Optional[str] = None
    animation: Optional[List[Frame]] = None
    objects: Optional[layer.Layer] = None
    image: Optional[Path] = None
    image_width: Optional[int] = None
    image_height: Optional[int] = None
    properties: Optional[properties_.Properties] = None
    tileset: Optional["Tileset"] = None
    flipped_horizontally: bool = False
    flipped_diagonally: bool = False
    flipped_vertically: bool = False


@attr.s(auto_attribs=True)
class Tileset:
    """Object for storing a TSX with all associated collision data.

    Args:
        name: The name of this tileset.
        max_tile_size: The maximum size of a tile in this tile set in pixels.
        spacing: The spacing in pixels between the tiles in this tileset (applies to
            the tileset image).
        margin: The margin around the tiles in this tileset (applies to the tileset
            image).
        tile_count: The number of tiles in this tileset.
        columns: The number of tile columns in the tileset. For image collection
            tilesets it is editable and is used when displaying the tileset.
        grid: Only used in case of isometric orientation, and determines how tile
            overlays for terrain and collision information are rendered.
        tileoffset: Used to specify an offset in pixels when drawing a tile from the
            tileset. When not present, no offset is applied.
        image: Used for spritesheet tile sets.
        tiles: Dict of Tile objects by Tile.id.
        tsx_file: Path of the file containing the tileset, None if loaded internally
            from a map
        parent_dir: Path of the parent directory of the file containing the tileset,
            None if loaded internally from a map
    """

    name: str
    tile_width: int
    tile_height: int

    tile_count: int
    columns: int

    firstgid: int

    type: str = "tileset"

    spacing: int = 0
    margin: int = 0

    tiled_version: Optional[str] = None
    version: Optional[str] = None

    image: Optional[Path] = None
    image_width: Optional[int] = None
    image_height: Optional[int] = None

    transformations: Optional[Transformations] = None

    background_color: Optional[Color] = None
    tile_offset: Optional[OrderedPair] = None
    transparent_color: Optional[Color] = None
    grid: Optional[Grid] = None
    properties: Optional[properties_.Properties] = None
    tiles: Optional[Dict[int, Tile]] = None
    wang_sets: Optional[List[WangSet]] = None


class RawFrame(TypedDict):
    """ The keys and their types that appear in a Frame JSON Object."""

    duration: int
    tileid: int


class RawTileOffset(TypedDict):
    """ The keys and their types that appear in a TileOffset JSON Object."""

    x: int
    y: int


class RawTransformations(TypedDict):
    """ The keys and their types that appear in a Transformations JSON Object."""

    hflip: bool
    vflip: bool
    rotate: bool
    preferuntransformed: bool


class RawTile(TypedDict):
    """ The keys and their types that appear in a Tile JSON Object."""

    animation: List[RawFrame]
    id: int
    image: str
    imageheight: int
    imagewidth: int
    opacity: float
    properties: List[properties_.RawProperty]
    objectgroup: layer.RawLayer
    type: str


class RawGrid(TypedDict):
    """ The keys and their types that appear in a Grid JSON Object."""

    height: int
    width: int
    orientation: str


class RawTileSet(TypedDict):
    """ The keys and their types that appear in a TileSet JSON Object."""

    backgroundcolor: str
    columns: int
    firstgid: int
    grid: RawGrid
    image: str
    imageheight: int
    imagewidth: int
    margin: int
    name: str
    properties: List[properties_.RawProperty]
    source: str
    spacing: int
    tilecount: int
    tiledversion: str
    tileheight: int
    tileoffset: RawTileOffset
    tiles: List[RawTile]
    tilewidth: int
    transparentcolor: str
    transformations: RawTransformations
    version: Union[str, float]
    wangsets: List[RawWangSet]


def _cast_frame(raw_frame: RawFrame) -> Frame:
    """Cast the raw_frame to a Frame.

    Args:
        raw_frame: RawFrame to be casted to a Frame

    Returns:
        Frame: The Frame created from the raw_frame
    """

    return Frame(duration=raw_frame["duration"], tile_id=raw_frame["tileid"])


def _cast_tile_offset(raw_tile_offset: RawTileOffset) -> OrderedPair:
    """Cast the raw_tile_offset to an OrderedPair.

    Args:
        raw_tile_offset: RawTileOffset to be casted to an OrderedPair

    Returns:
        OrderedPair: The OrderedPair created from the raw_tile_offset
    """

    return OrderedPair(raw_tile_offset["x"], raw_tile_offset["y"])


def _cast_tile(raw_tile: RawTile, external_path: Optional[Path] = None) -> Tile:
    """Cast the raw_tile to a Tile object.

    Args:
        raw_tile: RawTile to be casted to a Tile

    Returns:
        Tile: The Tile created from the raw_tile
    """

    id_ = raw_tile["id"]
    tile = Tile(id=id_)

    if raw_tile.get("animation") is not None:
        tile.animation = []
        for frame in raw_tile["animation"]:
            tile.animation.append(_cast_frame(frame))

    if raw_tile.get("objectgroup") is not None:
        tile.objects = layer.cast(raw_tile["objectgroup"])

    if raw_tile.get("properties") is not None:
        tile.properties = properties_.cast(raw_tile["properties"])

    if raw_tile.get("image") is not None:
        if external_path:
            tile.image = Path(external_path / raw_tile["image"]).absolute().resolve()
        else:
            tile.image = Path(raw_tile["image"])

    if raw_tile.get("imagewidth") is not None:
        tile.image_width = raw_tile["imagewidth"]

    if raw_tile.get("imageheight") is not None:
        tile.image_height = raw_tile["imageheight"]

    if raw_tile.get("type") is not None:
        tile.type = raw_tile["type"]

    return tile


def _cast_transformations(raw_transformations: RawTransformations) -> Transformations:
    """Cast the raw_transformations to a Transformations object.

    Args:
        raw_transformations: RawTransformations to be casted to a Transformations

    Returns:
        Transformations: The Transformations created from the raw_transformations
    """

    return Transformations(
        hflip=raw_transformations["hflip"],
        vflip=raw_transformations["vflip"],
        rotate=raw_transformations["rotate"],
        prefer_untransformed=raw_transformations["preferuntransformed"],
    )


def _cast_grid(raw_grid: RawGrid) -> Grid:
    """Cast the raw_grid to a Grid object.

    Args:
        raw_grid: RawGrid to be casted to a Grid

    Returns:
        Grid: The Grid created from the raw_grid
    """

    return Grid(
        orientation=raw_grid["orientation"],
        width=raw_grid["width"],
        height=raw_grid["height"],
    )


def cast(
    raw_tileset: RawTileSet,
    firstgid: int,
    external_path: Optional[Path] = None,
) -> Tileset:
    """Cast the raw tileset into a pytiled_parser type

    Args:
        raw_tileset: Raw Tileset to be cast.
        firstgid: GID corresponding the first tile in the set.
        external_path: The path to the tileset if it is not an embedded one.

    Returns:
        TileSet: a properly typed TileSet.
    """

    tileset = Tileset(
        name=raw_tileset["name"],
        tile_count=raw_tileset["tilecount"],
        tile_width=raw_tileset["tilewidth"],
        tile_height=raw_tileset["tileheight"],
        columns=raw_tileset["columns"],
        spacing=raw_tileset["spacing"],
        margin=raw_tileset["margin"],
        firstgid=firstgid,
    )

    if raw_tileset.get("version") is not None:
        if isinstance(raw_tileset["version"], float):
            tileset.version = str(raw_tileset["version"])
        else:
            tileset.version = raw_tileset["version"]

    if raw_tileset.get("tiledversion") is not None:
        tileset.tiled_version = raw_tileset["tiledversion"]

    if raw_tileset.get("image") is not None:
        if external_path:
            tileset.image = (
                Path(external_path / raw_tileset["image"]).absolute().resolve()
            )
        else:
            tileset.image = Path(raw_tileset["image"])

    if raw_tileset.get("imagewidth") is not None:
        tileset.image_width = raw_tileset["imagewidth"]

    if raw_tileset.get("imageheight") is not None:
        tileset.image_height = raw_tileset["imageheight"]

    if raw_tileset.get("backgroundcolor") is not None:
        tileset.background_color = parse_color(raw_tileset["backgroundcolor"])

    if raw_tileset.get("tileoffset") is not None:
        tileset.tile_offset = _cast_tile_offset(raw_tileset["tileoffset"])

    if raw_tileset.get("transparentcolor") is not None:
        tileset.transparent_color = parse_color(raw_tileset["transparentcolor"])

    if raw_tileset.get("grid") is not None:
        tileset.grid = _cast_grid(raw_tileset["grid"])

    if raw_tileset.get("properties") is not None:
        tileset.properties = properties_.cast(raw_tileset["properties"])

    if raw_tileset.get("tiles") is not None:
        tiles = {}
        for raw_tile in raw_tileset["tiles"]:
            tiles[raw_tile["id"]] = _cast_tile(raw_tile, external_path=external_path)
        tileset.tiles = tiles

    if raw_tileset.get("wangsets") is not None:
        wangsets = []
        for raw_wangset in raw_tileset["wangsets"]:
            wangsets.append(cast_wangset(raw_wangset))
        tileset.wang_sets = wangsets

    if raw_tileset.get("transformations") is not None:
        tileset.transformations = _cast_transformations(raw_tileset["transformations"])

    return tileset

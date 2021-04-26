# pylint: disable=too-few-public-methods
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional

import attr
from typing_extensions import TypedDict

from . import layer
from . import properties as properties_
from .common_types import Color, OrderedPair
from .util import parse_color


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


class Terrain(NamedTuple):
    """Terrain object.

    Args:
        name: The name of the terrain type.
        tile: The local tile-id of the tile that represents the terrain visually.
    """

    name: str
    tile: int
    properties: Optional[properties_.Properties] = None


@attr.s(auto_attribs=True)
class TileTerrain:
    """Defines each corner of a tile by Terrain index in
        'TileSet.terrain_types'.

    Defaults to 'None'. 'None' means that corner has no terrain.

    Attributes:
        top_left: Top left terrain type.
        top_right: Top right terrain type.
        bottom_left: Bottom left terrain type.
        bottom_right: Bottom right terrain type.
    """

    top_left: Optional[int] = None
    top_right: Optional[int] = None
    bottom_left: Optional[int] = None
    bottom_right: Optional[int] = None


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
    terrain: Optional[TileTerrain] = None
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
        terrain_types: List of of terrain types which can be referenced from the
            terrain attribute of the tile object. Ordered according to the terrain
            element's appearance in the TSX file.
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

    spacing: int = 0
    margin: int = 0

    type: Optional[str] = None

    tiled_version: Optional[str] = None
    version: Optional[float] = None

    image: Optional[Path] = None
    image_width: Optional[int] = None
    image_height: Optional[int] = None

    firstgid: Optional[int] = None
    background_color: Optional[Color] = None
    tile_offset: Optional[OrderedPair] = None
    transparent_color: Optional[Color] = None
    grid: Optional[Grid] = None
    properties: Optional[properties_.Properties] = None
    terrain_types: Optional[List[Terrain]] = None
    tiles: Optional[Dict[int, Tile]] = None


class RawFrame(TypedDict):
    """ The keys and their types that appear in a Frame JSON Object."""

    duration: int
    tileid: int


class RawTileOffset(TypedDict):
    """ The keys and their types that appear in a TileOffset JSON Object."""

    x: int
    y: int


class RawTerrain(TypedDict):
    """ The keys and their types that appear in a Terrain JSON Object."""

    name: str
    properties: List[properties_.RawProperty]
    tile: int


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
    terrain: List[int]
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
    terrains: List[RawTerrain]
    tilecount: int
    tiledversion: str
    tileheight: int
    tileoffset: RawTileOffset
    tiles: List[RawTile]
    tilewidth: int
    transparentcolor: str
    type: str
    version: float


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


def _cast_terrain(raw_terrain: RawTerrain) -> Terrain:
    """Cast the raw_terrain to a Terrain object.

    Args:
        raw_terrain: RawTerrain to be casted to a Terrain

    Returns:
        Terrain: The Terrain created from the raw_terrain
    """

    if raw_terrain.get("properties") is not None:
        return Terrain(
            name=raw_terrain["name"],
            tile=raw_terrain["tile"],
            properties=properties_.cast(raw_terrain["properties"]),
        )
    else:
        return Terrain(
            name=raw_terrain["name"],
            tile=raw_terrain["tile"],
        )


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

    if raw_tile.get("terrain") is not None:
        raw_terrain = raw_tile["terrain"]
        terrain = TileTerrain(
            top_left=raw_terrain[0],
            top_right=raw_terrain[1],
            bottom_left=raw_terrain[2],
            bottom_right=raw_terrain[3],
        )
        tile.terrain = terrain

    if raw_tile.get("type") is not None:
        tile.type = raw_tile["type"]

    return tile


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


def cast(raw_tileset: RawTileSet, external_path: Optional[Path] = None) -> Tileset:
    """Cast the raw tileset into a pytiled_parser type

    Args:
        raw_tileset: Raw Tileset to be cast.

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
    )

    if raw_tileset.get("type") is not None:
        tileset.type = raw_tileset["type"]

    if raw_tileset.get("version") is not None:
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

    if raw_tileset.get("firstgid") is not None:
        tileset.firstgid = raw_tileset["firstgid"]

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

    if raw_tileset.get("terrains") is not None:
        terrains = []
        for raw_terrain in raw_tileset["terrains"]:
            terrains.append(_cast_terrain(raw_terrain))
        tileset.terrain_types = terrains

    if raw_tileset.get("tiles") is not None:
        tiles = {}
        for raw_tile in raw_tileset["tiles"]:
            tiles[raw_tile["id"]] = _cast_tile(raw_tile, external_path=external_path)
        tileset.tiles = tiles

    return tileset

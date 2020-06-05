# pylint: disable=too-few-public-methods
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional

import attr

from pytiled_parser import OrderedPair, Size
from pytiled_parser.properties import Properties, Property
from pytiled_parser.tiled_object import TiledObject


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


@attr.s(auto_attribs=True)
class Image:
    """Image object.

    pytiled_parser does not support embedded data in image elements at this time,
        even though the TMX format technically does.

    Attributes:
        source: The reference to the tileset image file. Note that this is a relative
            path compared to FIXME
        trans: Defines a specific color that is treated as transparent.
        width: The image width in pixels (optional, used for tile index correction when
            the image changes).
        height: The image height in pixels (optional).
    """

    source: str
    size: Optional[Size] = None
    trans: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None


class Terrain(NamedTuple):
    """Terrain object.

    Args:
        name: The name of the terrain type.
        tile: The local tile-id of the tile that represents the terrain visually.
    """

    name: str
    tile: int


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
    type: Optional[str] = None
    terrain: Optional[TileTerrain] = None
    animation: Optional[List[Frame]] = None
    objectgroup: Optional[List[TiledObject]] = None
    image: Optional[Image] = None
    properties: Optional[List[Property]] = None
    tileset: Optional["TileSet"] = None
    flipped_horizontally: bool = False
    flipped_diagonally: bool = False
    flipped_vertically: bool = False


@attr.s(auto_attribs=True)
class TileSet:
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
    max_tile_size: Size

    spacing: Optional[int] = None
    margin: Optional[int] = None
    tile_count: Optional[int] = None
    columns: Optional[int] = None
    tile_offset: Optional[OrderedPair] = None
    grid: Optional[Grid] = None
    properties: Optional[Properties] = None
    image: Optional[Image] = None
    terrain_types: Optional[List[Terrain]] = None
    tiles: Optional[Dict[int, Tile]] = None
    tsx_file: Path = None
    parent_dir: Path = None


def cast():
    pass

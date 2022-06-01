"""Provides an interface for Tilesets and the various objects within them.

Also see [Tiled's Docs for Editing Tilesets](https://doc.mapeditor.org/en/stable/manual/editing-tilesets/)
and [TMX Reference](https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#tileset)
and [JSON Reference](https://doc.mapeditor.org/en/stable/reference/json-map-format/#tileset)
"""
# pylint: disable=too-few-public-methods
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional

import attr

from . import layer
from . import properties as properties_
from .common_types import Color, OrderedPair
from .wang_set import WangSet


class Grid(NamedTuple):
    """Contains info used in isometric maps.

    This element is only used in case of isometric orientation, and determines how tile
    overlays for terrain and collision information are rendered.

    [TMX Reference](https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#tmx-grid)

    [JSON Reference](https://doc.mapeditor.org/en/stable/reference/json-map-format/#grid)

    Attributes:
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

    This is only used as a part of an animation for Tile objects. A frame simply points
    to a tile within the tileset, and gives a duration. Meaning that tile would be
    displayed for the given duration.

    [TMX Reference](https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#tmx-frame)

    [JSON Reference](https://doc.mapeditor.org/en/stable/reference/json-map-format/#json-frame)

    Attributes:
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
    within a tileset. Within Tiled this primarily used with wang sets and
    the terrain system, however, could be used for any means a game/engine
    wants to really.

    [TMX Reference](https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#transformations)

    [JSON Reference](https://doc.mapeditor.org/en/stable/reference/json-map-format/#transformations)

    Attributes:
        hflip: Allow horizontal flip?
        vflip: Allow vertical flip?
        rotate: Allow rotation?
        prefer_untransformed: Should untransformed tiles be preferred?
    """

    hflip: bool = False
    vflip: bool = False
    rotate: bool = False
    prefer_untransformed: bool = False


@attr.s(auto_attribs=True, kw_only=True)
class Tile:
    """Individual tile object.

    This class more closely resembles the JSON format than TMX. A number of values
    within this class in the TMX format are pulled into other sub-tags such as <image>.

    [TMX Reference](https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#tile)

    [JSON Reference](https://doc.mapeditor.org/en/stable/reference/json-map-format/#tile-definition)

    Attributes:
        id: The local tile ID within it's tileset.
        opacity: The opacity this Tiled should be rendered with.
        type: An optional, arbitrary string that can be used to denote different
            types of tiles. For example "wall" or "floor".
        animation: A list of [Frame][pytiled_parser.tileset.Frame] objects which
            makeup the animation for an animated tile.
        objects: An [ObjectLayer][pytiled_parser.layer.ObjectLayer] which contains
            objects that can be used for custom collision on the Tile. This field
            is set by the Tile Collision editor in Tiled.
        image: A path to the image for this tile.
        image_width: The width of this tile's image.
        image_height: The height of this tile's image.
        properties: A list of properties on this Tile.
        tileset: The [Tileset][pytiled_parser.tileset.Tileset] this tile came from.
        flipped_horizontally: Should this Tile be flipped horizontally?
        flipped_diagonally: Should this Tile be flipped diagonally?
        flipped_vertically: Should this Tile be flipped vertically?
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
    """A Tileset is a collection of tiles.

    As with the Tile class, this one more closely resembles the JSON format than TMX.

    [TMX Reference](https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#tileset)

    [JSON Reference](https://doc.mapeditor.org/en/stable/reference/json-map-format/#tileset)

    Attributes:
        name: The name of this tileset.
        tile_width: The width of a tile in this tileset in pixels.
        tile_height: The height of a tile in this tileset in pixels.
        tile_count: The number of tiles in this tileset.
        columns: The number of tile columns in the tileset. For image collection
            tilesets it is editable and is used when displaying the tileset.
        spacing: The spacing in pixels between the tiles in this tileset (applies to
            the tileset image).
        firstgid: The global ID to give to the first Tile in this tileset. Global IDs
            for the rest of the tiles will increment from this number.
        type: Will always be `tileset`. Is statically included as a way to determine the
            type of a JSON file since Tiled does not have different extesnsions for map
            and tileset JSON files(as opposed to TMX/TSX files)
        spacing: Spacing between adjacent tiles in the image in pixels.
        margin: Buffer between the image edge and the first tile in the image in pixels.
        image: Used for spritesheet tile sets.
        image_width: The width of the `image` in pixels.
        image_height: The height of the `image` in pixels.
        transformations: What types of transformations are allowed on tiles within this
            Tileset
        background_color: The background color of the tileset.
        tileoffset: Used to specify an offset in pixels when drawing a tile from the
            tileset. When not present, no offset is applied.
        transparent_color: A color that acts as transparent on any tiles within the
            tileset.
        grid: Only used in case of isometric orientation, and determines how tile
            overlays for terrain and collision information are rendered.
        properties: The properties for this Tileset.
        tiles: Dict of Tile objects by Tile.id.
        wang_sets: List of WangSets used by the terrain system
        alignment: Which alignment to use for tile objects from this tileset.
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
    alignment: Optional[str] = None

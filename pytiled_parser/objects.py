"""
pytiled_parser objects for Tiled maps.
"""

import dataclasses
import functools
import re

from collections import OrderedDict
from pathlib import Path

import xml.etree.ElementTree as etree

from typing import NamedTuple, Union, Optional, List, Dict


class EncodingError(Exception):
    """Tmx layer encoding is of an unknown type."""


class TileNotFoundError(Exception):
    """Tile not found in tileset."""


class ImageNotFoundError(Exception):
    """Image not found."""


class Color(NamedTuple):
    """Color object.

    Attributes:
        :red (int): Red, between 1 and 255.
        :green (int): Green, between 1 and 255.
        :blue (int): Blue, between 1 and 255.
        :alpha (int): Alpha, between 1 and 255.
    """

    red: int
    green: int
    blue: int
    alpha: int


class OrderedPair(NamedTuple):
    """OrderedPair NamedTuple.

    Attributes:
        x (Union[int, float]): X coordinate.
        y (Union[int, float]): Y coordinate.
    """

    x: Union[int, float]
    y: Union[int, float]


class Size(NamedTuple):
    """Size NamedTuple.

    Attributes:
        width (Union[int, float]): The width of the object.
        size (Union[int, float]): The height of the object.
    """

    width: Union[int, float]
    height: Union[int, float]


class Template:
    """
    FIXME TODO
    """


@dataclasses.dataclass
class Chunk:
    """
    Chunk object for infinite maps.

    See: https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#chunk

    Attributes:
        :location (OrderedPair): Location of chunk in tiles.
        :width (int): The width of the chunk in tiles.
        :height (int): The height of the chunk in tiles.
        :layer_data (List[List(int)]): The global tile IDs in chunky
            according to row.
    """

    location: OrderedPair
    width: int
    height: int
    chunk_data: List[List[int]]


@dataclasses.dataclass
class Image:
    """
    Image object.

    This module does not support embedded data in image elements.

    Attributes:
        :source (Optional[str]): The reference to the tileset image file.
            Not that this is a relative path compared to FIXME
        :trans (Optional[Color]): Defines a specific color that is treated
            as transparent.
        :width (Optional[str]): The image width in pixels
            (optional, used for tile index correction when the image changes).
        :height (Optional[str]): The image height in pixels (optional).
    """

    source: str
    size: Optional[Size] = None
    trans: Optional[Color] = None


Properties = Dict[str, Union[int, float, Color, Path, str]]


class Grid(NamedTuple):
    """
    Contains info for isometric maps.

    This element is only used in case of isometric orientation, and
        determines how tile overlays for terrain and collision information
        are rendered.
    """

    orientation: str
    width: int
    height: int


class Terrain(NamedTuple):
    """
    Terrain object.

    Args:
        :name (str): The name of the terrain type.
        :tile (int): The local tile-id of the tile that represents the
            terrain visually.
    """

    name: str
    tile: int


class Frame(NamedTuple):
    """
    Animation Frame object.

    This is only used as a part of an animation for Tile objects.

    Args:
        :tile_id (int): The local ID of a tile within the parent tile set
            object.
        :duration (int): How long in milliseconds this frame should be
            displayed before advancing to the next frame.
    """

    tile_id: int
    duration: int


@dataclasses.dataclass
class TileTerrain:
    """
    Defines each corner of a tile by Terrain index in
        'TileSet.terrain_types'.

    Defaults to 'None'. 'None' means that corner has no terrain.

    Attributes:
        :top_left (Optional[int]): Top left terrain type.
        :top_right (Optional[int]): Top right terrain type.
        :bottom_left (Optional[int]): Bottom left terrain type.
        :bottom_right (Optional[int]): Bottom right terrain type.
    """

    top_left: Optional[int] = None
    top_right: Optional[int] = None
    bottom_left: Optional[int] = None
    bottom_right: Optional[int] = None


@dataclasses.dataclass
class _LayerTypeBase:
    id: int  # pylint: disable=C0103
    name: str


@dataclasses.dataclass
class _LayerTypeDefaults:
    offset: OrderedPair = OrderedPair(0, 0)
    opacity: int = 0xFF

    properties: Optional[Properties] = None


@dataclasses.dataclass
class LayerType(_LayerTypeDefaults, _LayerTypeBase):
    """
    Class that all layer classes inherit from.

    Not to be directly used.

    Args:
        :layer_element (etree.Element): Element to be parsed into a
            LayerType object.

    Attributes:
        :id (int): Unique ID of the layer. Each layer that added to a map
            gets a unique id. Even if a layer is deleted, no layer ever gets
            the same ID.
        :name (Optional[str):] The name of the layer object.
        :offset (OrderedPair): Rendering offset of the layer object in
            pixels. (default: (0, 0).
        :opacity (int): Value between 0 and 255 to determine opacity. NOTE:
            this value is converted from a float provided by Tiled, so some
            precision is lost.
        :properties (Optional[Properties]): Properties object for layer
            object.
    """


LayerData = Union[List[List[int]], List[Chunk]]
"""
The tile data for one layer.

Either a 2 dimensional array of integers representing the global tile IDs
    for a map layer, or a lists of chunks for an infinite map layer.
"""


@dataclasses.dataclass
class _LayerBase:
    size: Size
    data: LayerData


@dataclasses.dataclass
class Layer(LayerType, _LayerBase):
    """
    Map layer object.

    See: https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#layer

    Attributes:
        :size (Size): The width of the layer in tiles. Always the same
            as the map width for not infitite maps.
        :data (LayerData): Either an 2 dimensional array of integers
            representing the global tile IDs for the map layer, or a list of
            chunks for an infinite map.
    """


@dataclasses.dataclass
class _TiledObjectBase:
    id: int
    location: OrderedPair


@dataclasses.dataclass
class _TiledObjectDefaults:
    size: Size = Size(0, 0)
    rotation: int = 0
    opacity: int = 0xFF

    name: Optional[str] = None
    type: Optional[str] = None

    properties: Optional[Properties] = None
    template: Optional[Template] = None


@dataclasses.dataclass
class TiledObject(_TiledObjectDefaults, _TiledObjectBase):
    """
    TiledObjectGroup object.

    See:
        https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#object

    Args:
        :id (int): Unique ID of the object. Each object that is placed on a
            map gets a unique id. Even if an object was deleted, no object
            gets the same ID.
        :location (OrderedPair): The location of the object in pixels.
        :size (Size): The width of the object in pixels
            (default: (0, 0)).
        :rotation (int): The rotation of the object in degrees clockwise
            (default: 0).
        :opacity (int): The opacity of the object. (default: 255)
        :name (Optional[str]): The name of the object.
        :type (Optional[str]): The type of the object.
        :properties (Properties): The properties of the TiledObject.
        :template Optional[Template]: A reference to a Template object
            FIXME
    """


@dataclasses.dataclass
class RectangleObject(TiledObject):
    """
    Rectangle shape defined by a point, width, and height.

    See: https://doc.mapeditor.org/en/stable/manual/objects/#insert-rectangle
        (objects in tiled are rectangles by default, so there is no specific
        documentation on the tmx-map-format page for it.)
    """


@dataclasses.dataclass
class ElipseObject(TiledObject):
    """
    Elipse shape defined by a point, width, and height.

    See: https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#ellipse
    """


@dataclasses.dataclass
class PointObject(TiledObject):
    """
    Point defined by a point (x,y).

    See: https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#point
    """


@dataclasses.dataclass
class _TileImageObjectBase(_TiledObjectBase):
    gid: int


@dataclasses.dataclass
class TileImageObject(TiledObject, _TileImageObjectBase):
    """
    Polygon shape defined by a set of connections between points.

    See: https://doc.mapeditor.org/en/stable/manual/objects/#insert-tile

    Attributes:
        :gid (int): Refference to a global tile id.
    """


@dataclasses.dataclass
class _PointsObjectBase(_TiledObjectBase):
    points: List[OrderedPair]


@dataclasses.dataclass
class PolygonObject(TiledObject, _PointsObjectBase):
    """
    Polygon shape defined by a set of connections between points.

    See: https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#polygon

    Attributes:
        :points (List[OrderedPair])
    """


@dataclasses.dataclass
class PolylineObject(TiledObject, _PointsObjectBase):
    """
    Polyline defined by a set of connections between points.

    See:
        https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#polyline

    Attributes:
        :points (List[Tuple[int, int]]): List of coordinates relative to \
        the location of the object.
    """


@dataclasses.dataclass
class _TextObjectBase(_TiledObjectBase):
    text: str


@dataclasses.dataclass
class _TextObjectDefaults(_TiledObjectDefaults):
    font_family: str = "sans-serif"
    font_size: int = 16
    wrap: bool = False
    color: Color = Color(0xFF, 0, 0, 0)
    bold: bool = False
    italic: bool = False
    underline: bool = False
    strike_out: bool = False
    kerning: bool = False
    horizontal_align: str = "left"
    vertical_align: str = "top"


@dataclasses.dataclass
class TextObject(TiledObject, _TextObjectDefaults, _TextObjectBase):
    """
    Text object with associated settings.

    See: https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#text
        and https://doc.mapeditor.org/en/stable/manual/objects/#insert-text

    Attributes:
        :font_family (str): The font family used (default: “sans-serif”)
        :font_size (int): The size of the font in pixels. (default: 16)
        :wrap (bool): Whether word wrapping is enabled. (default: False)
        :color (Color): Color of the text. (default: #000000)
        :bold (bool): Whether the font is bold. (default: False)
        :italic (bool): Whether the font is italic. (default: False)
        :underline (bool): Whether the text is underlined. (default: False)
        :strike_out (bool): Whether the text is striked-out. (default: False)
        :kerning (bool): Whether kerning should be used while rendering the \
        text. (default: False)
        :horizontal_align (str): Horizontal alignment of the text \
        (default: "left")
        :vertical_align (str): Vertical alignment of the text (defalt: "top")
    """


@dataclasses.dataclass
class _ObjectGroupBase(_LayerTypeBase):
    objects: List[TiledObject]


@dataclasses.dataclass
class _ObjectGroupDefaults(_LayerTypeDefaults):
    color: Optional[Color] = None
    draw_order: Optional[str] = "topdown"


@dataclasses.dataclass
class ObjectGroup(LayerType, _ObjectGroupDefaults, _ObjectGroupBase):
    """
    TiledObject Group Object.

    The object group is in fact a map layer, and is hence called \
    “object layer” in Tiled.

    See: \
https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#objectgroup

    Attributes:
        :color (Optional[Color]): The color used to display the objects
            in this group. FIXME: editor only?
        :draworder (str): Whether the objects are drawn according to the
            order of the object elements in the object group element
            ('manual'), or sorted by their y-coordinate ('topdown'). Defaults
            to 'topdown'. See:
            https://doc.mapeditor.org/en/stable/manual/objects/#changing-stacking-order
            for more info.
        :objects (Dict[int, TiledObject]): Dict TiledObject objects by
            TiledObject.id.
    """


@dataclasses.dataclass
class _LayerGroupBase(_LayerTypeBase):
    layers: Optional[List[LayerType]]


@dataclasses.dataclass
class LayerGroup(LayerType):
    """
    Layer Group.

    A LayerGroup can be thought of as a layer that contains layers
        (potentially including other LayerGroups).

    Offset and opacity recursively affect child layers.

    See: https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#group

    Attributes:

    """


@dataclasses.dataclass
class Hitbox:
    """Group of hitboxes for
    """


@dataclasses.dataclass
class Tile:
    """
    Individual tile object.

    Args:
        :id (int): The local tile ID within its tileset.
        :type (str): The type of the tile. Refers to an object type and is
            used by tile objects.
        :terrain (int): Defines the terrain type of each corner of the tile.
        :animation (List[Frame]): Each tile can have exactly one animation
            associated with it.
    """

    id: int
    type: Optional[str]
    terrain: Optional[TileTerrain]
    animation: Optional[List[Frame]]
    image: Optional[Image]
    hitboxes: Optional[List[TiledObject]]


@dataclasses.dataclass
class TileSet:
    """
    Object for storing a TSX with all associated collision data.

    Args:
        :name (str): The name of this tileset.
        :max_tile_size (Size): The maximum size of a tile in this
            tile set in pixels.
        :spacing (int): The spacing in pixels between the tiles in this
            tileset (applies to the tileset image).
        :margin (int): The margin around the tiles in this tileset
            (applies to the tileset image).
        :tile_count (int): The number of tiles in this tileset.
        :columns (int): The number of tile columns in the tileset.
            For image collection tilesets it is editable and is used when
            displaying the tileset.
        :grid (Grid): Only used in case of isometric orientation, and
            determines how tile overlays for terrain and collision information
            are rendered.
        :tileoffset (Optional[OrderedPair]): Used to specify an offset in
            pixels when drawing a tile from the tileset. When not present, no
            offset is applied.
        :image (Image): Used for spritesheet tile sets.
        :terrain_types (Dict[str, int]): List of of terrain types which
            can be referenced from the terrain attribute of the tile object.
            Ordered according to the terrain element's appearance in the TSX
            file.
        :tiles (Optional[Dict[int, Tile]]): Dict of Tile objects by Tile.id.
    """

    name: str
    max_tile_size: Size
    spacing: Optional[int]
    margin: Optional[int]
    tile_count: Optional[int]
    columns: Optional[int]
    tile_offset: Optional[OrderedPair]
    grid: Optional[Grid]
    properties: Optional[Properties]
    image: Optional[Image]
    terrain_types: Optional[List[Terrain]]
    tiles: Optional[Dict[int, Tile]]


TileSetDict = Dict[int, TileSet]


@dataclasses.dataclass
class TileMap:
    """
    Object for storing a TMX with all associated layers and properties.

    See: https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#map

    Attributes:
        :parent_dir (Path): The directory the TMX file is in. Used for finding
            relative paths to TSX files and other assets.
        :version (str): The TMX format version.
        :tiledversion (str): The Tiled version used to save the file. May
            be a date (for snapshot builds).
        :orientation (str): Map orientation. Tiled supports “orthogonal”,
            “isometric”, “staggered” and “hexagonal”
        :renderorder (str): The order in which tiles on tile layers are
            rendered. Valid values are right-down, right-up, left-down and
            left-up. In all cases, the map is drawn row-by-row. (only
            supported for orthogonal maps at the moment)
        :map_size (Size): The map width in tiles.
        :tile_size (Size): The width of a tile.
        :infinite (bool): If the map is infinite or not.
        :hexsidelength (int): Only for hexagonal maps. Determines the width or
            height (depending on the staggered axis) of the tile’s edge, in
            pixels.
        :stagger_axis (str): For staggered and hexagonal maps, determines
            which axis (“x” or “y”) is staggered.
        :staggerindex (str): For staggered and hexagonal maps, determines
            whether the “even” or “odd” indexes along the staggered axis are
            shifted.
        :backgroundcolor (##FIXME##): The background color of the map.
        :nextlayerid (int): Stores the next available ID for new layers.
        :nextobjectid (int): Stores the next available ID for new objects.
        :tile_sets (dict[str, TileSet]): Dict of tile sets used
            in this map. Key is the first GID for the tile set. The value
            is a TileSet object.
        :layers List[LayerType]: List of layer objects by draw order.
    """

    parent_dir: Path

    version: str
    tiled_version: str
    orientation: str
    render_order: str
    map_size: Size
    tile_size: Size
    infinite: bool
    next_layer_id: int
    next_object_id: int

    tile_sets: TileSetDict
    layers: List[LayerType]

    hex_side_length: Optional[int] = None
    stagger_axis: Optional[int] = None
    stagger_index: Optional[int] = None
    background_color: Optional[Color] = None

    properties: Optional[Properties] = None


"""
[22:16] <__m4ch1n3__> i would "[i for i in int_list if i < littler_then_value]"
[22:16] <__m4ch1n3__> it returns a list of integers below "littler_then_value"
[22:17] <__m4ch1n3__> !py3 [i for i in [1,2,3,4,1,2,3,4] if i < 3]
[22:17] <codebot> __m4ch1n3__: [1, 2, 1, 2]
[22:17] <__m4ch1n3__> !py3 [i for i in [1,2,3,4,1,2,3,4] if i < 4]
[22:17] <codebot> __m4ch1n3__: [1, 2, 3, 1, 2, 3]
[22:22] <__m4ch1n3__> !py3 max([i for i in [1,2,3,4,1,2,3,4] if i < 4])
[22:22] <codebot> __m4ch1n3__: 3
[22:22] <__m4ch1n3__> max(...) would return the maximum of resulting list
[22:23] <__m4ch1n3__> !py3 max([i for i in  [1, 10, 100] if i < 20])
[22:23] <codebot> __m4ch1n3__: 10
[22:23] <__m4ch1n3__> !py3 max([i for i in  [1, 10, 100] if i < 242])
[22:23] <codebot> __m4ch1n3__: 100
[22:23] == markb1 [~mbiggers@45.36.35.206] has quit [Ping timeout: 245 seconds]
[22:23] <__m4ch1n3__> !py3 max(i for i in  [1, 10, 100] if i < 242)
"""

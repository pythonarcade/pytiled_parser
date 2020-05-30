"""pytiled_parser objects for Tiled maps.
"""

# pylint: disable=too-few-public-methods

from pathlib import Path
from typing import Dict, List, NamedTuple, Optional, Union

import attr

# See: https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#data
TileLayerGrid = List[List[int]]


class Color(NamedTuple):
    """Color object.

    Attributes:
        red: Red, between 1 and 255.
        green: Green, between 1 and 255.
        blue: Blue, between 1 and 255.
        alpha: Alpha, between 1 and 255.
    """

    red: int
    green: int
    blue: int
    alpha: int


class OrderedPair(NamedTuple):
    """OrderedPair NamedTuple.

    Attributes:
        x: X coordinate.
        y: Y coordinate.
    """

    x: Union[int, float]
    y: Union[int, float]


class Property(NamedTuple):
    """Property NamedTuple.

    Attributes:
        name: Name of property
        value: Value of property
    """

    name: str
    value: str


class Size(NamedTuple):
    """Size NamedTuple.

    Attributes:
        width: The width of the object.
        size: The height of the object.
    """

    width: Union[int, float]
    height: Union[int, float]


@attr.s(auto_attribs=True)
class Template:
    """FIXME TODO"""


@attr.s(auto_attribs=True)
class Chunk:
    """Chunk object for infinite maps.

    See: https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#chunk

    Attributes:
        location: Location of chunk in tiles.
        width: The width of the chunk in tiles.
        height: The height of the chunk in tiles.
        layer_data: The global tile IDs in chunky according to row.
    """

    location: OrderedPair
    width: int
    height: int
    chunk_data: TileLayerGrid


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


Properties = Dict[str, Union[int, float, Color, Path, str]]


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


@attr.s(auto_attribs=True, kw_only=True)
class Layer:
    # FIXME:this docstring appears to be innacurate
    """Class that all layers inherit from.

    Args:
        id: Unique ID of the layer. Each layer that added to a map gets a unique id.
            Even if a layer is deleted, no layer ever gets the same ID.
        name: The name of the layer object.
        tiled_objects: List of tiled_objects in the layer.
        offset: Rendering offset of the layer object in pixels.
        opacity: Decimal value between 0 and 1 to determine opacity. 1 is completely
            opaque, 0 is completely transparent.
        properties: Properties for the layer.
        color: The color used to display the objects in this group.
        draworder: Whether the objects are drawn according to the order of the object
            elements in the object group element ('manual'), or sorted by their
            y-coordinate ('topdown'). Defaults to 'topdown'.
            See:
            https://doc.mapeditor.org/en/stable/manual/objects/#changing-stacking-order
            for more info.

    """

    id_: int
    name: str

    offset: Optional[OrderedPair]
    opacity: Optional[float]
    properties: Optional[Properties]


LayerData = Union[TileLayerGrid, List[Chunk]]
"""The tile data for one layer.

Either a 2 dimensional array of integers representing the global tile IDs
    for a TileLayerGrid, or a list of chunks for an infinite map layer.
"""


@attr.s(auto_attribs=True, kw_only=True)
class TileLayer(Layer):
    """Tile map layer containing tiles.

    See: https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#layer

    Args:
        size: The width of the layer in tiles. The same as the map width unless map is
            infitite.
        data: Either an 2 dimensional array of integers representing the global tile
            IDs for the map layer, or a list of chunks for an infinite map.
    """

    size: Size
    layer_data: LayerData


@attr.s(auto_attribs=True, kw_only=True)
class TiledObject:
    """TiledObject object.

    See:
        https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#object

    Args:
        id: Unique ID of the object. Each object that is placed on a map gets a unique
            id. Even if an object was deleted, no object gets the same ID.
        gid: Global tiled object ID.
        location: The location of the object in pixels.
        size: The width of the object in pixels (default: (0, 0)).
        rotation: The rotation of the object in degrees clockwise (default: 0).
        opacity: The opacity of the object. (default: 255)
        name: The name of the object.
        type: The type of the object.
        properties: The properties of the TiledObject.
        template: A reference to a Template object FIXME
    """

    id_: int
    gid: Optional[int] = None

    location: OrderedPair
    size: Optional[Size] = None
    rotation: Optional[float] = None
    opacity: Optional[float] = None

    name: Optional[str] = None
    type: Optional[str] = None

    properties: Optional[Properties] = None
    template: Optional[Template] = None


@attr.s()
class RectangleObject(TiledObject):
    """Rectangle shape defined by a point, width, and height.

    See: https://doc.mapeditor.org/en/stable/manual/objects/#insert-rectangle
        (objects in tiled are rectangles by default, so there is no specific
        documentation on the tmx-map-format page for it.)
    """


@attr.s()
class ElipseObject(TiledObject):
    """Elipse shape defined by a point, width, and height.

    See: https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#ellipse
    """


@attr.s()
class PointObject(TiledObject):
    """Point defined by a point (x,y).

    See: https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#point
    """


@attr.s(auto_attribs=True, kw_only=True)
class TileImageObject(TiledObject):
    """Polygon shape defined by a set of connections between points.

    See: https://doc.mapeditor.org/en/stable/manual/objects/#insert-tile

    Attributes:
        gid: Refference to a global tile id.
    """

    gid: int


@attr.s(auto_attribs=True, kw_only=True)
class PolygonObject(TiledObject):
    """Polygon shape defined by a set of connections between points.

    See: https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#polygon

    Attributes:
        points: FIXME
    """

    points: List[OrderedPair]


@attr.s(auto_attribs=True, kw_only=True)
class PolylineObject(TiledObject):
    """Polyline defined by a set of connections between points.

    See:
        https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#polyline

    Attributes:
        points: List of coordinates relative to the location of the object.
    """

    points: List[OrderedPair]


@attr.s(auto_attribs=True, kw_only=True)
class TextObject(TiledObject):
    """Text object with associated settings.

    See: https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#text
        and https://doc.mapeditor.org/en/stable/manual/objects/#insert-text

    Attributes:
        font_family: The font family used (default: "sans-serif")
        font_size: The size of the font in pixels. (default: 16)
        wrap: Whether word wrapping is enabled. (default: False)
        color: Color of the text. (default: #000000)
        bold: Whether the font is bold. (default: False)
        italic: Whether the font is italic. (default: False)
        underline: Whether the text is underlined. (default: False)
        strike_out: Whether the text is striked-out. (default: False)
        kerning: Whether kerning should be used while rendering the text. (default:
            False)
        horizontal_align: Horizontal alignment of the text (default: "left")
        vertical_align: Vertical alignment of the text (defalt: "top")
    """

    text: str
    font_family: str = "sans-serif"
    font_size: int = 16
    wrap: bool = False
    color: str = "#000000"
    bold: bool = False
    italic: bool = False
    underline: bool = False
    strike_out: bool = False
    kerning: bool = False
    horizontal_align: str = "left"
    vertical_align: str = "top"


@attr.s(auto_attribs=True, kw_only=True)
class ObjectLayer(Layer):
    """
    TiledObject Group Object.

    The object group is in fact a map layer, and is hence called "object layer" in
        Tiled.

    See: https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#objectgroup

    Args:
        tiled_objects: List of tiled_objects in the layer.
        offset: Rendering offset of the layer object in pixels.
        color: The color used to display the objects in this group. FIXME: editor only?
        draworder: Whether the objects are drawn according to the order of the object
            elements in the object group element ('manual'), or sorted by their
            y-coordinate ('topdown'). Defaults to 'topdown'. See:
            https://doc.mapeditor.org/en/stable/manual/objects/#changing-stacking-order
            for more info.

    """

    tiled_objects: List[TiledObject]

    color: Optional[str] = None
    draw_order: Optional[str] = "topdown"


@attr.s(auto_attribs=True, kw_only=True)
class LayerGroup(Layer):
    """Layer Group.

    A LayerGroup can be thought of as a layer that contains layers
        (potentially including other LayerGroups).

    Offset and opacity recursively affect child layers.

    See: https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#group

    Attributes:
        Layers: Layers in group.
    """

    layers: Optional[List[Union["LayerGroup", Layer, ObjectLayer]]]


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
    tiles: Optional[Dict[int, "Tile"]] = None
    tsx_file: Path = None
    parent_dir: Path = None


TileSetDict = Dict[int, TileSet]


@attr.s(auto_attribs=True, kw_only=True)
class Tile:
    """Individual tile object.

    See: https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#tile

    Args:
        id: The local tile ID within its tileset.
        type: The type of the tile. Refers to an object type and is used by tile
            objects.
        terrain: Defines the terrain type of each corner of the tile.
        animation: Each tile can have exactly one animation associated with it.
    """

    id_: int
    type_: Optional[str] = None
    terrain: Optional[TileTerrain] = None
    animation: Optional[List[Frame]] = None
    objectgroup: Optional[List[TiledObject]] = None
    image: Optional[Image] = None
    properties: Optional[List[Property]] = None
    tileset: Optional[TileSet] = None
    flipped_horizontally: bool = False
    flipped_diagonally: bool = False
    flipped_vertically: bool = False


@attr.s(auto_attribs=True)
class TileMap:
    """Object for storing a TMX with all associated layers and properties.

    See: https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#map

    Attributes:
        parent_dir: The directory the TMX file is in. Used for finding relative paths
            to TSX files and other assets.
        version: The TMX format version.
        tiledversion: The Tiled version used to save the file. May be a date (for
            snapshot builds).
        orientation: Map orientation. Tiled supports "orthogonal", "isometric",
            "staggered" and "hexagonal"
        renderorder: The order in which tiles on tile layers are rendered. Valid values
            are right-down, right-up, left-down and left-up. In all cases, the map is
            drawn row-by-row. (only supported for orthogonal maps at the moment)
        map_size: The map width in tiles.
        tile_size: The width of a tile.
        infinite: If the map is infinite or not.
        hexsidelength: Only for hexagonal maps. Determines the width or height
            (depending on the staggered axis) of the tile's edge, in pixels.
        stagger_axis: For staggered and hexagonal maps, determines which axis ("x" or
            "y") is staggered.
        staggerindex: For staggered and hexagonal maps, determines whether the "even"
            or "odd" indexes along the staggered axis are shifted.
        backgroundcolor: The background color of the map.
        nextlayerid: Stores the next available ID for new layers.
        nextobjectid: Stores the next available ID for new objects.
        tile_sets: Dict of tile sets used in this map. Key is the first GID for the
            tile set. The value is a TileSet object.
        layers: List of layer objects by draw order.
    """

    parent_dir: Path
    tmx_file: Union[str, Path]

    version: str
    tiled_version: str
    orientation: str
    render_order: str
    map_size: Size
    tile_size: Size
    infinite: bool
    next_layer_id: Optional[int]
    next_object_id: int

    tile_sets: TileSetDict
    layers: List[Layer]

    hex_side_length: Optional[int] = None
    stagger_axis: Optional[int] = None
    stagger_index: Optional[int] = None
    background_color: Optional[Color] = None

    properties: Optional[Properties] = None

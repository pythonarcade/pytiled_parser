"""
Functions and classes for managing a map created in the "Tiled Map Editor"
"""

import csv
import dataclasses
import functools
import re

from collections import OrderedDict
from pathlib import Path

import xml.etree.ElementTree as etree

from typing import * # pylint: disable=W0401


class EncodingError(Exception):
    """
    Tmx layer encoding is of an unknown type.
    """


class TileNotFoundError(Exception):
    """
    Tile not found in tileset.
    """


class ImageNotFoundError(Exception):
    """
    Image not found.
    """


class Color(NamedTuple):
    """
    Color object.

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
    """
    OrderedPair NamedTuple.

    Attributes:
        :x (Union[int, float]): X coordinate.
        :y (Union[int, float]): Y coordinate.
    """
    x: Union[int, float]
    y: Union[int, float]


def _parse_color(color: str) -> Color:
    """
    Converts the color formats that Tiled uses into ones that Arcade accepts.

    Returns:
        :Color: Color object in the format that Arcade understands.
    """
    # strip initial '#' character
    if not len(color) % 2 == 0: # pylint: disable=C2001
        color = color[1:]

    if len(color) == 6:
        # full opacity if no alpha specified
        alpha = 0xFF
        red = int(color[0:2], 16)
        green = int(color[2:4], 16)
        blue = int(color[4:6], 16)
    else:
        alpha = int(color[0:2], 16)
        red = int(color[2:4], 16)
        green = int(color[4:6], 16)
        blue = int(color[6:8], 16)

    return Color(red, green, blue, alpha)


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


class Image(NamedTuple):
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
    trans: Optional[Color]
    width: Optional[int]
    height: Optional[int]


def _parse_image_element(image_element: etree.Element) -> Image:
    """
    Parse image element given.

    Returns:
        :Color: Color in Arcade's preffered format.
    """
    source = image_element.attrib['source']

    trans = None
    try:
        trans = _parse_color(image_element.attrib['trans'])
    except KeyError:
        pass

    width = None
    try:
        width = int(image_element.attrib['width'])
    except KeyError:
        pass

    height = None
    try:
        height = int(image_element.attrib['height'])
    except KeyError:
        pass

    return Image(source, trans, width, height)


Properties = Dict[str, Union[int, float, Color, Path, str]]


def _parse_properties_element(
        properties_element: etree.Element) -> Properties:
    """
    Adds Tiled property to Properties dict.

    Args:
        :name (str): Name of property.
        :property_type (str): Type of property. Can be string, int, float,
            bool, color or file. Defaults to string.
        :value (str): The value of the property.

    Returns:
        :Properties: Properties Dict object.
    """
    properties: Properties = {}
    for property_element in properties_element.findall('./property'):
        name = property_element.attrib['name']
        try:
            property_type = property_element.attrib['type']
        except KeyError:
            # strings do not have an attribute in property elements
            property_type = 'string'
        value = property_element.attrib['value']

        property_types = ['string', 'int', 'float', 'bool', 'color', 'file']
        assert property_type in property_types, (
            f"Invalid type for property {name}")

        if property_type == 'int':
            properties[name] = int(value)
        elif property_type == 'float':
            properties[name] = float(value)
        elif property_type == 'color':
            properties[name] = _parse_color(value)
        elif property_type == 'file':
            properties[name] = Path(value)
        elif property_type == 'bool':
            if value == 'true':
                properties[name] = True
            else:
                properties[name] = False
        else:
            properties[name] = value

    return properties


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
        :tileid (int): The local ID of a tile within the parent tile set
            object.
        :duration (int): How long in milliseconds this frame should be
            displayed before advancing to the next frame.
    """
    tileid: int
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
    id: int # pylint: disable=C0103
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


def _parse_layer_type(layer_element: etree.Element) -> LayerType:
    """
    Parse layer type element given.
    """
    id = int(layer_element.attrib['id'])

    name = layer_element.attrib['name']

    layer_type_object = LayerType(id, name)

    try:
        offset_x = float(layer_element.attrib['offsetx'])
    except KeyError:
        offset_x = 0

    try:
        offset_y = float(layer_element.attrib['offsety'])
    except KeyError:
        offset_y = 0
    offset = OrderedPair(offset_x, offset_y)

    try:
        layer_type_object.opacity = round(
            float(layer_element.attrib['opacity']) * 255)
    except KeyError:
        pass

    properties_element = layer_element.find('./properties')
    if properties_element is not None:
        layer_type_object.properties = _parse_properties_element(
            properties_element)

    if layer_element.tag == 'layer':
        return _parse_layer(layer_element, layer_type_object)
    elif layer_element.tag == 'objectgroup':
        return _parse_object_group(layer_element, layer_type_object)
    # else:
    #     return _parse_layer_group(layer_element, layer_type_object)


LayerData = Union[List[List[int]], List[Chunk]]
"""
The tile data for one layer.

Either a 2 dimensional array of integers representing the global tile IDs
    for a map layer, or a lists of chunks for an infinite map layer.
"""


@dataclasses.dataclass
class _LayerBase:
    width: int
    height: int
    data: LayerData


@dataclasses.dataclass
class Layer(LayerType, _LayerBase):
    """
    Map layer object.

    See: https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#layer

    Attributes:
        :width (int): The width of the layer in tiles. Always the same as
            the map width for fixed-size maps.
        :height (int): The height of the layer in tiles. Always the same as
            the map height for fixed-size maps.
        :data (LayerData): Either an 2 dimensional array of integers
            representing the global tile IDs for the map layer, or a list of
            chunks for an infinite map.
    """


def _parse_layer(element: etree.Element, layer_type: LayerType) -> Layer:
    """
    Parse layer element given.
    """
    width = int(element.attrib['width'])
    height = int(element.attrib['height'])
    data_element = element.find('./data')
    if data_element is not None:
        data: LayerData = _parse_data(data_element, width)
    else:
        raise ValueError('{element} has no child data element.')

    return Layer(width, height, data, **layer_type.__dict__)


@dataclasses.dataclass
class _ObjectBase:
    id: int
    location: OrderedPair


@dataclasses.dataclass
class _ObjectDefaults:
    size: OrderedPair = OrderedPair(0, 0)
    rotation: int = 0
    opacity: int = 0xFF

    name: Optional[str] = None
    type: Optional[str] = None

    properties: Optional[Properties] = None
    template: Optional[Template] = None


@dataclasses.dataclass
class Object(_ObjectDefaults, _ObjectBase):
    """
    ObjectGroup Object.

    See: \
    https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#object

    Args:
        :id (int): Unique ID of the object. Each object that is placed on a
            map gets a unique id. Even if an object was deleted, no object
            gets the same ID.
        :location (OrderedPair): The location of the object in pixels.
        :name (Optional[str]): The name of the object.
        :type (Optional[str]): The type of the object.
        :width (int): The width of the object in pixels (default: 0).
        :height (int): The height of the object in pixels (default: 0).
        :opacity (int): The opacity of the object. (default: 255)
        :rotation (int): The rotation of the object in degrees clockwise
            (default: 0).
        :template Optional[Template]: A reference to a Template object
            FIXME
    """


@dataclasses.dataclass
class RectangleObject(Object):
    """
    Rectangle shape defined by a point, width, and height.

    See: https://doc.mapeditor.org/en/stable/manual/objects/#insert-rectangle
        (objects in tiled are rectangles by default, so there is no specific
        documentation on the tmx-map-format page for it.)
    """


@dataclasses.dataclass
class ElipseObject(Object):
    """
    Elipse shape defined by a point, width, and height.

    See: https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#ellipse
    """


@dataclasses.dataclass
class PointObject(Object):
    """
    Point defined by a point (x,y).

    See: https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#point
    """


@dataclasses.dataclass
class _TileObjectBase(_ObjectBase):
    gid: int


@dataclasses.dataclass
class TileObject(Object, _TileObjectBase):
    """
    Polygon shape defined by a set of connections between points.

    See: https://doc.mapeditor.org/en/stable/manual/objects/#insert-tile

    Attributes:
        :gid (int): Refference to a global tile id.
    """


@dataclasses.dataclass
class _PointsObjectBase(_ObjectBase):
    points: List[OrderedPair]


@dataclasses.dataclass
class PolygonObject(Object, _PointsObjectBase):
    """
    Polygon shape defined by a set of connections between points.

    See: https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#polygon

    Attributes:
        :points (List[OrderedPair])
    """


@dataclasses.dataclass
class PolylineObject(Object, _PointsObjectBase):
    """
    Polyline defined by a set of connections between points.

    See: \
https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#polyline

    Attributes:
        :points (List[Tuple[int, int]]): List of coordinates relative to \
        the location of the object.
    """


@dataclasses.dataclass
class _TextObjectBase(_ObjectBase):
    text: str


@dataclasses.dataclass
class _TextObjectDefaults(_ObjectDefaults):
    font_family: str = 'sans-serif'
    font_size: int = 16
    wrap: bool = False
    color: Color = _parse_color('#000000')
    bold: bool = False
    italic: bool = False
    underline: bool = False
    strike_out: bool = False
    kerning: bool = False
    horizontal_align: str = 'left'
    vertical_align: str = 'top'


@dataclasses.dataclass
class TextObject(Object, _TextObjectDefaults, _TextObjectBase):
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
class _ObjectGroupBase:
    objects: List[Object]


@dataclasses.dataclass
class _ObjectGroupDefaults(_LayerTypeDefaults):
    color: Optional[Color] = None
    draworder: Optional[str] = 'topdown'


@dataclasses.dataclass
class ObjectGroup(LayerType, _ObjectGroupDefaults, _ObjectGroupBase):
    """
    Object Group Object.

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
        :objects (Dict[int, Object]): Dict Object objects by Object.id.
    """


def _parse_object_group(
        element: etree.Element, layer_type: LayerType) -> ObjectGroup:
    """
    Parse object group element given.
    """
    object_elements = element.findall('./object')
    objects: List[Object] = []

    for object_element in object_elements:
        id = int(object_element.attrib['id'])
        location_x = float(object_element.attrib['x'])
        location_y = float(object_element.attrib['y'])
        location = OrderedPair(location_x, location_y)

        object = Object(id, location)

        try:
            width = float(object_element.attrib['width'])
        except KeyError:
            width = 0

        try:
            height = float(object_element.attrib['height'])
        except KeyError:
            height = 0

        object.size = OrderedPair(width, height)

        try:
            object.opacity = round(
                float(object_element.attrib['opacity']) * 255)
        except KeyError:
            pass

        try:
            object.rotation = int(object_element.attrib['rotation'])
        except KeyError:
            pass

        try:
            object.name = object_element.attrib['name']
        except KeyError:
            pass


        properties_element = object_element.find('./properties')
        if properties_element is not None:
            print('hi')
            object.properties = _parse_properties_element(properties_element)

        objects.append(object)

    object_group = ObjectGroup(objects, **layer_type.__dict__)
    try:
        color = _parse_color(element.attrib['color'])
    except KeyError:
        pass

    try:
        draworder = element.attrib['draworder']
    except KeyError:
        pass

    return object_group


class LayerGroup:
    """
    Object for a Layer Group.

    A LayerGroup can be thought of as a layer that contains layers
        (potentially including other LayerGroups).

    Attributes offset_x, offset_y, and opacity recursively affect child
        layers.

    See: https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#group

    Attributes:
        FIXME
    """


def _decode_csv_layer(data_text):
    tile_grid = []
    lines = data_text.split("\n")
    # remove erronious empty lists due to a newline being on both ends of text
    lines = lines[1:]
    lines = lines[:-1]
    for line in lines:
        line_list = line.split(",")
        while '' in line_list:
            line_list.remove('')
        line_list_int = [int(item) for item in line_list]
        tile_grid.append(line_list_int)

    return tile_grid


def _decode_base64_data(data_text, compression, layer_width):
    tile_grid = [[]]

    unencoded_data = base64.b64decode(data_text)
    if compression == "zlib":
        unzipped_data = zlib.decompress(unencoded_data)
    elif compression == "gzip":
        unzipped_data = gzip.decompress(unencoded_data)
    elif compression is None:
        unzipped_data = unencoded_data
    else:
        raise ValueError(f"Unsupported compression type '{compression}'.")

    # Turn bytes into 4-byte integers
    byte_count = 0
    int_count = 0
    int_value = 0
    row_count = 0
    for byte in unzipped_data:
        int_value += byte << (byte_count * 8)
        byte_count += 1
        if byte_count % 4 == 0:
            byte_count = 0
            int_count += 1
            tile_grid[row_count].append(int_value)
            int_value = 0
            if int_count % layer_width == 0:
                row_count += 1
                tile_grid.append([])

    tile_grid.pop()
    return tile_grid


def _decode_data(element: etree.Element,
                 layer_width: int,
                 encoding: str,
                 compression: Optional[str]) -> List[List[int]]:
    """
    Decodes data or chunk data.

    Args:
        :element (Element): Element to have text decoded.
        :layer_width (int): Number of tiles per column in this layer. Used
            for determining when to cut off a row when decoding base64
            encoding layers.
        :encoding (str): Encoding format of the layer data.
        :compression (str): Compression format of the layer data.
    """
    # etree.Element.text comes with an appended and a prepended '\n'
    supported_encodings = ['base64', 'csv']
    if encoding not in supported_encodings:
        raise ValueError('{encoding} is not a valid encoding')

    supported_compression = [None, 'gzip', 'zlib']
    if compression is not None:
        if encoding != 'base64':
            raise ValueError('{encoding} does not support compression')
        if compression not in supported_compression:
            raise ValueError('{compression} is not a valid compression type')

    try:
        data_text = element.text[1:-1] # type: ignore
    except AttributeError:
        raise AttributeError('{element} lacks layer data.')

    if encoding == 'csv':
        return _decode_csv_layer(data_text)

    return _decode_base64_data(data_text, compression, layer_width)

def _parse_data(element: etree.Element, layer_width: int) -> LayerData:
    """
    Parses layer data.

    Will parse CSV, base64, gzip-base64, or zlip-base64 encoded data.

    Args:
        :element (Element): Data element to parse.
        :width (int): Layer width. Used for base64 decoding.

    Returns:
        :LayerData: Data object containing layer data or chunks of data.
    """
    encoding = element.attrib['encoding']
    compression = None
    try:
        compression = element.attrib['compression']
    except KeyError:
        pass

    chunk_elements = element.findall('./chunk')
    if chunk_elements:
        chunks: List[Chunk] = []
        for chunk_element in chunk_elements:
            x = int(chunk_element.attrib['x'])
            y = int(chunk_element.attrib['y'])
            location = OrderedPair(x, y)
            width = int(chunk_element.attrib['width'])
            height = int(chunk_element.attrib['height'])
            layer_data = _decode_data(
                chunk_element, layer_width, encoding, compression)
            chunks.append(Chunk(location, width, height, layer_data))
        return chunks

    return _decode_data(element, layer_width, encoding, compression)




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
    object_group: Optional[ObjectGroup]


@dataclasses.dataclass
class TileSet:
    """
    Object for storing a TSX with all associated collision data.

    Args:
        :name (str): The name of this tileset.
        :max_tile_size (OrderedPair): The maximum size of a tile in this
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
    max_tile_size: OrderedPair
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


def _parse_tiles(tile_element_list: List[etree.Element]) -> Dict[int, Tile]:
    tiles: Dict[int, Tile] = {}
    for tile_element in tile_element_list:
        # id is not optional
        id = int(tile_element.attrib['id'])

        # optional attributes
        type = None
        try:
            type = tile_element.attrib['type']
        except KeyError:
            pass

        tile_terrain = None
        try:
            tile_terrain_attrib = tile_element.attrib['terrain']
        except KeyError:
            pass
        else:
            # https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#tile
            # an attempt to explain how terrains are handled is below.
            # 'terrain' attribute is a comma seperated list of 4 values,
            # each is either an integer or blank

            # convert to list of values
            terrain_list_attrib = re.split(',', tile_terrain_attrib)
            # terrain_list is list of indexes of Tileset.terrain_types
            terrain_list: List[Optional[int]] = []
            # each index in terrain_list_attrib reffers to a corner
            for corner in terrain_list_attrib:
                if corner == '':
                    terrain_list.append(None)
                else:
                    terrain_list.append(int(corner))
            tile_terrain = TileTerrain(*terrain_list)

        # tile element optional sub-elements
        animation: Optional[List[Frame]] = None
        tile_animation_element = tile_element.find('./animation')
        if tile_animation_element:
            animation = []
            frames = tile_animation_element.findall('./frame')
            for frame in frames:
                # tileid reffers to the Tile.id of the animation frame
                tileid = int(frame.attrib['tileid'])
                # duration is in MS. Should perhaps be converted to seconds.
                # FIXME: make decision
                duration = int(frame.attrib['duration'])
                animation.append(Frame(tileid, duration))

        # if this is None, then the Tile is part of a spritesheet
        tile_image = None
        tile_image_element = tile_element.find('./image')
        if tile_image_element:
            tile_image = _parse_image_element(tile_image_element)

        object_group = None
        tile_object_group_element = tile_element.find('./objectgroup')
        if tile_object_group_element:
            object_group = ObjectGroup(tile_object_group_element)

        tiles[id] = Tile(id,
                         type,
                         tile_terrain,
                         animation,
                         tile_image,
                         object_group)

    return tiles


def _parse_tile_set(tile_set_element: etree.Element) -> TileSet:
    """
    Parses a tile set that is embedded into a TMX.
    """
    # get all basic attributes
    name = tile_set_element.attrib['name']
    max_tile_width = int(tile_set_element.attrib['tilewidth'])
    max_tile_height = int(tile_set_element.attrib['tileheight'])
    max_tile_size = OrderedPair(max_tile_width, max_tile_height)

    spacing = None
    try:
        spacing = int(tile_set_element.attrib['spacing'])
    except KeyError:
        pass

    margin = None
    try:
        margin = int(tile_set_element.attrib['margin'])
    except KeyError:
        pass

    tile_count = None
    try:
        tile_count = int(tile_set_element.attrib['tilecount'])
    except KeyError:
        pass

    columns = None
    try:
        columns = int(tile_set_element.attrib['columns'])
    except KeyError:
        pass

    tile_offset = None
    tileoffset_element = tile_set_element.find('./tileoffset')
    if tileoffset_element is not None:
        tile_offset_x = int(tileoffset_element.attrib['x'])
        tile_offset_y = int(tileoffset_element.attrib['y'])
        tile_offset = OrderedPair(tile_offset_x, tile_offset_y)

    grid = None
    grid_element = tile_set_element.find('./grid')
    if grid_element is not None:
        grid_orientation = grid_element.attrib['orientation']
        grid_width = int(grid_element.attrib['width'])
        grid_height = int(grid_element.attrib['height'])
        grid = Grid(grid_orientation, grid_width, grid_height)

    properties = None
    properties_element = tile_set_element.find('./properties')
    if properties_element is not None:
        properties = _parse_properties_element(properties_element)

    terrain_types: Optional[List[Terrain]] = None
    terrain_types_element = tile_set_element.find('./terraintypes')
    if terrain_types_element is not None:
        terrain_types = []
        for terrain in terrain_types_element.findall('./terrain'):
            name = terrain.attrib['name']
            terrain_tile = int(terrain.attrib['tile'])
            terrain_types.append(Terrain(name, terrain_tile))

    image = None
    image_element = tile_set_element.find('./image')
    if image_element is not None:
        image = _parse_image_element(image_element)

    tile_element_list = tile_set_element.findall('./tile')
    tiles = _parse_tiles(tile_element_list)

    return TileSet(
        name,
        max_tile_size,
        spacing,
        margin,
        tile_count,
        columns,
        tile_offset,
        grid,
        properties,
        image,
        terrain_types,
        tiles,
    )


@functools.lru_cache()
def _parse_external_tile_set(
        parent_dir: Path, tile_set_element: etree.Element) -> TileSet:
    """
    Parses an external tile set.

    Caches the results to speed up subsequent instances.
    """
    source = Path(tile_set_element.attrib['source'])
    tile_set_tree = etree.parse(str(parent_dir / Path(source))).getroot()

    return _parse_tile_set(tile_set_tree)


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
        :width (int): The map width in tiles.
        :height (int): The map height in tiles.
        :tile_width (int): The width of a tile.
        :tile_height (int): The height of a tile.
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
            in this map. Key is the source for external tile sets or the name
            for embedded ones. The value is a TileSet object.
        :layers (OrderedDict[str, Union[Layer, ObjectGroup, LayerGroup]]):
            OrderedDict of layer objects by draw order.
    """
    parent_dir: Path

    version: str
    tiled_version: str
    orientation: str
    render_order: str
    width: int
    height: int
    tile_width: int
    tile_height: int
    infinite: bool
    next_layer_id: int
    next_object_id: int

    tile_sets: Dict[int, TileSet]
    layers: List[LayerType]

    hex_side_length: Optional[int] = None
    stagger_axis: Optional[int] = None
    stagger_index: Optional[int] = None
    background_color: Optional[Color] = None

    properties: Optional[Properties] = None


def parse_tile_map(tmx_file: Union[str, Path]):
    # setting up XML parsing
    map_tree = etree.parse(str(tmx_file))
    map_element = map_tree.getroot()

    # positional arguments for TileMap
    parent_dir = Path(tmx_file).parent

    version = map_element.attrib['version']
    tiled_version = map_element.attrib['tiledversion']
    orientation = map_element.attrib['orientation']
    render_order = map_element.attrib['renderorder']
    width = int(map_element.attrib['width'])
    height = int(map_element.attrib['height'])
    tile_width = int(map_element.attrib['tilewidth'])
    tile_height = int(map_element.attrib['tileheight'])

    infinite_attribute = map_element.attrib['infinite']
    infinite = True if infinite_attribute == 'true' else False

    next_layer_id = int(map_element.attrib['nextlayerid'])
    next_object_id = int(map_element.attrib['nextobjectid'])

    # parse all tilesets
    tile_sets: Dict[int, TileSet] = {}
    tile_set_element_list = map_element.findall('./tileset')
    for tile_set_element in tile_set_element_list:
        # tiled docs are ambiguous about the 'firstgid' attribute
        # current understanding is for the purposes of mapping the layer
        # data to the tile set data, add the 'firstgid' value to each
        # tile 'id'; this means that the 'firstgid' is specific to each,
        # tile set as they pertain to the map, not tile set specific as
        # the tiled docs can make it seem
        # 'firstgid' is saved beside each TileMapXML
        firstgid = int(tile_set_element.attrib['firstgid'])
        try:
            # check if is an external TSX
            source = tile_set_element.attrib['source']
        except KeyError:
            # the tile set in embedded
            name = tile_set_element.attrib['name']
            tile_sets[firstgid] = _parse_tile_set(
                tile_set_element)
        else:
            # tile set is external
            tile_sets[firstgid] = _parse_external_tile_set(
                parent_dir, tile_set_element)

    # parse all layers
    layers: List[LayerType] = []
    layer_tags = ['layer', 'objectgroup', 'group']
    for element in map_element.findall('./'):
        if element.tag not in layer_tags:
            # only layer_tags are layer elements
            continue
        layers.append(_parse_layer_type(element))

    tile_map = TileMap(
        parent_dir,
        version,
        tiled_version,
        orientation,
        render_order,
        width,
        height,
        tile_width,
        tile_height,
        infinite,
        next_layer_id,
        next_object_id,
        tile_sets,
        layers,
    )

    try:
        tile_map.hex_side_length = int(map_element.attrib['hexsidelength'])
    except KeyError:
        pass

    try:
        tile_map.stagger_axis = int(map_element.attrib['staggeraxis'])
    except KeyError:
        pass

    try:
        tile_map.stagger_index = int(map_element.attrib['staggerindex'])
    except KeyError:
        pass

    try:
        backgroundcolor = map_element.attrib['backgroundcolor']
    except KeyError:
        pass
    else:
        tile_map.background_color = _parse_color(backgroundcolor)

    properties_element = map_tree.find('./properties')
    if properties_element is not None:
        tile_map.properties = _parse_properties_element(properties_element)

    return tile_map


'''
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
'''




#buffer

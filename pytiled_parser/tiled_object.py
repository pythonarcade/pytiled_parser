# pylint: disable=too-few-public-methods

from typing import Callable, Dict, List, Optional, Union

import attr

from pytiled_parser import OrderedPair, Size
from pytiled_parser.properties import Properties
from pytiled_parser.template import Template


@attr.s(auto_attribs=True, kw_only=True)
class TiledObject:
    """TiledObject object.

    See:
        https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#object

    Attributes:
        id_: Unique ID of the tiled object. Each tiled object that is placed on a map
            gets a unique id. Even if an tiled object was deleted, no tiled object gets
            the same ID.
        gid: Global tiled object ID.
        coordinates: The location of the tiled object in pixels.
        size: The width of the tiled object in pixels (default: (0, 0)).
        rotation: The rotation of the tiled object in degrees clockwise (default: 0).
        opacity: The opacity of the tiled object. (default: 1)
        name: The name of the tiled object.
        type: The type of the tiled object.
        properties: The properties of the TiledObject.
        template: A reference to a Template tiled object FIXME
    """

    id_: int
    gid: Optional[int] = None

    coordinates: OrderedPair
    size: Size = Size(0, 0)
    rotation: float = 0
    opacity: float = 1

    name: Optional[str] = None
    type: Optional[str] = None

    properties: Optional[Properties] = None
    template: Optional[Template] = None


@attr.s()
class Ellipse(TiledObject):
    """Elipse shape defined by a point, width, height, and rotation.

    See: https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#ellipse
    """


@attr.s()
class Point(TiledObject):
    """Point defined by a coordinate (x,y).

    See: https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#point
    """


@attr.s(auto_attribs=True, kw_only=True)
class Polygon(TiledObject):
    """Polygon shape defined by a set of connections between points.

    See: https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#polygon

    Attributes:
        points: FIXME
    """

    points: List[OrderedPair]


@attr.s(auto_attribs=True, kw_only=True)
class Polyline(TiledObject):
    """Polyline defined by a set of connections between points.

    See:
        https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#polyline

    Attributes:
        points: List of coordinates relative to the location of the object.
    """

    points: List[OrderedPair]


@attr.s()
class Rectangle(TiledObject):
    """Rectangle shape defined by a point, width, and height.

    See: https://doc.mapeditor.org/en/stable/manual/objects/#insert-rectangle
        (objects in tiled are rectangles by default, so there is no specific
        documentation on the tmx-map-format page for it.)
    """


@attr.s(auto_attribs=True, kw_only=True)
class Text(TiledObject):
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
class TileImage(TiledObject):
    """Tile object

    See: https://doc.mapeditor.org/en/stable/manual/objects/#insert-tile

    Attributes:
        gid: Reference to a global tile id.
    """

    gid: int


RawProperties = Dict[str, Union[str, int, float, bool]]


RawTiledObject = Dict[str, Union[str, int, float, bool, RawProperties]]


RawTiledObjects = List[RawTiledObject]


def _cast_ellipse(raw_tiled_object: RawTiledObject) -> Ellipse:
    pass


def _cast_rectangle(raw_tiled_object: RawTiledObject) -> Rectangle:
    pass


def _cast_point(raw_tiled_object: RawTiledObject) -> Point:
    pass


def _cast_tile_image(raw_tiled_object: RawTiledObject) -> TileImage:
    pass


def _cast_polygon(raw_tiled_object: RawTiledObject) -> Polygon:
    pass


def _cast_polyline(raw_tiled_object: RawTiledObject) -> Polyline:
    pass


def _cast_text(raw_tiled_object: RawTiledObject) -> Text:
    pass


def _get_tiled_object_caster(
    raw_tiled_object: RawTiledObject,
) -> Callable[[RawTiledObject], TiledObject]:
    """ Get the caster function for the raw tiled object.

    Args:
        raw_tiled_object: Raw Tiled object that is analysed to determine which caster
            to return.

    Returns:
        Callable[[RawTiledObject], TiledObject]: The caster function.
    """


def _cast_tiled_object(raw_tiled_object: RawTiledObject) -> TiledObject:
    """ Cast the raw tiled object into a pytiled_parser type

    Args:
        raw_tiled_object: Raw Tiled object that is to be cast.

    Returns:
        TiledObject: a properly typed Tiled object.
    """
    caster = _get_tiled_object_caster(raw_tiled_object)

    tiled_object = caster(raw_tiled_object)
    return tiled_object


def cast_tiled_objects(raw_tiled_objects: RawTiledObjects) -> List[TiledObject]:
    """Parses objects found in a 'objectgroup' element.

    Args:
        object_elements: List of object elements to be parsed.

    Returns:
        list: List of parsed tiled objects.
    """
    tiled_objects: List[TiledObject] = []

    for raw_tiled_object in raw_tiled_objects:
        tiled_objects.append(_cast_tiled_object(raw_tiled_object))

    return tiled_objects
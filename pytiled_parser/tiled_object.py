# pylint: disable=too-few-public-methods

from typing import Callable, Dict, List, Mapping, Optional, Union

import attr
from typing_extensions import TypedDict

from .common_types import OrderedPair, Size
from .properties import Properties
from .template import Template


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

    id: int

    coordinates: OrderedPair
    size: Size = Size(0, 0)
    rotation: float = 0
    opacity: float = 1
    visible: bool

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
class Tile(TiledObject):
    """Tile object

    See: https://doc.mapeditor.org/en/stable/manual/objects/#insert-tile

    Attributes:
        gid: Reference to a global tile id.
    """

    gid: int


RawProperties = Dict[str, Union[str, float, bool]]


class RawTiledObject(TypedDict):
    """ The keys and their types that appear in a Tiled JSON Object."""

    id: int
    gid: int
    x: float
    y: float
    width: float
    height: float
    rotation: float
    opacity: float
    visible: bool
    name: str
    type: str
    properties: Properties
    template: Template
    ellipse: bool
    point: bool
    polygon: List[Dict]


RawTiledObjects = List[RawTiledObject]


def _get_common_attributes(raw_tiled_object: RawTiledObject) -> TiledObject:
    """ Create a TiledObject containing all the attributes common to all tiled objects

    Args:
        raw_tiled_object: Raw Tiled object get common attributes from

    Returns:
        TiledObject: The attributes in common of all Tiled Objects
    """

    # required attributes
    id_ = raw_tiled_object["id"]
    coordinates = OrderedPair(x=raw_tiled_object["x"], y=raw_tiled_object["y"])
    visible = raw_tiled_object["visible"]

    common_attributes = TiledObject(id=id_, coordinates=coordinates, visible=visible)

    # optional attributes
    if any([raw_tiled_object.get("width"), raw_tiled_object.get("height")]):
        # we have to check if either are truthy before we proceed to create Size
        _width = raw_tiled_object.get("width")
        if _width:
            width = _width
        else:
            width = 0

        _height = raw_tiled_object.get("height")
        if _height:
            height = _height
        else:
            height = 0

        common_attributes.size = Size(width, height)

    if raw_tiled_object.get("rotation"):
        common_attributes.rotation = raw_tiled_object["rotation"]

    if raw_tiled_object.get("opacity"):
        common_attributes.opacity = raw_tiled_object["opacity"]

    if raw_tiled_object.get("name"):
        common_attributes.name = raw_tiled_object["name"]

    if raw_tiled_object.get("type"):
        common_attributes.type = raw_tiled_object["type"]

    if raw_tiled_object.get("properties"):
        raise NotImplementedError

    if raw_tiled_object.get("template"):
        raise NotImplementedError

    return common_attributes


def _cast_ellipse(raw_tiled_object: RawTiledObject) -> Ellipse:
    """ Cast the raw_tiled_object to an Ellipse object.

    Args:
        raw_tiled_object: Raw Tiled object to be casted to an Ellipse

    Returns:
        Ellipse: The Ellipse object created from the raw_tiled_object
    """
    return Ellipse(**_get_common_attributes(raw_tiled_object).__dict__)


def _cast_rectangle(raw_tiled_object: RawTiledObject) -> Rectangle:
    """ Cast the raw_tiled_object to a Rectangle object.

    Args:
        raw_tiled_object: Raw Tiled object to be casted to a Rectangle

    Returns:
        Rectangle: The Rectangle object created from the raw_tiled_object
    """
    return Rectangle(**_get_common_attributes(raw_tiled_object).__dict__)


def _cast_point(raw_tiled_object: RawTiledObject) -> Point:
    """ Cast the raw_tiled_object to a Point object.

    Args:
        raw_tiled_object: Raw Tiled object to be casted to a Point

    Returns:
        Point: The Point object created from the raw_tiled_object
    """
    return Point(**_get_common_attributes(raw_tiled_object).__dict__)


def _cast_tile(raw_tiled_object: RawTiledObject) -> Tile:
    raise NotImplementedError


def _cast_polygon(raw_tiled_object: RawTiledObject) -> Polygon:
    """ Cast the raw_tiled_object to a Polygon object.

    Args:
        raw_tiled_object: Raw Tiled object to be casted to a Polygon

    Returns:
        Polygon: The Polygon object created from the raw_tiled_object
    """
    polygon = []
    for point in raw_tiled_object["polygon"]:
        polygon.append(OrderedPair(point["x"], point["y"]))

    return Polygon(points=polygon, **_get_common_attributes(raw_tiled_object).__dict__)


def _cast_polyline(raw_tiled_object: RawTiledObject) -> Polyline:
    raise NotImplementedError


def _cast_text(raw_tiled_object: RawTiledObject) -> Text:
    raise NotImplementedError


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
    if raw_tiled_object.get("ellipse"):
        return _cast_ellipse

    if raw_tiled_object.get("point"):
        return _cast_point

    if raw_tiled_object.get("gid"):
        # Only Tile objects have the `gid` key (I think)
        return _cast_tile

    if raw_tiled_object.get("polygon"):
        return _cast_polygon

    if raw_tiled_object.get("polyline"):
        return _cast_polyline

    if raw_tiled_object.get("text"):
        return _cast_text

    return _cast_rectangle


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

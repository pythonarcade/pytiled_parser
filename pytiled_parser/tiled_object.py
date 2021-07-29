# pylint: disable=too-few-public-methods
import json
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

import attr
from typing_extensions import TypedDict

from . import properties as properties_
from .common_types import Color, OrderedPair, Size
from .util import parse_color


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
    """

    id: int

    coordinates: OrderedPair
    size: Size = Size(0, 0)
    rotation: float = 0
    visible: bool

    name: Optional[str] = None
    type: Optional[str] = None

    properties: properties_.Properties = {}


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
    color: Color = Color(255, 255, 255, 255)

    font_family: str = "sans-serif"
    font_size: float = 16

    bold: bool = False
    italic: bool = False
    kerning: bool = True
    strike_out: bool = False
    underline: bool = False

    horizontal_align: str = "left"
    vertical_align: str = "top"
    wrap: bool = False


@attr.s(auto_attribs=True, kw_only=True)
class Tile(TiledObject):
    """Tile object

    See: https://doc.mapeditor.org/en/stable/manual/objects/#insert-tile

    Attributes:
        gid: Reference to a global tile id.
    """

    gid: int
    new_tileset: Optional[Dict[str, Any]] = None
    new_tileset_path: Optional[Path] = None


class RawTextDict(TypedDict):
    """ The keys and their types that appear in a Text JSON Object."""

    text: str
    color: str

    fontfamily: str
    pixelsize: float  # this is `font_size` in Text

    bold: bool
    italic: bool
    strikeout: bool
    underline: bool
    kerning: bool

    halign: str
    valign: str
    wrap: bool


class RawTiledObject(TypedDict):
    """ The keys and their types that appear in a Tiled JSON Object."""

    id: int
    gid: int
    template: str
    x: float
    y: float
    width: float
    height: float
    rotation: float
    visible: bool
    name: str
    type: str
    properties: List[properties_.RawProperty]
    ellipse: bool
    point: bool
    polygon: List[Dict[str, float]]
    polyline: List[Dict[str, float]]
    text: Dict[str, Union[float, str]]


RawTiledObjects = List[RawTiledObject]


def _get_common_attributes(raw_tiled_object: RawTiledObject) -> TiledObject:
    """Create a TiledObject containing all the attributes common to all tiled objects

    Args:
        raw_tiled_object: Raw Tiled object get common attributes from

    Returns:
        TiledObject: The attributes in common of all Tiled Objects
    """

    common_attributes = TiledObject(
        id=raw_tiled_object["id"],
        coordinates=OrderedPair(raw_tiled_object["x"], raw_tiled_object["y"]),
        visible=raw_tiled_object["visible"],
        size=Size(raw_tiled_object["width"], raw_tiled_object["height"]),
        rotation=raw_tiled_object["rotation"],
        name=raw_tiled_object["name"],
        type=raw_tiled_object["type"],
    )

    if raw_tiled_object.get("properties") is not None:
        common_attributes.properties = properties_.cast(raw_tiled_object["properties"])

    return common_attributes


def _cast_ellipse(raw_tiled_object: RawTiledObject) -> Ellipse:
    """Cast the raw_tiled_object to an Ellipse object.

    Args:
        raw_tiled_object: Raw Tiled object to be casted to an Ellipse

    Returns:
        Ellipse: The Ellipse object created from the raw_tiled_object
    """
    return Ellipse(**_get_common_attributes(raw_tiled_object).__dict__)


def _cast_rectangle(raw_tiled_object: RawTiledObject) -> Rectangle:
    """Cast the raw_tiled_object to a Rectangle object.

    Args:
        raw_tiled_object: Raw Tiled object to be casted to a Rectangle

    Returns:
        Rectangle: The Rectangle object created from the raw_tiled_object
    """
    return Rectangle(**_get_common_attributes(raw_tiled_object).__dict__)


def _cast_point(raw_tiled_object: RawTiledObject) -> Point:
    """Cast the raw_tiled_object to a Point object.

    Args:
        raw_tiled_object: Raw Tiled object to be casted to a Point

    Returns:
        Point: The Point object created from the raw_tiled_object
    """
    return Point(**_get_common_attributes(raw_tiled_object).__dict__)


def _cast_tile(
    raw_tiled_object: RawTiledObject,
    new_tileset: Optional[Dict[str, Any]] = None,
    new_tileset_path: Optional[Path] = None,
) -> Tile:
    """Cast the raw_tiled_object to a Tile object.

    Args:
        raw_tiled_object: Raw Tiled object to be casted to a Tile

    Returns:
        Tile: The Tile object created from the raw_tiled_object
    """
    gid = raw_tiled_object["gid"]

    return Tile(
        gid=gid,
        new_tileset=new_tileset,
        new_tileset_path=new_tileset_path,
        **_get_common_attributes(raw_tiled_object).__dict__
    )


def _cast_polygon(raw_tiled_object: RawTiledObject) -> Polygon:
    """Cast the raw_tiled_object to a Polygon object.

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
    """Cast the raw_tiled_object to a Polyline object.

    Args:
        raw_tiled_object: Raw Tiled Object to be casted to a Polyline

    Returns:
        Polyline: The Polyline object created from the raw_tiled_object
    """
    polyline = []
    for point in raw_tiled_object["polyline"]:
        polyline.append(OrderedPair(point["x"], point["y"]))

    return Polyline(
        points=polyline, **_get_common_attributes(raw_tiled_object).__dict__
    )


def _cast_text(raw_tiled_object: RawTiledObject) -> Text:
    """Cast the raw_tiled_object to a Text object.

    Args:
        raw_tiled_object: Raw Tiled object to be casted to a Text object

    Returns:
        Text: The Text object created from the raw_tiled_object
    """
    # required attributes
    raw_text_dict: RawTextDict = raw_tiled_object["text"]
    text = raw_text_dict["text"]

    # create base Text object
    text_object = Text(text=text, **_get_common_attributes(raw_tiled_object).__dict__)

    # optional attributes
    if raw_text_dict.get("color") is not None:
        text_object.color = parse_color(raw_text_dict["color"])

    if raw_text_dict.get("fontfamily") is not None:
        text_object.font_family = raw_text_dict["fontfamily"]

    if raw_text_dict.get("pixelsize") is not None:
        text_object.font_size = raw_text_dict["pixelsize"]

    if raw_text_dict.get("bold") is not None:
        text_object.bold = raw_text_dict["bold"]

    if raw_text_dict.get("italic") is not None:
        text_object.italic = raw_text_dict["italic"]

    if raw_text_dict.get("kerning") is not None:
        text_object.kerning = raw_text_dict["kerning"]

    if raw_text_dict.get("strikeout") is not None:
        text_object.strike_out = raw_text_dict["strikeout"]

    if raw_text_dict.get("underline") is not None:
        text_object.underline = raw_text_dict["underline"]

    if raw_text_dict.get("halign") is not None:
        text_object.horizontal_align = raw_text_dict["halign"]

    if raw_text_dict.get("valign") is not None:
        text_object.vertical_align = raw_text_dict["valign"]

    if raw_text_dict.get("wrap") is not None:
        text_object.wrap = raw_text_dict["wrap"]

    return text_object


def _get_caster(
    raw_tiled_object: RawTiledObject,
) -> Callable[[RawTiledObject], TiledObject]:
    """Get the caster function for the raw tiled object.

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


def cast(
    raw_tiled_object: RawTiledObject,
    parent_dir: Optional[Path] = None,
) -> TiledObject:
    """Cast the raw tiled object into a pytiled_parser type

    Args:
        raw_tiled_object: Raw Tiled object that is to be cast.
        parent_dir: The parent directory that the map file is in.

    Returns:
        TiledObject: a properly typed Tiled object.

    Raises:
        RuntimeError: When a required parameter was not sent based on a condition.
    """
    new_tileset = None
    new_tileset_path = None

    if raw_tiled_object.get("template"):
        if not parent_dir:
            raise RuntimeError(
                "A parent directory must be specified when using object templates"
            )
        template_path = Path(parent_dir / raw_tiled_object["template"])
        with open(template_path) as raw_template_file:
            template = json.load(raw_template_file)
            if "tileset" in template:
                tileset_path = Path(
                    template_path.parent / template["tileset"]["source"]
                )
                with open(tileset_path) as raw_tileset_file:
                    new_tileset = json.load(raw_tileset_file)
                    new_tileset_path = tileset_path.parent

            loaded_template = template["object"]
            for key in loaded_template:
                if key != "id":
                    raw_tiled_object[key] = loaded_template[key]  # type: ignore

    if raw_tiled_object.get("gid"):
        return _cast_tile(raw_tiled_object, new_tileset, new_tileset_path)

    return _get_caster(raw_tiled_object)(raw_tiled_object)

"""Object parsing for the JSON Map Format.
"""
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from typing_extensions import NotRequired, TypedDict

from pytiled_parser.common_types import Color, OrderedPair, Size
from pytiled_parser.parsers.json.properties import RawProperty
from pytiled_parser.parsers.json.properties import parse as parse_properties
from pytiled_parser.parsers.json.properties import serialize as serialize_properties
from pytiled_parser.tiled_object import (
    Ellipse,
    Point,
    Polygon,
    Polyline,
    Rectangle,
    Text,
    Tile,
    TiledObject,
)
from pytiled_parser.util import load_object_template, parse_color, serialize_color

RawText = TypedDict(
    "RawText",
    {
        "text": str,
        "color": NotRequired[str],
        "fontfamily": NotRequired[str],
        "pixelsize": NotRequired[float],  # this is `font_size` in Text
        "bold": NotRequired[bool],
        "italic": NotRequired[bool],
        "strikeout": NotRequired[bool],
        "underline": NotRequired[bool],
        "kerning": NotRequired[bool],
        "halign": NotRequired[str],
        "valign": NotRequired[str],
        "wrap": NotRequired[bool],
    },
)
RawText.__doc__ = """
    The keys and their types that appear in a Tiled JSON Text Object.

    Tiled Doc: https://doc.mapeditor.org/en/stable/reference/json-map-format/#text-example
"""


RawObject = TypedDict(
    "RawObject",
    {
        "id": int,
        "gid": NotRequired[int],
        "template": NotRequired[str],
        "x": float,
        "y": float,
        "width": float,
        "height": float,
        "rotation": float,
        "visible": bool,
        "name": str,
        "class": str,
        "type": NotRequired[str],
        "properties": NotRequired[List[RawProperty]],
        "ellipse": NotRequired[bool],
        "point": NotRequired[bool],
        "polygon": NotRequired[List[Dict[str, float]]],
        "polyline": NotRequired[List[Dict[str, float]]],
        "text": NotRequired[RawText],
    },
)
RawObject.__doc__ = """
    The keys and their types that appear in a Tiled JSON Object.

    Tiled Doc: https://doc.mapeditor.org/en/stable/reference/json-map-format/#object
"""


def _parse_common(raw_object: RawObject) -> TiledObject:
    """Create an Object containing all the attributes common to all types of objects.

    Args:
        raw_object: Raw object to get common attributes from

    Returns:
        Object: The attributes in common of all types of objects
    """

    common = TiledObject(
        id=raw_object["id"],
        coordinates=OrderedPair(raw_object["x"], raw_object["y"]),
        visible=raw_object["visible"],
        size=Size(raw_object["width"], raw_object["height"]),
        rotation=raw_object["rotation"],
        name=raw_object["name"],
    )

    if raw_object.get("type") is not None:
        common.class_ = raw_object["type"]

    if raw_object.get("class") is not None:
        common.class_ = raw_object["class"]

    if raw_object.get("properties") is not None:
        common.properties = parse_properties(raw_object["properties"])

    return common


def _serialize_common(object: TiledObject) -> RawObject:
    common: RawObject = {
        "id": object.id,
        "x": object.coordinates.x,
        "y": object.coordinates.y,
        "visible": object.visible,
        "width": object.size.width,
        "height": object.size.height,
        "rotation": object.rotation,
        "name": object.name,
        "class": object.class_,
    }

    if object.properties:
        common["properties"] = serialize_properties(object.properties)

    return common


def _parse_ellipse(raw_object: RawObject) -> Ellipse:
    """Parse the raw object into an Ellipse.

    Args:
        raw_object: Raw object to be parsed to an Ellipse

    Returns:
        Ellipse: The Ellipse object created from the raw object
    """
    return Ellipse(**_parse_common(raw_object).__dict__)


def _serialize_ellipse(object: Ellipse) -> RawObject:
    common = _serialize_common(object)
    common["ellipse"] = True
    return common


def _parse_rectangle(raw_object: RawObject) -> Rectangle:
    """Parse the raw object into a Rectangle.

    Args:
        raw_object: Raw object to be parsed to a Rectangle

    Returns:
        Rectangle: The Rectangle object created from the raw object
    """
    return Rectangle(**_parse_common(raw_object).__dict__)


def _serialize_rectangle(object: Rectangle) -> RawObject:
    return _serialize_common(object)


def _parse_point(raw_object: RawObject) -> Point:
    """Parse the raw object into a Point.

    Args:
        raw_object: Raw object to be parsed to a Point

    Returns:
        Point: The Point object created from the raw object
    """
    return Point(**_parse_common(raw_object).__dict__)


def _serialize_point(object: Point) -> RawObject:
    common = _serialize_common(object)
    common["point"] = True
    return common


def _parse_polygon(raw_object: RawObject) -> Polygon:
    """Parse the raw object into a Polygon.

    Args:
        raw_object: Raw object to be parsed to a Polygon

    Returns:
        Polygon: The Polygon object created from the raw object
    """
    polygon = []
    for point in raw_object["polygon"]:
        polygon.append(OrderedPair(point["x"], point["y"]))

    return Polygon(points=polygon, **_parse_common(raw_object).__dict__)


def _serialize_polygon(object: Polygon) -> RawObject:
    common = _serialize_common(object)

    points = []
    for point in object.points:
        points.append({"x": point.x, "y": point.y})
    common["polygon"] = points

    return common


def _parse_polyline(raw_object: RawObject) -> Polyline:
    """Parse the raw object into a Polyline.

    Args:
        raw_object: Raw object to be parsed to a Polyline

    Returns:
        Polyline: The Polyline object created from the raw object
    """
    polyline = []
    for point in raw_object["polyline"]:
        polyline.append(OrderedPair(point["x"], point["y"]))

    return Polyline(points=polyline, **_parse_common(raw_object).__dict__)


def _serialize_polyline(object: Polyline) -> RawObject:
    common = _serialize_common(object)

    points = []
    for point in object.points:
        points.append({"x": point.x, "y": point.y})
    common["polyline"] = points

    return common


def _parse_tile(
    raw_object: RawObject,
    new_tileset: Optional[Dict[str, Any]] = None,
    new_tileset_path: Optional[Path] = None,
) -> Tile:
    """Parse the raw object into a Tile.

    Args:
        raw_object: Raw object to be parsed to a Tile

    Returns:
        Tile: The Tile object created from the raw object
    """
    gid = raw_object["gid"]

    return Tile(
        gid=gid,
        new_tileset=new_tileset,
        new_tileset_path=new_tileset_path,
        **_parse_common(raw_object).__dict__,
    )


def _serialize_tile(object: Tile) -> RawObject:
    common = _serialize_common(object)
    common["gid"] = object.gid
    return common


def _parse_text(raw_object: RawObject) -> Text:
    """Parse the raw object into Text.

    Args:
        raw_object: Raw object to be parsed to a Text

    Returns:
        Text: The Text object created from the raw object
    """
    # required attributes
    raw_text: RawText = raw_object["text"]
    text = raw_text["text"]

    # create base Text object
    text_object = Text(text=text, **_parse_common(raw_object).__dict__)

    # optional attributes
    if raw_text.get("color") is not None:
        text_object.color = parse_color(raw_text["color"])

    if raw_text.get("fontfamily") is not None:
        text_object.font_family = raw_text["fontfamily"]

    if raw_text.get("pixelsize") is not None:
        text_object.font_size = raw_text["pixelsize"]

    if raw_text.get("bold") is not None:
        text_object.bold = raw_text["bold"]

    if raw_text.get("italic") is not None:
        text_object.italic = raw_text["italic"]

    if raw_text.get("kerning") is not None:
        text_object.kerning = raw_text["kerning"]

    if raw_text.get("strikeout") is not None:
        text_object.strike_out = raw_text["strikeout"]

    if raw_text.get("underline") is not None:
        text_object.underline = raw_text["underline"]

    if raw_text.get("halign") is not None:
        text_object.horizontal_align = raw_text["halign"]

    if raw_text.get("valign") is not None:
        text_object.vertical_align = raw_text["valign"]

    if raw_text.get("wrap") is not None:
        text_object.wrap = raw_text["wrap"]

    return text_object


def _serialize_text(object: Text) -> RawObject:
    common = _serialize_common(object)

    text: RawText = {"text": object.text}
    if object.color != Color(0, 0, 0, 255):
        text["color"] = serialize_color(object.color)

    if object.font_family != "sans-serif":
        text["fontfamily"] = object.font_family

    if object.font_size != 16:
        text["pixelsize"] = object.font_size

    if object.bold:
        text["bold"] = object.bold

    if object.italic:
        text["italic"] = object.italic

    if not object.kerning:
        text["kerning"] = object.kerning

    if object.strike_out:
        text["strikeout"] = object.strike_out

    if object.underline:
        text["underline"] = object.underline

    if object.horizontal_align != "left":
        text["halign"] = object.horizontal_align

    if object.vertical_align != "top":
        text["valign"] = object.vertical_align

    if object.wrap:
        text["wrap"] = object.wrap

    common["text"] = text
    return common


def _get_parser(raw_object: RawObject) -> Callable[[RawObject], TiledObject]:
    """Get the parser function for a given raw object.

    Only used internally by the JSON parser.

    Args:
        raw_object: Raw object that is analyzed to determine the parser function.

    Returns:
        Callable[[RawObject], Object]: The parser function.
    """
    if raw_object.get("ellipse"):
        return _parse_ellipse

    if raw_object.get("point"):
        return _parse_point

    # This is excluded from tests because the coverage is broken. I promise
    # there are tests for Tile objects, but for some reason the coverage
    # isn't picking up this if statement(though it does pickup the _parse_tile)
    # function so who knows
    if raw_object.get("gid"):  # pragma: no cover
        # Only tile objects have the `gid` key
        return _parse_tile

    if raw_object.get("polygon"):
        return _parse_polygon

    if raw_object.get("polyline"):
        return _parse_polyline

    if raw_object.get("text"):
        return _parse_text

    # If it's none of the above, rectangle is the only one left.
    # Rectangle is the only object which has no special properties to signify that.
    return _parse_rectangle


def parse(
    raw_object: RawObject,
    parent_dir: Optional[Path] = None,
) -> TiledObject:
    """Parse the raw object into a pytiled_parser version

    Args:
        raw_object: Raw object that is to be cast.
        parent_dir: The parent directory that the map file is in.

    Returns:
        Object: A parsed Object.

    Raises:
        RuntimeError: When a parameter that is conditionally required was not sent.
    """
    new_tileset = None
    new_tileset_path = None

    if raw_object.get("template"):
        if not parent_dir:
            raise RuntimeError(
                "A parent directory must be specified when using object templates."
            )
        template_path = Path(parent_dir / raw_object["template"])
        template, new_tileset, new_tileset_path = load_object_template(template_path)

        if isinstance(template, dict):
            loaded_template = template["object"]
            for key in loaded_template:
                if key != "id":
                    raw_object[key] = loaded_template[key]  # type: ignore
        else:
            raise NotImplementedError(
                "Loading TMX object templates inside a JSON map is currently not supported, "
                "but will be in a future release."
            )

    if raw_object.get("gid"):
        return _parse_tile(raw_object, new_tileset, new_tileset_path)

    return _get_parser(raw_object)(raw_object)


def serialize(object: TiledObject) -> RawObject:
    if isinstance(object, Tile):
        return _serialize_tile(object)
    elif isinstance(object, Text):
        return _serialize_text(object)
    elif isinstance(object, Rectangle):
        return _serialize_rectangle(object)
    elif isinstance(object, Polyline):
        return _serialize_polyline(object)
    elif isinstance(object, Polygon):
        return _serialize_polygon(object)
    elif isinstance(object, Point):
        return _serialize_point(object)
    elif isinstance(object, Ellipse):
        return _serialize_ellipse(object)

    raise AttributeError("Unknown Object Type passed to tiled_object.serialize")

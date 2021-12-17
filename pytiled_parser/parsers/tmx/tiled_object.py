import xml.etree.ElementTree as etree
from pathlib import Path
from typing import Callable, Optional

from pytiled_parser.common_types import OrderedPair, Size
from pytiled_parser.parsers.tmx.properties import parse as parse_properties
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
from pytiled_parser.util import parse_color


def _parse_common(raw_object: etree.Element) -> TiledObject:
    """Create an Object containing all the attributes common to all types of objects.

    Args:
        raw_object: XML Element to get common attributes from

    Returns:
        Object: The attributes in common of all types of objects
    """

    common = TiledObject(
        id=int(raw_object.attrib["id"]),
        coordinates=OrderedPair(
            float(raw_object.attrib["x"]), float(raw_object.attrib["y"])
        ),
        visible=bool(int(raw_object.attrib["visible"])),
        size=Size(
            float(raw_object.attrib["width"]), float(raw_object.attrib["height"])
        ),
        rotation=float(raw_object.attrib["rotation"]),
        name=raw_object.attrib["name"],
        type=raw_object.attrib["type"],
    )

    properties_element = raw_object.find("./properties")
    if properties_element:
        common.properties = parse_properties(properties_element)

    return common


def _parse_ellipse(raw_object: etree.Element) -> Ellipse:
    """Parse the raw object into an Ellipse.

    Args:
        raw_object: XML Element to be parsed to an Ellipse

    Returns:
        Ellipse: The Ellipse object created from the raw object
    """
    return Ellipse(**_parse_common(raw_object).__dict__)


def _parse_rectangle(raw_object: etree.Element) -> Rectangle:
    """Parse the raw object into a Rectangle.

    Args:
        raw_object: XML Element to be parsed to a Rectangle

    Returns:
        Rectangle: The Rectangle object created from the raw object
    """
    return Rectangle(**_parse_common(raw_object).__dict__)


def _parse_point(raw_object: etree.Element) -> Point:
    """Parse the raw object into a Point.

    Args:
        raw_object: XML Element to be parsed to a Point

    Returns:
        Point: The Point object created from the raw object
    """
    return Point(**_parse_common(raw_object).__dict__)


def _parse_polygon(raw_object: etree.Element) -> Polygon:
    """Parse the raw object into a Polygon.

    Args:
        raw_object: XML Element to be parsed to a Polygon

    Returns:
        Polygon: The Polygon object created from the raw object
    """
    polygon = []
    for raw_point in raw_object.attrib["points"].split(" "):
        point = raw_point.split(",")
        polygon.append(OrderedPair(float(point[0]), float(point[1])))

    return Polygon(points=polygon, **_parse_common(raw_object).__dict__)


def _parse_polyline(raw_object: etree.Element) -> Polyline:
    """Parse the raw object into a Polyline.

    Args:
        raw_object: Raw object to be parsed to a Polyline

    Returns:
        Polyline: The Polyline object created from the raw object
    """
    polyline = []
    for raw_point in raw_object.attrib["polyline"].split(" "):
        point = raw_point.split(",")
        polyline.append(OrderedPair(float(point[0]), float(point[1])))

    return Polyline(points=polyline, **_parse_common(raw_object).__dict__)


def _parse_tile(
    raw_object: etree.Element,
    new_tileset: Optional[etree.Element] = None,
    new_tileset_path: Optional[Path] = None,
) -> Tile:
    """Parse the raw object into a Tile.

    Args:
        raw_object: XML Element to be parsed to a Tile

    Returns:
        Tile: The Tile object created from the raw object
    """
    return Tile(
        gid=int(raw_object.attrib["gid"]),
        new_tileset=new_tileset,
        new_tileset_path=new_tileset_path,
        **_parse_common(raw_object).__dict__
    )


def _parse_text(raw_object: etree.Element) -> Text:
    """Parse the raw object into Text.

    Args:
        raw_object: XML Element to be parsed to a Text

    Returns:
        Text: The Text object created from the raw object
    """
    # required attributes
    text = raw_object.text

    if not text:
        text = ""
    # create base Text object
    text_object = Text(text=text, **_parse_common(raw_object).__dict__)

    # optional attributes
    if raw_object.attrib.get("color") is not None:
        text_object.color = parse_color(raw_object.attrib["color"])

    if raw_object.attrib.get("fontfamily") is not None:
        text_object.font_family = raw_object.attrib["fontfamily"]

    if raw_object.attrib.get("pixelsize") is not None:
        text_object.font_size = float(raw_object.attrib["pixelsize"])

    if raw_object.attrib.get("bold") is not None:
        text_object.bold = bool(int(raw_object.attrib["bold"]))

    if raw_object.attrib.get("italic") is not None:
        text_object.italic = bool(int(raw_object.attrib["italic"]))

    if raw_object.attrib.get("kerning") is not None:
        text_object.kerning = bool(int(raw_object.attrib["kerning"]))

    if raw_object.attrib.get("strikeout") is not None:
        text_object.strike_out = bool(int(raw_object.attrib["strikeout"]))

    if raw_object.attrib.get("underline") is not None:
        text_object.underline = bool(int(raw_object.attrib["underline"]))

    if raw_object.attrib.get("halign") is not None:
        text_object.horizontal_align = raw_object.attrib["halign"]

    if raw_object.attrib.get("valign") is not None:
        text_object.vertical_align = raw_object.attrib["valign"]

    if raw_object.attrib.get("wrap") is not None:
        text_object.wrap = bool(int(raw_object.attrib["wrap"]))

    return text_object


def _get_parser(raw_object: etree.Element) -> Callable[[etree.Element], TiledObject]:
    """Get the parser function for a given raw object.

    Only used internally by the TMX parser.

    Args:
        raw_object: XML Element that is analyzed to determine the parser function.

    Returns:
        Callable[[Element], Object]: The parser function.
    """
    if raw_object.find("./ellipse"):
        return _parse_ellipse

    if raw_object.find("./point"):
        return _parse_point

    if raw_object.attrib.get("gid"):
        # Only tile objects have the `gid` attribute
        return _parse_tile

    if raw_object.find("./polygon"):
        return _parse_polygon

    if raw_object.find("./polyline"):
        return _parse_polyline

    if raw_object.find("./text"):
        return _parse_text

    # If it's none of the above, rectangle is the only one left.
    # Rectangle is the only object which has no properties to signify that.
    return _parse_rectangle


def parse(raw_object: etree.Element, parent_dir: Optional[Path] = None) -> TiledObject:
    """Parse the raw object into a pytiled_parser version

    Args:
        raw_object: XML Element that is to be parsed.
        parent_dir: The parent directory that the map file is in.

    Returns:
        TiledObject: A parsed Object.

    Raises:
        RuntimeError: When a parameter that is conditionally required was not sent.
    """
    new_tileset = None
    new_tileset_path = None

    if raw_object.attrib.get("template"):
        if not parent_dir:
            raise RuntimeError(
                "A parent directory must be specified when using object templates."
            )
        template_path = Path(parent_dir / raw_object.attrib["template"])
        with open(template_path) as template_file:
            template = etree.parse(template_file).getroot()

            tileset_element = template.find("./tileset")
            if tileset_element:
                tileset_path = Path(
                    template_path.parent / tileset_element.attrib["source"]
                )
                with open(tileset_path) as tileset_file:
                    new_tileset = etree.parse(tileset_file).getroot()
                    new_tileset_path = tileset_path.parent

            new_object = template.find("./object")
            if raw_object.attrib.get("id") and new_object:
                new_object.attrib["id"] = raw_object.attrib["id"]

            if new_object:
                raw_object = new_object

    if raw_object.attrib.get("gid"):
        return _parse_tile(raw_object, new_tileset, new_tileset_path)

    return _get_parser(raw_object)(raw_object)

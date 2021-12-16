"""Layer parsing for the TMX Map Format.
"""
import xml.etree.ElementTree as etree
from pathlib import Path
from typing import Optional

from pytiled_parser.common_types import OrderedPair, Size
from pytiled_parser.layer import ImageLayer, Layer
from pytiled_parser.parsers.tmx.properties import parse as parse_properties
from pytiled_parser.util import parse_color


def _parse_common(raw_layer: etree.Element) -> Layer:
    """Create a Layer containing all the attributes common to all layer types.

    This is to create the stub Layer object that can then be used to create the actual
        specific sub-classes of Layer.

    Args:
        raw_layer: XML Element to get common attributes from

    Returns:
        Layer: The attributes in common of all layer types
    """
    common = Layer(
        name=raw_layer.attrib["name"],
        opacity=float(raw_layer.attrib["opacity"]),
        visible=bool(int(raw_layer.attrib["visible"])),
    )

    if raw_layer.attrib.get("id") is not None:
        common.id = int(raw_layer.attrib["id"])

    if raw_layer.attrib.get("offsetx") is not None:
        common.offset = OrderedPair(
            float(raw_layer.attrib["offsetx"]), float(raw_layer.attrib["offsety"])
        )

    properties_element = raw_layer.find("./properties")
    if properties_element:
        common.properties = parse_properties(properties_element)

    parallax = [1.0, 1.0]

    if raw_layer.attrib.get("parallaxx") is not None:
        parallax[0] = float(raw_layer.attrib["parallaxx"])

    if raw_layer.attrib.get("parallaxy") is not None:
        parallax[1] = float(raw_layer.attrib["parallaxy"])

    common.parallax_factor = OrderedPair(parallax[0], parallax[1])

    if raw_layer.attrib.get("tintcolor") is not None:
        common.tint_color = parse_color(raw_layer.attrib["tintcolor"])

    return common


def _parse_image_layer(raw_layer: etree.Element) -> ImageLayer:
    """Parse the raw_layer to an ImageLayer.

    Args:
        raw_layer: XML Element to be parsed to an ImageLayer.

    Returns:
        ImageLayer: The ImageLayer created from raw_layer
    """
    image_element = raw_layer.find("./image")
    if image_element:
        source = Path(image_element.attrib["source"])
        width = int(image_element.attrib["width"])
        height = int(image_element.attrib["height"])

        transparent_color = None
        if image_element.attrib.get("trans") is not None:
            transparent_color = parse_color(image_element.attrib["trans"])

        return ImageLayer(
            image=source,
            size=Size(width, height),
            transparent_color=transparent_color,
            **_parse_common(raw_layer).__dict__,
        )

    raise RuntimeError("Tried to parse an image layer that doesn't have an image!")


def parse(
    raw_layer: etree.Element,
    parent_dir: Optional[Path] = None,
) -> Layer:
    """Parse a raw Layer into a pytiled_parser object.

    This function will determine the type of layer and parse accordingly.

    Args:
        raw_layer: Raw layer to be parsed.
        parent_dir: The parent directory that the map file is in.

    Returns:
        Layer: A parsed Layer.

    Raises:
        RuntimeError: For an invalid layer type being provided
    """
    type_ = raw_layer.tag

    if type_ == "objectgroup":
        return _parse_object_layer(raw_layer, parent_dir)
    elif type_ == "group":
        return _parse_group_layer(raw_layer, parent_dir)
    elif type_ == "imagelayer":
        return _parse_image_layer(raw_layer)
    elif type_ == "layer":
        return _parse_tile_layer(raw_layer)

    raise RuntimeError(f"An invalid layer type of {type_} was supplied")

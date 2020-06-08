# pylint: disable=too-few-public-methods

from pathlib import Path
from typing import Any, Callable, List, Optional, Union

import attr
from typing_extensions import TypedDict

from . import properties as properties_
from .common_types import Color, OrderedPair, Size
from .tiled_object import RawTiledObject, TiledObject


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

    name: str

    height: int
    width: int

    id: Optional[int] = None
    offset: Optional[OrderedPair] = None
    opacity: Optional[float] = 1
    properties: Optional[properties_.Properties] = None
    start: Optional[OrderedPair] = None
    visible: Optional[bool] = True


TileLayerGrid = List[List[int]]


@attr.s(auto_attribs=True)
class Chunk:
    """Chunk object for infinite maps.

    See: https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#chunk

    Attributes:
        coordinates: Location of chunk in tiles.
        size: The size of the chunk in tiles.
        data: The global tile IDs in chunky according to row.
    """

    coordinates: OrderedPair
    size: Size

    data: Optional[Union[List[int], str]] = None


LayerData = Union[TileLayerGrid, List[Chunk]]
# The tile data for one layer.
#
# Either a 2 dimensional array of integers representing the global tile IDs
#     for a TileLayerGrid, or a list of chunks for an infinite map layer.


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

    encoding: str = "csv"

    compression: Optional[str] = None
    chunks: Optional[List[Chunk]] = None
    data: Optional[Union[List[int], str]] = None


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

    draw_order: Optional[str] = "topdown"


@attr.s(auto_attribs=True, kw_only=True)
class ImageLayer(Layer):
    """Map layer containing images.

    See: https://doc.mapeditor.org/en/stable/manual/layers/#image-layers

    Attributes:
        image: The image used by this layer.
        transparent_color: Color that is to be made transparent on this layer.
    """

    image: Path
    transparent_color: Optional[Color] = None


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

    layers: Optional[List[Union["LayerGroup", ImageLayer, ObjectLayer, TileLayer]]]


class RawChunk(TypedDict):
    """ The keys and their types that appear in a Chunk JSON Object."""

    data: Union[List[int], str]
    height: int
    width: int
    x: int
    y: int


class RawLayer(TypedDict):
    # FIXME Make the layers attribute function
    """ The keys and their types that appear in a Layer JSON Object."""

    chunks: List[RawChunk]
    compression: str
    data: Union[List[int], str]
    draworder: str
    encoding: str
    height: int
    id: int
    image: str
    layers: List[Any]
    name: str
    objects: List[RawTiledObject]
    offsetx: float
    offsety: float
    opacity: float
    properties: List[properties_.RawProperty]
    startx: int
    starty: int
    transparentcolor: str
    type: str
    visible: bool
    width: int
    x: int
    y: int


def _cast_chunk(raw_chunk: RawChunk) -> Chunk:
    """ Cast the raw_chunk to a Chunk.

    Args:
        raw_chunk: RawChunk to be casted to a Chunk

    Returns:
        Chunk: The Chunk created from the raw_chunk
    """

    chunk = Chunk(
        coordinates=OrderedPair(raw_chunk["x"], raw_chunk["y"]),
        size=Size(raw_chunk["width"], raw_chunk["height"]),
    )

    if raw_chunk.get("data") is not None:
        chunk.data = raw_chunk["data"]

    return chunk


def _cast_tile_layer(raw_layer: RawLayer) -> TileLayer:
    pass


def _cast_object_layer(raw_layer: RawLayer) -> ObjectLayer:
    pass


def _cast_image_layer(raw_layer: RawLayer) -> ImageLayer:
    pass


def _cast_group_layer(raw_layer: RawLayer) -> LayerGroup:
    pass


def _get_caster(type_: str) -> Callable[[RawLayer], Layer]:
    """ Get the caster function for the raw layer.

    Args:
        type_: the type of the layer

    Returns:
        Callable[[RawLayer], Layer]: The caster function.
    """
    casters = {
        "tilelayer": _cast_tile_layer,
        "objectgroup": _cast_object_layer,
        "imagelayer": _cast_image_layer,
        "group": _cast_group_layer,
    }
    return casters[type_]


def cast(raw_layer: RawLayer) -> Layer:
    caster = _get_caster(raw_layer["type"])

    return caster(raw_layer)

"""This module provides classes for all layer types

There is the base Layer class, which TileLayer, ObjectLayer, ImageLayer, 
and LayerGroup all derive from. The base Layer class is never directly used,
and serves only as an abstract base for common elements between all types.

For more information about Layers, see [Tiled's Manual](https://doc.mapeditor.org/en/stable/manual/layers/)
"""

# pylint: disable=too-few-public-methods

from pathlib import Path
from typing import List, Optional, Union

import attr

from pytiled_parser.common_types import Color, OrderedPair, Size
from pytiled_parser.properties import Properties
from pytiled_parser.tiled_object import TiledObject


@attr.s(auto_attribs=True, kw_only=True)
class Layer:
    """Base class that all layer types inherit from. Includes common attributes between
    the various types of layers.

    [TMX Reference](https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#layer)

    [JSON Reference](https://doc.mapeditor.org/en/stable/reference/json-map-format/#layer)

    Attributes:
        name: The name of the layer object.
        opacity: Decimal value between 0 and 1 to determine opacity. 1 is completely
            opaque, 0 is completely transparent.
        visible: If the layer is visible in the Tiled Editor. (Do not use for games)
        coordinates: Where layer content starts in tiles. (For infinite maps)
        id: Unique ID of the layer. Each layer that added to a map gets a unique id.
            Even if a layer is deleted, no layer ever gets the same ID.
        size: Ordered pair of size of map in tiles.
        offset: Rendering offset of the layer object in pixels.
        properties: Properties for the layer.
        tint_color: Tint color that is multiplied with any graphics in this layer.
    """

    name: str
    opacity: float = 1
    visible: bool = True

    coordinates: OrderedPair = OrderedPair(0, 0)
    parallax_factor: OrderedPair = OrderedPair(1, 1)
    offset: OrderedPair = OrderedPair(0, 0)

    id: Optional[int] = None
    size: Optional[Size] = None
    properties: Optional[Properties] = None
    tint_color: Optional[Color] = None


TileLayerGrid = List[List[int]]


@attr.s(auto_attribs=True)
class Chunk:
    """Chunk object for infinite maps. Stores `data` like you would have in a normal
    TileLayer but only for the area specified by `coordinates` and `size`.

    [Infinite Maps Docs](https://doc.mapeditor.org/en/stable/manual/using-infinite-maps/)

    [TMX Reference](https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#chunk)

    [JSON Reference](https://doc.mapeditor.org/en/stable/reference/json-map-format/#chunk)

    Attributes:
        coordinates: Location of chunk in tiles.
        size: The size of the chunk in tiles.
        data: The global tile IDs in chunky according to row.
    """

    coordinates: OrderedPair
    size: Size
    data: List[List[int]]


# The tile data for one layer.
#
# Either a 2 dimensional array of integers representing the global tile IDs
#     for a TileLayerGrid, or a list of chunks for an infinite map layer.
LayerData = Union[TileLayerGrid, List[Chunk]]


@attr.s(auto_attribs=True, kw_only=True)
class TileLayer(Layer):
    """The base type of layer which stores tile data for an area of a map.

    [Tiled Docs](https://doc.mapeditor.org/en/stable/manual/layers/#tile-layers)

    [TMX Reference](https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#layer)

    [JSON Reference](https://doc.mapeditor.org/en/stable/reference/json-map-format/#tile-layer-example)

    Attributes:
        chunks: List of chunks (only populated for infinite maps)
        data: A 2 dimensional array of integers representing the global tile
            IDs for the map layer (only populated for non-infinite maps)
    """

    chunks: Optional[List[Chunk]] = None
    data: Optional[List[List[int]]] = None


@attr.s(auto_attribs=True, kw_only=True)
class ObjectLayer(Layer):
    """A Layer type which stores a list of Tiled Objects

    [Tiled Docs](https://doc.mapeditor.org/en/stable/manual/layers/#object-layers)

    [TMX Reference](https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#objectgroup)

    [JSON Reference](https://doc.mapeditor.org/en/stable/reference/json-map-format/#object-layer-example)

    Attributes:
        tiled_objects: List of tiled_objects in the layer.
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
    """Map layer containing a single image

    [Tiled Docs](https://doc.mapeditor.org/en/stable/manual/layers/#image-layers)

    [TMX Reference](https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#imagelayer)

    [JSON Reference](https://doc.mapeditor.org/en/stable/reference/json-map-format/#layer)

    Attributes:
        image: The image used by this layer.
        transparent_color: Color that is to be made transparent on this layer.
    """

    image: Path
    transparent_color: Optional[Color] = None


@attr.s(auto_attribs=True, kw_only=True)
class LayerGroup(Layer):
    """A layer that contains layers (potentially including other LayerGroups, nested infinitely).

    In Tiled, offset and opacity recursively affect child layers, however that is not enforced during
    parsing by pytiled_parser, and is up to the implementation how to handle recursive effects of
    LayerGroups

    [Tiled Docs](https://doc.mapeditor.org/en/stable/manual/layers/#group-layers)

    [TMX Reference](https://doc.mapeditor.org/en/stable/reference/tmx-map-format/#group)

    [JSON Reference](https://doc.mapeditor.org/en/stable/reference/json-map-format/#layer)

    Attributes:
        Layers: list of layers contained in the group.
    """

    layers: Optional[List[Layer]]

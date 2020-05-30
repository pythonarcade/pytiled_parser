# pylint: disable=too-few-public-methods

from typing import List, Optional, Union

import attr

from .common_types import OrderedPair, Size
from .properties import Properties


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


TileLayerGrid = List[List[int]]


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

    size: Size
    layer_data: LayerData

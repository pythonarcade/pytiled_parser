"""This module handles parsing all types of layers.

See:
    - https://doc.mapeditor.org/en/stable/reference/json-map-format/#layer
    - https://doc.mapeditor.org/en/stable/manual/layers/
    - https://doc.mapeditor.org/en/stable/manual/editing-tile-layers/
"""

# pylint: disable=too-few-public-methods

import base64
import gzip
import importlib.util
import zlib
from pathlib import Path
from typing import Any, List, Optional, Union
from typing import cast as type_cast

import attr
from typing_extensions import TypedDict

from . import properties as properties_
from . import tiled_object
from .common_types import Color, OrderedPair, Size
from .util import parse_color

zstd_spec = importlib.util.find_spec("zstd")
if zstd_spec:
    import zstd  # pylint: disable=import-outside-toplevel
else:
    zstd = None  # pylint: disable=invalid-name


@attr.s(auto_attribs=True, kw_only=True)
class Layer:
    """Class that all layers inherit from.

    See: https://doc.mapeditor.org/en/stable/reference/json-map-format/#layer

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
    """

    name: str
    opacity: float
    visible: bool

    coordinates: OrderedPair = OrderedPair(0, 0)
    parallax_factor: OrderedPair = OrderedPair(1, 1)
    offset: OrderedPair = OrderedPair(0, 0)

    id: Optional[int] = None
    size: Optional[Size] = None
    properties: Optional[properties_.Properties] = None
    tint_color: Optional[Color] = None


TileLayerGrid = List[List[int]]


@attr.s(auto_attribs=True)
class Chunk:
    """Chunk object for infinite maps.

    See: https://doc.mapeditor.org/en/stable/reference/json-map-format/#chunk

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
    """Tile map layer containing tiles.

    See:
        https://doc.mapeditor.org/en/stable/reference/json-map-format/#tile-layer-example

    Attributes:
        chunks: list of chunks (infinite maps)
        data: Either an 2 dimensional array of integers representing the global tile
            IDs for the map layer, or a list of chunks for an infinite map.
    """

    chunks: Optional[List[Chunk]] = None
    data: Optional[List[List[int]]] = None


@attr.s(auto_attribs=True, kw_only=True)
class ObjectLayer(Layer):
    """TiledObject Group Object.

    The object group is in fact a map layer, and is hence called "object layer" in
        Tiled.

    See:
        https://doc.mapeditor.org/en/stable/reference/json-map-format/#object-layer-example

    Attributes:
        tiled_objects: List of tiled_objects in the layer.
        draworder: Whether the objects are drawn according to the order of the object
            elements in the object group element ('manual'), or sorted by their
            y-coordinate ('topdown'). Defaults to 'topdown'. See:
            https://doc.mapeditor.org/en/stable/manual/objects/#changing-stacking-order
            for more info.
    """

    tiled_objects: List[tiled_object.TiledObject]

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
    """A layer that contains layers (potentially including other LayerGroups).

    Offset and opacity recursively affect child layers.

    See:
        - https://doc.mapeditor.org/en/stable/reference/json-map-format/#layer
        - https://doc.mapeditor.org/en/stable/manual/layers/#group-layers

    Attributes:
        Layers: list of layers contained in the group.
    """

    layers: Optional[List[Layer]]


class RawChunk(TypedDict):
    """The keys and their types that appear in a Chunk JSON Object.

    See: https://doc.mapeditor.org/en/stable/reference/json-map-format/#chunk
    """

    data: Union[List[int], str]
    height: int
    width: int
    x: int
    y: int


class RawLayer(TypedDict):
    """The keys and their types that appear in a Layer JSON Object.

    See: https://doc.mapeditor.org/en/stable/reference/json-map-format/#layer
    """

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
    objects: List[tiled_object.RawTiledObject]
    offsetx: float
    offsety: float
    parallaxx: float
    parallaxy: float
    opacity: float
    properties: List[properties_.RawProperty]
    startx: int
    starty: int
    tintcolor: str
    transparentcolor: str
    type: str
    visible: bool
    width: int
    x: int
    y: int


def _convert_raw_tile_layer_data(data: List[int], layer_width: int) -> List[List[int]]:
    """Convert raw layer data into a nested lit based on the layer width

    Args:
        data: The data to convert
        layer_width: Width of the layer

    Returns:
        List[List[int]]: A nested list containing the converted data
    """
    tile_grid: List[List[int]] = [[]]

    column_count = 0
    row_count = 0
    for item in data:
        column_count += 1
        tile_grid[row_count].append(item)
        if not column_count % layer_width and column_count < len(data):
            row_count += 1
            tile_grid.append([])

    return tile_grid


def _decode_tile_layer_data(
    data: str, compression: str, layer_width: int
) -> List[List[int]]:
    """Decode Base64 Encoded tile data. Optionally supports gzip and zlib compression.

    Args:
        data: The base64 encoded data
        compression: Either zlib, gzip, or empty. If empty no decompression is done.

    Returns:
        List[List[int]]: A nested list containing the decoded data

    Raises:
        ValueError: For an unsupported compression type.
    """
    unencoded_data = base64.b64decode(data)
    if compression == "zlib":
        unzipped_data = zlib.decompress(unencoded_data)
    elif compression == "gzip":
        unzipped_data = gzip.decompress(unencoded_data)
    elif compression == "zstd" and zstd is None:
        raise ValueError(
            "zstd compression support is not installed."
            "To install use 'pip install pytiled-parser[zstd]'"
        )
    elif compression == "zstd":
        unzipped_data = zstd.decompress(unencoded_data)
    else:
        unzipped_data = unencoded_data

    tile_grid: List[int] = []

    byte_count = 0
    int_count = 0
    int_value = 0
    for byte in unzipped_data:
        int_value += byte << (byte_count * 8)
        byte_count += 1
        if not byte_count % 4:
            byte_count = 0
            int_count += 1
            tile_grid.append(int_value)
            int_value = 0

    return _convert_raw_tile_layer_data(tile_grid, layer_width)


def _cast_chunk(
    raw_chunk: RawChunk,
    encoding: Optional[str] = None,
    compression: Optional[str] = None,
) -> Chunk:
    """Cast the raw_chunk to a Chunk.

    Args:
        raw_chunk: RawChunk to be casted to a Chunk
        encoding: Encoding type. ("base64" or None)
        compression: Either zlib, gzip, or empty. If empty no decompression is done.

    Returns:
        Chunk: The Chunk created from the raw_chunk
    """
    if encoding == "base64":
        assert isinstance(compression, str)
        assert isinstance(raw_chunk["data"], str)
        data = _decode_tile_layer_data(
            raw_chunk["data"], compression, raw_chunk["width"]
        )
    else:
        data = _convert_raw_tile_layer_data(
            raw_chunk["data"], raw_chunk["width"]  # type: ignore
        )

    chunk = Chunk(
        coordinates=OrderedPair(raw_chunk["x"], raw_chunk["y"]),
        size=Size(raw_chunk["width"], raw_chunk["height"]),
        data=data,
    )

    return chunk


def _get_common_attributes(raw_layer: RawLayer) -> Layer:
    """Create a Layer containing all the attributes common to all layers.

    This is to create the stub Layer object that can then be used to create the actual
        specific sub-classes of Layer.

    Args:
        raw_layer: Raw Tiled object get common attributes from

    Returns:
        Layer: The attributes in common of all layers
    """
    common_attributes = Layer(
        name=raw_layer["name"],
        opacity=raw_layer["opacity"],
        visible=raw_layer["visible"],
    )

    # if startx is present, starty is present
    if raw_layer.get("startx") is not None:
        common_attributes.coordinates = OrderedPair(
            raw_layer["startx"], raw_layer["starty"]
        )

    if raw_layer.get("id") is not None:
        common_attributes.id = raw_layer["id"]

    # if either width or height is present, they both are
    if raw_layer.get("width") is not None:
        common_attributes.size = Size(raw_layer["width"], raw_layer["height"])

    if raw_layer.get("offsetx") is not None:
        common_attributes.offset = OrderedPair(
            raw_layer["offsetx"], raw_layer["offsety"]
        )

    if raw_layer.get("properties") is not None:
        common_attributes.properties = properties_.cast(raw_layer["properties"])

    parallax = [1.0, 1.0]

    if raw_layer.get("parallaxx") is not None:
        parallax[0] = raw_layer["parallaxx"]

    if raw_layer.get("parallaxy") is not None:
        parallax[1] = raw_layer["parallaxy"]

    common_attributes.parallax_factor = OrderedPair(parallax[0], parallax[1])

    if raw_layer.get("tintcolor") is not None:
        common_attributes.tint_color = parse_color(raw_layer["tintcolor"])

    return common_attributes


def _cast_tile_layer(raw_layer: RawLayer) -> TileLayer:
    """Cast the raw_layer to a TileLayer.

    Args:
        raw_layer: RawLayer to be casted to a TileLayer

    Returns:
        TileLayer: The TileLayer created from raw_layer
    """
    tile_layer = TileLayer(**_get_common_attributes(raw_layer).__dict__)

    if raw_layer.get("chunks") is not None:
        tile_layer.chunks = []
        for chunk in raw_layer["chunks"]:
            if raw_layer.get("encoding") is not None:
                tile_layer.chunks.append(
                    _cast_chunk(chunk, raw_layer["encoding"], raw_layer["compression"])
                )
            else:
                tile_layer.chunks.append(_cast_chunk(chunk))

    if raw_layer.get("data") is not None:
        if raw_layer.get("encoding") is not None:
            tile_layer.data = _decode_tile_layer_data(
                data=type_cast(str, raw_layer["data"]),
                compression=raw_layer["compression"],
                layer_width=raw_layer["width"],
            )
        else:
            tile_layer.data = _convert_raw_tile_layer_data(
                raw_layer["data"], raw_layer["width"]  # type: ignore
            )

    return tile_layer


def _cast_object_layer(
    raw_layer: RawLayer,
    parent_dir: Optional[Path] = None,
) -> ObjectLayer:
    """Cast the raw_layer to an ObjectLayer.

    Args:
        raw_layer: RawLayer to be casted to an ObjectLayer
    Returns:
        ObjectLayer: The ObjectLayer created from raw_layer
    """

    tiled_objects = []
    for tiled_object_ in raw_layer["objects"]:
        tiled_objects.append(tiled_object.cast(tiled_object_, parent_dir))

    return ObjectLayer(
        tiled_objects=tiled_objects,
        draw_order=raw_layer["draworder"],
        **_get_common_attributes(raw_layer).__dict__,
    )


def _cast_image_layer(raw_layer: RawLayer) -> ImageLayer:
    """Cast the raw_layer to a ImageLayer.

    Args:
        raw_layer: RawLayer to be casted to a ImageLayer

    Returns:
        ImageLayer: The ImageLayer created from raw_layer
    """
    image_layer = ImageLayer(
        image=Path(raw_layer["image"]), **_get_common_attributes(raw_layer).__dict__
    )

    if raw_layer.get("transparentcolor") is not None:
        image_layer.transparent_color = parse_color(raw_layer["transparentcolor"])

    return image_layer


def _cast_group_layer(
    raw_layer: RawLayer, parent_dir: Optional[Path] = None
) -> LayerGroup:
    """Cast the raw_layer to a LayerGroup.

    Args:
        raw_layer: RawLayer to be casted to a LayerGroup

    Returns:
        LayerGroup: The LayerGroup created from raw_layer
    """

    layers = []

    for layer in raw_layer["layers"]:
        layers.append(cast(layer, parent_dir=parent_dir))

    return LayerGroup(layers=layers, **_get_common_attributes(raw_layer).__dict__)


def cast(
    raw_layer: RawLayer,
    parent_dir: Optional[Path] = None,
) -> Layer:
    """Cast a raw Tiled layer into a pytiled_parser type.

    This function will determine the type of layer and cast accordingly.

    Args:
        raw_layer: Raw layer to be cast.
        parent_dir: The parent directory that the map file is in.

    Returns:
        Layer: a properly typed Layer.

    Raises:
        RuntimeError: For an invalid layer type being provided
    """
    type_ = raw_layer["type"]

    if type_ == "objectgroup":
        return _cast_object_layer(raw_layer, parent_dir)
    elif type_ == "group":
        return _cast_group_layer(raw_layer, parent_dir)
    elif type_ == "imagelayer":
        return _cast_image_layer(raw_layer)
    elif type_ == "tilelayer":
        return _cast_tile_layer(raw_layer)

    raise RuntimeError(f"An invalid layer type of {type_} was supplied")

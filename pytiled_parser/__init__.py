"""Parse Tiled Maps and Tilesets

See: https://www.mapeditor.org/

This library is for parsing JSON formatted Tiled Map Editormaps and tilesets to be
    used as maps and levels for 2D top-down (orthogonal, hexogonal, or isometric)
    or side-scrolling games in a strictly typed fashion.

PyTiled Parser is not tied to any particular graphics library or game engine.
"""

# pylint: disable=too-few-public-methods

from .common_types import OrderedPair, Size
from .layer import ImageLayer, Layer, LayerGroup, ObjectLayer, TileLayer
from .properties import Properties
from .tiled_map import TiledMap, parse_map
from .tileset import Tile, Tileset
from .version import __version__

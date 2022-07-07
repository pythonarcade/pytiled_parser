"""Module containing types that are common to other modules."""

# pylint: disable=too-few-public-methods

from typing import NamedTuple


class Color(NamedTuple):
    """Represents an RGBA color value as a four value Tuple.

    :param int red: Red value, between 0 and 255.
    :param int green: Green value, between 0 and 255.
    :param int blue: Blue value, between 0 and 255.
    :param int alpha: Alpha value, between 0 and 255.
    """
    red: int
    green: int
    blue: int
    alpha: int


class Size(NamedTuple):
    """Represents a two dimensional size as a two value Tuple.

    :param int width: The width of the object. Can be in either pixels or number of tiles.
    :param int height: The height of the object. Can be in either pixels or number of tiles.
    """

    width: float
    height: float


class OrderedPair(NamedTuple):
    """Represents a two dimensional position as a two value Tuple.

    :param int x: X coordinate. Can be in either pixels or number of tiles.
    :param int y: Y coordinate. Can be in either pixels or number of tiles.
    """

    x: float
    y: float

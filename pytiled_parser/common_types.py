"""Module containing types that are common to other modules."""

# pylint: disable=too-few-public-methods

from typing import NamedTuple


class Color(NamedTuple):
    """Represents an RGBA color value as a four value Tuple.

    Attributes:
        red: Red, between 1 and 255.
        green: Green, between 1 and 255.
        blue: Blue, between 1 and 255.
        alpha: Alpha, between 1 and 255.
    """

    red: int
    green: int
    blue: int
    alpha: int


class Size(NamedTuple):
    """Represents a two dimensional size as a two value Tuple.

    Attributes:
        width: The width of the object in pixels.
        height: The height of the object in pixels.
    """

    width: float
    height: float


class OrderedPair(NamedTuple):
    """Represents a two dimensional position as a two value Tuple.

    Attributes:
        x: X coordinate.
        y: Y coordinate.
    """

    x: float
    y: float

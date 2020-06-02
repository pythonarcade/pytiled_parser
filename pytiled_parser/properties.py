"""Properties Module

This module casts raw properties from Tiled maps into a dictionary of
properly typed Properties.
"""

from pathlib import Path
from typing import Dict, List, Union

from typing_extensions import TypedDict

from .common_types import Color

Property = Union[float, Path, str, bool, Color]


Properties = Dict[str, Property]


RawProperty = Union[float, str, bool]


class RawProperties(TypedDict):
    """A dictionary of raw properties."""

    name: str
    type: str
    value: RawProperty


def cast(raw_properties: List[RawProperties]) -> Properties:
    """ Cast a list of `RawProperties` into `Properties`

    Args:
        raw_properties: The list of `RawProperty`s to cast.

    Returns:
        Properties: The casted `Properties`.
    """

    final: Properties = {}
    value: Property

    for property_ in raw_properties:
        if property_["type"] == "file":
            value = Path(str(property_["value"]))
        elif property_["type"] == "color":
            value = Color(str(property_["value"]))
        else:
            value = property_["value"]
        final[str(property_["name"])] = value

    return final

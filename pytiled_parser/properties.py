"""Properties Module

This module casts raw properties from Tiled maps into a dictionary of
properly typed Properties.
"""

from pathlib import Path
from typing import Dict, List, Union
from typing import cast as type_cast

from typing_extensions import TypedDict

from .common_types import Color
from .util import parse_color

Property = Union[float, Path, str, bool, Color]


Properties = Dict[str, Property]


RawValue = Union[float, str, bool]


class RawProperty(TypedDict):
    """A dictionary of raw properties."""

    name: str
    type: str
    value: RawValue


def cast(raw_properties: List[RawProperty]) -> Properties:
    """Cast a list of `RawProperty`s into `Properties`

    Args:
        raw_properties: The list of `RawProperty`s to cast.

    Returns:
        Properties: The casted `Properties`.
    """

    final: Properties = {}
    value: Property

    for property_ in raw_properties:
        if property_["type"] == "file":
            value = Path(type_cast(str, property_["value"]))
        elif property_["type"] == "color":
            value = parse_color(type_cast(str, property_["value"]))
        else:
            value = property_["value"]
        final[property_["name"]] = value

    return final

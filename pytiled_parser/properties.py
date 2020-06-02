from pathlib import Path
from typing import Dict, List, NamedTuple, Optional, Union

from typing_extensions import TypedDict

from .common_types import Color

Property = Union[float, Path, str, bool, Color]
RawProperty = Union[float, str, bool]


class RawProperties(TypedDict):
    """A dictionary of raw properties."""

    name: str
    type: str
    value: RawProperty


Properties = Dict[str, Property]


def cast(raw: List[RawProperties]) -> Dict[str, Property]:
    final: Properties = {}
    value: Property

    for prop in raw:
        if prop["type"] == "file":
            value = Path(str(prop["value"]))
        elif prop["type"] == "color":
            value = Color(str(prop["value"]))
        else:
            value = prop["value"]
        final[str(prop["name"])] = value

    return final

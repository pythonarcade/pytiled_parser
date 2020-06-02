from pathlib import Path
from typing import Dict, List, NamedTuple, Optional, Union

from .common_types import Color

Property = Union[int, float, Path, str, bool, Color]
class 

RawProperties = List[Dict[str, Property]]


Properties = Dict[str, Property]


def cast(raw: RawProperties) -> Dict[str, Property]:
    final: Properties = {}
    for prop in raw:
        value = prop["value"]
        if prop["type"] == "file":
            value = Path(str(value))
        elif prop["type"] == "color":
            value = Color(str(value))
        final[str(prop["name"])] = value

    return final

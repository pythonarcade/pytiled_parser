from pathlib import Path
from typing import Dict, List, NamedTuple, Optional, Union

from .common_types import Color

RawProperties = List[Dict[str, Union[str, bool, int, float]]]


Property = Union[int, float, Path, str, bool, Color]


Properties = Dict[str, Property]

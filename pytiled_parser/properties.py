from pathlib import Path
from typing import Dict, List, NamedTuple, Optional, Union

from .common_types import Color


Property = Union[int, float, Path, str, bool, Color]


RawProperties = List[Dict[str, Property]]


Properties = Dict[str, Property]

import os
from pathlib import Path

import pytest

from pytiled_parser import UnknownFormat, parse_map

TESTS_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
MAP_FILE = TESTS_DIR / "test_data/invalid_format.garbage"

def test_map_invalid_format():
    with pytest.raises(UnknownFormat) as e:
        parse_map(MAP_FILE)

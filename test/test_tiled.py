import pickle
import pprint
from io import StringIO

import pytiled_parser

MAP_NAME = "/home/ben/Projects/pytiled_parser/pytiled_parser-venv/pytiled_parser/tests/test_data/test_map_simple_hitboxes.tmx"

map = pytiled_parser.parse_tile_map(MAP_NAME)

print(map.__dict__)

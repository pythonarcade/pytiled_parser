import pprint
import pickle

from io import StringIO

import arcade
import arcade.tiled


pp = pprint.PrettyPrinter(indent=4, compact=True, width=100)

pp = pp.pprint

MAP_NAME = '/home/ben/Projects/arcade/arcade-venv/arcade/tests/test_data/test_map_image_tile_set.tmx'

map = arcade.tiled.parse_tile_map(MAP_NAME)

pp(map.__dict__)

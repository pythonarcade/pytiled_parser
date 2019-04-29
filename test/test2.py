import arcade

import config

from arcade.tiled import read_tiled_map

class MyTestWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.map = arcade.generate_sprites(my_map, "Tile Layer 1", 1, "./assets/")

    def on_draw(self):
        arcade.start_render()
        self.map.draw()


MAP_NAME = 'assets/tiled_test_4.tmx'
my_map = arcade.read_tiled_map(config.MAP_NAME, 1)

for row in my_map.layers["Tile Layer 1"]:
    for grid_object in row:
        print(grid_object)
        print(
            f"{grid_object.tile.local_id}, {grid_object.center_x}, {grid_object.center_y}")
test = MyTestWindow(640,800,"meme")
test.test()
test.close()

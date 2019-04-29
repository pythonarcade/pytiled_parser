import arcade
import arcade.tiled

import pprint

pp = pprint.PrettyPrinter(indent=4, compact=True, width=200)

class MyTestWindow(arcade.Window):
    def __init__(self, width, height, title, map_name):
        super().__init__(width, height, title)

        self.layers = []
        my_map = arcade.tiled.read_tiled_map(map_name, 1)
        pp.pprint(my_map.layers_int_data)
        for layer in my_map.layers_int_data:
            self.layers.append(arcade.tiled.generate_sprites(
                my_map, layer, 1, "../arcade/arcade/examples/"))

    def on_draw(self):
        arcade.start_render()
        for layer in self.layers:
            layer.draw()


MAP_NAME = '../arcade/arcade/examples/map_base64_gzip.tmx'

test = MyTestWindow(640, 800, "meme", MAP_NAME)
arcade.run()

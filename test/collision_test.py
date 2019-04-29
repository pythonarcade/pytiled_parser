import os
import arcade
import arcade.tiled

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

SPRITE_SCALING = 1
GRAVITY = 1.1

class BasicTestWindow(arcade.Window):

    def __init__(self, width, height, title, map_name):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.layers = []
        my_map = arcade.tiled.read_tiled_map(map_name, 1)
        for layer in my_map.layers:
            self.layers.append(arcade.tiled.generate_sprites(
                my_map, layer, 1, "../arcade/arcade/examples/"))

    def on_draw(self):
        arcade.start_render()
        for layer in self.layers:
            layer.draw()

class CollisionTestWindow(BasicTestWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frame_count = 0

        self.player_list = arcade.SpriteList()
        self.player_sprite = arcade.Sprite(
            "../arcade/arcade/examples/images/character.png", SPRITE_SCALING)
        self.player_sprite.center_x = 400
        self.player_sprite.center_y = 800
        self.player_list.append(self.player_sprite)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, self.layers[0], gravity_constant=GRAVITY)

    def on_draw(self):
        super().on_draw()
        self.frame_count += 1

        self.player_list.draw()

        if self.frame_count == 20:
            print(self.player_sprite.center_x, self.player_sprite.center_y)

    def update(self, delta_time):
        self.physics_engine.update()




window = CollisionTestWindow(
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    "Test Text",
    "../arcade/arcade/examples/map_polyline_collision.tmx"
)
arcade.run()

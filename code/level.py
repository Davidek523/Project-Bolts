from settings import *
from sprite import Sprite
from player import Player

class Level:
    def __init__(self, tmx_map, level_frames):
        self.display_surface = pygame.display.get_surface()
        # self.scale_factor = min(3, WINDOW_WIDTH // (WINDOW_WIDTH * 16))

        # groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        self.setup(tmx_map, level_frames)

    def setup(self, tmx_map, level_frames):
        for x, y, surf in tmx_map.get_layer_by_name("Terrain").tiles():
            Sprite((x * 16, y * 16), surf, (self.all_sprites, self.collision_sprites))
            # print(f"Tile at ({x}, {y}) -> Scaled Position: ({x * 16 * self.scale_factor}, {y * 16 * self.scale_factor})")

        for obj in tmx_map.get_layer_by_name("Objects"):
            if obj.name == "Player":
                Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
            else:
                frames = level_frames[obj.name]
                print(frames)

    def run(self, dt):
        self.display_surface.fill("darkorange3")
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.display_surface)
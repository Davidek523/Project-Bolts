from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = pygame.Surface((16, 16))
        self.image.fill("White")
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()
from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf = pygame.Surface((16, 16)), groups = None):
        super().__init__(groups)
        self.image = surf
        # self.image.fill("White")
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()
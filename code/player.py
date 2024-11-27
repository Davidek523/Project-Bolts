from settings import *
from timer_script import Timer
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(join(".", "graphics", "png", "player", "idle", "0.png"))

        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()

        self.direction = pygame.math.Vector2()
        self.speed = 150
        self.gravity = 1300
        self.jump = False
        self.jump_height = 750

        self.collision_sprites = collision_sprites
        self.on_sruface = {"floor" : False, "left" : False, "right" : False}

        self.timers = {
            "wall_jump": Timer(400),
            "delay" : Timer(250)
        }

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = pygame.math.Vector2(0, 0)
        if not self.timers["wall_jump"].active:

            if keys[pygame.K_a]:
                input_vector.x = -1
            elif keys[pygame.K_d]:
                input_vector.x = 1
            self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

        if keys[pygame.K_SPACE]:
            self.jump = True

    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collsion("horizontal")

        if not self.on_sruface["floor"] and any((self.on_sruface["left"], self.on_sruface["right"])) and not self.timers["delay"].active:
            self.direction.y = 0
            self.rect.y += self.gravity / 10 * dt
        else:
            self.direction.y += self.gravity / 2 * dt
            self.rect.y += self.direction.y * dt
            self.direction.y += self.gravity / 2 * dt 

        self.collsion("vertical")
        
        if self.jump:
            if self.on_sruface["floor"]:
                self.direction.y = -self.jump_height
                self.timers["delay"].activate()
            elif any((self.on_sruface["left"], self.on_sruface["right"])) and not self.timers["delay"].active:
                self.timers["wall_jump"].activate()
                self.direction.y = -self.jump_height
                self.direction.x = 1 if self.on_sruface["left"] else -1
            self.jump = False

    def check_contacts(self):
        floor_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, 2))
        right_rect = pygame.Rect(self.rect.topright + pygame.math.Vector2(0, self.rect.height / 4), (2, self.rect.height / 2))
        left_rect = pygame.Rect(self.rect.topleft + pygame.math.Vector2(-2, self.rect.height / 4), (2, self.rect.height / 2))
        collide_recs = [sprite.rect for sprite in self.collision_sprites]

        self.on_sruface["floor"] = True if floor_rect.collidelist(collide_recs) >= 0 else False
        self.on_sruface["right"] = True if right_rect.collidelist(collide_recs) >= 0 else False
        self.on_sruface["left"] = True if left_rect.collidelist(collide_recs) >= 0 else False

    def collsion(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if axis == "horizontal":
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right

                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                else:
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom

                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                    self.direction.y = 0

    def udpate_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.udpate_timers()
        self.input()
        self.move(dt)
        self.check_contacts()
        # print(self.timers["delay"].active)
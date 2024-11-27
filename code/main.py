from settings import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((TOTAL_WIDTH, TOTAL_HEIGHT))
        pygame.display.set_caption("Fall Game Jam")

        # self.tmx_maps = {0: load_pygame("Pygame_game_jam_2024/data/tmx/home_planet.tmx")}


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()


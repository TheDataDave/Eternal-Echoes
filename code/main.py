import pygame, sys

from level import Level

from pygame.locals import *
from settings import * 

class Game:
    def __init__(self):

        # general setup
        pygame.init()
        if pygame.display.mode_ok((WIDTH, HEIGHT), DOUBLEBUF):
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF)
        pygame.display.set_caption('Eternal Echoes')
        self.clock = pygame.time.Clock()

        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
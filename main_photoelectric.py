#!/usr/bin/env python

import random, pygame, math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Main():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Effet Compton")
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))

    def __call__(self, *args, **kwargs):
        while True:
#             events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()

if __name__ == "__main__":
    print('salut')
    m = Main()
    m()

#!/usr/bin/env python

import pygame
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Main:
    def __init__(self):
        """Initializing the simulation."""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Effet Compton")
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))

    def __call__(self, *args, **kwargs):
        """Main loop."""
        while True:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

            update()
            show()

    def update(self):
        """Update the simulation."""

    def show(self):
        """Show the simulation."""
        pass


if __name__ == "__main__":
    m = Main()
    m()

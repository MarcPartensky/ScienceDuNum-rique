#!/usr/bin/env python

import pygame
import random


class Photon:
    def __init__(self, x, y, color=0x000000, radius=2):
        """Create a photon."""
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius

    def show(self, screen):
        """Show the photon."""
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


class Main:
    def __init__(self):
        """Initializing the simulation."""
        pygame.init()
        self.screen = pygame.display.set_mode(flags=pygame.RESIZABLE)
        pygame.display.set_caption("Effet Compton")
        self.photon = Photon(self.w / 2, self.h / 2)
        self.background_color = 0x000000

    @property
    def w(self):
        """Return the width."""
        return self.screen.get_width()

    @property
    def h(self):
        """Return the height."""
        return self.screen.get_height()

    def __call__(self, *args, **kwargs):
        """Main loop."""
        while True:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                # elif event.type == pygame.VIDEORESIZE:

            self.update()
            self.show()

    def update(self):
        """Update the simulation."""
        pass

    def show(self):
        """Show the simulation."""
        self.screen.fill(self.background_color)
        self.photon.show(self.screen)
        pygame.display.flip()


if __name__ == "__main__":
    m = Main()
    m()

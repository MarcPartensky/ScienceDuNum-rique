#!/usr/bin/env python
"""Simulation of the photoelectric effect."""

import pygame
import random

from print import print


class Photon:
    """Store a photon."""

    def __init__(
        self,
        x: float,
        y: float,
        vx: int = 0,
        vy: int = 0,
        color: int = 0x000000,
        radius: int = 20,
    ):
        """Create a photon."""
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.radius = radius

    def update(self, dt: float):
        """Update the photon."""
        self.x += self.vx * dt
        self.y += self.vy * dt

    def show(self, screen):
        """Show the photon."""
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


class Main:
    def __init__(self):
        """Initializing the simulation."""
        pygame.init()
        pygame.display.set_caption("Effet Compton")
        self.screen = pygame.display.set_mode(flags=pygame.RESIZABLE)
        self.photon = Photon(self.w / 2, self.h / 2)
        self.background_color = 0x000000
        self.dt = 0.1
        self.clock = pygame.time.Clock()
        self.fps = 60

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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        pygame.quit()
                        raise SystemExit

            self.update()
            self.show()
            self.clock.tick(self.fps)

    def update(self):
        """Update the simulation."""
        self.photon.update(self.dt)

    def show(self):
        """Show the simulation."""
        self.screen.fill(self.background_color)
        self.photon.show(self.screen)
        pygame.display.flip()


if __name__ == "__main__":
    m = Main()
    m()

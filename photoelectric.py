#!/usr/bin/env python
"""Simulation of the photoelectric effect."""

import pygame

from rich import print

PRECISION = 3


class Window:
    """Window."""

    def __init__(self, screen):
        """Initialize."""
        self.screen = screen

    def convert(self, x: float, y: float):
        """Convert in the new coordinates system."""
        length = self.length
        return ((x + 1 / 2) * length, (-y + 1 / 2) * length)

    def unconvert(self, x: float, y: float):
        """Convert in the new coordinates system."""
        length = self.length
        return (x / length - 1 / 2, -y / length - 1 / 2)

    @property
    def length(self):
        """Return the minimum of the width and height."""
        return min(self.width, self.height)

    @property
    def width(self):
        """Return the width."""
        return self.screen.get_width()

    @property
    def height(self):
        """Return the height."""
        return self.screen.get_height()


class Particle:
    """Particle"""

    def __str__(self):
        """Return the string representation of the particle."""
        return f"{type(self).__name__}{type(self).id}(x={round(self.x, 3)},y={round(self.y, 3)})"


class Photon(Particle):
    """Photon."""

    id = 0

    def __init__(
        self,
        x: float,
        y: float,
        vx: int = 0,
        vy: int = 0,
        color: int = 0xFFFF77,
        radius: int = 0.01,
    ):
        """Create a photon."""
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.radius = radius
        Photon.id += 1

    def update(self, dt: float):
        """Update the photon."""
        self.x += self.vx * dt
        self.y += self.vy * dt

    def show(self, window: Window):
        """Show the photon."""
        print(self)
        x, y = window.convert(self.x, self.y)
        pygame.draw.circle(
            window.screen, self.color, (x, y), self.radius * window.length
        )


class Electron(Particle):
    """Electron."""

    id = 0

    def __init__(
        self,
        x: float,
        y: float,
        vx: int = 0,
        vy: int = 0,
        color: int = 0xFFFF00,
        radius: int = 0.01,
    ):
        """Create a electron."""
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.radius = radius
        Electron.id += 1

    def update(self, dt: float):
        """Update the electron."""
        self.x += self.vx * dt
        self.y += self.vy * dt

    def show(self, window: Window):
        """Show the electron."""
        print(self)
        x, y = window.convert(self.x, self.y)
        pygame.draw.circle(
            window.screen, self.color, (x, y), self.radius * window.length
        )


class Main:
    def __init__(self):
        """Initializing the simulation."""
        pygame.init()
        pygame.display.set_caption("Effet Compton")
        screen = pygame.display.set_mode(flags=pygame.RESIZABLE)
        self.window = Window(screen)
        self.background_color = 0x000000
        self.dt = 0.1
        self.clock = pygame.time.Clock()
        self.fps = 60
        print(self.window.screen.get_size())
        self.load()

    def load(self):
        """Load objects."""
        self.photon = Photon(-0.5, 0, 0.005)
        self.electron = Electron(0, 0)

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
        self.window.screen.fill(self.background_color)
        self.photon.show(self.window)
        pygame.display.flip()


if __name__ == "__main__":
    m = Main()
    m()

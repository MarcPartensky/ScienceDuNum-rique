#!/usr/bin/env python
"""Simulation of the photoelectric effect."""

import pygame
import itertools

from rich import print


class Window:
    """Window."""

    def __init__(self, screen):
        """Initialize."""
        self.screen = screen

    def convert(self, x: float, y: float):
        """Convert in the new coordinates system."""
        return ((x + 1 / 2) * self.width, (-y + 1 / 2) * self.height)

    def unconvert(self, x: float, y: float):
        """Convert in the new coordinates system."""
        return (x / self.width - 1 / 2, -y / self.height - 1 / 2)

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

    def __init__(
        self,
        x: float,
        y: float,
        vx: int = 0,
        vy: int = 0,
    ):
        """Create a photon."""
        self.position: pygame.Vector = pygame.Vector2(x, y)
        self.velocity: pygame.Vector = pygame.Vector2(vx, vy)

    def __str__(self):
        """Return the string representation of the particle."""
        return f"{type(self).__name__}{type(self).id}(x={round(self.x, 3)},y={round(self.y, 3)})"

    @property
    def x(self):
        return self.position.x

    @property
    def y(self):
        return self.position.y

    @property
    def vx(self):
        return self.velocity.x

    @property
    def vy(self):
        return self.velocity.y


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
        super().__init__(x, y, vx, vy)
        self.color = color
        self.radius = radius
        Photon.id += 1

    def update(self, dt: float):
        """Update the photon."""
        self.position += self.velocity * dt

    def show(self, window: Window):
        """Show the photon."""
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
        color: int = 0xFF9010,
        radius: int = 0.01,
    ):
        """Create a electron."""
        super().__init__(x, y, vx, vy)
        self.color = color
        self.radius = radius
        Electron.id += 1

    def update(self, dt: float):
        """Update the electron."""
        self.position += self.velocity * dt

    def show(self, window: Window):
        """Show the electron."""
        x, y = window.convert(self.x, self.y)
        pygame.draw.circle(
            window.screen, self.color, (x, y), self.radius * window.length
        )


class Main:
    """Main class."""

    def __init__(self):
        """Initializing the simulation."""
        pygame.init()
        pygame.display.set_caption("Effet Compton")
        screen = pygame.display.set_mode(flags=pygame.RESIZABLE)
        self.window = Window(screen)
        self.clock = pygame.time.Clock()
        self.background_color = 0x000000
        self.dt = 0.1
        self.fps = 60
        self.photons = (Photon(-0.5, 0, 0.005),)
        self.electrons = (Electron(0, 0),)
        self.pause = False

    def __call__(self, *args, **kwargs):
        """Main loop."""
        while True:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                elif event.type == pygame.VIDEORESIZE:
                    self.window.screen = pygame.display.set_mode(
                        event.size, flags=pygame.RESIZABLE
                    )
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        pygame.quit()
                        raise SystemExit
                    elif event.key == pygame.K_o:
                        self.dt *= 2
                    elif event.key == pygame.K_p:
                        self.dt /= 2
                    elif event.key == pygame.K_SPACE:
                        self.pause = not self.pause

            if not self.pause:
                self.update()
                self.collide()
                self.show()
            self.clock.tick(self.fps)

    def collide(self):
        """Deal with particle collisions."""
        for electron in self.electrons:
            for photon in self.photons:
                self.collide_electron_photon(electron, photon)

    def collide_electron_photon(self, electron: Electron, photon: Photon):
        """Deal with the collision with an electron and a photon."""
        if (electron.position - photon.position).magnitude() < (
            electron.radius + photon.radius
        ):
            p1, p2 = photon.position, electron.position
            v1, v2 = photon.velocity, electron.velocity
            n = (v2 - v1).magnitude()
            photon.velocity

    def update(self):
        """Update the simulation."""
        for electron in self.electrons:
            electron.update(self.dt)
        for photon in self.photons:
            photon.update(self.dt)

    def show(self):
        """Show the simulation."""
        self.window.screen.fill(self.background_color)
        for electron in self.electrons:
            electron.show(self.window)
        for photon in self.photons:
            photon.show(self.window)
        pygame.draw.line(
            self.window.screen,
            0xff00ff,
            (0, self.window.height / 2),
            (self.window.width, self.window.height / 2),
        )
        pygame.display.flip()


if __name__ == "__main__":
    # import sys
    # sys.argv
    m = Main()
    m()

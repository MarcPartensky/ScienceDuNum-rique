#!/usr/bin/env python
"""Simulation of the photoelectric effect."""

import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import itertools
import argparse

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

    id = 0

    def __init__(
        self,
        x: float,
        y: float,
        vx: float = 0,
        vy: float = 0,
        energy: float = 0,
    ):
        """Create a photon."""
        self.position: pygame.Vector = pygame.Vector2(x, y)
        self.velocity: pygame.Vector = pygame.Vector2(vx, vy)
        self.energy: float = energy

    def __str__(self):
        """Return the string representation of the particle."""
        id = type(self).id
        name = type(self).__name__
        rx = round(self.x, 3)
        ry = round(self.y, 3)
        re = round(self.energy, 3)
        return f"{name}{n}(x={rx},y={ry},e={re})"

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
    plank_constant = 0

    def __init__(
        self,
        x: float,
        y: float,
        vx: float = 0,
        vy: float = 0,
        energy: float = 0,
        color: int = 0xFFFF77,
        radius: float = 0.01,
    ):
        """Create a photon."""
        super().__init__(x, y, vx, vy, energy)
        self.color = color
        self.radius = radius
        Photon.id += 1

    def update(self, dt: float):
        """Update the photon."""
        self.position += self.velocity * dt
        self.energy = self.velocity.magnitude() * Photon.plank_constant

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
        vx: int,
        vy: int,
        energy: float,
        color: int,
        radius: float,
    ):
        """Create a electron."""
        super().__init__(x, y, vx, vy, energy)
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

    def __init__(self, config: argparse.Namespace):
        """Initializing the simulation."""
        pygame.init()
        pygame.display.set_caption("Effet Compton")
        screen = pygame.display.set_mode(flags=pygame.RESIZABLE)
        self.window = Window(screen)
        self.clock = pygame.time.Clock()
        self.background_color = config.background_color
        self.line_color = config.line_color
        self.dt = float(config.dt)
        self.fps = int(config.fps)
        self.electron_energy = float(config.electron_energy)
        Photon.plank_constant = float(config.plank_constant)
        self.start()

    def start(self):
        """Start the simulation."""
        self.photons = (Photon(-0.5, 0, 0.005),)
        self.electrons = (Electron(0, 0, energy=self.electron_energy),)
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
                    elif event.key == pygame.K_r:
                        self.start()

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
        pygame.draw.line(
            self.window.screen,
            self.line_color,
            (0, self.window.height / 2),
            (self.window.width, self.window.height / 2),
        )
        for electron in self.electrons:
            electron.show(self.window)
        for photon in self.photons:
            photon.show(self.window)
        pygame.display.flip()


def parse_config(config: dict) -> dict:
    """Return the dictionary config."""
    for key, value in config.items():
        value i
def get_parser() -> argparse.ArgumentParser:
    """Parser that parses terminal arguments."""
    import yaml

    parser = argparse.ArgumentParser(description=__doc__)
    with open("config.yml", "r") as stream:
        config = yaml.safe_load(stream)

    for key, value in content.items():
        if isinstance(value, dict):
            key += "_"
        parser.add_argument("--" + key, default=value, required=False, nargs="?")

    return parser


if __name__ == "__main__":
    import sys

    parser = get_parser()
    config = parser.parse_args(sys.argv[1::])
    m = Main(config)
    m()

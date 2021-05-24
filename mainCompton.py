#!/usr/bin/env python
"""Simulation of the compton effect."""

import random, pygame, math, os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

State = 0
Phi = math.pi / 4
Psi = math.pi / 4


def load_png(name: str):
    """Charge une image et retourne un objet image"""
    fullname = name  # os.path.join('data', name)
    image = pygame.image.load(fullname)
    if image.get_alpha is None:
        image = image.convert()
    else:
        image = image.convert_alpha()
    return image, image.get_rect()


class Ball(pygame.sprite.Sprite):
    """Ball class used as mother class of electron and photon classes."""

    def __init__(self, img_path, x, color=0x700090, radius=30, velocity=(5,) * 2):
        """Initialize the ball with image."""
        super().__init__()
        self.x = x
        self.screen = pygame.display.get_surface()
        self.radius = radius
        self.y = (self.screen.get_height() - self.radius) / 2
        self.color = color
        self.image, self.rect = load_png(img_path)
        self.image = pygame.transform.scale(self.image, (self.radius,) * 2)
        self.rect = self.rect.move((self.x, self.y))
        self.velocity = velocity


class Electron(Ball):
    """Electron class."""

    def __init__(
        self, x, color=0x700090, radius=30, velocity=(5,) * 2, image="img/electron.png"
    ):
        super().__init__(image, x, color=color, radius=radius, velocity=velocity)
        self.state = 0

    def update(self, *args, **kwargs) -> None:
        global State  # todo
        if State == 0:
            self.rect.x = (self.screen.get_width() - self.radius) / 2
            self.rect.y = (self.screen.get_height() - self.radius) / 2
        else:
            self.rect.x += self.velocity[0] * math.cos(Psi)
            self.rect.y += self.velocity[1] * math.sin(Psi)

        # self.rect = self.rect.move((self.x, self.y))


class Photon(Ball):
    """Photon ball."""

    def __init__(
        self, x, color=0x700090, radius=30, velocity=(5,) * 2, image="img/photon.png"
    ):
        """Initialize the ball."""
        super().__init__(image, x, color=color, radius=radius, velocity=velocity)

    def update(self, *args, **kwargs) -> None:
        """Update the ball."""
        global State

        if self.rect.x + self.radius / 2 > self.screen.get_width() / 2:
            State = 1
            self.rect.x += self.velocity[0] * math.cos(Phi)
            self.rect.y -= self.velocity[1] * math.sin(Phi)
        else:
            State = 0
            self.rect.x += self.velocity[0]

        if self.rect.x + self.radius > self.screen.get_width():
            self.rect.x = 0
            self.rect.y = (self.screen.get_height() - self.radius) / 2


class Main:
    """Main class"""

    def __init__(self):
        """Initialize the main class."""
        pygame.init()
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )  # , flags=pygame.RESIZABLE)
        pygame.display.set_caption("Effet Compton")
        pygame.display.set_icon(pygame.image.load("img/photon.png").convert())
        self.make_background()

        self.photon = Photon(0)
        self.electron = Electron(0)
        pygame.display.flip()

        self.all_sprites_list = pygame.sprite.Group([self.photon, self.electron])

        self.pause = False

    @property
    def w(self):
        """Width of the screen."""
        return self.screen.get_width()

    @property
    def h(self):
        """Height of the screen."""
        return self.screen.get_height()

    def make_background(self):
        """Create the background"""
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(0xFFFFFF)
        pygame.draw.line(
            self.background, (0,) * 3, (0, self.h / 2), (self.w, self.h / 2)
        )
        self.screen.blit(self.background, (0, 0))

    def __call__(self, *args, **kwargs):
        """Main loop."""
        game_exit = False
        clock = pygame.time.Clock()
        while not game_exit:
            clock.tick(60)
            # self.screen.blit(self.background, self.electron)
            self.make_background()

            if not self.pause:
                self.all_sprites_list.draw(self.screen)
                self.all_sprites_list.update()

            pygame.display.flip()
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    game_exit = True
                elif event.type == pygame.VIDEORESIZE:
                    self.window.screen = pygame.display.set_mode(
                        event.size, flags=pygame.RESIZABLE
                    )
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        pygame.quit()
                        raise SystemExit
                    elif event.key == pygame.K_SPACE:
                        self.pause = not self.pause


if __name__ == "__main__":
    a = Main()
    a()


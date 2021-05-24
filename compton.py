#!/usr/bin/env python
"""Simulation of the compton effect."""
import random, pygame,math,os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

State = -1
Phi = math.pi/4
Psi = -math.pi/4

def load_png(name: str):
    """Charge une image et retourne un objet image"""
    fullname = name #os.path.join('data', name)
    image = pygame.image.load(fullname)
    if image.get_alpha is None:
        image = image.convert()
    else:
        image = image.convert_alpha()
    return image, image.get_rect()


class Ball(pygame.sprite.Sprite):
    def __init__(self, img_path, x, color=0x700090, radius=30, velocity=(5,) * 2):
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
    def __init__(self, x, color=0x700090, radius=30,velocity=(5,)*2):
        super().__init__(
            "img/electron.png", x, color=color, radius=radius, velocity=velocity
        )
        self.state=0
    def update(self, *args, **kwargs) -> None:
        global State  # todo
        self.rect.x = ((self.screen.get_width() - self.radius) / 2) + self.velocity[0] * math.cos(Psi) * max(State,0)
        self.rect.y = ((self.screen.get_height() - self.radius) / 2) - self.velocity[1] * math.sin(Psi) * max(State,0)




class Photon (Ball):
    def __init__(self, x, color=0x700090, radius=30,velocity=(5,)*2):
        super().__init__("img/photon.png", x, color=color, radius=radius, velocity=velocity)

    def update(self, *args, **kwargs) -> None:
        global State

        if self.rect.x + self.radius / 2 > self.screen.get_width() / 2 and State<0:
            State = 0
        elif self.rect.x +self.radius/2 > self.screen.get_width():
            State = -1
            self.rect.x = 0
            self.rect.y = (self.screen.get_height() - self.radius) / 2

        if State < 0:
            self.rect.x += self.velocity[0]
        else:
            self.rect.x = ((self.screen.get_width() - self.radius) / 2) + self.velocity[0] * math.cos(Phi) * State
            self.rect.y = ((self.screen.get_height() - self.radius) / 2) - self.velocity[1] * math.sin(Phi) * State
            State += 1




class Main():

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))#, flags=pygame.RESIZABLE)
        pygame.display.set_caption("Effet Compton")
        pygame.display.set_icon(pygame.image.load("img/photon.png").convert())
        self.make_background()

        self.photon = Photon(0)
        self.electron = Electron(0)
        pygame.display.flip()

        self.all_sprites_list = pygame.sprite.Group([self.photon, self.electron])

    @property
    def w(self):
        return self.screen.get_width()

    @property
    def h(self):
        return self.screen.get_height()

    def make_background(self):
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(0xffffff)
        pygame.draw.line(self.background, (0,)*3, (0, self.h/2), (self.w, self.h/2))
        self.screen.blit(self.background, (0, 0))

    def draw_lines(self):
        lengthPhi = self.h/(2*math.sin(Phi))
        endPosPhi=(lengthPhi*math.cos(Phi)+self.w/2,0)
        pygame.draw.line(self.screen, (0,)*3, (self.w/2, self.h/2), endPosPhi)

        lengthPsi = self.h / (2 * math.sin(Psi))
        end_posPsi = (lengthPhi*math.cos(Psi)+self.w/2,self.h)
        pygame.draw.line(self.screen, (0,)*3, (self.w/2, self.h/2), end_posPsi)



    def __call__(self, *args, **kwargs):
        game_exit = False
        clock = pygame.time.Clock()
        while not game_exit:
            clock.tick(60)
            #self.screen.blit(self.background, self.electron)
            self.make_background()
            self.draw_lines()
            self.all_sprites_list.draw(self.screen)
            self.all_sprites_list.update()

            pygame.display.flip()
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    game_exit = True


if __name__ == "__main__":
    a = Main()
    a()

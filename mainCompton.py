import random, pygame,math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600





class Electron(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/electron.png").convert()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect = self.image.get_rect()
        self.x=x
        self.y=SCREEN_HEIGHT/2
        self.inMovement=True

    def update(self, *args, **kwargs) -> None:
        newpos = self.rect.move((self.x, self.y))
        self.rect = newpos
        pygame.event.pump()


class Main():

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))#, flags=pygame.RESIZABLE)
        pygame.display.set_caption("Effet Compton")
        self.make_background()
        self.electron = Electron(0)
        self.electron_sprite= pygame.sprite.RenderPlain(self.electron)
        self.screen.blit(self.background, (0,0))
        pygame.display.flip()

    @property
    def w(self):
        return self.screen.get_width()

    @property
    def h(self):
        return self.screen.get_height()

    def make_background(self):
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((255,) * 3)
        pygame.draw.line(self.background, (0,)*3, (0, self.h/2), (self.w, self.h/2))


    def __call__(self, *args, **kwargs):
        game_exit = False
        clock = pygame.time.Clock()
        while not game_exit:
            clock.tick(60)
            self.screen.blit(self.background, self.electron)
            self.electron.update()
            self.electron_sprite.draw(self.screen)
            pygame.display.flip()
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    game_exit = True


a=Main()
a()
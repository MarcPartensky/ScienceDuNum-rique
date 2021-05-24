import random, pygame,math

class Electron(pygame.sprite.Sprite):
    def __init__(self):
        pass

class Main():
    def __init__(self):
        SCREEN_WIDTH = 800
        SCREEN_HEIGHT = 600
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Effet Compton")
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((255,)*3)
        self.screen.blit(background, (40,30))
        pygame.display.flip()

    def __call__(self, *args, **kwargs):
        game_exit = False
        while not game_exit:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    game_exit = True


a=Main()
a()
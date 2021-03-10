import os, sys
import random as rnd
import pygame as pg
from pygame.locals import *

DEBUG = True

COLORS = {'bg': (0, 0, 0), 'title': (255, 0, 0), 'menu_items': (255, 255, 255),
          'menu_selected_item': (255, 0, 0), 'sky': (177, 205, 252),
          'water': (77, 143, 172), 'sun': (252, 241, 75), 'oxygen': (177, 205, 252),
          'life': (255, 0, 0), 'score': (255, 255, 255)}
GAME_STATES = {'title': 0, 'menu': 1, 'game': 2, 'score': 3, 'gameover': 4, 'quit': 99}
SIZE = WIDTH, HEIGHT = 800, 600
MENU_ITEMS = {0: 'Начать игру', 1: 'Музыка вкл.', 2: 'Счёт', 3: 'Выход'}
ICONS_SIZE = 20

isMusic = True
music_volume = 0.4
FPS = 60

def load_image(name, colorkey=None):
    fullname = os.path.join('data/img', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pg.image.load(fullname)
    if colorkey is not None:
        image = pg.image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

class TTitle(pg.sprite.Sprite):
    def __init__(self,*group):
        super().__init__(*group)
        self.text = 'The Submarin'
        self.font = pg.font.Font('Ru.ttf', 60)
        txt = self.font.render(self.text, True, (255,0,0))
        self.image = pg.Surface((txt.get_width(), txt.get_height()))
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10
        self.image.blit(txt, (0, 0))

    def update(self,*args):
        pass

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

def main():
    pg.init()
    pg.font.init()

    screen = pg.display.set_mode(SIZE)

    font = pg.font.Font('Ru.ttf', 60)

    running = True
    clock = pg.time.Clock()
    all_sprites = pg.sprite.Group()
    title = TTitle()
    all_sprites.add(title)

    while running:
        for event in pg.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                pass
        screen.fill((0, 0, 0))
        all_sprites.update(event)
        all_sprites.draw(screen)

        pg.display.flip()
        clock.tick(FPS)
    pg.quit()

if __name__ == '__main__':
    main()


import os, sys
import pygame as pg
import random as rnd
from pygame.locals import *

DEBUG = True
COLORS = {'bg': (0, 0, 0), 'title': (255, 0, 0), 'menu_items': (255, 255, 255),
          'menu_selected_item': (255, 0, 0), 'sky': (177, 205, 252),
          'water': (77, 143, 172), 'sun': (252, 241, 75), 'oxygen': (177, 205, 252),
          'life': (255, 0, 0), 'score': (255, 255, 255)}
GAME_STATES = {'title': 0, 'menu': 1, 'game': 2, 'pause': 3, 'gameover': 4}
SIZE = WIDTH, HEIGHT = 800, 600
MENU_ITEMS = {0: 'Начать игру', 1: 'Музыка вкл.', 2: 'Выход'}
ICONS_SIZE = 20

isMusic = True
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

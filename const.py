import os
import sys

import pygame as pg

# Общие для всех модулей игры константы, переменные и функции

DEBUG = True  # вкл/выкл вывод отладочных сообщений

SIZE = WIDTH, HEIGHT = 800, 600  # Размеры окна
TILE_SIZE = 20  # Размер плитки, для загрузки карты мира (если пригодится :-) )
MAX_FONT_SIZE = 60
# Пункты меню и их соответствие состояниям игры
MENU_ITEMS = ['Начать игру', 'Музыка вкл.', 'Счёт', 'Выход']
MENU_ITEMS_TO_GS = [2, -1, 3, 5]

FPS = 60  # Частоста обновления экрана
# Пути к директориям с данными
DATA_DIR = 'data'
IMG_DIR = 'img'
FONTS_DIR = 'fonts'
MUSIC_DIR = 'music'
LEVELS_DIR = 'levels'

class TCaption:
    def __init__(self,lang='ru'):
        if lang=='ru':
            self.ru()
        else:
            self.en()
    def ru(self):
        self.game_name='The Submarin'
        self.press_any_key = 'Нажми любую клавишу'
        MENU_ITEMS = ['Начать игру', 'Музыка вкл.', 'Счёт', 'Выход']
    def en(self):
        self.game_name='The Submarin'
        self.press_any_key = 'Press any key'
        MENU_ITEMS = ['Start game', 'Music on', 'Score', 'Exit']

class TColor():  # Цвета, используемые в игре
    def __init__(self):
        self.bg = (0, 0, 0)
        self.title = (255, 0, 0)
        self.menu_items = (255, 255, 255)
        self.menu_selected_item = (255, 0, 0)
        self.sky = (177, 205, 252)
        self.water = (77, 143, 172)
        self.sun = (252, 241, 75)
        self.oxygen = (177, 205, 252)
        self.life = (255, 0, 0)
        self.score = (255, 255, 255)


COLORS = TColor()


class TGameStates():  # Состояния игры между которыми будем переключаться
    def __init__(self):
        self.current = 0
        self.title = 0
        self.menu = 1
        self.game = 2
        self.score = 3
        self.gameover = 4
        self.quit = 5

    def __str__(self):
        r = f"Игра сейчас в состоянии - '{self.current}'"
        return r


class TFonts():  # Шрифты нескольких размеров
    def __init__(self, name):
        fullname = os.path.join(DATA_DIR, FONTS_DIR)
        fullname = os.path.join(fullname, name)
        self.font1 = pg.font.Font(fullname, MAX_FONT_SIZE)
        self.font2 = pg.font.Font(fullname, MAX_FONT_SIZE - 20)
        self.font3 = pg.font.Font(fullname, MAX_FONT_SIZE - 20)


FONTS = TFonts('Ru.ttf')
game_state = TGameStates()
caption = TCaption('ru')


def load_image(name, colorkey=None):  # Загрузка картинок
    fullname = os.path.join(DATA_DIR, IMG_DIR)
    fullname = os.path.join(fullname, name)
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


class TText(pg.sprite.Sprite):  # Текстовые надписи
    def __init__(self, text='NoText', color=(255, 255, 255), font=FONTS.font1, xy=(0, 0), *group):
        super().__init__(*group)
        self.text = text
        self.font = font
        self.color = color
        self.image_txt = self.font.render(self.text, True, self.color)
        self.rect = self.image_txt.get_rect()
        self.image = pg.Surface((self.rect.width, self.rect.height))
        # self.rect.x, self.rect.y = xy
        self.rect.center = xy
        colorkey = self.image.get_at((0, 0))
        self.image.set_colorkey(colorkey)
        self.image.blit(self.image_txt, (0, 0))

    def set_new_text(self, text):
        self.image.fill((0, 0, 0))
        self.text = text
        self.image_txt = self.font.render(self.text, True, self.color)
        x, y = self.rect.x, self.rect.y
        self.rect = self.image_txt.get_rect()
        self.rect.center = (x, y)
        # self.rect.x, self.rect.y = x, y
        self.image = pg.Surface((self.rect.width, self.rect.height))
        colorkey = self.image.get_at((0, 0))
        self.image.set_colorkey(colorkey)
        self.image.blit(self.image_txt, (0, 0))

    def set_xy(self, x=0, y=0):
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, (100, 0))


class TBlinkText(pg.sprite.Sprite):
    def __init__(self, text='NoText', color=[125, 125, 125], font=FONTS.font1, xy=(0, 0), *group):
        super().__init__(*group)
        self.text = text
        self.font = font
        self.color = [0, 0, 0]
        self.color_target = color[:]
        self.dc = 5
        self.image_txt = self.font.render(self.text, True, self.color)
        self.rect = self.image_txt.get_rect()
        self.image = pg.Surface((self.rect.width, self.rect.height))
        # self.rect.x, self.rect.y = xy
        self.rect.center = xy
        colorkey = self.image.get_at((0, 0))
        self.image.set_colorkey(colorkey)
        self.image.blit(self.image_txt, (0, 0))

    def set_new_text(self, text):
        self.image.fill((0, 0, 0))
        self.text = text
        self.image_txt = self.font.render(self.text, True, self.color)
        x, y = self.rect.x, self.rect.y
        self.rect = self.image_txt.get_rect()
        self.rect.center = (x, y)
        # self.rect.x, self.rect.y = x, y
        self.image = pg.Surface((self.rect.width, self.rect.height))
        colorkey = self.image.get_at((0, 0))
        self.image.set_colorkey(colorkey)
        self.image.blit(self.image_txt, (0, 0))

    def set_xy(self, x=0, y=0):
        self.rect.x = x
        self.rect.y = y

    def update(self, *args, **kwargs):
        for i in range(len(self.color)):
            self.color[i] += self.dc
            if self.color[i] > 255:
                self.color[i] = 255
                self.dc = -self.dc
            if self.color[i] < 0:
                self.color[i] = 0
                self.dc = -self.dc
        self.image.fill(COLORS.bg)
        self.image_txt = self.font.render(self.text, True, self.color)
        self.image.blit(self.image_txt, (0, 0))

    def draw(self, screen):
        screen.blit(self.image, (100, 0))

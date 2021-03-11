import os
import sys
import random
import pygame as pg

# Общие для всех модулей игры константы, переменные и функции

DEBUG = True  # вкл/выкл вывод отладочных сообщений

SIZE = WIDTH, HEIGHT = 800, 600  # Размеры окна
TILE_SIZE = 20  # Размер плитки, для загрузки карты мира (если пригодится :-) )
# Пункты меню и их соответствие состояниям игры
MENU_ITEMS = ['Начать игру', 'Музыка', 'Счёт', 'Выход']

FPS = 60  # Частоста обновления экрана
# Пути к директориям с данными
DATA_DIR = 'data'
IMG_DIR = 'img'
FONTS_DIR = 'fonts'
MUSIC_DIR = 'music'
SND_DIR = 'snd'
LEVELS_DIR = 'levels'

SUN_WIDTH = WIDTH * 0.1
SUN_WIDTH_MAX = WIDTH * 0.2
SUN_DX = 1
WATER_LEVEL = HEIGHT // 3

MUSIC_ITEM_N = 1
MUSIC_VOLUME_MAX = 10
ICONS_SIZE = WIDTH * 0.02

SCORE_DX = 10
SCORE_NEXT_LEVEL_DX = 50


class TCaption:
    def __init__(self, lang='ru'):
        if lang == 'ru':
            self.ru()
        else:
            self.en()

    def ru(self):
        self.game_name = 'The Submarin'
        self.press_any_key = 'Нажми любую клавишу'
        self.music_on = 'вкл.'
        self.music_off = 'выкл.'
        self.music_volume = 'громкость'
        self.hiscore = 'Счёт'
        self.gameover = 'Игра завершена'
        self.enteryourname = 'Введи своё имя'
        MENU_ITEMS = ['Начать игру', 'Музыка', 'Счёт', 'Выход']

    def en(self):
        self.game_name = 'The Submarin'
        self.press_any_key = 'Press any key'
        self.music_on = 'on'
        self.music_off = 'off'
        self.music_volume = 'volume'
        self.hiscore = 'Hi Score'
        self.gameover = 'Game Over'
        self.enteryourname = 'Enter your name'
        MENU_ITEMS = ['Start game', 'Music', 'Score', 'Exit']


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
        self.username = 4
        self.gameover = 5
        self.quit = 6

    def __str__(self):
        r = f"Игра сейчас в состоянии - '{self.current}'"
        return r


class TFonts():  # Шрифты нескольких размеров
    def __init__(self, name):
        fullname = os.path.join(DATA_DIR, FONTS_DIR)
        fullname = os.path.join(fullname, name)
        self.font1 = pg.font.Font(fullname, 60)
        self.font2 = pg.font.Font(fullname, 50)
        self.font3 = pg.font.Font(fullname, 40)
        self.font4 = pg.font.Font(fullname, 30)
        self.font5 = pg.font.Font(fullname, 20)
        self.font6 = pg.font.Font(fullname, 10)


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


class TSnd():
    def __init__(self):
        path = os.path.join(DATA_DIR, SND_DIR)
        filename = os.path.join(path, 'menu1.wav')
        self.menu_updown = pg.mixer.Sound(filename)
        filename = os.path.join(path,
                                'atmosfernyiy-zvuk-glubinyi-kotoruyu-slyishit-dayver-vo-vremya-plavaniya-5864.ogg')
        self.underwatter = pg.mixer.Sound(filename)
        filename = os.path.join(path, 'iz-ballona-vyihodit-vozduh-5861.ogg')
        self.abovewater = pg.mixer.Sound(filename)
        filename = os.path.join(path, 'boom.wav')
        self.boom = pg.mixer.Sound(filename)
        filename = os.path.join(path, 'uskorenie-kosmicheskogo-korablya-2701.wav')
        self.submarine = pg.mixer.Sound(filename)
        self.channel = pg.mixer.Sound.play(self.menu_updown, 0)

        filename = os.path.join(path, 'volshebnaya-palochka-ne-ispolnila-jelanie-zvuk-oshibki-3577.wav')
        self.collect = pg.mixer.Sound(filename)

        filename = os.path.join(path, 'vam-zachislena-pobeda-4551.wav')
        self.next_level = pg.mixer.Sound(filename)

    def play_updown(self):
        self.channel = pg.mixer.Sound.play(self.menu_updown)

    def play_underwater(self):
        self.underwatter.play(-1)
        # self.channel = pg.mixer.Sound.play(self.underwatter)

    def play_abovewater(self):
        self.abovewater.play()
        # self.channel = pg.mixer.Sound.play(self.abovewater)

    def play_boom(self):
        self.boom.play()

    def play_submarine(self):
        self.submarine.play()


# Загружаем музыку
class TMusic():
    def __init__(self):
        path = os.path.join(DATA_DIR, MUSIC_DIR)
        self.music = self.get_music(path)

    def get_music(self, path):
        files = os.listdir(path)
        r = [os.path.join(path, song) for song in files if song.endswith('.ogg')]
        # r = [pg.mixer.Sound(os.path.join(path, song)) for song in files if song.endswith('.ogg')]
        return r

    def play(self):
        self.stop()
        pg.mixer.music.load(self.music[random.randint(0, len(self.music) - 1)])
        self.set_volume(music_volume)
        pg.mixer.music.play()
        print(dir(pg.mixer.music.play))
        # pg.mixer.Channel(0).play(self.music[random.randint(0,len(self.music)-1)])

    def stop(self):
        # pg.mixer.music.stop()
        pg.mixer.Channel(0).stop()

    def set_volume(self, volume):
        pg.mixer.music.set_volume(volume / 10)


FONTS = TFonts('Ru.ttf')


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

    def set_new_text(self, text, cur_item=0):
        self.image.fill(COLORS.bg)
        self.text = text
        self.image_txt = self.font.render(self.text, True, self.color)
        # x, y = self.rect.x, self.rect.y
        self.rect = self.image_txt.get_rect()
        x = WIDTH * 0.5
        y = HEIGHT * 0.3 + cur_item * self.rect.height
        self.rect.center = (x, y)
        self.image = pg.Surface((self.rect.width, self.rect.height))
        colorkey = self.image.get_at((0, 0))
        self.image.set_colorkey(colorkey)
        self.image.blit(self.image_txt, (0, 0))

    def set_xy(self, x=0, y=0):
        self.rect.x = x
        self.rect.y = y

    def active_item(self, isActive=False):
        if isActive:
            self.color = COLORS.title
        else:
            self.color = COLORS.menu_items
        self.image_txt = self.font.render(self.text, True, self.color)
        self.image.fill(COLORS.bg)
        self.image.blit(self.image_txt, (0, 0))

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
        self.image.fill(COLORS.bg)
        self.text = text
        self.image_txt = self.font.render(self.text, True, self.color)
        # x, y = self.rect.x, self.rect.y
        self.rect = self.image_txt.get_rect()
        x = WIDTH * 0.5
        y = HEIGHT * 0.9
        self.rect.center = (x, y)
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


# Всякие игровые переменные
game_state = TGameStates()  # состояние игры
caption = TCaption('ru')  # все надписи на указанном языке
isMusic = True  # вкл/выкл музыки
music_volume = 4  # громкость музыки
game_snd = TSnd()  # все звуки в игре
game_music = TMusic()
game_music.play()
speed = 2
user_score = 0
username = 'NoName'

# next_level_event = pg.USEREVENT + 1
next_level_event = pg.event.Event(pg.USEREVENT + 1, attr1='next_level_event')
# pg.event.post(next_level_event)

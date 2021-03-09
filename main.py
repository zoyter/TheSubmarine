import os, sys
import pygame as pg
import random as rnd
from pygame.locals import *

debug = True

pg.init()
size = width, height = 800, 600
screen = pg.display.set_mode(size)

game_states = {'title': 0, 'menu': 1, 'game': 2, 'pause': 3, 'gameover': 4}
game_state = game_states['title']

colors = {'gui': (255, 0, 0), 'text': (0, 0, 0), 'bg': (0, 0, 0), 'text_title': (255, 0, 0)}

title_data={'text_color_target':[254,0,0],'text_color_cur':[0,0,0],'x1':width,'y1':height//3}

text_size = {'gui': int(height * 0.05),
             'menu': int(height * 0.10)}
font1 = pg.font.Font('data/fonts/Ru.ttf', text_size['gui'])
font2 = pg.font.Font('data/fonts/Ru.ttf', text_size['menu'])


class Title():
    def __init__(self):
        self.isRunning = True
        self.color = [0, 0, 0]
        self.color_target = [255, 0, 0]

    def update(self):
        self.color += 1
        if self.color[0] < self.color_target[0]:
            self.isRunning = False


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    if '.png' in fullname:
        image = pg.image.load(fullname).convert_alpha()
    else:
        image = pg.image.load(fullname)
    return image


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


class AnimatedSprite(pg.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pg.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pg.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


def draw_gui():
    pg.draw.rect(screen, colors['gui'], (0, 0, width, height * 0.05), 0)
    draw_text("Menu", 10, 10)


def draw_text(text='NoText', x=0, y=0, color=(255, 0, 0)):
    txt = font1.render(text, True, color)
    screen.blit(txt, (x, y))

def color_to_target(cur_color, targ_color):
    flag = True
    for i in range(len(cur_color)):
        cur_color[i]+=1
        if cur_color[i]>=targ_color[i]:
            cur_color[i]=targ_color[i]
        if cur_color[i] != targ_color[i]:
            flag=False
    return cur_color, flag

def draw_title():
    # draw_text("The Submarine", 100, 100)
    screen.fill(colors['bg'])
    text = "The Submarin"
    txt = font2.render(text, True, colors['text_title'])
    x = width // 2 - txt.get_width() // 2
    y = height // 2 - txt.get_height() // 2
    color,flag=color_to_target(title_data['text_color_cur'],title_data['text_color_target'])
    txt = font2.render(text, True, color)
    screen.blit(txt, (x, y))
    return flag

def draw_menu():
    screen.fill(colors['bg'])
    text = "Menu"
    txt = font2.render(text, True, colors['text_title'])
    x = width // 2 - txt.get_width() // 2
    y = txt.get_height() // 4
    txt = font2.render(text, True, title_data['text_color_cur'])
    screen.blit(txt, (x, y))
    # draw_text("menu", 100, 100)


def draw_game():
    screen.fill(colors['bg'])
    # отрисовка и изменение свойств объектов

    # изменяем ракурс камеры

    # обновляем положение всех спрайтов

    # рисуем GUI
    draw_gui()


def draw_pause():
    draw_text("pause", 100, 100)


def draw_gameover():
    draw_text("gameover", 100, 100)


running = True
camera = Camera()
clock = pg.time.Clock()

while running:
    # внутри игрового цикла ещё один цикл
    # приема и обработки сообщений
    for event in pg.event.get():
        # при закрытии окна
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if game_state == game_states['title']:
                title_data['text_color_cur']=title_data['text_color_target']
            if debug:
                if event.key == K_0:
                    game_state = game_states['title']
                if event.key == K_1:
                    game_state = game_states['menu']
                if event.key == K_2:
                    game_state = game_states['game']
                if event.key == K_3:
                    game_state = game_states['pause']
                if event.key == K_4:
                    game_state = game_states['gameover']

    # отрисовка и изменение свойств объектов
    # screen.fill(colors['bg'])
    # изменяем ракурс камеры
    # обновляем положение всех спрайтов
    if game_state == game_states['title']:
        if draw_title():
            game_state = game_states['menu']
    elif game_state == game_states['menu']:
        draw_menu()
    elif game_state == game_states['game']:
        draw_game()
    elif game_state == game_states['pause']:
        draw_pause()
    elif game_state == game_states['gameover']:
        draw_gameover()
    # обновление экрана
    pg.display.flip()
    clock.tick(60)
pg.quit()

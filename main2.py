import os, sys
import pygame as pg
import random as rnd
from pygame.locals import *

debug = True

pg.init()
SIZE = WIDTH, HEIGHT = 800, 600
screen = pg.display.set_mode(SIZE)
GAME_STATES = {'title': 0, 'menu': 1, 'game': 2, 'pause': 3, 'gameover': 4}


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

class TGame():
    def __init__(self):
        self.state = GAME_STATES['title']

class TTitle(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.bg = [0, 0, 0]
        self.color = [0, 0, 0]
        self.color_target = [255, 0, 0]
        self.color_step = 5
        self.text = 'The Submarin'
        self.font = pg.font.Font('data/fonts/Ru.ttf', 40)
        txt = self.font.render(self.text, True, self.color)
        self.image = pg.Surface((txt.get_width(), txt.get_height()))
        colorkey = self.image.get_at((0, 0))
        self.image.set_colorkey(colorkey)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - txt.get_width() // 2
        self.rect.y = HEIGHT // 3 - txt.get_height() // 2
        self.image.blit(txt, (0, 0))

    def update(self):
        if self.color != self.color_target:
            for i in range(len(self.color)):
                self.color[i] += self.color_step
                if self.color[i] >= self.color_target[i]:
                    self.color[i] = self.color_target[i]
                if self.color[i] > 255:
                    self.color = 255
            txt = self.font.render(self.text, True, self.color)
            self.image = pg.Surface((txt.get_width(), txt.get_height()))
            self.image.blit(txt, (0, 0))

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


game = TGame()

title = TTitle()

running = True
clock = pg.time.Clock()

title_sprites = pg.sprite.Group()
title_sprites.add(title)

while running:
    for event in pg.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if debug:
                if event.key == K_0:
                    game.state = GAME_STATES['title']
                if event.key == K_1:
                    game.state = GAME_STATES['menu']
                if event.key == K_2:
                    game.state = GAME_STATES['game']
                if event.key == K_3:
                    game.state = GAME_STATES['pause']
                if event.key == K_4:
                    game.state = GAME_STATES['gameover']

    screen.fill((0, 0, 0))

    if game.state == GAME_STATES['title']:
        title_sprites.update()
        title_sprites.update()
        title_sprites.draw(screen)
    elif game.state == GAME_STATES['menu']:
        pass
    elif game.state == GAME_STATES['game']:
        pass
    elif game.state == GAME_STATES['pause']:
        pass
    elif game.state == GAME_STATES['gameover']:
        pass

    pg.display.flip()
    clock.tick(60)

pg.quit()

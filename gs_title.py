import os, sys
import pygame as pg
import random as rnd
from pygame.locals import *

from const import * # Общие константы для всех компонентов игры

class TTitle(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.bg = [0, 0, 0]
        self.color = [0, 0, 0]
        self.color_target = [255, 0, 0]
        self.color_step = 5
        self.text = 'The Submarin'
        self.font = pg.font.Font('data/fonts/Ru.ttf', 60)
        txt = self.font.render(self.text, True, self.color)
        self.image = pg.Surface((txt.get_width(), txt.get_height()))
        colorkey = self.image.get_at((0, 0))
        self.image.set_colorkey(colorkey)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - txt.get_width() // 2
        self.rect.y = HEIGHT // 2 - txt.get_height() // 2
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

class TTitle_Blink(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.bg = [0, 0, 0]
        self.color = [0, 0, 0]
        self.color_target = [0, 255, 0]
        self.color_step = 3
        self.text = 'нажми любую клавишу'
        self.font = pg.font.Font('data/fonts/Ru.ttf', 30)
        txt = self.font.render(self.text, True, self.color)
        self.image = pg.Surface((txt.get_width(), txt.get_height()))
        colorkey = self.image.get_at((0, 0))
        self.image.set_colorkey(colorkey)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - txt.get_width() // 2
        self.rect.y = HEIGHT - HEIGHT // 3 - txt.get_height() // 2
        self.image.blit(txt, (0, 0))

    def update(self):
        if self.color != self.color_target:
            for i in range(len(self.color)):
                self.color[i] += self.color_step
                if self.color[i] > 255:
                    self.color[i] = 255
                    self.color_step=-self.color_step
                if self.color[i]<0:
                    self.color[i]=0
                    self.color_step=-self.color_step

            txt = self.font.render(self.text, True, self.color)
            self.image = pg.Surface((txt.get_width(), txt.get_height()))
            self.image.blit(txt, (0, 0))

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

def title(screen):
    if DEBUG:
        print('Запустилась заставка')

    z=TTitle()
    z2 = TTitle_Blink()
    title_sprites = pg.sprite.Group()
    title_sprites.add(z)
    title_sprites.add(z2)

    font = pg.font.Font('data/fonts/Ru.ttf',60)

    running = True
    clock = pg.time.Clock()
    while running:
        # внутри игрового цикла ещё один цикл
        # приема и обработки сообщений
        for event in pg.event.get():
            # при закрытии окна
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                return
        screen.fill((0,0,0))
        title_sprites.update()
        title_sprites.update()
        title_sprites.draw(screen)

        pg.display.flip()
        clock.tick(FPS)


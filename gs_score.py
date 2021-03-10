import os, sys
import pygame as pg
import random as rnd
from pygame.locals import *

from const import * # Общие константы для всех компонентов игры


def score(screen):
    if DEBUG:
        print('Запустилася вывод счёта')

    running = True
    clock = pg.time.Clock()
    while running:
        for event in pg.event.get():
            # при закрытии окна
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                return GAME_STATES['menu']
        screen.fill((0,0,0))


        pg.display.flip()
        clock.tick(FPS)
    return GAME_STATES['menu']


import pygame as pg

# Загружаем функции различных состояний игры из соответствующих файлов
from gs_title import *  # заставка
from gs_menu import *  # меню
from gs_game import *  # игра
from gs_score import *  # счёт
from gs_gameover import *  # игра завершена

# Общий для всех состояний игры экран на котором всё рисуем
screen = pg.display.set_mode(SIZE)



def main():
    pg.init()  # Инициализируем pygame
    # Последовательно запускаем разные состояния игры
    gs = GAME_STATES['title']
    while gs !=GAME_STATES['quit']:
        if gs == GAME_STATES['title']:
            print('Заставка')
            gs = title(screen)

        if gs == GAME_STATES['menu']:
            print('Меню')
            gs = menu(screen)
        if gs == GAME_STATES['score']:
            print('счёт')
            gs = score(screen)
        player = None
        if gs == GAME_STATES['game']:
            print('Игра')
            gs, player = game(screen)
        if gs == GAME_STATES['gameover']:
            print('Игра завершена')
            gameover(screen, player)


if __name__ == '__main__':
    main()

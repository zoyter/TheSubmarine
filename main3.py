import pygame as pg

# Загружаем функции различных состояний игры из соответствующих файлов
from gs_title import *  # заставка
from gs_menu import *  # меню
from gs_game import *  # игра
from gs_gameover import *  # игра завершена

# Общий для всех состояний игры экран на котором всё рисуем
screen = pg.display.set_mode(SIZE)


def main():
    pg.init()  # Инициализируем pygame
    # Последовательно запускаем разные состояния игры
    print('Заставка')
    title(screen)
    print('Меню')
    menu(screen)
    print('Игра')
    player = game(screen)
    print('Игра завершена')
    gameover(screen, player)


if __name__ == '__main__':
    main()

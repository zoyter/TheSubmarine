import pygame as pg

# Инициализация компонентов pygame
pg.init()
pg.font.init()
pg.mixer.init()

# Импортируем компоненты игры
from gs_title import *
from gs_menu import *
from gs_score import *
from gs_game import *
from gs_username import *
from gs_gameover import *
from const import *

# Заголовок окна
pg.display.set_caption("The Submarine")


def main():
    screen = pg.display.set_mode(SIZE)  # Окно, в котором будет всё рисоваться
    user_score=0
    running = True
    while running:  # Основной цикл
        for event in pg.event.get():  # Перебираем события
            if event.type == QUIT:  # Закрытие окна
                running = False
            if event.type == KEYDOWN:  # Нажатие на кнопку клавиатуры
                if event.key == K_ESCAPE:  # Выход по клавише ESCSAPE
                    running = False
        # Проверям в каком состоянии находится игра
        if game_state.current == game_state.title:  # Заставка
            title(screen)
        if game_state.current == game_state.menu:  # Меню
            menu(screen)
        if game_state.current == game_state.game:  # Игра
            user_score = game(screen)
        if game_state.current == game_state.score:  # Вывод счёта/рейтинга игроков
            score(screen)
        if game_state.current == game_state.username:  # Ввод имени игрока
            enter_username(screen, user_score)
        if game_state.current == game_state.gameover:  # Игра завершена
            gameover(screen, user_score)
        if game_state.current == game_state.quit:  # Выход
            running = False
    pg.quit()


if __name__ == '__main__':
    main()

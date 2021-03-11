import pygame as pg

pg.init()
pg.font.init()
pg.mixer.init()

from gs_title import *
from gs_menu import *
from gs_score import *
from gs_game import *
from gs_username import *
from gs_gameover import *
pg.display.set_caption("The Submarine")



def main():
    screen = pg.display.set_mode(SIZE)

    game_state.current=game_state.gameover
    running = True
    while running:
        for event in pg.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        if game_state.current == game_state.title:
            title(screen)
        if game_state.current == game_state.menu:
            menu(screen)
        if game_state.current == game_state.game:
            game(screen)
        if game_state.current == game_state.score:
            score(screen)
        if game_state.current == game_state.username:
            enter_username(screen)
        if game_state.current == game_state.gameover:
            gameover(screen)
        if game_state.current == game_state.quit:
            print('quit')
            running = False
    pg.quit()


if __name__ == '__main__':
    main()

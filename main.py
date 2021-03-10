import pygame as pg

pg.init()
pg.font.init()

from gs_title import *
from gs_menu import *
from gs_score import *

isMusic = True
music_volume = 0.4


def main():
    screen = pg.display.set_mode(SIZE)
    # clock = pg.time.Clock()
    # all_sprites = pg.sprite.Group()
    # title = TText(color=(255, 0, 0), text="qqwfsd", x=100, y=100)
    # title.set_xy(50, 300)
    # title.set_new_text('Hello world')
    # all_sprites.add(title)
    running = True
    while running:
        for event in pg.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_1:
                    game_state.current = game_state.title
                if event.key == K_2:
                    game_state.current = game_state.menu
                if event.key == K_3:
                    game_state.current = game_state.quit

        if game_state.current == game_state.title:
            title(screen)
        if game_state.current == game_state.menu:
            menu(screen)
        if game_state.current == game_state.game:
            print('game')
        if game_state.current == game_state.score:
            score(screen)
        if game_state.current == game_state.gameover:
            print('gameover')
        if game_state.current == game_state.quit:
            print('quit')
            running = False
    pg.quit()


if __name__ == '__main__':
    main()

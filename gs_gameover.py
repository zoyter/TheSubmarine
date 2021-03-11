from const import *  # Общие константы для всех компонентов игры
from pygame.locals import *

abc = 'qwertyuiopasdfghjklzxcvbnm '#chr(8)


def input_name(key, username):
    if key:
        if key == 8:
            username = username[:-1]
        if chr(key) in abc:
            username += chr(key)
    return username


def gameover(screen, player=None):
    if DEBUG:
        print('Игра завершена')


    all_sprites = pg.sprite.Group()
    x = WIDTH * 0.5
    y = HEIGHT * 0.4
    name_input = TText(text=caption.gameover, color=COLORS.menu_items, font=FONTS.font1, xy=(x, y))
    all_sprites.add(name_input)


    x = WIDTH * 0.5
    y = HEIGHT * 0.6
    name_input = TBlinkText(text=str(user_score), color=COLORS.menu_items, font=FONTS.font2, xy=(x, y))
    all_sprites.add(name_input)

    running = True
    clock = pg.time.Clock()
    tick = pg.time.get_ticks()

    while running:
        if pg.time.get_ticks() - tick > 2000:
            running=False
            game_state.current=game_state.username
        for event in pg.event.get():
            if event.type == QUIT:
                running = False
                game_state.current = game_state.quit
            if event.type==KEYDOWN:
                game_state.current = game_state.username



        screen.fill(COLORS.bg)
        all_sprites.update()
        all_sprites.draw(screen)
        pg.display.flip()
        clock.tick(FPS)
    return

from pygame.locals import *

from const import *  # Общие константы для всех компонентов игры


def title(screen):
    if DEBUG:
        print('Запустилась заставка')

    all_sprites = pg.sprite.Group()
    x = WIDTH * 0.5
    y = HEIGHT * 0.3
    game_title = TText(text=caption.game_name, color=COLORS.title, font=FONTS.font1, xy=(x, y))
    all_sprites.add(game_title)

    x = WIDTH * 0.5
    y = HEIGHT * 0.9
    press_any_key = TBlinkText(text=caption.press_any_key, color=COLORS.menu_items, font=FONTS.font2, xy=(x, y))
    all_sprites.add(press_any_key)

    clock = pg.time.Clock()
    tick = pg.time.get_ticks()
    running = True
    while running:
        for event in pg.event.get():
            if event.type == QUIT:
                running = False
                game_state.current = game_state.quit
            if event.type == KEYDOWN:
                running = False
                game_state.current = game_state.menu

        screen.fill(COLORS.bg)
        all_sprites.update()
        all_sprites.draw(screen)
        pg.display.flip()
        clock.tick(FPS)

    return

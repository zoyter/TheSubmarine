from pygame.locals import *

from const import *  # Общие константы для всех компонентов игры


def set_active_item(items, cur_item):
    for i in range(len(items)):
        if i == cur_item:
            items[i].active_item(True)
        else:
            items[i].active_item(False)
        if i == MUSIC_ITEM_N:
            if isMusic:
                items[i].set_new_text(MENU_ITEMS[MUSIC_ITEM_N] + ' ' + caption.music_on, i)
            else:
                items[i].set_new_text(MENU_ITEMS[MUSIC_ITEM_N] + ' ' + caption.music_off, i)


def menu(screen):
    global music_volume, isMusic
    if DEBUG:
        print('Запустилось меню')

    all_sprites = pg.sprite.Group()
    all_menu_items = pg.sprite.Group()

    x = WIDTH * 0.5
    y = HEIGHT * 0.1
    game_title = TText(text=caption.game_name, color=COLORS.title, font=FONTS.font1, xy=(x, y))
    all_sprites.add(game_title)

    x = WIDTH * 0.5
    y = HEIGHT * 0.9
    info = TBlinkText(text=caption.music_volume, color=COLORS.menu_items, font=FONTS.font4, xy=(x, y))
    all_sprites.add(info)

    cur_menu_item = 0

    y = HEIGHT * 0.3
    items = []
    tmp_img = TText(text=MENU_ITEMS[0], color=COLORS.menu_items, font=FONTS.font2, xy=(x, y))
    for i in range(len(MENU_ITEMS)):
        items.append(
            TText(text=MENU_ITEMS[i], color=COLORS.menu_items, font=FONTS.font3, xy=(x, y + i * tmp_img.rect.height)))
    all_sprites.add(items)
    set_active_item(items, cur_menu_item)

    clock = pg.time.Clock()
    tick = pg.time.get_ticks()
    running = True
    while running:
        for event in pg.event.get():
            if event.type == QUIT:
                running = False
                game_state.current = game_state.quit
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    game_state.current = game_state.quit
                if event.key == K_UP:
                    cur_menu_item -= 1
                    if cur_menu_item < 0:
                        cur_menu_item = len(MENU_ITEMS) - 1
                if event.key == K_DOWN:
                    cur_menu_item += 1
                    if cur_menu_item > len(MENU_ITEMS) - 1:
                        cur_menu_item = 0
                if event.key == K_RETURN:
                    if MENU_ITEMS[cur_menu_item] == MENU_ITEMS[MUSIC_ITEM_N]:
                        isMusic = not isMusic
                    if MENU_ITEMS[cur_menu_item] == MENU_ITEMS[-1]:
                        running = False
                        game_state.current = game_state.quit
                    if MENU_ITEMS[cur_menu_item] == MENU_ITEMS[-2]:
                        running = False
                        game_state.current = game_state.score
                if event.key == K_LEFT:
                    music_volume -= 1
                    if music_volume <= 0:
                        music_volume = 0
                if event.key == K_RIGHT:
                    music_volume += 1
                    if music_volume >= MUSIC_VOLUME_MAX:
                        music_volume = MUSIC_VOLUME_MAX
                info.set_new_text(caption.music_volume + ' ' + str(music_volume))
                set_active_item(items, cur_menu_item)

        screen.fill(COLORS.bg)
        all_sprites.update()
        all_sprites.draw(screen)
        pg.display.flip()
        clock.tick(FPS)

    return

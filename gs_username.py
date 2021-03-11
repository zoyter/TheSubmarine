import sqlite3

from const import *  # Общие константы для всех компонентов игры
from pygame.locals import *

abc = 'qwertyuiopasdfghjklzxcvbnm '  # chr(8)


def input_name(key, username):
    if key:
        if key == 8:
            username = username[:-1]
        if chr(key) in abc:
            username += chr(key)
    return username


def save_user_score(username,user_score=0):
    if user_score <= 0:
        return
    db = os.path.join(DATA_DIR, "db.sqlite")
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("insert into info values (Null, '%s', '%s') "%(username, user_score))
    con.commit()
    con.close()
    return


def enter_username(screen,user_score):
    global username
    if DEBUG:
        print('Игра завершена')

    all_sprites = pg.sprite.Group()
    x = WIDTH * 0.5
    y = HEIGHT * 0.3
    caption1 = TText(text=caption.enteryourname, color=COLORS.menu_items, font=FONTS.font1, xy=(x, y))
    all_sprites.add(caption1)

    x = WIDTH * 0.5
    y = HEIGHT * 0.5
    name_input = TText(text=username, color=COLORS.title, font=FONTS.font3, xy=(x, y))
    all_sprites.add(name_input)

    x = WIDTH * 0.5
    y = HEIGHT * 0.9
    caption2 = TBlinkText(text=caption.press_any_key, color=COLORS.menu_items, font=FONTS.font4, xy=(x, y))
    all_sprites.add(caption2)

    running = True
    clock = pg.time.Clock()
    tick = pg.time.get_ticks()

    while running:
        # if pg.time.get_ticks() - tick > 2000:
        #     running=False
        #     game_state.current=game_state.quit
        for event in pg.event.get():
            if event.type == QUIT:
                running = False
                game_state.current = game_state.quit
            if event.type == KEYDOWN:
                username = input_name(event.key, username)
                if len(username) > 0:
                    name_input.set_new_text(username)
                else:
                    name_input.set_new_text(" ")
                x = WIDTH * 0.5 - name_input.rect.width // 2
                y = HEIGHT * 0.5
                name_input.rect.x = x
                name_input.rect.y = y
                if event.key == K_RETURN or event.key == K_ESCAPE:
                    running = False
                    save_user_score(username,user_score)
                    game_state.current = game_state.score

        screen.fill(COLORS.bg)
        all_sprites.update()
        all_sprites.draw(screen)
        pg.display.flip()
        clock.tick(FPS)
    return

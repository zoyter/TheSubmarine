import sqlite3
from pygame.locals import *

from const import *  # Общие константы для всех компонентов игры


def get_top_players():
    db = os.path.join(DATA_DIR, "db.sqlite")
    table = "info"
    query = "SELECT * FROM " + table + " ORDER BY score DESC"
    con = sqlite3.connect(db)
    cur = con.cursor()
    result = cur.execute(query).fetchall()
    con.close()
    return result[:10]


def save_user_score(user_score=0):
    if user_score <= 0:
        return
    db = os.path.join(DATA_DIR, "db.sqlite")
    table = "info"
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("insert into info values (Null, '%s', '%s') "%(username, user_score))
    con.commit()
    con.close()
    return


def score(screen, user_score):
    if DEBUG:
        print('Запустился вывод самых крутых игроков')
    save_user_score(user_score)
    all_sprites = pg.sprite.Group()
    x = WIDTH * 0.5
    y = HEIGHT * 0.1
    game_title = TText(text=caption.hiscore, color=COLORS.title, font=FONTS.font3, xy=(x, y))
    all_sprites.add(game_title)

    x = WIDTH * 0.5
    y = HEIGHT * 0.9
    info = TBlinkText(text=caption.press_any_key, color=COLORS.menu_items, font=FONTS.font4, xy=(x, y))
    all_sprites.add(info)

    y = HEIGHT * 0.2
    items = []
    top_players = get_top_players()
    tmp_img = TText(text=MENU_ITEMS[0], color=COLORS.menu_items, font=FONTS.font5, xy=(x, y))
    for i in range(len(top_players)):
        items.append(
            TText(text=top_players[i][1] + ' ' + str(top_players[i][2]), color=COLORS.menu_items, font=FONTS.font5,
                  xy=(x, y + i * tmp_img.rect.height)))
    all_sprites.add(items)
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

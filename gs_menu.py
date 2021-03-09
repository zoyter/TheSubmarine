from const import *  # Общие константы для всех компонентов игры


class TMenu(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.font = pg.font.Font('data/fonts/Ru.ttf', 60)
        self.img_title = self.font.render('The Submarin', True, COLORS['title'])
        self.image = pg.Surface((WIDTH, HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.font = pg.font.Font('data/fonts/Ru.ttf', 40)
        self.item_cur = 0

    def draw_items(self):
        x = WIDTH // 2 - self.img_title.get_width() // 2
        y = HEIGHT * 0.1
        self.image.blit(self.img_title, (x, y))
        for i in MENU_ITEMS:
            if i == self.item_cur:
                self.img_item = self.font.render(MENU_ITEMS[i], True, COLORS['menu_selected_item'])
            else:
                self.img_item = self.font.render(MENU_ITEMS[i], True, COLORS['menu_items'])
            x = WIDTH // 2 - self.img_item.get_width() // 2
            y = HEIGHT * 0.1 + self.img_title.get_height() + self.img_title.get_height() * 0.05
            y += i * self.img_item.get_height() + self.img_item.get_height() * 0.2
            self.image.blit(self.img_item, (x, y))

    def update(self):
        self.image.fill(COLORS['bg'])
        if isMusic:
            MENU_ITEMS[1] = 'Музыка вкл.'
        else:
            MENU_ITEMS[1] = 'Музыка выкл.'
        self.draw_items()


def menu(screen):
    global isMusic
    if DEBUG:
        print('Запустилось меню перед игрой')

    main_menu = TMenu()
    all_sprites = pg.sprite.Group()
    all_sprites.add(main_menu)

    running = True
    clock = pg.time.Clock()
    while running:
        for event in pg.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    main_menu.item_cur += 1
                    if main_menu.item_cur + 1 > len(MENU_ITEMS):
                        main_menu.item_cur = 0
                if event.key == K_UP:
                    main_menu.item_cur -= 1
                    if main_menu.item_cur < 0:
                        main_menu.item_cur = len(MENU_ITEMS) - 1
                if event.key == K_RETURN:
                    if main_menu.item_cur == len(MENU_ITEMS) - 1:
                        running = False
                    if main_menu.item_cur == 0:
                        return
                    if main_menu.item_cur == 1:
                        isMusic = not isMusic
                if event.key == K_LEFT or event.key == K_RIGHT:
                    if main_menu.item_cur == 1:
                        isMusic = not isMusic

        screen.fill(COLORS['bg'])
        all_sprites.update()
        all_sprites.draw(screen)

        pg.display.flip()
        clock.tick(FPS)

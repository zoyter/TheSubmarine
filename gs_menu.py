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
        self.img_volume = self.font.render('/'*int(music_volume*10), True, COLORS['menu_items'])
        x = WIDTH - self.img_volume.get_width()
        y = HEIGHT - self.img_volume.get_height()
        self.image.blit(self.img_volume, (x, y))

    def update(self):
        self.image.fill(COLORS['bg'])
        if isMusic:
            MENU_ITEMS[1] = 'Музыка вкл. ('+str(int(music_volume*10))+')'
        else:
            MENU_ITEMS[1] = 'Музыка выкл.('+str(int(music_volume*10))+')'
        self.draw_items()


def menu(screen):
    global isMusic, music_volume
    if DEBUG:
        print('Запустилось меню перед игрой')

    main_menu = TMenu()
    all_sprites = pg.sprite.Group()
    all_sprites.add(main_menu)

    running = True
    clock = pg.time.Clock()


    pg.mixer.music.load('data/music/the_guta_jasna_-_underwater_mind.ogg')
    if isMusic:
        pg.mixer.music.play()

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
                    if main_menu.item_cur == 0:
                        return GAME_STATES['game']

                    if main_menu.item_cur == 3:
                        return GAME_STATES['gameover']

                    if main_menu.item_cur == 1:
                        isMusic = not isMusic
                        if isMusic:
                            pg.mixer.music.play()
                        else:
                            pg.mixer.music.stop()
                if event.key == K_LEFT:
                    if main_menu.item_cur == 1:
                        music_volume -=0.1
                        if music_volume<0:
                            music_volume=0
                        pg.mixer.music.set_volume(music_volume)
                if event.key == K_RIGHT:
                    if main_menu.item_cur == 1:
                        music_volume +=0.1
                        if music_volume>1:
                            music_volume=1
                        pg.mixer.music.set_volume(music_volume)

        screen.fill(COLORS['bg'])
        all_sprites.update()
        all_sprites.draw(screen)

        pg.display.flip()
        clock.tick(FPS)
    return GAME_STATES['gameover']

from const import *  # Общие константы для всех компонентов игры


class TSprite(pg.sprite.Sprite):
    def __init__(self, player):
        pg.sprite.Sprite.__init__(self)
        self.font = pg.font.Font('data/fonts/Ru.ttf', 60)
        self.font2 = pg.font.Font('data/fonts/Ru.ttf', 40)
        self.img_title = self.font.render('Игра завершена', True, COLORS['title'])
        self.image = pg.Surface((WIDTH, HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - self.img_title.get_width() // 2
        self.rect.y = HEIGHT // 2 - self.img_title.get_height() // 2
        self.image.blit(self.img_title, (0, 0))
        txt = ''
        if player:
            if player.isWin and player.isAlive:
                txt = 'Вы победиили'
            elif not player.isAlive:
                txt = 'Вы проиграли'
        self.img_subtitle = self.font2.render(txt, True, COLORS['title'])
        self.image.blit(self.img_subtitle, (self.img_subtitle.get_width() // 2, 100))


def gameover(screen, player=None):
    if DEBUG:
        print('Игра завершена')

    z = TSprite(player)
    all_sprites = pg.sprite.Group()
    all_sprites.add(z)

    running = True
    clock = pg.time.Clock()
    tick = pg.time.get_ticks()
    while running:
        if pg.time.get_ticks() - tick > 2000:
            return GAME_STATES['quit']
        for event in pg.event.get():
            if event.type == QUIT:
                running = False
                return GAME_STATES['quit']
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return GAME_STATES['quit']

        screen.fill(COLORS['bg'])
        all_sprites.update()
        all_sprites.draw(screen)
        pg.display.flip()
        clock.tick(FPS)
    return GAME_STATES['quit']

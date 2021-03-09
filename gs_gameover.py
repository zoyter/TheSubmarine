from const import *  # Общие константы для всех компонентов игры


class TSprite(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.font = pg.font.Font('data/fonts/Ru.ttf', 60)
        self.img_title = self.font.render('Игра завершена', True, COLORS['title'])
        self.image = pg.Surface((WIDTH, HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH //2 - self.img_title.get_width()//2
        self.rect.y = HEIGHT//2 -self.img_title.get_height()//2
        self.image.blit(self.img_title, (0, 0))

def gameover(screen):
    if DEBUG:
        print('Игра завершена')

    z = TSprite()
    all_sprites = pg.sprite.Group()
    all_sprites.add(z)

    running = True
    clock = pg.time.Clock()
    tick = pg.time.get_ticks()
    while running:
        if pg.time.get_ticks()-tick > 2000:
            return
        for event in pg.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return

        screen.fill(COLORS['bg'])
        all_sprites.update()
        all_sprites.draw(screen)

        pg.display.flip()
        clock.tick(FPS)

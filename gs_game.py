from const import *  # Общие константы для всех компонентов игры

SUN_WIDTH = WIDTH*0.1
SUN_WIDTH_MAX=WIDTH*0.2
SUN_DX = 1


class TPlayer(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = load_image('player1.png')
        self.image_normal = load_image('player1.png')
        self.image_up = load_image('player2.png')
        self.image_down = load_image('player3.png')
        self.rect = self.image.get_rect()
        self.rect.y = HEIGHT // 2
        self.rect.x = 100

        self.up = False
        self.down = False
        self.right = False
        self.left = False
        self.dx = 5
        self.dy = 5

    def update(self, *args, **kwargs):
        self.image = self.image_normal
        if self.down:
            self.image = self.image_down
            self.rect.y += self.dy
        if self.up:
            self.image = self.image_up
            self.rect.y -= self.dy
        if self.right:
            self.rect.x += self.dx
        if self.left:
            self.rect.x -= self.dx


def draw_bg(screen):
    sky = pg.Rect((0, 0, WIDTH, HEIGHT // 3))
    water = pg.Rect((0, HEIGHT // 3, WIDTH, HEIGHT))
    pg.draw.rect(screen, COLORS['sky'], sky)
    pg.draw.rect(screen, COLORS['water'], water)
    sun = pg.Rect((0, 0, SUN_WIDTH,SUN_WIDTH))
    pg.draw.ellipse(screen, COLORS['sun'], sun)


def game(screen):
    if DEBUG:
        print('Запустилась игра')

    player = TPlayer()
    all_sprites = pg.sprite.Group()
    all_sprites.add(player)

    running = True
    clock = pg.time.Clock()
    while running:
        for event in pg.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                if event.key == K_UP:
                    player.up = True
                if event.key == K_DOWN:
                    player.down = True
                if event.key == K_RIGHT:
                    player.right = True
                if event.key == K_LEFT:
                    player.left = True
            if event.type == KEYUP:
                if event.key == K_UP:
                    player.up = False
                if event.key == K_DOWN:
                    player.down = False
                if event.key == K_RIGHT:
                    player.right = False
                if event.key == K_LEFT:
                    player.left = False
        draw_bg(screen)
        all_sprites.update()
        all_sprites.draw(screen)

        pg.display.flip()
        clock.tick(FPS)

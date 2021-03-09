import random

from const import *  # Общие константы для всех компонентов игры

SUN_WIDTH = WIDTH * 0.1
SUN_WIDTH_MAX = WIDTH * 0.2
SUN_DX = 1
WATER_LEVEL = HEIGHT // 3


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

        self.mask = pg.mask.from_surface(self.image)

        self.font = pg.font.Font('data/fonts/Ru.ttf', 30)

        self.up = False
        self.down = False
        self.right = False
        self.left = False
        self.dx = 5
        self.dy = 5
        self.oxygen = 50
        self.life = 3
        self.isAlive = True
        self.score = 0
        self.isWin = False
        self.isBoom = False
        self.BoomTime = 10
        self.BoomTimeMax = 10

        self.current_time = 0
        self.oxygen_dx = 0.001

    def boom_start(self):
        self.isBoom = True
        self.life -=1

    def boom_stop(self):
        self.isBoom = False
        self.BoomTime = self.BoomTimeMax

    def update(self, dt, player):
        if not self.isBoom:
            self.image = self.image_normal
            if self.down:
                self.image = self.image_down
                self.rect.y += self.dy
            if self.up:
                self.image = self.image_up
                self.rect.y -= self.dy
                if self.rect.y < WATER_LEVEL - self.rect.height // 2:
                    self.rect.y = WATER_LEVEL - self.rect.height // 2
            if self.right:
                self.rect.x += self.dx
            if self.left:
                self.rect.x -= self.dx
            # oxygen
            self.current_time += dt
            if self.current_time >= self.oxygen_dx:
                if self.rect.y <= WATER_LEVEL - self.rect.height // 3:
                    if self.oxygen < 100:
                        self.oxygen += 1
                else:
                    if self.oxygen > 0:
                        self.oxygen -= 1
                        if self.oxygen <= 0:
                            self.life -= 1
                            self.oxygen = 100
                self.current_time = 0
            if self.life < 0:
                self.isAlive = False
                return


class TBoom(pg.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, t=0.03):
        pg.sprite.Sprite.__init__(self)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.animation_time = t
        self.current_time = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pg.Rect(0, 0, sheet.get_width() // columns,
                            sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pg.Rect(
                    frame_location, self.rect.size)))

    def update(self, dt, player):
        if player.isBoom:
            self.rect = player.rect
            self.current_time += dt
            if self.current_time >= self.animation_time:
                self.current_time = 0
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
            if self.cur_frame >= len(self.frames)-1:
                player.boom_stop()
                player.rect.x = 0
                player.rect.y = WATER_LEVEL


class TBird(pg.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, t=0.03):
        pg.sprite.Sprite.__init__(self)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.animation_time = t
        self.current_time = 0
        self.dx = 5

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pg.Rect(0, 0, sheet.get_width() // columns,
                            sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pg.Rect(
                    frame_location, self.rect.size)))

    def update(self, dt, player):
        self.rect.x += self.dx
        if self.rect.x > WIDTH:
            self.rect.x = -self.image.get_width()
            self.rect.y = random.randint(0, WATER_LEVEL - self.image.get_height())
        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]


class TFish(pg.sprite.Sprite):
    def __init__(self, sheet, columns, rows):
        pg.sprite.Sprite.__init__(self)
        # super().__init__(self)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        x = WIDTH - random.randint(0, 100)
        y = random.randint(WATER_LEVEL, HEIGHT - self.image.get_height())
        self.rect = self.rect.move(x, y)
        self.current_time = 0
        self.dx = random.randint(1, 5)
        self.animation_time = 0.1 - self.dx // 10
        self.dx = -self.dx

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pg.Rect(0, 0, sheet.get_width() // columns,
                            sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pg.Rect(
                    frame_location, self.rect.size)))

    def update(self, dt, player):
        self.rect.x += self.dx
        if self.rect.x < 0 - self.image.get_width():
            self.rect.x = WIDTH
            self.rect.y = random.randint(WATER_LEVEL, HEIGHT - self.image.get_height())
        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.mask = pg.mask.from_surface(self.image)
        if pg.sprite.collide_mask(self, player):
            if DEBUG:
                print('Столкновение с рыбой')
            player.boom_start()
        if player.isBoom:
            self.rect.x = WIDTH
            self.rect.y = random.randint(WATER_LEVEL, HEIGHT - self.image.get_height())


class TCloud(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = load_image('cloud.png')
        self.rect = self.image.get_rect()
        self.dx = - random.randint(1, 5)

    def update(self, dt, player):
        self.rect.x += self.dx
        if self.rect.x < 0 - self.image.get_width():
            self.dx = - random.randint(1, 5)
            self.rect.x = WIDTH
            self.rect.y = random.randint(0, WATER_LEVEL - self.image.get_height())


class TDiver(pg.sprite.Sprite):
    def __init__(self, sheet, columns, rows, t=0.03):
        pg.sprite.Sprite.__init__(self)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        x = WIDTH - random.randint(0, 100)
        y = random.randint(WATER_LEVEL, HEIGHT - self.image.get_height())
        self.rect = self.rect.move(x, y)
        self.animation_time = t
        self.current_time = 0
        self.dx = -2

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pg.Rect(0, 0, sheet.get_width() // columns,
                            sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pg.Rect(
                    frame_location, self.rect.size)))

    def update(self, dt, player):
        self.rect.x += self.dx
        if self.rect.x < 0 - self.image.get_width():
            self.rect.x = WIDTH - random.randint(0, 100)
            self.rect.y = random.randint(WATER_LEVEL, HEIGHT - self.image.get_height())
        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]


def draw_bg(screen):
    sky = pg.Rect((0, 0, WIDTH, HEIGHT // 3))
    water = pg.Rect((0, WATER_LEVEL, WIDTH, HEIGHT))
    pg.draw.rect(screen, COLORS['sky'], sky)
    pg.draw.rect(screen, COLORS['water'], water)
    sun = pg.Rect((0, 0, SUN_WIDTH, SUN_WIDTH))
    pg.draw.ellipse(screen, COLORS['sun'], sun)


def draw_gui(screen, player):
    draw_oxygen(screen, player)
    draw_life(screen, player)
    draw_score(screen, player)


def draw_oxygen(screen, player):
    w = ICONS_SIZE
    y = HEIGHT - w * 2
    for x in range(player.oxygen // 10):
        x1 = x * w
        r1 = pg.Rect((x1, y, w, w))
        pg.draw.ellipse(screen, COLORS['oxygen'], r1)


def draw_life(screen, player):
    w = ICONS_SIZE
    y = HEIGHT - w * 2
    for x in range(player.life, 0, -1):
        x1 = WIDTH - x * w
        r1 = pg.Rect((x1, y, w, w))
        pg.draw.ellipse(screen, COLORS['life'], r1)


def draw_score(screen, player):
    txt_score = player.font.render(str(player.score), True, COLORS['menu_items'])
    w = ICONS_SIZE
    x = WIDTH // 2 - txt_score.get_width() // 2
    y = HEIGHT - txt_score.get_height()
    screen.blit(txt_score, (x, y))


def game(screen):
    if DEBUG:
        print('Запустилась игра')

    all_sprites = pg.sprite.Group()
    all_players = pg.sprite.Group()
    # групп для тех, кто причинят вред
    all_enemy = pg.sprite.Group()
    # Группа для тех, кто причиняет пользу :-)
    all_good = pg.sprite.Group()
    all_boom = pg.sprite.Group()

    player = TPlayer()
    all_players.add(player)

    bird = TBird(load_image("bird.png"), 3, 3, 50, 50, t=0.02)
    all_sprites.add(bird)

    fishes = []
    fishes.append(TFish(load_image("fish1.png"), 6, 1))
    fishes.append(TFish(load_image("fish2.png"), 6, 1))
    fishes.append(TFish(load_image("fish3.png"), 6, 1))
    all_enemy.add(fishes)

    clouds = []
    for i in range(3):
        clouds.append(TCloud())
    all_sprites.add(clouds)

    divers = []
    divers.append(TDiver(load_image("diver.png"), 4, 1, t=0.1))
    divers.append(TDiver(load_image("diver2.png"), 2, 3, t=0.1))
    all_good.add(divers)

    boom = TBoom(load_image("boom.png"), 16, 1, 50, 50, t=0.02)
    all_boom.add(boom)







    running = True
    clock = pg.time.Clock()
    while running and player.isAlive:
        dt = clock.tick(FPS) / 1000

        for event in pg.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return player
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
        all_sprites.update(dt, player)
        if not player.isBoom:
            all_enemy.update(dt, player)
            all_good.update(dt, player)
            all_players.update(dt, player)
        else:
            all_boom.update(dt, player)

        all_sprites.draw(screen)

        if not player.isBoom:
            all_enemy.draw(screen)
            all_good.draw(screen)
            all_players.draw(screen)
        else:
            all_boom.draw(screen)
        draw_gui(screen, player)

        pg.display.flip()
        clock.tick(FPS)
    return player

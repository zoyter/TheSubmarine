from pygame.locals import *

from const import *  # Общие константы для всех компонентов игры

#
ICONS_SIZE = WIDTH * 0.02

WATER_LEVEL = HEIGHT // 3

SCORE_DX = 10
SCORE_NEXT_LEVEL_DX = 50


class TSun(pg.sprite.Sprite):  # Солнце
    def __init__(self, *group):
        super().__init__(*group)
        self.SUN_WIDTH = WIDTH * 0.1
        self.SUN_WIDTH_MAX = WIDTH * 0.2
        self.SUN_DX = 1
        self.dw = -1
        self.width = self.SUN_WIDTH
        self.min_width = self.SUN_WIDTH * 0.8
        self.image = pg.Surface((self.width, self.width))
        self.rect = self.image.get_rect()
        self.rect.center = (50, 50)
        colorkey = self.image.get_at((0, 0))
        self.image.set_colorkey(colorkey)
        pg.draw.ellipse(self.image, COLORS.sun, (0, 0, self.width, self.width))

        self.animation_time = 0.02
        self.current_time = 0

    def update(self, *args, **kwargs):
        if 'dt' in kwargs:
            self.current_time += kwargs['dt']
            if self.current_time >= self.animation_time:
                self.current_time = 0
                self.width += self.dw
                if self.width >= self.SUN_WIDTH:
                    self.width = self.SUN_WIDTH
                    self.dw = -self.dw
                elif self.width <= self.min_width:
                    self.width = self.min_width
                    self.dw = -self.dw
        self.image.fill(COLORS.bg)
        colorkey = self.image.get_at((0, 0))
        self.image.set_colorkey(colorkey)
        pg.draw.ellipse(self.image, COLORS.sun, (0, 0, self.width, self.width))


class TPlayer(pg.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.images = []
        self.images.append(load_image('player1.png'))
        self.images.append(load_image('player2.png'))
        self.images.append(load_image('player3.png'))
        self.images.append(load_image('player_boom.png'))
        self.image = self.images[0]

        self.rect = self.image.get_rect()
        self.rect.y = HEIGHT // 2
        self.rect.x = 100

        self.mask = pg.mask.from_surface(self.image)

        self.up = False
        self.down = False
        self.right = False
        self.left = False
        self.dx = 5
        self.dy = 5
        self.oxygen = 50
        self.life = 15
        self.isAlive = True
        self.score = 0
        self.isWin = False
        self.isBoom = False
        self.BoomTime = 10
        self.BoomTimeMax = 10

        self.current_time = 0
        self.oxygen_dx = 0.001

        self.score_next_level = 50
        self.level = 1

        game_snd.play_underwater()

    def boom_start(self):  # Запуск процедуры взрыва
        self.isBoom = not self.isBoom
        self.image = self.images[-1]
        self.life -= 1
        game_snd.play_boom()

    def boom_stop(self):  # Остановка процедуры взрыва
        self.isBoom = not self.isBoom
        self.image = self.images[0]
        self.BoomTime = self.BoomTimeMax

    def update(self, *args, **kwargs):
        if not self.isBoom:
            self.image = self.images[0]
            if self.up:
                self.image = self.images[1]
                self.rect.y -= self.dy
                if self.rect.y < WATER_LEVEL - self.rect.height // 2:
                    self.rect.y = WATER_LEVEL - self.rect.height // 2
            if self.down:
                self.image = self.images[2]
                self.rect.y += self.dy
                if self.rect.y + self.rect.height > HEIGHT:
                    self.rect.y = HEIGHT - self.rect.height
            if self.right:
                self.rect.x += self.dx
                if self.rect.x + self.rect.width > WIDTH:
                    self.rect.x = WIDTH - self.rect.width
            if self.left:
                self.rect.x -= self.dx
                if self.rect.x < 0:
                    self.rect.x = 0
            # oxygen
            self.current_time += kwargs['dt']
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
                game_state.current = game_state.gameover


class TBoom(pg.sprite.Sprite):
    def __init__(self, sheet, columns, rows, t=0.03):
        pg.sprite.Sprite.__init__(self)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(-100, -100)
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

    def update(self, *args, **kwargs):  #
        if kwargs['player'].isBoom:
            self.rect = kwargs['player'].rect
            self.current_time += kwargs['dt']
            if self.current_time >= self.animation_time:
                self.current_time = 0
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
            if self.cur_frame >= len(self.frames) - 1:
                self.rect = kwargs['player'].rect
                kwargs['player'].boom_stop()
                kwargs['player'].rect.x = 0
                kwargs['player'].rect.y = WATER_LEVEL
                self.cur_frame = 0


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

    def update(self, *args, **kwargs):
        self.rect.x += self.dx
        if self.rect.x > WIDTH:
            self.rect.x = -self.image.get_width()
            self.rect.y = random.randint(0, WATER_LEVEL - self.image.get_height())
        self.current_time += kwargs['dt']
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

    def update(self, *args, **kwargs):
        self.rect.x += self.dx
        if self.rect.x < 0 - self.image.get_width():
            self.rect.x = WIDTH
            self.rect.y = random.randint(WATER_LEVEL, HEIGHT - self.image.get_height())
        self.current_time += kwargs['dt']
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.mask = pg.mask.from_surface(self.image)
        # Проверям столкновение рыбы с подводной лодкой
        if pg.sprite.collide_mask(self, kwargs['player']):
            if DEBUG:
                print('Столкновение с рыбой')
            kwargs['player'].boom_start()
        if kwargs['player'].isBoom:
            self.die()
        for e in kwargs['event']:
            if e == next_level_event:
                if DEBUG:
                    print('я рыба и вижу переход на след. уровень')
                self.dx = - random.randint(1, kwargs['player'].level)
                COLORS.next_level()

    def die(self):
        self.rect.x = WIDTH
        self.rect.y = random.randint(WATER_LEVEL, HEIGHT - self.image.get_height())

    def next_level(self, player):
        self.dx = -player.level


class TCloud(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = load_image('cloud.png')
        self.rect = self.image.get_rect()
        self.dx = - random.randint(1, 5)

    def update(self, *args, **kwargs):
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
        self.dx = -speed

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pg.Rect(0, 0, sheet.get_width() // columns,
                            sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pg.Rect(
                    frame_location, self.rect.size)))

    def update(self, *args, **kwargs):
        self.rect.x += self.dx
        if self.rect.x < 0 - self.image.get_width():
            self.rect.x = WIDTH - random.randint(0, 100)
            self.rect.y = random.randint(WATER_LEVEL, HEIGHT - self.image.get_height())
        self.current_time += kwargs['dt']
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        if pg.sprite.collide_mask(self, kwargs['player']):
            if DEBUG:
                print('Столкновение с дайвером')
            kwargs['player'].score += SCORE_DX
            if kwargs['player'].score >= kwargs['player'].score_next_level:
                kwargs['player'].level += 1
                kwargs['player'].score_next_level += SCORE_NEXT_LEVEL_DX
                game_snd.next_level.play()
                pg.event.post(next_level_event)
            self.die()

    def die(self):
        game_snd.collect.play()
        self.rect.x = WIDTH + random.randint(0, 100)
        self.rect.y = random.randint(WATER_LEVEL, HEIGHT - self.image.get_height())


def draw_bg(screen):
    sky = pg.Rect((0, 0, WIDTH, HEIGHT // 3))
    water = pg.Rect((0, WATER_LEVEL, WIDTH, HEIGHT))
    pg.draw.rect(screen, COLORS.sky, sky)
    pg.draw.rect(screen, COLORS.water, water)


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
        pg.draw.ellipse(screen, COLORS.oxygen, r1)


def draw_life(screen, player):
    w = ICONS_SIZE
    y = HEIGHT - w * 2
    for x in range(player.life, 0, -1):
        x1 = WIDTH - x * w
        r1 = pg.Rect((x1, y, w, w))
        pg.draw.ellipse(screen, COLORS.life, r1)


def draw_score(screen, player):
    txt_score = FONTS.font4.render(str(player.score), True, COLORS.menu_items)
    x = WIDTH - txt_score.get_width()
    y = HEIGHT * 0.001
    screen.blit(txt_score, (x, y))
    txt_level = FONTS.font4.render(str(player.level), True, COLORS.title)
    x = WIDTH - txt_level.get_width()
    y = HEIGHT * 0.05
    screen.blit(txt_level, (x, y))


def game(screen):
    global user_score
    if DEBUG:
        print('Запустилась игра')
    all_sprites = pg.sprite.Group()
    sun = TSun(all_sprites)
    # групп для тех, кто причинят вред
    all_enemy = pg.sprite.Group()
    # Группа для тех, кто причиняет пользу :-)
    all_good = pg.sprite.Group()
    all_boom = pg.sprite.Group()

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

    boom = TBoom(load_image("boom.png"), 16, 1, t=0.02)
    all_boom.add(boom)

    all_players = pg.sprite.Group()
    player = TPlayer(all_players)

    clock = pg.time.Clock()
    tick = pg.time.get_ticks()

    running = True
    while running:
        if game_state.current != game_state.game:
            running = False
        dt = clock.tick(FPS) / 1000
        all_event = pg.event.get()
        for event in all_event:
            if event.type == QUIT:
                running = False
                game_state.current = game_state.quit
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    game_state.current = game_state.menu
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

        screen.fill(COLORS.bg)
        draw_bg(screen)

        all_sprites.update(dt=dt, player=player)
        if not player.isBoom:
            all_enemy.update(dt=dt, player=player, event=all_event)
            all_good.update(dt=dt, player=player, event=all_event)
            all_players.update(dt=dt, player=player, event=all_event)
        else:
            all_boom.update(dt=dt, player=player)

        all_players.update(dt=dt, player=player)

        all_sprites.draw(screen)
        all_players.draw(screen)

        if not player.isBoom:
            all_enemy.draw(screen)
            all_good.draw(screen)
            all_players.draw(screen)
        else:
            all_boom.draw(screen)

        draw_gui(screen, player)
        pg.display.flip()
        clock.tick(FPS)
    return player.score

import pygame
from settings import *
from sprites import Generic
from support import import_folder
from random import randint, choice


class Sky:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.full_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.start_color = [255, 255, 255]
        self.now_color = [255, 255, 255]
        self.end_color = [38, 101, 189]
        self.day_flag = True

    def update(self, dt):
        if self.day_flag:
            cnt_color = 0
            for index, value in enumerate(self.end_color):
                if self.now_color[index] > value and self.day_flag:
                    if self.now_color[2] < 190:
                        self.now_color[index] -= 0.5 * dt
                    else:
                        self.now_color[index] -= 0.1 * dt
                if self.now_color[2] < 190 and self.now_color[1] < 102 and self.now_color[0] < 39:
                    self.day_flag = False
                    break


    def display(self):
        self.full_surf.fill(self.now_color)
        self.display_surface.blit(self.full_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)


class Drop(Generic):
    def __init__(self, surf, pos, moving, groups, z):
        # general setup
        super().__init__(pos, surf, groups, z)
        self.lifetime = randint(400, 500)
        self.start_time = pygame.time.get_ticks()

        # moving
        self.moving = moving
        if self.moving:
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.direction = pygame.math.Vector2(-2, 4)
            self.speed = randint(200, 250)

    def update(self, dt):
        # movement
        if self.moving:
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = (round(self.pos.x)), round(self.pos.y)

        # timer
        start_time = pygame.time.get_ticks()
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()


class Rain:
    def __init__(self, all_sprites):
        self.all_sprites = all_sprites
        self.rain_drops = import_folder('../graphics/rain/drops')
        self.rain_floor = import_folder('../graphics/rain/floor')

        self.player_pos = [1000, 1000]

        self.floor_w, self.floor_h = pygame.image.load('../graphics/world/ground.png').get_size()

    def create_floor(self):
        Drop(
            surf=choice(self.rain_floor),
            pos=(randint(self.player_pos[0] - 1000, self.player_pos[0] + 1000),
                 randint(self.player_pos[1] - 1000, self.player_pos[1] + 1000)),
            moving=False,
            groups=self.all_sprites,
            z=LAYERS['rain floor'])

    def create_drops(self):
        Drop(
            surf=choice(self.rain_drops),
            pos=(randint(self.player_pos[0] - 1000, self.player_pos[0] + 1000),
                 randint(self.player_pos[1] - 1000, self.player_pos[1] + 1000)),
            moving=True,
            groups=self.all_sprites,
            z=LAYERS['rain drops'])

    def update(self):
        self.create_floor()
        self.create_drops()
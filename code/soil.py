from resourse import *
from support import *
from settings import *
from random import choice
from pytmx.util_pygame import load_pygame


class SoilTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['soil']


class WaterTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['soil water']


class Plant(pygame.sprite.Sprite):
    def __init__(self, plant_type, groups, soil, check_watered):
        super().__init__(groups)

        # setup
        self.plant_type = plant_type
        self.frames = import_folder(f'../graphics/fruit/{plant_type}')
        self.soil = soil
        self.check_watered = check_watered

        # Проверяем, что кадры загружены
        if not self.frames:
            print(f"Error: No frames found for plant type: {plant_type}")
            # Создаем временный поверхность, чтобы избежать краша
            self.frames = [pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)]
            self.frames[0].fill((255, 0, 0, 128))  # Красный квадрат для отладки

        # plant growing
        self.age = 0
        self.max_age = len(self.frames) - 1
        self.grow_speed = GROW_SPEED[plant_type]
        self.harvestable = False

        # sprite setup
        self.image = self.frames[self.age]
        self.y_offset = -25 if plant_type == 'corn' else -30
        self.rect = self.image.get_rect(midbottom=self.soil.rect.midbottom + pygame.math.Vector2(0, self.y_offset))
        self.z = LAYERS['ground plant']

    def grow(self, load: bool = False):
        if self.check_watered(self.rect.center) and not load:
            self.age += self.grow_speed

        if int(self.age) > 0:
            self.z = LAYERS['main']
            self.hitbox = self.image.get_rect(midbottom=(self.rect.midbottom[0]-1, self.rect.midbottom[1]-27)).inflate(-self.rect.width * 0.3, - self.rect.height * 0.95)

        if self.age >= self.max_age:
            self.age = self.max_age
            self.harvestable = True

        # Убеждаемся, что возраст не выходит за границы
        frame_index = min(int(self.age), self.max_age)
        self.image = self.frames[frame_index]
        self.rect = self.image.get_rect(midbottom=self.soil.rect.midbottom + pygame.math.Vector2(0, self.y_offset))

class SoilLayer:
    def __init__(self, all_sprites, collision_sprites):
        # sprite groups
        self.all_sprites = all_sprites
        self.collision_sprites = collision_sprites
        self.soil_sprites = pygame.sprite.Group()
        self.water_sprites = pygame.sprite.Group()
        self.plant_sprites = pygame.sprite.Group()

        # graphics
        self.soil_surfs = pygame.image.load('../graphics/soil/x.png').convert_alpha()
        self.water_surfs = import_folder('../graphics/soil_water/')

        self.create_soil_grid()
        self.create_hit_rects()

        # sounds
        self.hoe_sound = sound_list['Hoe']
        self.plant_sound = sound_list['Plant']

    def create_soil_grid(self):
        ground = pygame.image.load('../graphics/world/ground.png')
        h_tiles, w_tiles = ground.get_width() // TILE_SIZE, ground.get_height() // TILE_SIZE

        self.grid = [[[] for _ in range(h_tiles)] for _ in range(w_tiles)]

        for x, y, _ in load_pygame('../data/map.tmx').get_layer_by_name('Farmable').tiles():
            self.grid[y][x].append('F')

    def create_hit_rects(self):
        self.hit_rects = []
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'F' in cell:
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.hit_rects.append(rect)

    def get_hit(self, point):
        for rect in self.hit_rects:
            if rect.collidepoint(point):

                x = rect.x // TILE_SIZE
                y = rect.y // TILE_SIZE

                if 'F' in self.grid[y][x] and 'X' not in self.grid[y][x]:
                    # sound play
                    self.hoe_sound.play()

                    # create soil
                    self.grid[y][x].append('X')
                    self.create_soil_tiles()
                    if self.raining:
                        self.water_all()

    def water(self, target_pos):
        for soil_sprites in self.soil_sprites.sprites():
            if soil_sprites.rect.collidepoint(target_pos):
                x = soil_sprites.rect.x // TILE_SIZE
                y = soil_sprites.rect.y // TILE_SIZE

                if 'W' not in self.grid[y][x]:
                    WaterTile(pos=soil_sprites.rect.topleft,
                              surf=choice(self.water_surfs),
                              groups=[self.all_sprites, self.water_sprites])

                self.grid[y][x].append('W')

    def water_all(self):
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'X' in cell and 'W' not in cell:
                    cell.append('W')

                    WaterTile(pos=(index_col * TILE_SIZE, index_row * TILE_SIZE),
                              surf=choice(self.water_surfs),
                              groups=[self.all_sprites, self.water_sprites])

    def remove_water(self):
        # destroy all water sprites
        for sprite in self.water_sprites.sprites():
            sprite.kill()

        # clean up the grid
        for row in self.grid:
            for cell in row:
                if 'W' in cell:
                    cell.remove('W')

    def remove_soil(self):
        for soil_sprite in self.soil_sprites.sprites():

            x = soil_sprite.rect.x // TILE_SIZE
            y = soil_sprite.rect.y // TILE_SIZE

            if 'P' not in self.grid[y][x]:
                self.grid[y][x].remove('X')

                for sprite in self.soil_sprites.sprites():
                    if sprite.rect.x == x * TILE_SIZE and sprite.rect.y == y * TILE_SIZE:
                        sprite.kill()

    def restore_water_tiles(self):
        """Восстанавливает водные тайлы после загрузки"""
        # Очищаем существующие водные тайлы
        for water_tile in self.water_sprites.sprites():
            water_tile.kill()

        # Создаем водные тайлы для всех политых клеток
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'W' in cell:
                    WaterTile(
                        pos=(index_col * TILE_SIZE, index_row * TILE_SIZE),
                        surf=choice(self.water_surfs),
                        groups=[self.all_sprites, self.water_sprites]
                    )

    def check_watered(self, pos):
        x = pos[0] // TILE_SIZE
        y = pos[1] // TILE_SIZE
        cell = self.grid[y][x]
        is_watered = 'W' in cell

        return is_watered

    def plant_seed(self, target_pos, seed, seed_inventory, selected_seed):
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):

                x = soil_sprite.rect.x // TILE_SIZE
                y = soil_sprite.rect.y // TILE_SIZE

                if 'P' not in self.grid[y][x]:
                    # Проверяем, есть ли семена этого типа
                    if seed_inventory[selected_seed] <= 0:
                        return

                    self.plant_sound.play()

                    self.grid[y][x].append('P')

                    seed_inventory[selected_seed] -= 1

                    try:
                        Plant(plant_type=seed,
                              groups=[self.all_sprites, self.plant_sprites, self.collision_sprites],
                              soil=soil_sprite,
                              check_watered=self.check_watered)
                    except Exception as e:
                        print(f"Error planting {seed}: {e}")
                        # Откатываем изменения если посадка не удалась
                        self.grid[y][x].remove('P')
                        seed_inventory[selected_seed] += 1

    def update_plants(self, load: bool = False):
        for plant in self.plant_sprites.sprites():
            plant.grow(load)

    def create_soil_tiles(self):
        self.soil_sprites.empty()
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'X' in cell:
                    SoilTile(pos=(index_col * TILE_SIZE, index_row * TILE_SIZE),
                             surf=self.soil_surfs,
                             groups=[self.all_sprites, self.soil_sprites])
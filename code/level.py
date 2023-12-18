from menu import Menu
from support import *
from settings import *
from sky import Rain, Sky
from player import Player
from random import randint
from soil import SoilLayer
from overlay import Overlay
from start_menu import StartMenu
from transition import Transition
from pytmx.util_pygame import load_pygame
from sprites import Generic, Water, WildFlower, Tree, Interaction, Particle, Collision


class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()

        self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites)
        self.setup()
        self.overlay = Overlay(self.player)
        self.transition = Transition(self.reset, self.player)

        # sky
        self.rain = Rain(self.all_sprites)
        self.raining = randint(0, 10) > 10
        self.soil_layer.raining = self.raining
        self.sky = Sky()

        # shop
        self.menu = Menu(self.player, self.toggle_shop)
        self.shop_active = False

        # music
        self.rain_sound = pygame.mixer.Sound('../audio/rain.mp3')
        self.rain_sound.set_volume(SOUND_VOLUME['Rain'])
        self.success = pygame.mixer.Sound('../audio/success3.mp3')
        self.success.set_volume(SOUND_VOLUME['Success'])
        self.music = pygame.mixer.Sound('../audio/bg_music2.mp3')
        self.music.set_volume(SOUND_VOLUME['Music'])
        self.music.play(loops=-1)

        # start menu
        self.start_menu = StartMenu(self.player, self.start_game_menu)
        self.start_menu_active = False

    def setup(self):
        # load map tmx
        tmx_data = load_pygame('../data/map.tmx')

        # house
        for layer in ['HouseFloor', 'HouseFurnitureBottom']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, LAYERS['house bottom'])

        for layer in ['HouseWalls', 'HouseFurnitureTop']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

        # Fence
        for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE), surf, [self.all_sprites, self.collision_sprites])

        # Water
        water_frames = import_folder('../graphics/water')
        for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
            Water((x * TILE_SIZE, y * TILE_SIZE), water_frames, self.all_sprites)

        # Trees
        for obj in tmx_data.get_layer_by_name('Trees'):
            Tree(pos=(obj.x, obj.y),
                 surf=obj.image,
                 groups=[self.all_sprites, self.collision_sprites, self.tree_sprites],
                 name=obj.name,
                 player_add=self.player_add)

        # Wild Flowers
        for obj in tmx_data.get_layer_by_name('Decoration'):
            WildFlower((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])

        # Collision tiles
        for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
            Collision('Collision', (x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)),
                      self.collision_sprites)
        for x, y, surf in tmx_data.get_layer_by_name('Collision up').tiles():
            Collision('Collision up', (x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)),
                      self.collision_sprites)
        for x, y, surf in tmx_data.get_layer_by_name('Collision down').tiles():
            Collision('Collision down', (x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)),
                      self.collision_sprites)
        for x, y, surf in tmx_data.get_layer_by_name('Collision right').tiles():
            Collision('Collision right', (x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)),
                      self.collision_sprites)
        for x, y, surf in tmx_data.get_layer_by_name('Collision left').tiles():
            Collision('Collision left', (x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)),
                      self.collision_sprites)
        for x, y, surf in tmx_data.get_layer_by_name('Collision corner').tiles():
            Collision('Collision corner', (x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)),
                      self.collision_sprites)

        # Player
        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name == 'Start':
                self.player = Player(
                    pos=(obj.x, obj.y),
                    group=self.all_sprites,
                    collision_sprites=self.collision_sprites,
                    tree_sprites=self.tree_sprites,
                    interaction=self.interaction_sprites,
                    soil_layer=self.soil_layer,
                    toggle_shop=self.toggle_shop,
                    start_menu=self.start_game_menu)

            if obj.name == 'Bed':
                Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

            if obj.name == 'Trader':
                Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

        # Ground
        Generic(
            pos=(0, 0),
            surf=pygame.image.load('../graphics/world/ground.png').convert_alpha(),
            groups=self.all_sprites,
            z=LAYERS['ground']
        )

    def player_add(self, item):
        self.player.item_inventory[item] += 1
        self.success.play()

    def start_game_menu(self):
        self.start_menu_active = not self.start_menu_active

    def toggle_shop(self):
        self.shop_active = not self.shop_active

    def reset(self):
        # plants
        self.soil_layer.update_plants()

        # soil
        self.soil_layer.remove_soil()
        self.soil_layer.remove_water()
        self.raining = randint(0, 10) > 7
        self.soil_layer.raining = self.raining
        if self.raining:
            self.rain_sound.play(loops=-1)
            self.soil_layer.water_all()
        else:
            self.rain_sound.play(loops=-1)
            self.rain_sound.stop()

        # appel on the trees
        for tree in self.tree_sprites.sprites():
            for apple in tree.apple_sprites.sprites():
                apple.kill()
            tree.create_fruit()

        # sky
        self.sky.start_color = [255, 255, 255]

    def plant_collision(self):
        if self.soil_layer.plant_sprites:
            for plant in self.soil_layer.plant_sprites.sprites():
                if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
                    self.player_add(plant.plant_type)
                    plant.kill()
                    Particle(pos=plant.rect.topleft,
                             surf=plant.image,
                             groups=self.all_sprites,
                             z=LAYERS['main'])

                    self.soil_layer.grid[plant.rect.centery // TILE_SIZE][plant.rect.centerx // TILE_SIZE].remove('P')

    def run(self, dt):
        # drawing logic
        self.display_surface.fill('black')
        self.all_sprites.custom_draw(self.player)

        # updates
        if self.shop_active:
            self.sky.display()
            self.menu.update()
        elif self.start_menu_active:
            self.sky.display()
            self.start_menu.update()
            self.success.set_volume(SOUND_VOLUME['Success'])
            self.music.set_volume(SOUND_VOLUME['Music'])
            self.soil_layer.hoe_sound.set_volume(SOUND_VOLUME['Hoe'])
            self.soil_layer.plant_sound.set_volume(SOUND_VOLUME['Plant'])
        else:
            self.all_sprites.update(dt)
            self.plant_collision()

        # weather
        self.overlay.display()
        if self.raining and not self.shop_active and not self.start_menu_active:
            self.rain.update()  # rain

        if not self.shop_active and not self.start_menu_active:
            self.rain.player_pos = [self.player.rect.centerx, self.player.rect.centery]
            self.sky.display()
            self.sky.update(dt)
            self.overlay.display()

        # transition overlay
        if self.player.sleep:
            self.transition.play()


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)

                # # analytics
                # if sprite == player:
                #     pygame.draw.rect(self.display_surface, 'red', offset_rect, 5)
                #     hitbox_rect = player.hitbox.copy()
                #     hitbox_rect.center = offset_rect.center
                #     pygame.draw.rect(self.display_surface, 'green', hitbox_rect, 5)
                #     target_pos = offset_rect.center + PLAYER_TOOL_OFFSET[player.status.split('_')[0]]
                #     pygame.draw.circle(self.display_surface, 'blue', target_pos, 5)

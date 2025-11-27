from timer import Timer
from shop import Shop
from support import *
from settings import *
from sky import Rain, Sky
from player import Player
from random import randint
from soil import SoilLayer
from overlay import Overlay
from esc_menu import EscMenu
from inventory import Inventory
from start_menu import StartMenu
from transition import Transition
from pytmx.util_pygame import load_pygame
from sprites import Generic, WildFlower, Tree, Interaction, Particle, Collision


class Level:
    def __init__(self):
        # get the display surface
        self.timer = Timer(250)
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

        # Инвентарь
        self.inventory = Inventory(self.player, self.toggle_inventory)
        self.inventory_active = False

        # sky
        self.rain = Rain(self.all_sprites)
        self.raining = randint(0, 10) > 10
        self.soil_layer.raining = self.raining
        self.sky = Sky()

        # start menu
        self.start_menu = StartMenu(self.toggle_start_menu)
        self.start_menu_active = False

        # esc menu
        self.esc_menu = EscMenu(self.player, self.toggle_esc_menu)
        self.esc_menu_active = False
        self.menu_cooldown = Timer(250)

        # shop
        self.shop_menu = Shop(self.player, self.toggle_shop)
        self.shop_active = False

        # import
        self.cursor_surf = pygame.image.load(f'../graphics/overlay/cursor.png').convert_alpha()

        # music
        self.rain_sound = pygame.mixer.Sound('../audio/rain.mp3')
        self.rain_sound.set_volume(SOUND_VOLUME['Rain'])
        self.success = pygame.mixer.Sound('../audio/success3.mp3')
        self.success.set_volume(SOUND_VOLUME['Success'])
        self.music = pygame.mixer.Sound('../audio/bg_music2.mp3')
        self.music.set_volume(SOUND_VOLUME['Music'])
        self.music.play(loops=-1)

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
        for i in collision_list:
            for x, y, surf in tmx_data.get_layer_by_name(f'{i}').tiles():
                Collision(f'{i}', (x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)),self.collision_sprites)

        # Player, bed, trader
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
                    start_menu=self.toggle_esc_menu,
                    toggle_inventory=self.toggle_inventory)

            if obj.name == 'Bed':
                Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

            if obj.name == 'Trader':
                Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

        # Ground
        Generic(pos=(0, 0),surf=pygame.image.load('../graphics/world/ground.png').convert_alpha(),groups=self.all_sprites,z=LAYERS['ground'])

    def player_add(self, item, cnt=1):
        self.player.item_inventory[item] += cnt
        self.success.play()

    def toggle_esc_menu(self):
        self.esc_menu_active = not self.esc_menu_active
        self.menu_cooldown.activate()

    def toggle_shop(self):
        self.shop_active = not self.shop_active
        self.menu_cooldown.activate()

    def toggle_inventory(self):
        self.inventory_active = not self.inventory_active
        self.menu_cooldown.activate()

    def toggle_start_menu(self):
        self.start_menu_active = not self.start_menu_active

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
            if tree.alive:
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
        self.sky.display()

        # updates
        if self.start_menu_active:
            self.start_menu.update()

        elif self.shop_active:
            self.shop_menu.update()

        elif self.esc_menu_active:
            self.esc_menu.update()

            self.success.set_volume(SOUND_VOLUME['Success'])
            self.music.set_volume(SOUND_VOLUME['Music'])
            self.soil_layer.hoe_sound.set_volume(SOUND_VOLUME['Hoe'])
            self.soil_layer.plant_sound.set_volume(SOUND_VOLUME['Plant'])
            self.player.axe_sound.set_volume(SOUND_VOLUME['Axe'])

        else:
            # sprites
            self.all_sprites.update(dt)
            self.plant_collision()

            # weather
            self.sky.update(dt)

            if self.raining:
                self.rain.update()  # rain
            self.rain.player_pos = [self.player.rect.centerx, self.player.rect.centery]

            # overlay
            self.overlay.display()
            if self.inventory_active:
                self.inventory.update()

            # transition overlay
            if self.player.sleep:
                self.transition.play()

        # mouse
        pygame.mouse.set_visible(False)
        self.display_surface.blit(self.cursor_surf, (pygame.mouse.get_pos()))


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
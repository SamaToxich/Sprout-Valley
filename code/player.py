from resourse import sound_list
from support import *
from settings import *
from timer import Timer
from resourse import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, tree_sprites, interaction, soil_layer, toggle_shop, start_menu, toggle_inventory):
        super().__init__(group)

        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        # Инвентарь
        self.toggle_inventory = toggle_inventory

        # general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS['main']

        # movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        # collision
        self.hitbox = self.rect.copy().inflate((-126, -70))
        self.collision_sprite = collision_sprites

        # timers
        self.timers = {
            'water use': Timer(850, self.use_tool),
            'axe use': Timer(600, self.use_tool),
            'hoe use': Timer(600, self.use_tool),
            'tool switch': Timer(200),
            'seed use': Timer(300, self.use_seed),
            'seed switch': Timer(200),
            'ESC timer': Timer(200),
        }


        # tools
        self.tools = ['hoe', 'axe', 'water']
        self.tool_index = 1
        self.selected_tool = self.tools[self.tool_index]

        # seeds
        self.seeds = ['corn', 'tomato', 'cabbage', 'carrot', 'pumpkin', 'turnip', 'zucchini', 'cucumber']
        self.seed_index = 0
        self.seed_select_index = 0
        self.selected_seed = self.seeds[self.seed_index]

        # inventory
        self.item_inventory = item_inventory
        self.seed_inventory = seed_inventory

        self.money = MONEY

        # interaction
        self.tree_sprites = tree_sprites
        self.interaction = interaction
        self.sleep = False
        self.soil_layer = soil_layer
        self.toggle_shop = toggle_shop
        self.start_menu = start_menu

        # sound
        self.axe_sound = sound_list['Axe']
        self.switch = sound_list['Switch tool']
        self.watering = sound_list['Water']
        self.wave = sound_list['Wave']
        self.choice = sound_list['Choice']

    def use_tool(self):
        if self.selected_tool == 'hoe':
            self.soil_layer.get_hit(self.target_pos)

        if self.selected_tool == 'axe':
            for tree in self.tree_sprites.sprites():
                if tree.rect.collidepoint(self.target_pos) and tree.alive:
                    if hasattr(tree, 'damage'):
                        tree.damage()

        if self.selected_tool == 'water':
            self.soil_layer.water(self.target_pos)
            self.watering.play()

    def get_target_pos(self):
        if self.selected_tool == 'water':
            self.target_pos = self.rect.center + PLAYER_WATER_OFFSET[self.status.split('_')[0]]
        elif self.selected_tool == 'hoe':
            self.target_pos = self.rect.center + PLAYER_HOE_OFFSET[self.status.split('_')[0]]
        elif self.selected_tool == 'axe':
            self.target_pos = self.rect.center + PLAYER_AXE_OFFSET[self.status.split('_')[0]]

    def use_seed(self):
        target_pos = self.rect.center + PLAYER_SEED_OFFSET[self.status.split('_')[0]]
        if self.seed_inventory[self.selected_seed] > 0:
            self.soil_layer.plant_seed(target_pos, self.selected_seed, self.seed_inventory, self.selected_seed)

    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_run': [], 'left_run': [], 'up_run': [], 'down_run': [],
                           'right_hoe': [], 'left_hoe': [], 'up_hoe': [], 'down_hoe': [],
                           'right_axe': [], 'left_axe': [], 'up_axe': [], 'down_axe': [],
                           'right_water': [], 'left_water': [], 'up_water': [], 'down_water': []}

        for animation in self.animations.keys():
            full_path = '../graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += 9 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers['axe use'].active and not self.sleep and not self.timers['water use'].active and \
                not self.timers['hoe use'].active:
            # directions
            if keys[pygame.K_w]:
                self.status = 'up'
                self.direction.y = -1
            elif keys[pygame.K_s]:
                self.status = 'down'
                self.direction.y = 1
            else:
                self.direction.y = 0

            if keys[pygame.K_d]:
                self.status = 'right'
                self.direction.x = 1
            elif keys[pygame.K_a]:
                self.status = 'left'
                self.direction.x = -1
            else:
                self.direction.x = 0

            if keys[pygame.K_LSHIFT]:
                self.speed = 300
                if keys[pygame.K_d]:
                    self.status = 'right_run'
                elif keys[pygame.K_a]:
                    self.status = 'left_run'
                elif keys[pygame.K_w]:
                    self.status = 'up_run'
                elif keys[pygame.K_s]:
                    self.status = 'down_run'
            else:
                self.speed = 200

            # tool use
            if keys[pygame.K_SPACE]:
                # timer for the tool use
                if self.selected_tool == 'water':
                    self.timers['water use'].activate()
                elif self.selected_tool == 'hoe':
                    self.timers['hoe use'].activate()
                elif self.selected_tool == 'axe':
                    self.timers['axe use'].activate()
                    self.soil_layer.get_hit(self.target_pos)
                    for tree in self.tree_sprites.sprites():
                        if tree.rect.collidepoint(self.target_pos) and tree.alive:
                            self.axe_sound.play()

                self.direction = pygame.math.Vector2()
                self.frame_index = 0
                self.wave.play()

            # change tool
            if not self.timers['tool switch'].active:
                if keys[pygame.K_q] or keys[pygame.K_e]:
                    self.switch.play()
                    self.timers['tool switch'].activate()
                    if keys[pygame.K_q]:
                        self.tool_index += 1
                        self.tool_index = self.tool_index if self.tool_index < len(self.tools) else 0
                        self.selected_tool = self.tools[self.tool_index]
                    else:
                        self.tool_index -= 1
                        self.tool_index = self.tool_index if self.tool_index >= 0 else len(self.tools) - 1
                        self.selected_tool = self.tools[self.tool_index]

            # change seed
            if not self.timers['seed switch'].active:
                if keys[pygame.K_1]:
                    self.timers['seed switch'].activate()
                    self.switch.play()
                    self.seed_select_index = 0
                    self.seed_index = 0
                if keys[pygame.K_2]:
                    self.timers['seed switch'].activate()
                    self.switch.play()
                    self.seed_select_index = 1
                    self.seed_index = 1
                if keys[pygame.K_3]:
                    self.timers['seed switch'].activate()
                    self.switch.play()
                    self.seed_select_index = 2
                    self.seed_index = 2
                if keys[pygame.K_4]:
                    self.timers['seed switch'].activate()
                    self.switch.play()
                    self.seed_select_index = 3
                    self.seed_index = 3
                if keys[pygame.K_5]:
                    self.timers['seed switch'].activate()
                    self.switch.play()
                    self.seed_select_index = 4
                    self.seed_index = 4
                if keys[pygame.K_6]:
                    self.timers['seed switch'].activate()
                    self.switch.play()
                    self.seed_select_index = 5
                    self.seed_index = 5
                if keys[pygame.K_7]:
                    self.timers['seed switch'].activate()
                    self.switch.play()
                    self.seed_select_index = 6
                    self.seed_index = 6
                if keys[pygame.K_8]:
                    self.timers['seed switch'].activate()
                    self.switch.play()
                    self.seed_select_index = 7
                    self.seed_index = 7

            self.selected_seed = self.seeds[self.seed_index]

            # seed use
            if keys[pygame.K_TAB]:
                # timer for the seed use
                self.timers['seed use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            if keys[pygame.K_i] and not self.timers['tool switch'].active:
                self.toggle_inventory()
                self.timers['tool switch'].activate()

            # shop
            if keys[pygame.K_f]:
                collided_interaction_sprite = pygame.sprite.spritecollide(self, self.interaction, False)

                if collided_interaction_sprite:
                    if collided_interaction_sprite[0].name == 'Trader':
                        self.toggle_shop()

                    if collided_interaction_sprite[0].name == 'Bed':
                        self.status = 'left_idle'
                        self.sleep = True

            # menu
            if keys[pygame.K_ESCAPE]:
                if not self.timers['ESC timer'].active:
                    self.start_menu()
                    self.choice.play()
                    self.timers['ESC timer'].activate()

    def get_status(self):
        # idle
        # if the player is not moving:
        if self.direction.magnitude() == 0:
            # add _idle to the status
            self.status = self.status.split('_')[0] + '_idle'

        # tool use
        if self.timers['axe use'].active or self.timers['water use'].active or self.timers['hoe use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool

    def update_timer(self):
        for timer in self.timers.values():
            timer.update()

    def collision(self, direction):
        for sprite in self.collision_sprite.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == 'horizontal':
                        if self.direction.x > 0:  # moving right
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:  # moving left
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                    if direction == 'vertical':
                        if self.direction.y > 0:  # moving down
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:  # moving up
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery

    def move(self, dt):
        # normalizing a vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timer()
        self.get_target_pos()

        self.move(dt)
        self.animate(dt)

        self.watering.set_volume(SOUND_VOLUME['Water'])
        self.switch.set_volume(SOUND_VOLUME['Switch tool'])
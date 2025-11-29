from support import *
from resourse import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, tree_sprites, interaction, soil_layer, toggle_shop, esc_menu, toggle_inventory):
        super().__init__(group)

        # Словарь для анимаций
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [],
            'right_idle':    [], 'left_idle':    [], 'up_idle':  [], 'down_idle':    [],
            'right_run':     [], 'left_run':     [], 'up_run':   [], 'down_run':     [],
            'right_hoe':     [], 'left_hoe':     [], 'up_hoe':   [], 'down_hoe':     [],
            'right_axe':     [], 'left_axe':     [], 'up_axe':   [], 'down_axe':     [],
            'right_water':   [], 'left_water':   [], 'up_water': [], 'down_water':   []
                           }

        # Импорт анимаций
        for animation in self.animations.keys():
            full_path = '../graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)

        # Статус и индекс кадра анимации
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


        # tools
        self.target_pos = None
        self.tools = ['hoe', 'axe', 'water']
        self.tool_index = 1
        self.selected_tool = self.tools[self.tool_index]

        # seeds
        self.seeds = ['corn', 'tomato', 'cabbage', 'carrot', 'pumpkin', 'turnip', 'zucchini', 'cucumber']
        self.seed_index = 0
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
        self.esc_menu = esc_menu

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
                    if hasattr(tree, 'damage') and tree.health > 0:
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

    def animate(self, dt):
        self.frame_index += 9 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]

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
        self.get_target_pos()
        self.move(dt)
        self.animate(dt)
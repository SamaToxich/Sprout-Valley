import pygame
from resourse import *
from settings import *
from random import randint, choice


class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS['main']):

        super().__init__(groups)

        self.first_image = surf
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z
        self.hitbox = self.image.get_rect(topleft=(pos[0], pos[1]+10)).inflate(-self.rect.width * 0.2, -self.rect.height * 0.85)


class Collision(Generic):
    def __init__(self, name, pos, surf, groups):
        super().__init__(pos, surf, groups)

        if name == 'Collision':
            self.hitbox = self.image.get_rect(topleft=(pos[0], pos[1]-32)).inflate(-self.rect.width * 0.04, -self.rect.height * 0.13)
        if name == 'Collision up':
            self.hitbox = self.image.get_rect(topleft=(pos[0], pos[1]-50)).inflate(0, -self.rect.height * 0.7)
        if name == 'Collision down':
            self.hitbox = self.image.get_rect(topleft=(pos[0], pos[1]-20)).inflate(0, -self.rect.height * 0.5)
        if name == 'Collision corner':
            self.hitbox = self.image.get_rect(topleft=(pos[0], pos[1]-32)).inflate(-self.rect.width * 0.04, -self.rect.height * 0.13)
        if name == 'Collision left':
            self.hitbox = self.image.get_rect(topleft=(pos[0]-18, pos[1]-20)).inflate(-self.rect.width * 0.6, -self.rect.height * 0.5)
        if name == 'Collision right':
            self.hitbox = self.image.get_rect(topleft=(pos[0]+18, pos[1]-20)).inflate(-self.rect.width * 0.6, -self.rect.height * 0.5)


class Interaction(Generic):
    def __init__(self, pos, size, groups, name):
        surf = pygame.Surface(size)
        super().__init__(pos, surf, groups)

        self.name = name


class WildFlower(Generic):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

        self.hitbox = self.image.get_rect(topleft=(pos[0], pos[1]-25)).inflate(-20, -self.rect.height * 0.6)


class Particle(Generic):
    def __init__(self, pos, surf, groups, z, duration=200):
        super().__init__(pos, surf, groups, z)

        self.start_time = pygame.time.get_ticks()
        self.duration = duration

        # white surface
        mask_surf = pygame.mask.from_surface(self.image)
        new_surf = mask_surf.to_surface()
        new_surf.set_colorkey((0, 0, 0))
        self.image = new_surf

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration:
            self.kill()


class Tree(Generic):
    def __init__(self, pos, surf, groups, name, player_add):
        super().__init__(pos, surf, groups)

        self.all_sprites = groups[0]

        # tree attributes
        self.name = name
        self.health = 5 if self.name == 'Small' else 8
        self.alive = True
        stump_path = f'../graphics/stumps/{"small" if self.name == "Small" else "large"}.png'
        self.stump_surf = pygame.image.load(stump_path).convert_alpha()

        # Генерируем уникальный ID для дерева
        self.tree_id = f"{name}_{pos[0]}_{pos[1]}"

        # apples
        self.apple_surf = sprite_list['apple']
        self.apple_pos = APPLE_POS[self.name]
        self.apple_sprites = pygame.sprite.Group()
        self.create_fruit()

        self.player_add = player_add

        # Resurrection system
        self.days_since_cut = 0  # дней с момента срубки
        self.days_to_resurrect = 3  # дней до воскрешения

    def damage(self):
        if self.alive and self.health > 0:
            # damaging the tree
            self.health -= 1

            # remove apple
            if len(self.apple_sprites.sprites()) > 0:
                random_apple = choice(self.apple_sprites.sprites())
                Particle(
                    pos=random_apple.rect.topleft,
                    surf=random_apple.image,
                    groups=self.all_sprites,
                    z=LAYERS['fruit'])
                self.player_add('apple')
                random_apple.kill()

    def check_death(self):
        if self.health <= 0:
            if self.alive:
                Particle(self.rect.topleft,self.image,self.all_sprites,LAYERS['fruit'],300)
            self.image = self.stump_surf
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            self.hitbox = self.image.get_rect(midbottom=(self.rect.midbottom[0], self.rect.midbottom[1] - 26)).inflate(
                -20, -self.rect.height * 0.99)

            if self.alive:
                self.days_since_cut = 0
                self.player_add('wood', 5 if self.name == 'Small' else 8)
            self.alive = False

            # Удаляем все яблоки при срубке дерева
            for apple in self.apple_sprites.sprites():
                apple.kill()

    def increment_day(self):
        """Увеличивает счетчик дней для срубленного дерева"""
        if not self.alive:
            self.days_since_cut += 1
            if self.days_since_cut >= self.days_to_resurrect:
                self.resurrect()

    def resurrect(self):
        """Воскрешает дерево"""
        # Восстанавливаем здоровье
        self.health = 5 if self.name == 'Small' else 8
        self.alive = True

        # Восстанавливаем оригинальное изображение
        self.image = self.first_image

        # Восстанавливаем хитбокс
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        self.hitbox = self.image.get_rect(topleft=(self.rect.topleft[0], self.rect.topleft[1] + 10)).inflate(
            -self.rect.width * 0.2, -self.rect.height * 0.85)

        # Создаем новые яблоки
        self.create_fruit()

        # Сбрасываем счетчик дней
        self.days_since_cut = 0

    def create_fruit_from_save(self, has_apples):
        """Создает фрукты при загрузке сохранения"""
        if has_apples and self.alive:
            self.create_fruit()

    def create_fruit(self):
        for pos in self.apple_pos:
            if randint(0, 10) < 2:
                x = pos[0] + self.rect.left
                y = pos[1] + self.rect.top
                Generic(
                    pos=(x, y),
                    surf=self.apple_surf,
                    groups=[self.apple_sprites, self.all_sprites],
                    z=LAYERS['fruit'])

    def update(self, dt):
        if self.alive:
            self.check_death()
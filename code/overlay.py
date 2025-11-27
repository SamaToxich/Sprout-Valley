import pygame
from settings import *


class Overlay:
    def __init__(self, player):
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player

        # time
        self.clock = pygame.time.get_ticks()

        # imports
        self.font = pygame.font.Font('../font/Pixeltype.ttf', 55)
        self.font_seed = pygame.font.Font('../font/Pixeltype.ttf', 25)
        self.font_time = pygame.font.Font('../font/Pixeltype.ttf', 40)
        overlay_path = '../graphics/overlay/'
        self.tools_sufr = {tool: pygame.image.load(f'{overlay_path}{tool}.png').convert_alpha() for tool in
                           player.tools}
        self.seeds_sufr = {seed: pygame.image.load(f'{overlay_path}{seed}.png').convert_alpha() for seed in
                           player.seeds}
        self.slot_surf = pygame.image.load(f'{overlay_path}slot.png').convert_alpha()
        self.background_surf = pygame.image.load(f'{overlay_path}back.png').convert_alpha()
        self.hp_money_bar = pygame.image.load(f'{overlay_path}hp_money_bar.png').convert_alpha()
        self.select_slot = pygame.image.load(f'{overlay_path}select.png').convert_alpha()

        # Создаем элементы времени программно
        self.create_time_elements()

    def create_time_elements(self):
        # Создаем фон для времени
        self.time_bg_surf = pygame.Surface((160, 60), pygame.SRCALPHA)
        # Рисуем скругленный прямоугольник с градиентом
        for i in range(60):
            alpha = 150 - i // 2
            pygame.draw.rect(self.time_bg_surf, (0, 0, 0, alpha),
                             (0, i, 160, 1), border_radius=10)

        # Создаем иконки времени суток
        self.time_icons = {
            'morning': self.create_morning_icon(),
            'day': self.create_day_icon(),
            'evening': self.create_evening_icon(),
            'night': self.create_night_icon()
        }

    def create_morning_icon(self):
        """Создает иконку утра (восходящее солнце)"""
        icon = pygame.Surface((32, 32), pygame.SRCALPHA)
        # Фон неба
        pygame.draw.rect(icon, (135, 206, 235, 200), (0, 0, 32, 32), border_radius=16)
        # Солнце
        pygame.draw.circle(icon, (255, 215, 0), (16, 20), 10)
        # Лучи
        for angle in range(0, 360, 45):
            rad = angle * 3.14159 / 180
            start_x = 16 + 12 * pygame.math.Vector2(1, 0).rotate(angle).x
            start_y = 20 + 12 * pygame.math.Vector2(1, 0).rotate(angle).y
            end_x = 16 + 16 * pygame.math.Vector2(1, 0).rotate(angle).x
            end_y = 20 + 16 * pygame.math.Vector2(1, 0).rotate(angle).y
            pygame.draw.line(icon, (255, 215, 0), (start_x, start_y), (end_x, end_y), 2)
        return icon

    def create_day_icon(self):
        """Создает иконку дня (солнце)"""
        icon = pygame.Surface((32, 32), pygame.SRCALPHA)
        # Фон неба
        pygame.draw.rect(icon, (135, 206, 235, 200), (0, 0, 32, 32), border_radius=16)
        # Солнце
        pygame.draw.circle(icon, (255, 255, 0), (16, 16), 12)
        # Лучи
        for angle in range(0, 360, 30):
            rad = angle * 3.14159 / 180
            start_x = 16 + 14 * pygame.math.Vector2(1, 0).rotate(angle).x
            start_y = 16 + 14 * pygame.math.Vector2(1, 0).rotate(angle).y
            end_x = 16 + 18 * pygame.math.Vector2(1, 0).rotate(angle).x
            end_y = 16 + 18 * pygame.math.Vector2(1, 0).rotate(angle).y
            pygame.draw.line(icon, (255, 255, 0), (start_x, start_y), (end_x, end_y), 2)
        return icon

    def create_evening_icon(self):
        """Создает иконку вечера (закат)"""
        icon = pygame.Surface((32, 32), pygame.SRCALPHA)
        # Фон неба (градиент от оранжевого к фиолетовому)
        for i in range(32):
            color = (255 - i * 2, 100 - i * 2, 50 + i * 3, 200)
            pygame.draw.rect(icon, color, (0, i, 32, 1))
        # Солнце у горизонта
        pygame.draw.circle(icon, (255, 140, 0), (16, 24), 8)
        # Горизонт
        pygame.draw.rect(icon, (101, 67, 33), (0, 26, 32, 6))
        return icon

    def create_night_icon(self):
        """Создает иконку ночи (луна и звезды)"""
        icon = pygame.Surface((32, 32), pygame.SRCALPHA)
        # Фон ночного неба
        pygame.draw.rect(icon, (25, 25, 112, 200), (0, 0, 32, 32), border_radius=16)
        # Луна
        pygame.draw.circle(icon, (220, 220, 220), (20, 12), 8)
        # Фаза луны (полумесяц)
        pygame.draw.circle(icon, (25, 25, 112), (16, 12), 7)
        # Звезды
        star_positions = [(8, 8), (12, 20), (24, 16), (6, 16), (18, 6)]
        for pos in star_positions:
            pygame.draw.circle(icon, (255, 255, 255), pos, 1)
            # Лучи звезд
            for offset in [(0, -2), (0, 2), (-2, 0), (2, 0)]:
                pygame.draw.line(icon, (255, 255, 255),
                                 (pos[0] + offset[0] * 0.7, pos[1] + offset[1] * 0.7),
                                 (pos[0] + offset[0] * 1.3, pos[1] + offset[1] * 1.3), 1)
        return icon

    def display(self):
        # tools
        tool_surf = self.tools_sufr[self.player.selected_tool]
        tool_rect = tool_surf.get_rect(center=OVERLAY_POSITIONS['tool'])

        self.display_surface.blit(tool_surf, tool_rect)

        # hp and money bar
        hp_money_bar_rect = self.hp_money_bar.get_rect(topleft=OVERLAY_POSITIONS['hp_money_bar'])
        self.display_surface.blit(self.hp_money_bar, hp_money_bar_rect)

        text_surf = self.font.render(f'{self.player.money}', True, '#b68962')
        text_rect = text_surf.get_rect(topleft=(60, 155))
        self.display_surface.blit(text_surf, text_rect)

        # background
        back_rect = self.slot_surf.get_rect(midbottom=(SCREEN_WIDTH // 2 - 337, SCREEN_HEIGHT - 93))
        self.display_surface.blit(self.background_surf, back_rect)

        # slot
        for i in range(8):
            slot_rect = self.slot_surf.get_rect(center=((340 + (i * 76)), SCREEN_HEIGHT - 88))
            self.display_surface.blit(self.slot_surf, slot_rect)

        # select slot
        select_slot_rect = self.select_slot.get_rect(
            center=((340 + (self.player.seed_select_index * 76)), SCREEN_HEIGHT - 88))
        self.display_surface.blit(self.select_slot, select_slot_rect)

        # seeds
        for i in range(len(self.seeds_sufr)):
            seed_surf = list(self.seeds_sufr.values())[i]
            seed_rect = seed_surf.get_rect(center=((340 + (76 * i)), SCREEN_HEIGHT - 88))

            text_surf = self.font_seed.render(f'{self.player.seed_inventory[self.player.seeds[i]]}', True, 'black')
            text_rect = text_surf.get_rect(topleft=(seed_rect.centerx + 16, seed_rect.centery + 16))

            self.display_surface.blit(seed_surf, seed_rect)
            self.display_surface.blit(text_surf, text_rect)

        # Время - улучшенное отображение
        self.display_time()

    def display_time(self):
        # Получаем игровое время
        self.clock = pygame.time.get_ticks() // 1000
        game_hours = (self.clock // 60) + 6  # Начинаем с 6 утра
        game_minutes = self.clock % 60

        # Определяем время суток для иконки и цвета
        if 6 <= game_hours < 10:
            time_of_day = 'morning'
            time_color = '#FFD700'  # золотистый для утра
            bg_color = (135, 206, 235, 150)  # светло-голубой
        elif 10 <= game_hours < 16:
            time_of_day = 'day'
            time_color = '#FFFF00'  # желтый для дня
            bg_color = (135, 206, 235, 150)  # светло-голубой
        elif 16 <= game_hours < 20:
            time_of_day = 'evening'
            time_color = '#FF8C00'  # оранжевый для вечера
            bg_color = (255, 140, 0, 100)  # оранжевый
        else:
            time_of_day = 'night'
            time_color = '#4169E1'  # синий для ночи
            bg_color = (25, 25, 112, 150)  # темно-синий

        # Ограничиваем часы до 24-часового формата
        game_hours = game_hours % 24

        # Форматируем время
        time_text = f'{game_hours}:{"0" + str(game_minutes) if game_minutes < 10 else game_minutes}'

        # Создаем динамический фон на основе времени суток
        dynamic_bg = pygame.Surface((160, 60), pygame.SRCALPHA)
        pygame.draw.rect(dynamic_bg, bg_color, (0, 0, 160, 60), border_radius=10)
        pygame.draw.rect(dynamic_bg, (255, 255, 255, 50), (0, 0, 160, 60), 2, border_radius=10)

        # Отображаем фон времени
        time_bg_rect = dynamic_bg.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        self.display_surface.blit(dynamic_bg, time_bg_rect)

        # Отображаем иконку времени суток
        time_icon = self.time_icons[time_of_day]
        time_icon_rect = time_icon.get_rect(midleft=(time_bg_rect.left + 10, time_bg_rect.centery-2))
        self.display_surface.blit(time_icon, time_icon_rect)

        # Отображаем текст времени
        text_surf = self.font_time.render(time_text, True, time_color)
        text_rect = text_surf.get_rect(midleft=(time_icon_rect.right + 22, time_bg_rect.centery+3))
        self.display_surface.blit(text_surf, text_rect)

        # Отображаем название времени суток под временем
        day_names = {
            'morning': 'morning',
            'day': 'day',
            'evening': 'evening',
            'night': 'night'
        }
        day_surf = self.font_seed.render(day_names[time_of_day], True, time_color)
        day_rect = day_surf.get_rect(midtop=(time_bg_rect.centerx, time_bg_rect.bottom + 5))
        self.display_surface.blit(day_surf, day_rect)
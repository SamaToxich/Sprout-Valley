import pygame
from resourse import *
from settings import *


class Overlay:
    def __init__(self, player):
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player

        # time - храним игровое время отдельно
        self.game_start_time = pygame.time.get_ticks()
        self.game_time_offset = 0  # смещение времени для сброса
        self.last_update_time = pygame.time.get_ticks()

        # imports
        self.font = font_list['font_55']
        self.font_seed = font_list['font_25']
        self.font_time = font_list['font_40']
        self.tools_sufr = {tool: tool_sprite  for tool in player.tools for tool_name, tool_sprite in sprite_list.items() if tool == tool_name}
        self.seeds_sufr = {seed: seed_sprite for seed in player.seeds for seed_name, seed_sprite in sprite_list.items() if seed == seed_name}
        self.slot_surf = sprite_list['slot']
        self.background_surf = sprite_list['back']
        self.hp_money_bar = sprite_list['hp_money_bar']
        self.select_slot = sprite_list['select']

        # Создаем элементы времени программно
        self.create_time_elements()

        # Устанавливаем время на 6
        self.reset_time()

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
        back_rect = self.background_surf.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10))
        self.display_surface.blit(self.background_surf, back_rect)

        # slot
        for i in range(8):
            slot_rect = self.slot_surf.get_rect(center=((SCREEN_WIDTH // 2 - 67 * 4 + (i * 76)), SCREEN_HEIGHT - 84))
            self.display_surface.blit(self.slot_surf, slot_rect)

        # select slot
        select_slot_rect = self.select_slot.get_rect(
            center=((SCREEN_WIDTH // 2 - 67 * 4 + (self.player.seed_index * 76)), SCREEN_HEIGHT - 84))
        self.display_surface.blit(self.select_slot, select_slot_rect)

        # seeds
        for i in range(len(self.seeds_sufr)):
            seed_surf = list(self.seeds_sufr.values())[i]
            seed_rect = seed_surf.get_rect(center=((SCREEN_WIDTH // 2 - 67 * 4 + (76 * i)), SCREEN_HEIGHT - 84))

            text_surf = self.font_seed.render(f'{self.player.seed_inventory[self.player.seeds[i]]}', True, 'black')
            text_rect = text_surf.get_rect(topleft=(seed_rect.centerx + 16, seed_rect.centery + 16))

            self.display_surface.blit(seed_surf, seed_rect)
            self.display_surface.blit(text_surf, text_rect)

        # Время
        self.display_time()

    def display_time(self):

        # Получаем игровое время
        game_hours, game_minutes = self.get_game_time()

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
        time_icon_rect = time_icon.get_rect(midleft=(time_bg_rect.left + 10, time_bg_rect.centery))
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

    def reset_time(self):
        """Сбрасывает время на 6:00"""
        current_time = pygame.time.get_ticks()
        # Устанавливаем смещение так, чтобы текущее время стало 6:00
        # 6 часов = 6 * 60 * 60 = 21600 секунд игрового времени
        self.time_offset = current_time - (21600 * 1000)  # преобразуем в миллисекунды
        self.last_update_time = current_time

    def get_game_time(self):
        """Возвращает текущее игровое время в часах и минутах"""
        # Используем реальное время с начала игры, но сбрасываем смещение при сне
        current_time = pygame.time.get_ticks()
        game_seconds = (current_time - self.time_offset) // 1000

        # Имитируем 24-часовой цикл (1 реальная секунда = 1 игровая минута)
        total_minutes = game_seconds
        game_hours = (total_minutes // 60) % 24 + 8
        if game_hours > 24:
            game_hours = game_hours % 24
        game_minutes = total_minutes % 60

        return game_hours, game_minutes
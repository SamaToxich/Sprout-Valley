import pygame
from settings import *
from timer import Timer
from resourse import *


class Inventory:
    def __init__(self, player, toggle_inventory):
        self.player = player
        self.toggle_inventory = toggle_inventory
        self.display_surface = pygame.display.get_surface()
        self.font = font_list['font_50']
        self.small_font = font_list['font_35']
        self.item_font = font_list['font_30']

        # Создаем элементы инвентаря программно
        self.create_inventory_elements()

        # Таймер для обработки ввода
        self.timer = Timer(200)

    def create_inventory_elements(self):
        # Создаем фон инвентаря - упрощенная версия без градиента
        self.bg_surf = pygame.Surface((450, 550), pygame.SRCALPHA)

        # Заливаем фон полупрозрачным темным цветом
        self.bg_surf.fill((40, 40, 40, 200))

        # Рисуем рамку
        pygame.draw.rect(self.bg_surf, (139, 69, 19, 255), (0, 0, 450, 550), 3, border_radius=12)
        pygame.draw.rect(self.bg_surf, (205, 133, 63, 200), (2, 2, 446, 546), 2, border_radius=12)

        # Создаем слоты для предметов
        self.slot_surf = pygame.Surface((70, 70), pygame.SRCALPHA)
        # Заливаем слот полупрозрачным цветом
        self.slot_surf.fill((60, 60, 60, 180))
        # Рисуем рамку слота
        pygame.draw.rect(self.slot_surf, (139, 69, 19, 255), (0, 0, 70, 70), 2, border_radius=8)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timer.active:
            if keys[pygame.K_i] or keys[pygame.K_ESCAPE]:
                self.toggle_inventory()
                self.timer.activate()

    def draw_inventory(self):
        # Отображаем фон инвентаря
        bg_rect = self.bg_surf.get_rect(topright=(SCREEN_WIDTH - 20, 80))
        self.display_surface.blit(self.bg_surf, bg_rect)

        # Заголовок инвентаря
        title_surf = self.font.render("INVENTORY", True, '#dcb98a')
        title_rect = title_surf.get_rect(midtop=(bg_rect.centerx, bg_rect.top + 15))
        self.display_surface.blit(title_surf, title_rect)

        # Разделительная линия после заголовка
        pygame.draw.line(self.display_surface, '#b68962',
                         (bg_rect.left + 20, bg_rect.top + 40),
                         (bg_rect.right - 20, bg_rect.top + 40), 2)

        # Отображаем предметы
        self.draw_items_section(bg_rect.left + 25, bg_rect.top + 85, "ITEMS", self.player.item_inventory)

        # Разделительная линия между предметами и семенами
        pygame.draw.line(self.display_surface, '#b68962',
                         (bg_rect.left + 20, bg_rect.top + 335),
                         (bg_rect.right - 20, bg_rect.top + 335), 2)

        # Отображаем семена
        self.draw_items_section(bg_rect.left + 25, bg_rect.top + 385, "SEEDS", self.player.seed_inventory)

    def draw_items_section(self, start_x, start_y, section_title, inventory):
        # Заголовок раздела
        title_surf = self.small_font.render(section_title, True, '#b68962')
        title_rect = title_surf.get_rect(topleft=(start_x, start_y - 30))
        self.display_surface.blit(title_surf, title_rect)

        items = list(inventory.items())

        # Рассчитываем максимальное количество строк для аккуратного отображения
        max_rows = 3
        items_per_row = 4

        for i, (item_name, count) in enumerate(items):
            if i >= max_rows * items_per_row:
                break

            row = i // items_per_row
            col = i % items_per_row

            x = start_x + col * 110
            y = start_y + row * 80

            # Отображаем слот
            slot_rect = self.slot_surf.get_rect(topleft=(x, y))
            self.display_surface.blit(self.slot_surf, slot_rect)

            # Отображаем название предмета
            display_name = self.get_display_name(item_name)
            name_surf = self.item_font.render(display_name, True, '#ffffff')
            name_rect = name_surf.get_rect(center=(slot_rect.centerx, slot_rect.centery - 8))
            self.display_surface.blit(name_surf, name_rect)

            # Отображаем количество
            count_surf = self.item_font.render(f"x{count}", True, '#ffd700')
            count_rect = count_surf.get_rect(center=(slot_rect.centerx, slot_rect.centery + 12))
            self.display_surface.blit(count_surf, count_rect)

        # Если предметов больше, чем помещается, показываем многоточие
        if len(items) > max_rows * items_per_row:
            dots_surf = self.item_font.render("...", True, '#b68962')
            dots_rect = dots_surf.get_rect(topleft=(start_x, start_y + max_rows * 80 + 5))
            self.display_surface.blit(dots_surf, dots_rect)

    def get_display_name(self, item_name):
        # Сокращаем длинные названия для лучшего отображения
        names = {
            'wood': 'Wood',
            'apple': 'Apple',
            'corn': 'Corn',
            'tomato': 'Tomato',
            'cabbage': 'Cabbage',
            'carrot': 'Carrot',
            'pumpkin': 'Pumpkin',
            'turnip': 'Turnip',
            'zucchini': 'Zucchini',
            'cucumber': 'Cucumber'
        }
        return names.get(item_name, item_name.capitalize())

    def update(self):
        self.input()
        self.draw_inventory()
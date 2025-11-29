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

        # sprite
        self.inventory_surf = sprite_list['inventory']

        # Создаем элементы инвентаря программно
        self.create_inventory_elements()

    def create_inventory_elements(self):
        # Создаем фон инвентаря - упрощенная версия без градиента
        self.bg_surf = pygame.Surface((450, 550), pygame.SRCALPHA)
        self.bg_surf_rect = pygame.Rect(0, 0, 450, 550)

        # Заливаем фон полупрозрачным темным цветом
        pygame.draw.rect(self.bg_surf, (40,40,40,200), self.bg_surf_rect, border_radius=12)

        # Рисуем рамку
        pygame.draw.rect(self.bg_surf, (205, 133, 63, 250), (2, 2, 446, 546), 2, border_radius=12)

    def draw_inventory(self):
        # Отображаем фон инвентаря
        bg_rect = self.bg_surf.get_rect(center=(SCREEN_WIDTH - self.inventory_surf.get_width() // 1.5, SCREEN_HEIGHT // 2 - 10))
        self.display_surface.blit(self.bg_surf, bg_rect)

        self.inventory_surf_rect = self.inventory_surf.get_rect(center=(SCREEN_WIDTH - self.inventory_surf.get_width() // 1.5, SCREEN_HEIGHT // 2))
        self.display_surface.blit(self.inventory_surf, self.inventory_surf_rect)

        # Заголовок инвентаря
        title_surf = self.font.render("Inventory", True, '#dcb98a')
        title_rect = title_surf.get_rect(midtop=(self.inventory_surf_rect.centerx, self.inventory_surf_rect.top - 35))
        self.display_surface.blit(title_surf, title_rect)

        # Отображаем предметы
        self.draw_items_section(bg_rect.left + 122, bg_rect.top + 132, self.player.item_inventory)

        # Отображаем семена
        self.draw_items_section(bg_rect.left + 122, bg_rect.top + 378, self.player.seed_inventory)

    def draw_items_section(self, start_x, start_y, inventory):

        items = list(inventory.items())

        # Рассчитываем максимальное количество строк для аккуратного отображения
        max_rows = 3
        items_per_row = 4

        for i, (item_name, count) in enumerate(items):
            if i >= max_rows * items_per_row:
                break

            row = i // items_per_row
            col = i % items_per_row

            x = start_x + col * 82
            y = start_y + row * 82

            # Отображаем количество
            count_surf = self.item_font.render(f"x{count}", True, (40,40,40))
            count_rect = count_surf.get_rect(center=(x, y + 12))
            self.display_surface.blit(count_surf, count_rect)

    def update(self):
        self.draw_inventory()
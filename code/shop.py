import pygame
from resourse import *
from settings import *
from timer import Timer


class Shop:
    def __init__(self, player, toggle_menu):
        # general setup
        self.player = player
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        self.font = font_list['font_55']
        self.count_font = font_list['font_40']

        # import
        self.inventory_surf = sprite_list['inventory_back']
        self.shop_surf = sprite_list['shop_back']
        self.select_surf = sprite_list['select']
        self.back_text_surf = sprite_list['back_text']

        # entries
        self.seed = list(self.player.seed_inventory.keys())
        self.inventory = list(self.player.item_inventory.keys())

        # movement
        self.index = 0
        self.timer = Timer(200)

        # sound
        self.buy_sell = sound_list['Bye or Sell']

    def display_money(self):
        text_surf = self.font.render(f'${self.player.money}', True, '#b68962')
        text_rect = text_surf.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))

        pygame.draw.rect(self.display_surface, '#dcb98a', text_rect.inflate(10, 10), 0, 4)
        self.display_surface.blit(text_surf, (text_rect[0], text_rect[1] + 5))

    def input(self):
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        # Сбрасываем отображение количества
        self.show_count = False

        # ----------------------------------ОБВОДКА И ПОКУПКА В МАГАЗИНЕ----------------------------------

        # Обработка магазина покупок
        self.handle_buy_shop(mouse_pos, keys)

        # Обработка магазина продаж
        self.handle_sell_shop(mouse_pos, keys)

    def draw_back(self):
        # background
        self.shop_rect = self.shop_surf.get_rect(midleft=(30, SCREEN_HEIGHT // 2 + 45))
        self.display_surface.blit(self.shop_surf, self.shop_rect)

        self.inventory_rect = self.inventory_surf.get_rect(midright=(SCREEN_WIDTH - 30, SCREEN_HEIGHT // 2 + 45))
        self.display_surface.blit(self.inventory_surf, self.inventory_rect)

        back_text_left_rect = self.back_text_surf.get_rect(topleft=(125, SCREEN_HEIGHT // 2 - self.inventory_rect.height // 1.8))
        self.display_surface.blit(self.back_text_surf, back_text_left_rect)

        back_text_right_rect = self.back_text_surf.get_rect(topright=(SCREEN_WIDTH - 125, SCREEN_HEIGHT // 2 - self.inventory_rect.height // 1.8))
        self.display_surface.blit(self.back_text_surf, back_text_right_rect)

        # text
        buy_surf = self.font.render("Buy", True, "#b68962")
        buy_rect = buy_surf.get_rect(topleft=(190, SCREEN_HEIGHT // 2 - self.inventory_rect.height // 1.8 + 10))
        self.display_surface.blit(buy_surf, buy_rect)

        sell_surf = self.font.render("Sell", True, "#b68962")
        sell_rect = sell_surf.get_rect(topright=(SCREEN_WIDTH - 190, SCREEN_HEIGHT // 2 - self.inventory_rect.height // 1.8 + 10))
        self.display_surface.blit(sell_surf, sell_rect)

    def display_item_count(self):
        if self.show_count:
            # Создаем текст с названием и количеством предмета
            if self.current_item_type == 'seed':
                count_text = f"{self.current_item_name}: {self.current_item_count}"
            else:
                count_text = f"{self.current_item_name}: {self.current_item_count}"

            # Создаем поверхность с текстом
            count_surf = self.count_font.render(count_text, True, '#b68962')

            # Позиция в правом нижнем углу
            if self.current_item_type == 'seed':
                count_rect = count_surf.get_rect(bottomleft=(40, SCREEN_HEIGHT - 30))
            else:
                count_rect = count_surf.get_rect(bottomright=(SCREEN_WIDTH - 40, SCREEN_HEIGHT - 30))

            # Создаем фон для текста
            bg_rect = count_rect.inflate(20, 10)
            pygame.draw.rect(self.display_surface, '#dcb98a', bg_rect, 0, 6)
            pygame.draw.rect(self.display_surface, '#b68962', bg_rect, 2, 6)

            # Отображаем текст
            self.display_surface.blit(count_surf, count_rect)

    def handle_buy_shop(self, mouse_pos, keys):
        """Обрабатывает магазин покупок"""
        if self.shop_rect.collidepoint(mouse_pos):
            i, j = self.get_cell_indices(mouse_pos, self.shop_rect)

            if i is not None and j is not None:
                self.draw_selection(i, j, self.shop_rect)
                self.handle_buy_selection(i, j)
                self.handle_buy_action(keys)
        else:
            self.index_shop = 'none'

    def handle_sell_shop(self, mouse_pos, keys):
        """Обрабатывает магазин продаж"""
        if self.inventory_rect.collidepoint(mouse_pos):
            i, j = self.get_cell_indices(mouse_pos, self.inventory_rect)

            if i is not None and j is not None:
                self.draw_selection(i, j, self.inventory_rect)
                self.handle_sell_selection(i, j)
                self.handle_sell_action(keys)
        else:
            self.index_inventory = 'none'

    # Общие вспомогательные методы
    def get_cell_indices(self, mouse_pos, rect):
        """Возвращает индексы ячейки по позиции мыши"""
        rel_x = mouse_pos[0] - rect.left - 30
        rel_y = mouse_pos[1] - rect.top - 30

        cell_size = 70 + 12  # размер ячейки + отступ
        i = rel_x // cell_size
        j = rel_y // cell_size

        return (i, j) if 0 <= i < 4 and 0 <= j < 5 else (None, None)

    def draw_selection(self, i, j, rect):
        """Отрисовывает выделение на ячейке"""
        cell_size = 70 + 12
        select_x = rect.left + i * cell_size + 30
        select_y = rect.top + j * cell_size + 30
        select_rect = self.select_surf.get_rect(topleft=(select_x, select_y))
        self.display_surface.blit(self.select_surf, select_rect)

    # Методы для покупок
    def handle_buy_selection(self, i, j):
        """Обрабатывает выбор в магазине покупок"""
        if j < 2:  # Только первые 2 строки для покупок
            self.index_shop = i + j * 4
            if self.index_shop < len(self.seed):
                self.set_item_display_data(self.seed[self.index_shop], self.player.seed_inventory, 'seed')
            else:
                self.index_shop = 'none'
        else:
            self.index_shop = 'none'

    def handle_buy_action(self, keys):
        """Обрабатывает действие покупки"""
        if (keys[pygame.K_SPACE] and self.index_shop != 'none' and not self.timer.active):

            item_name = self.seed[self.index_shop]
            price = PURCHASE_PRICES[item_name]

            if self.player.money >= price:
                self.player.money -= price
                self.player.seed_inventory[item_name] += 1
                self.buy_sell.play()
                self.timer.activate()

    # Методы для продаж
    def handle_sell_selection(self, i, j):
        """Обрабатывает выбор в магазине продаж"""
        if j < 2 or (j == 2 and i < 2):  # Первые 2 строки + 2 ячейки в 3-й строке
            self.index_inventory = i + j * 4
            if self.index_inventory < len(self.inventory):
                self.set_item_display_data(self.inventory[self.index_inventory], self.player.item_inventory, 'item')
            else:
                self.index_inventory = 'none'
        else:
            self.index_inventory = 'none'

    def handle_sell_action(self, keys):
        """Обрабатывает действие продажи"""
        if (keys[pygame.K_SPACE] and self.index_inventory != 'none' and not self.timer.active):

            item_name = self.inventory[self.index_inventory]

            if self.player.item_inventory[item_name] > 0:
                self.player.money += SALE_PRICES[item_name]
                self.player.item_inventory[item_name] -= 1
                self.buy_sell.play()
                self.timer.activate()

    # Общий метод для отображения данных
    def set_item_display_data(self, item_name, inventory_dict, item_type):
        """Устанавливает данные для отображения количества"""
        self.show_count = True
        self.current_item_name = item_name
        self.current_item_count = inventory_dict[item_name]
        self.current_item_type = item_type

    def update(self):
        self.draw_back()
        self.input()
        self.timer.update()
        self.display_money()
        self.display_item_count()
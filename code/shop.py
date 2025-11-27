import pygame
from settings import *
from timer import Timer


class Shop:
    def __init__(self, player, toggle_menu):
        # general setup
        self.player = player
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../font/Pixeltype.ttf', 55)
        self.count_font = pygame.font.Font('../font/Pixeltype.ttf', 40)

        # import
        self.inventory_surf = pygame.image.load(f'../graphics/overlay/inventory_back.png').convert_alpha()
        self.shop_surf = pygame.image.load(f'../graphics/overlay/shop_back.png').convert_alpha()
        self.select_surf = pygame.image.load(f'../graphics/overlay/select.png').convert_alpha()
        self.back_text_surf = pygame.image.load(f'../graphics/overlay/back_text.png').convert_alpha()

        # options
        self.width = 400
        self.space = 10
        self.padding = 8

        # entries
        self.seed = list(self.player.seed_inventory.keys())
        self.inventory = list(self.player.item_inventory.keys())

        # movement
        self.index = 0
        self.timer = Timer(200)

        # sound
        self.buy_sell = pygame.mixer.Sound('../audio/buy or sell.mp3')
        self.buy_sell.set_volume(SOUND_VOLUME['Bye or Sell'])

    def display_money(self):
        text_surf = self.font.render(f'${self.player.money}', True, '#b68962')
        text_rect = text_surf.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))

        pygame.draw.rect(self.display_surface, '#dcb98a', text_rect.inflate(10, 10), 0, 4)
        self.display_surface.blit(text_surf, (text_rect[0], text_rect[1] + 5))

    def input(self):
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        self.timer.update()

        # Сбрасываем отображение количества
        self.show_count = False

        if self.shop_rect.collidepoint(mouse_pos):
            for i in range(4):
                for j in range(5):
                    start_pos_x = 60
                    start_pos_y = 204
                    if start_pos_x + 70 * i + 12 * i <= mouse_pos[0] <= start_pos_x + 70 * (i + 1) + 12 * i and\
                            start_pos_y + 70 * j + 12 * j <= mouse_pos[1] <= start_pos_y + 70 * (j + 1) + 12 * j:

                        select_rect = self.select_surf.get_rect(topleft=(start_pos_x + 70 * i + 12 * i, start_pos_y + 70 * j + 12 * j))
                        self.display_surface.blit(self.select_surf, select_rect)

                        # index seed
                        if j < 2:
                            self.index_shop = i + j * 4
                            # Устанавливаем данные для отображения количества
                            if self.index_shop < len(self.seed):
                                self.show_count = True
                                self.current_item_name = self.seed[self.index_shop]
                                self.current_item_count = self.player.seed_inventory[self.current_item_name]
                                self.current_item_type = 'seed'
                        else:
                            self.index_shop = 'none'

                        # buy
                        if keys[pygame.K_SPACE] and self.index_shop != 'none' and not self.timer.active:
                            if  self.player.money > PURCHASE_PRICES[self.seed[self.index_shop]]:

                                self.player.money -= PURCHASE_PRICES[self.seed[self.index_shop]]
                                self.player.seed_inventory[self.seed[self.index_shop]] += 1
                                self.buy_sell.play()
                                self.timer.activate()
        else:
            self.index_shop = 'none'

        if self.inventory_rect.collidepoint(mouse_pos):
            for i in range(4):
                for j in range(5):
                    start_pos_x = SCREEN_WIDTH - 381
                    start_pos_y = 204
                    if start_pos_x + 70 * i + 12 * i <= mouse_pos[0] <= start_pos_x + 70 * (i + 1) + 12 * i and\
                            start_pos_y + 70 * j + 12 * j <= mouse_pos[1] <= start_pos_y + 70 * (j + 1) + 12 * j:

                        select_rect = self.select_surf.get_rect(topleft=(start_pos_x + 70 * i + 12 * i, start_pos_y + 70 * j + 12 * j))
                        self.display_surface.blit(self.select_surf, select_rect)

                        # index inventory
                        if j < 2:
                            self.index_inventory = i + j * 4
                            # Устанавливаем данные для отображения количества
                            if self.index_inventory < len(self.inventory):
                                self.show_count = True
                                self.current_item_name = self.inventory[self.index_inventory]
                                self.current_item_count = self.player.item_inventory[self.current_item_name]
                                self.current_item_type = 'item'
                        elif j == 2 and i < 2:
                            self.index_inventory = i + j * 4
                            # Устанавливаем данные для отображения количества
                            if self.index_inventory < len(self.inventory):
                                self.show_count = True
                                self.current_item_name = self.inventory[self.index_inventory]
                                self.current_item_count = self.player.item_inventory[self.current_item_name]
                                self.current_item_type = 'item'
                        else:
                            self.index_inventory = 'none'

                        # sell
                        if keys[pygame.K_SPACE] and self.index_inventory != 'none' and not self.timer.active:
                            if self.player.item_inventory[self.inventory[self.index_inventory]] > 0:

                                self.player.money += SALE_PRICES[self.inventory[self.index_inventory]]
                                self.player.item_inventory[self.inventory[self.index_inventory]] -= 1
                                self.buy_sell.play()
                                self.timer.activate()
        else:
            self.index_inventory = 'none'

        if keys[pygame.K_ESCAPE] and not self.timer.active:
            self.player.toggle_shop()
            self.timer.activate()

        if keys[pygame.K_BACKSPACE]:
            self.toggle_menu()

    def draw_back(self):
        # background
        self.shop_rect = self.shop_surf.get_rect(midleft=(30, SCREEN_HEIGHT // 2 + 45))
        self.display_surface.blit(self.shop_surf, self.shop_rect)

        self.inventory_rect = self.inventory_surf.get_rect(midright=(SCREEN_WIDTH - 30, SCREEN_HEIGHT // 2 + 45))
        self.display_surface.blit(self.inventory_surf, self.inventory_rect)

        back_text_left_rect = self.back_text_surf.get_rect(topleft=(125, 110))
        self.display_surface.blit(self.back_text_surf, back_text_left_rect)

        back_text_right_rect = self.back_text_surf.get_rect(topright=(SCREEN_WIDTH - 125, 110))
        self.display_surface.blit(self.back_text_surf, back_text_right_rect)

        # text
        buy_surf = self.font.render("Buy", True, "#b68962")
        buy_rect = buy_surf.get_rect(topleft=(190, 122))
        self.display_surface.blit(buy_surf, buy_rect)

        sell_surf = self.font.render("Sell", True, "#b68962")
        sell_rect = sell_surf.get_rect(topright=(SCREEN_WIDTH - 190, 122))
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
                count_rect = count_surf.get_rect(bottomleft=(20, SCREEN_HEIGHT - 30))
            else:
                count_rect = count_surf.get_rect(bottomright=(SCREEN_WIDTH - 20, SCREEN_HEIGHT - 30))

            # Создаем фон для текста
            bg_rect = count_rect.inflate(20, 10)
            pygame.draw.rect(self.display_surface, '#dcb98a', bg_rect, 0, 6)
            pygame.draw.rect(self.display_surface, '#b68962', bg_rect, 2, 6)

            # Отображаем текст
            self.display_surface.blit(count_surf, count_rect)
    def update(self):
        self.draw_back()
        self.input()
        self.display_money()
        self.display_item_count()

        self.buy_sell.set_volume(SOUND_VOLUME['Bye or Sell'])
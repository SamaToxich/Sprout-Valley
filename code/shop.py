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
        mouse = pygame.mouse.get_pressed()[0]
        mouse_pos = pygame.mouse.get_pos()
        self.timer.update()

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
                        elif j == 2 and i < 2:
                            self.index_inventory = i + j * 4
                        else:
                            self.index_inventory = 'none'

                        # sell
                        if keys[pygame.K_SPACE] and self.index_shop != 'none' and not self.timer.active:
                            if self.player.item_inventory[self.inventory[self.index_inventory]] > 0:
                                self.player.money += SALE_PRICES[self.inventory[self.index_inventory]]
                                self.player.item_inventory[self.inventory[self.index_inventory]] -= 1
                                self.buy_sell.play()
                                self.timer.activate()
        else:
            self.index_inventory = 'none'

        if keys[pygame.K_BACKSPACE]:
            self.player.toggle_shop()

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

    def update(self):
        self.draw_back()
        self.input()
        self.display_money()

        self.buy_sell.set_volume(SOUND_VOLUME['Bye or Sell'])

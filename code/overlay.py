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
            text_rect = text_surf.get_rect(topleft=(seed_rect.centerx+16, seed_rect.centery+16))

            self.display_surface.blit(seed_surf, seed_rect)
            self.display_surface.blit(text_surf, text_rect)

        # time
        self.clock = pygame.time.get_ticks() // 1000
        text_surf = self.font_time.render(f'{self.clock//60+6}: {"0" + str(self.clock % 60) if self.clock % 60 < 10 else self.clock - (self.clock//60*60)}', True, '#b68962')
        text_rect = text_surf.get_rect(topright=(SCREEN_WIDTH-30, 20))

        self.display_surface.blit(text_surf, text_rect)


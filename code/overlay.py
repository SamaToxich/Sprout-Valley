import pygame
from settings import *


class Overlay:
    def __init__(self, player):
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player

        # imports
        self.font = pygame.font.Font('../font/Pixeltype.ttf', 37)
        overlay_path = '../graphics/overlay/'
        self.tools_sufr = {tool: pygame.image.load(f'{overlay_path}{tool}.png').convert_alpha() for tool in
                           player.tools}
        self.seeds_sufr = {seed: pygame.image.load(f'{overlay_path}{seed}.png').convert_alpha() for seed in
                           player.seeds}
        self.slot_surf = pygame.image.load(f'{overlay_path}slot.png').convert_alpha()
        self.background_surf = pygame.image.load(f'{overlay_path}back.png').convert_alpha()
        self.hp_money_bar = pygame.image.load(f'{overlay_path}hp_money_bar.png').convert_alpha()
        self.select_slot = pygame.image.load(f'{overlay_path}select.png').convert_alpha()

    def selection_box(self, left, top):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def display(self):
        # tools
        tool_surf = self.tools_sufr[self.player.selected_tool]
        tool_rect = tool_surf.get_rect(center=OVERLAY_POSITIONS['tool'])

        self.display_surface.blit(tool_surf, tool_rect)

        # hp and money bar
        hp_money_bar_rect = self.hp_money_bar.get_rect(topleft=OVERLAY_POSITIONS['hp_money_bar'])
        self.display_surface.blit(self.hp_money_bar, hp_money_bar_rect)

        text_surf = self.font.render(f'{self.player.money}', False, '#b68962')
        text_rect = text_surf.get_rect(topleft=(48, 118))
        self.display_surface.blit(text_surf, (text_rect[0], text_rect[1] + 5))

        # background
        back_rect = self.slot_surf.get_rect(midbottom=OVERLAY_POSITIONS['background'])
        self.display_surface.blit(self.background_surf, back_rect)

        # slot
        for i in range(9):
            slot_rect = self.slot_surf.get_rect(center=OVERLAY_POSITIONS[f'slot{i + 1}'])
            self.display_surface.blit(self.slot_surf, slot_rect)

        # seeds
        for i in range(len(self.seeds_sufr)):
            seed_surf = list(self.seeds_sufr.values())[i]
            seed_rect = seed_surf.get_rect(center=OVERLAY_POSITIONS[self.player.seeds[i]])

            self.display_surface.blit(seed_surf, seed_rect)

        # select slot
        select_slot_rect = self.select_slot.get_rect(
            center=OVERLAY_POSITIONS[f'slot{self.player.seed_select_index + 1}'])
        self.display_surface.blit(self.select_slot, select_slot_rect)

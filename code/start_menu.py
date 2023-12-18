import sys
import pygame
from settings import *
from timer import Timer


class StartMenu:
    def __init__(self, player, menu):
        self.player = player
        self.menu = menu
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../font/Pixeltype.ttf', 60)

        # options
        self.width = 400
        self.space = 10
        self.padding = 8

        # movement
        self.index = 0
        self.timer = Timer(250)

        # entries
        self.all_options = ALL_OPTIONS
        self.current_option = 'options'
        self.setup(self.current_option)

        # sound
        self.switch = pygame.mixer.Sound('../audio/switch.mp3')
        self.switch.set_volume(0.05)

    def setup(self, option):
        # create text surfaces
        self.text_surfs = []
        self.total_height = 0
        for item in self.all_options[option]:
            text_surf = self.font.render(item, False, 'Black')
            self.text_surfs.append(text_surf)
            self.total_height += text_surf.get_height() + (self.padding * 2)

        self.total_height += (len(self.text_surfs) - 1) * self.space
        self.menu_top = SCREEN_HEIGHT // 2 - self.total_height // 2
        self.main_rect = pygame.Rect(SCREEN_WIDTH // 2 - self.width // 2, self.menu_top, self.width, self.total_height)

        # volume level
        if self.current_option == 'volume':
            current_item = self.all_options[self.current_option][self.index]
            if len(str(SOUND_VOLUME[current_item])) == 4:
                if str(SOUND_VOLUME[current_item])[0:2] == '1.':
                    volume_lev = str(SOUND_VOLUME[current_item])[0] + str(SOUND_VOLUME[current_item])[2]
                else:
                    volume_lev = (str(SOUND_VOLUME[current_item]))[-1]
            if len(str(SOUND_VOLUME[current_item])) == 1:
                if str(SOUND_VOLUME[current_item]) == '1':
                    volume_lev = str(SOUND_VOLUME[current_item]) + '0'
                else:
                    volume_lev = str(SOUND_VOLUME[current_item])
            if len(str(SOUND_VOLUME[current_item])) == 3:
                if str(SOUND_VOLUME[current_item])[0:2] == '1.':
                    volume_lev = str(SOUND_VOLUME[current_item])[0] + str(SOUND_VOLUME[current_item])[2]
                else:
                    volume_lev = (str(SOUND_VOLUME[current_item]))[-1]
            self.level_surf = self.font.render(volume_lev, False, 'Black')

    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if not self.timer.active:
            if keys[pygame.K_w]:
                self.index -= 1
                self.switch.play()
                self.timer.activate()

            if keys[pygame.K_s]:
                self.index += 1
                self.switch.play()
                self.timer.activate()

            if keys[pygame.K_RETURN]:
                self.timer.activate()
                self.switch.play()

                # get item
                current_item = self.all_options[self.current_option][self.index]

                # options
                if current_item == 'Play':
                    self.menu()
                    self.timer.activate()

                if current_item == 'Exit':
                    pygame.quit()
                    sys.exit()

                if current_item == 'Back':
                    if self.current_option == 'volume':
                        self.current_option = 'in_options'
                    else:
                        self.current_option = 'options'

                # In options
                if current_item == 'Options':
                    self.current_option = 'in_options'

                if current_item == 'Volume':
                    self.current_option = 'volume'

            if keys[pygame.K_a]:
                self.timer.activate()
                current_item = self.all_options[self.current_option][self.index]

                if self.current_option == 'volume':
                    self.switch.play()
                    if current_item == 'Tools':
                        SOUND_VOLUME['Tools'] -= 0.1
                        SOUND_VOLUME['Axe'] -= 0.1
                        SOUND_VOLUME['Water'] -= 0.1
                        SOUND_VOLUME['Hoe'] -= 0.1
                    else:
                        SOUND_VOLUME[current_item] -= 0.1

                    if len(str(SOUND_VOLUME[current_item])) > 4:
                        SOUND_VOLUME[current_item] = float(str(SOUND_VOLUME[current_item])[:4])
                        if str(SOUND_VOLUME[current_item])[-1] != '0' and str(SOUND_VOLUME[current_item])[-1] != '5':
                            SOUND_VOLUME[current_item] = round(float(str(SOUND_VOLUME[current_item])[:4]), 1)

                    if SOUND_VOLUME[current_item] <= 0:
                        if current_item == 'Tools':
                            SOUND_VOLUME['Tools'] = SOUND_VOLUME['Axe'] = SOUND_VOLUME['Water'] = SOUND_VOLUME[
                                'Hoe'] = 0
                        else:
                            SOUND_VOLUME[current_item] = 0

            if keys[pygame.K_d]:
                self.timer.activate()
                current_item = self.all_options[self.current_option][self.index]

                if self.current_option == 'volume':
                    self.switch.play()
                    if current_item == 'Tools':
                        if SOUND_VOLUME['Tools'] == 0:
                            SOUND_VOLUME['Tools'] += 0.1
                            SOUND_VOLUME['Axe'] += 0.3
                            SOUND_VOLUME['Water'] += 0.1
                            SOUND_VOLUME['Hoe'] += 0.4
                        else:
                            SOUND_VOLUME['Tools'] += 0.1
                            SOUND_VOLUME['Axe'] += 0.1
                            SOUND_VOLUME['Water'] += 0.1
                            SOUND_VOLUME['Hoe'] += 0.1
                    else:
                        SOUND_VOLUME[current_item] += 0.1

                    if len(str(SOUND_VOLUME[current_item])) > 4:
                        SOUND_VOLUME[current_item] = float(str(SOUND_VOLUME[current_item])[:4])
                        if str(SOUND_VOLUME[current_item])[-1] != '0' and str(SOUND_VOLUME[current_item])[-1] != '5':
                            SOUND_VOLUME[current_item] = round(float(str(SOUND_VOLUME[current_item])[:4]), 1)

                    if SOUND_VOLUME[current_item] >= 1:
                        if current_item == 'Tools':
                            SOUND_VOLUME['Tools'] = SOUND_VOLUME['Water'] = 1
                            SOUND_VOLUME['Axe'] = 1.2
                            SOUND_VOLUME['Hoe'] = 1.3
                        else:
                            SOUND_VOLUME[current_item] = 1

            if keys[pygame.K_ESCAPE]:
                if self.current_option != 'options':
                    if self.current_option == 'volume' or self.current_option == 'hotkeys':
                        self.current_option = 'in_options'
                        self.timer.activate()
                    else:
                        self.current_option = 'options'
                        self.timer.activate()

        # clamp the values
        if self.index < 0:
            self.index = len(self.text_surfs) - 1
        if self.index > len(self.text_surfs) - 1:
            self.index = 0

    def show_entry(self, text_surf, top, selected):
        # background
        bg_rect = pygame.Rect(self.main_rect.left, top, self.width, text_surf.get_height() + (self.padding * 2))
        pygame.draw.rect(self.display_surface, 'White', bg_rect, 0, 4)

        # text
        text_rect = text_surf.get_rect(center=(self.main_rect.centerx, bg_rect.centery + 5))
        self.display_surface.blit(text_surf, text_rect)

        # selected
        if selected:
            pygame.draw.rect(self.display_surface, 'black', bg_rect, 4, 4)

    def show_entry_volume(self, text_surf, top, selected):
        # background
        bg_rect = pygame.Rect(self.main_rect.left, top, self.width, text_surf.get_height() + (self.padding * 2))
        pygame.draw.rect(self.display_surface, 'White', bg_rect, 0, 4)

        # text
        text_rect = text_surf.get_rect(midleft=(self.main_rect.left + 20, bg_rect.centery + 5))
        self.display_surface.blit(text_surf, text_rect)

        # selected
        if selected:
            pygame.draw.rect(self.display_surface, 'black', bg_rect, 4, 4)

            level_rect = self.level_surf.get_rect(midright=(self.main_rect.right - 20, bg_rect.centery + 5))
            self.display_surface.blit(self.level_surf, level_rect)

    def update(self):
        self.input()
        self.setup(self.current_option)

        if self.current_option == 'volume':
            for text_index, text_surf in enumerate(self.text_surfs):
                top = self.main_rect.top + text_index * (text_surf.get_height() + (self.padding * 2) + self.space)

                self.show_entry_volume(text_surf, top, self.index == text_index)

        else:
            for text_index, text_surf in enumerate(self.text_surfs):
                top = self.main_rect.top + text_index * (text_surf.get_height() + (self.padding * 2) + self.space)

                self.show_entry(text_surf, top, self.index == text_index)

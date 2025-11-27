import sys
import pygame
from settings import *
from timer import Timer
from resourse import *


class EscMenu:
    def __init__(self, player, toggle):
        self.player = player
        self.toggle_esc_menu = toggle
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../font/Pixeltype.ttf', 80)

        # sprites
        self.sound_on_surf = sprite_list['sound_on']
        self.sound_off_surf = sprite_list['sound_off']
        self.slot_surf = sprite_list['slot_menu']
        self.select_slot_surf = sprite_list['select_slot_menu']
        self.background_setting_surf = sprite_list['setting']

        self.background_setting_rect = self.background_setting_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.select_setting_surf = [self.background_setting_surf, self.background_setting_rect]

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

        # sound
        self.switch = sound_list['Choice']


    def draw_menu(self, option):
        # count slot
        cnt = len(self.all_options[option])

        try:
            current_item = self.all_options[option][self.index]
        except IndexError:
            self.index = 0
            current_item = self.all_options[option][self.index]

        for i in range(cnt):
            # draw slots
            slot_rect = self.slot_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.3 + (i * 130)))
            self.display_surface.blit(self.slot_surf, slot_rect)

            # draw text
            if option == 'volume':
                text_surf = self.font.render(f'{self.all_options[option][i]}', True, '#b68962')
                text_rect = text_surf.get_rect(topleft=(SCREEN_WIDTH // 2 - 197, SCREEN_HEIGHT // 2.43 + (i * 130)))
                self.display_surface.blit(text_surf, (text_rect[0], text_rect[1] + 4))
            else:
                text_surf = self.font.render(f'{self.all_options[option][i]}', True, '#b68962')
                text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.3 + (i * 130)))
                self.display_surface.blit(text_surf, (text_rect[0], text_rect[1] + 4))

        # draw selection
        select_slot_rect = self.select_slot_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.3 + (self.all_options[option].index(current_item) * 130)))
        self.display_surface.blit(self.select_slot_surf, select_slot_rect)

        if option == 'volume':

            count_on = int(SOUND_VOLUME[current_item] * 10)
            count_off = 10

            for i in range(count_off):
                sound_off_rect = self.sound_off_surf.get_rect(center=(SCREEN_WIDTH // 2 + 38 + (i * 17), SCREEN_HEIGHT // 2.32 + (self.index * 130)))
                self.display_surface.blit(self.sound_off_surf, sound_off_rect)

            for i in range(count_on):
                sound_on_rect = self.sound_on_surf.get_rect(center=(SCREEN_WIDTH // 2 + 38 + (i * 17), SCREEN_HEIGHT // 2.32 + (self.index * 130)))
                self.display_surface.blit(self.sound_on_surf, sound_on_rect)

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
                    self.toggle_esc_menu()
                    self.timer.activate()

                if current_item == 'Exit':
                    pygame.quit()
                    sys.exit()

                # In options
                if current_item == 'Options':
                    self.current_option = 'in_options'
                    self.select_setting_surf = [self.background_setting_surf, self.background_setting_rect]

                if current_item == 'Volume':
                    self.current_option = 'volume'

            if keys[pygame.K_a]:
                self.timer.activate()
                current_item = self.all_options[self.current_option][self.index]

                if self.current_option == 'volume':
                    self.switch.play()
                    if current_item == 'Tools':
                        SOUND_VOLUME['Tools'] -= 0.1
                        SOUND_VOLUME['Wave'] -= 0.1
                        SOUND_VOLUME['Axe'] -= 0.1
                        SOUND_VOLUME['Water'] -= 0.1
                        SOUND_VOLUME['Hoe'] -= 0.1
                        SOUND_VOLUME['Plant'] -= 0.1

                    elif current_item == 'Affects':
                        SOUND_VOLUME['Affects'] -= 0.1
                        SOUND_VOLUME['Choice'] -= 0.03
                        SOUND_VOLUME['Switch tool'] -= 0.1
                        SOUND_VOLUME['Bye or Sell'] -= 0.1
                        SOUND_VOLUME['Success'] -= 0.1
                    else:
                        SOUND_VOLUME[current_item] -= 0.1

                    if len(str(SOUND_VOLUME[current_item])) > 4:
                        SOUND_VOLUME[current_item] = float(str(SOUND_VOLUME[current_item])[:4])
                        if str(SOUND_VOLUME[current_item])[-1] != '0' and str(SOUND_VOLUME[current_item])[-1] != '5':
                            SOUND_VOLUME[current_item] = round(float(str(SOUND_VOLUME[current_item])[:4]), 1)

                    if SOUND_VOLUME[current_item] <= 0:
                        if current_item == 'Tools':
                            SOUND_VOLUME['Tools'] = SOUND_VOLUME['Axe'] = SOUND_VOLUME['Water'] = SOUND_VOLUME['Hoe'] = SOUND_VOLUME['Plant'] = SOUND_VOLUME['Wave'] = 0.0

                        elif current_item == 'Affects':
                            SOUND_VOLUME['Affects'] = SOUND_VOLUME['Choice'] = SOUND_VOLUME['Success'] = SOUND_VOLUME['Switch tool'] = SOUND_VOLUME['Bye or Sell'] = 0.0
                        else:
                            SOUND_VOLUME[current_item] = 0.0

                all_sound_volume(SOUND_VOLUME)

            if keys[pygame.K_d]:
                self.timer.activate()
                current_item = self.all_options[self.current_option][self.index]

                if self.current_option == 'volume':
                    self.switch.play()
                    if current_item == 'Tools':
                        if SOUND_VOLUME['Tools'] == 0.0:
                            SOUND_VOLUME['Tools'] += 0.1
                            SOUND_VOLUME['Wave'] += 0.1
                            SOUND_VOLUME['Axe'] += 0.3
                            SOUND_VOLUME['Water'] += 0.1
                            SOUND_VOLUME['Hoe'] += 0.4
                            SOUND_VOLUME['Plant'] += 0.5
                        else:
                            SOUND_VOLUME['Tools'] += 0.1
                            SOUND_VOLUME['Wave'] += 0.1
                            SOUND_VOLUME['Axe'] += 0.1
                            SOUND_VOLUME['Water'] += 0.1
                            SOUND_VOLUME['Hoe'] += 0.1
                            SOUND_VOLUME['Plant'] += 0.1

                    elif current_item == 'Affects':
                        if SOUND_VOLUME['Affects'] == 0.0:
                            SOUND_VOLUME['Affects'] += 0.1
                            SOUND_VOLUME['Choice'] += 0.03
                            SOUND_VOLUME['Success'] += 0.1
                            SOUND_VOLUME['Switch tool'] += 0.2
                            SOUND_VOLUME['Bye or Sell'] += 0.1
                        else:
                            SOUND_VOLUME['Affects'] += 0.1
                            SOUND_VOLUME['Choice'] += 0.03
                            SOUND_VOLUME['Success'] += 0.1
                            SOUND_VOLUME['Switch tool'] += 0.1
                            SOUND_VOLUME['Bye or Sell'] += 0.1

                    else:
                        SOUND_VOLUME[current_item] += 0.1

                    if len(str(SOUND_VOLUME[current_item])) > 4:
                        SOUND_VOLUME[current_item] = float(str(SOUND_VOLUME[current_item])[:4])
                        if str(SOUND_VOLUME[current_item])[-1] != '0' and str(SOUND_VOLUME[current_item])[-1] != '5':
                            SOUND_VOLUME[current_item] = round(float(str(SOUND_VOLUME[current_item])[:4]), 1)

                    if SOUND_VOLUME[current_item] >= 1:
                        if current_item == 'Tools':
                            SOUND_VOLUME['Tools'] = SOUND_VOLUME['Water'] = SOUND_VOLUME['Wave'] = 1
                            SOUND_VOLUME['Axe'] = 1.2
                            SOUND_VOLUME['Hoe'] = 1.3
                            SOUND_VOLUME['Plant'] = 1.5
                        elif current_item == 'Affects':
                            SOUND_VOLUME['Affects'] = SOUND_VOLUME['Success'] = SOUND_VOLUME['Bye or Sell'] = SOUND_VOLUME['Switch tool'] = 1
                            SOUND_VOLUME['Choice'] = 0.33
                        else:
                            SOUND_VOLUME[current_item] = 1

                all_sound_volume(SOUND_VOLUME)

            if keys[pygame.K_ESCAPE]:
                if self.current_option != 'options':
                    if self.current_option == 'volume' or self.current_option == 'hotkeys':
                        self.current_option = 'in_options'
                        self.timer.activate()
                    else:
                        self.current_option = 'options'
                        self.timer.activate()

    def update(self):
        self.display_surface.blit(self.select_setting_surf[0], self.select_setting_surf[1])
        self.input()
        self.draw_menu(self.current_option)
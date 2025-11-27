import os
import pygame
import hashlib
from settings import *
from timer import Timer
from resourse import *


class StartMenu:
    def __init__(self, toggle):
        self.toggle = toggle

        self.accounts = {}
        self.authorization_status = ''
        self.authorization = False

        # display
        self.display_surface = pygame.display.get_surface()

        # timer
        self.timer_back = Timer(150)
        self.timer_down = Timer(150)

        # font
        self.font = font_list['font_50']
        self.font_enter = font_list['font_40']
        self.font_error = font_list['font_30']
        self.font_text = font_list['font_75']
        self.font_name = font_list['font_110']

        # imports
        self.slot_surf = sprite_list['slot_surf']
        self.select_slot_surf = sprite_list['select_slot']
        self.enter_slot_surf = sprite_list['enter_slot']
        self.select_enter_slot_surf = sprite_list['select_enter_slot']
        self.background_down_surf = sprite_list['background_down']
        self.background_up_surf = sprite_list['background_up']
        self.play_key_surf = sprite_list['play_key']
        self.select_play_key_surf = sprite_list['select_play_key']

        # login and password
        self.login_active = False
        self.password_active = False

        self.index = 0
        self.login_text = ''
        self.password_text = ''
        self.password_text_copy = ''

        # sound
        self.switch = sound_list['Choice']

        # keys
        self.keys = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',
                     'z', 'x', 'c', 'v', 'b', 'n', 'm', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'BACKSPACE']

    def draw_screen(self):
        if not self.authorization:
            # draw background
            background_down_rect = self.background_down_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.display_surface.blit(self.background_down_surf, background_down_rect)

            background_up_rect = self.background_up_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.display_surface.blit(self.background_up_surf, background_up_rect)

            # game name
            name_surf = self.font_name.render("Cat's Farm", True, "White")
            login_rect = name_surf.get_rect(midtop=(SCREEN_WIDTH // 2, 100))
            self.display_surface.blit(name_surf, (login_rect[0] + 4, login_rect[1] + 12))

            # login slot
            self.login_surf = self.slot_surf
            self.login_rect = self.login_surf.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10))
            self.display_surface.blit(self.login_surf, self.login_rect)

            # password slot
            self.password_surf = self.slot_surf
            self.password_rect = self.password_surf.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
            self.display_surface.blit(self.password_surf, self.password_rect)

            # select
            if self.login_active or self.password_active:
                select_surf = self.select_slot_surf
                select_rect = self.login_surf.get_rect(midbottom=(SCREEN_WIDTH // 2 - 3, SCREEN_HEIGHT // 2 - 13 + (self.index * 160)))
                self.display_surface.blit(select_surf, select_rect)

            # text name
            login_surf = self.font_text.render('Login', True, 'White')
            login_rect = login_surf.get_rect(midtop=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 155))
            self.display_surface.blit(login_surf, (login_rect[0], login_rect[1] + 5))

            password_surf = self.font_text.render('Password', True, 'White')
            password_rect = password_surf.get_rect(midtop=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 5))
            self.display_surface.blit(password_surf, (password_rect[0], password_rect[1] + 5))

            # login and password text input
            login_text_surf = self.font.render(self.login_text, True, 'black')
            login_text_rect = login_text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
            self.display_surface.blit(login_text_surf, (login_text_rect[0], login_text_rect[1] + 9))

            password_text_surf = self.font.render(self.password_text, True, 'black')
            password_text_rect = password_text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            self.display_surface.blit(password_text_surf, (password_text_rect[0], password_text_rect[1] + 9))

            # authorization and registration
            self.entry_surf = self.enter_slot_surf
            self.entry_rect = self.entry_surf.get_rect(center=(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 117))
            self.display_surface.blit(self.entry_surf, self.entry_rect)

            authorization_text_surf = self.font_enter.render('Enter', True, '#b68962')
            authorization_text_rect = authorization_text_surf.get_rect(center=(SCREEN_WIDTH // 2 - 95, SCREEN_HEIGHT - 125))
            self.display_surface.blit(authorization_text_surf, (authorization_text_rect[0], authorization_text_rect[1] + 9))

            self.registration_surf = self.enter_slot_surf
            self.registration_rect = self.registration_surf.get_rect(center=(SCREEN_WIDTH // 2 + 105, SCREEN_HEIGHT -117))
            self.display_surface.blit(self.registration_surf, self.registration_rect)

            registration_text_surf = self.font_enter.render('Registration', True, '#b68962')
            registration_text_rect = registration_text_surf.get_rect(center=(SCREEN_WIDTH // 2 + 108, SCREEN_HEIGHT - 125))
            self.display_surface.blit(registration_text_surf, (registration_text_rect[0], registration_text_rect[1] + 9))

            # authorization error
            if self.authorization_status != '':
                if self.authorization_status == 'invalid':
                    error_text_surf = self.font_error.render('Invalid username or password', True, '#f24646')

                elif self.authorization_status == 'none':
                    error_text_surf = self.font_error.render('There is no such account', True, '#f24646')

                elif self.authorization_status == 'true':
                    error_text_surf = self.font_error.render('Successfully registered!', True, '#d2e077')

                elif self.authorization_status == 'empty':
                    error_text_surf = self.font_error.render('Fill in the empty fields', True, '#f24646')

                elif self.authorization_status == 'exists':
                    error_text_surf = self.font_error.render('An account with this username already exists', True,'#f24646')

                error_text_rect = error_text_surf.get_rect(center=(SCREEN_WIDTH // 2 + 3, SCREEN_HEIGHT - 175))
                self.display_surface.blit(error_text_surf, error_text_rect)

        elif self.authorization:
            # background
            background_down_rect = self.background_down_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.display_surface.blit(self.background_down_surf, background_down_rect)

            # play key
            self.play_key_rect = self.play_key_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 350))
            self.display_surface.blit(self.play_key_surf, self.play_key_rect)

    def input(self):
        self.timer_back.update()
        self.timer_down.update()
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()[0]
        mouse_pos = pygame.mouse.get_pos()

        if not self.authorization:
            if self.entry_rect.collidepoint(mouse_pos):
                select_enter_slot_rect = self.select_enter_slot_surf.get_rect(center=(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 117))
                self.display_surface.blit(self.select_enter_slot_surf, select_enter_slot_rect)
            elif self.registration_rect.collidepoint(mouse_pos):
                select_enter_slot_rect = self.select_enter_slot_surf.get_rect(center=(SCREEN_WIDTH // 2 + 105, SCREEN_HEIGHT - 117))
                self.display_surface.blit(self.select_enter_slot_surf, select_enter_slot_rect)
        else:
            if self.play_key_rect.collidepoint(mouse_pos):
                select_play_rect = self.select_play_key_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 350))
                self.display_surface.blit(self.select_play_key_surf, select_play_rect)

        # mouse click
        if not self.timer_down.active and not self.timer_back.active:
            if mouse:
                if self.login_rect.collidepoint(mouse_pos):
                    self.login_active = True
                    self.password_active = False

                    self.index = 0

                elif self.password_rect.collidepoint(mouse_pos):
                    self.login_active = False
                    self.password_active = True

                    self.index = 1

                if self.authorization:
                    if self.play_key_rect.collidepoint(mouse_pos):
                        self.toggle()

                if self.entry_rect.collidepoint(mouse_pos):
                    status = self.check_account()
                    if status == 'entry':
                        self.authorization = True
                    if status == 'empty':
                        self.authorization_status = 'empty'
                    if status == 'invalid':
                        self.authorization_status = 'invalid'
                    if status == 'none':
                        self.authorization_status = 'none'
                    self.timer_back.activate()

                elif self.registration_rect.collidepoint(mouse_pos):
                    status = self.registrate()
                    if status == 'true':
                        self.authorization_status = 'true'
                    if status == 'empty':
                        self.authorization_status = 'empty'
                    if status == 'exists':
                        self.authorization_status = 'exists'
                    self.timer_back.activate()

        # keys down
        if any(keys):
            if not self.timer_down.active and not self.timer_back.active:
                for i in self.keys:
                    key_backspace = pygame.key.key_code('BACKSPACE')
                    key_name = pygame.key.key_code(i)

                    if self.login_active:

                        if keys[key_backspace]:
                            self.login_text = self.login_text[:-1]
                            self.timer_back.activate()
                            break
                        elif keys[key_name]:
                            if len(self.login_text) < 14:
                                self.timer_down.activate()
                                self.login_text += i
                                break

                    if self.password_active:

                        if keys[key_backspace]:
                            self.password_text = self.password_text[:-1]
                            self.password_text_copy = self.password_text_copy[:-1]
                            self.timer_back.activate()
                            break
                        elif keys[key_name]:
                            if len(self.password_text) < 14:
                                self.timer_down.activate()
                                self.password_text_copy += i
                                self.password_text += '#'
                                break

    def check_account(self):
        if len(self.login_text) == 0 or len(self.password_text_copy) == 0:
            return 'empty'
        else:
            password_code = hashlib.sha256(self.password_text_copy.encode()).hexdigest()
            file = open('../save/accounts.txt', 'r+')
            a = file.readline()[:-1].split(' ')

            while True:
                if a != ['']:
                    self.accounts[a[0]] = a[1]
                    a = file.readline()[:-1].split(' ')
                else:
                    break

            true_account = False
            account_exists = False
            for i in self.accounts.items():
                login, password = i
                if self.login_text == login and password_code == password:
                    true_account = True
                    break
                if self.login_text == login and password_code != password:
                    account_exists = True
                    break

            if true_account:
                return 'entry'
            elif account_exists:
                return 'invalid'
            elif not true_account and not account_exists:
                return 'none'

    def registrate(self):
        if len(self.login_text) == 0 or len(self.password_text_copy) == 0:
            return 'empty'
        else:
            password_code = hashlib.sha256(self.password_text_copy.encode()).hexdigest()
            file = open('../save/accounts.txt', 'r+')
            a = file.readline()[:-1].split(' ')

            while True:
                if a != ['']:
                    self.accounts[a[0]] = a[1]
                    a = file.readline()[:-1].split(' ')
                else:
                    break

            account_exists = False

            for i in self.accounts.items():
                login, password = i
                if self.login_text == login:
                    account_exists = True
                    print('true')

            if not account_exists:
                file = open('../save/accounts.txt', 'r+')
                file.seek(0, os.SEEK_END)
                file.write(f'{self.login_text} {password_code}\n')
                file.close()
                return 'true'
            else:
                return 'exists'

    def update(self):
        self.draw_screen()
        self.input()
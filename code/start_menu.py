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

        # sprites and rects
        self.entry_surf = self.enter_slot_surf
        self.entry_rect = self.entry_surf.get_rect(center=(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 317))

        self.registration_surf = self.enter_slot_surf
        self.registration_rect = self.registration_surf.get_rect(center=(SCREEN_WIDTH // 2 + 105, SCREEN_HEIGHT - 317))

        self.login_surf = self.slot_surf
        self.login_rect = self.login_surf.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10))

        self.password_surf = self.slot_surf
        self.password_rect = self.password_surf.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))

        # login and password status
        self.login_active = False
        self.password_active = False

        # authorization and registration and play status
        self.authorization_key_status = False
        self.registration_key_status = False
        self.play_key_status = False

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
            # -------------------------------------ВЕСЬ ЗАДНИК-------------------------------------

            # draw background
            background_down_rect = self.background_down_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.display_surface.blit(self.background_down_surf, background_down_rect)

            background_up_rect = self.background_up_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.display_surface.blit(self.background_up_surf, background_up_rect)

            # -------------------------------------НАЗВАНИЕ ИГРЫ-------------------------------------

            # game name
            name_surf = self.font_name.render("Cat's Farm", True, "White")
            login_rect = name_surf.get_rect(midtop=(SCREEN_WIDTH // 2, 280))
            self.display_surface.blit(name_surf, (login_rect[0] + 4, login_rect[1] + 12))

            # -------------------------------------ПОЛЯ ПОД ЛОГИН И ПАРОЛЬ-------------------------------------

            # login slot
            self.display_surface.blit(self.login_surf, self.login_rect)

            # password slot
            self.display_surface.blit(self.password_surf, self.password_rect)

            # -------------------------------------ОБВОДКА ПОЛЕЙ ЛОГИНА И ПАРОЛЯ-------------------------------------

            # select
            if self.login_active or self.password_active:
                select_surf = self.select_slot_surf
                select_rect = self.login_surf.get_rect(midbottom=(SCREEN_WIDTH // 2 - 3, SCREEN_HEIGHT // 2 - 13 + (self.index * 160)))
                self.display_surface.blit(select_surf, select_rect)

            # -------------------------------------НАДПИСИ ЛОГИН И ПАРОЛЬ-------------------------------------

            text_login_surf = self.font_text.render('Login', True, 'White')
            text_login_rect = text_login_surf.get_rect(midtop=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 155))
            self.display_surface.blit(text_login_surf, (text_login_rect[0], text_login_rect[1] + 5))

            text_password_surf = self.font_text.render('Password', True, 'White')
            text_password_rect = text_password_surf.get_rect(midtop=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 5))
            self.display_surface.blit(text_password_surf, (text_password_rect[0], text_password_rect[1] + 5))

            # -------------------------------------ВВОДИМЫЙ ТЕКСТ-------------------------------------

            # login and password text input
            login_input_text_surf = self.font.render(self.login_text, True, 'black')
            login_input_text_rect = login_input_text_surf.get_rect(midbottom=(self.login_rect.x + 150, self.login_rect.y + 60))
            self.display_surface.blit(login_input_text_surf, login_input_text_rect)

            password_input_text_surf = self.font.render(self.password_text, True, 'black')
            password_input_text_rect = password_input_text_surf.get_rect(midbottom=(self.password_rect.x + 151, self.password_rect.y + 60))
            self.display_surface.blit(password_input_text_surf, password_input_text_rect)

            # -------------------------------------КНОПКИ АВТОРИЗАЦИИ И РЕГИСТРАЦИИ-------------------------------------

            # authorization
            self.display_surface.blit(self.entry_surf, self.entry_rect)

            authorization_text_surf = self.font_enter.render('Enter', True, '#b68962')
            authorization_text_rect = authorization_text_surf.get_rect(center=(SCREEN_WIDTH // 2 - 95, SCREEN_HEIGHT - 316))
            self.display_surface.blit(authorization_text_surf, authorization_text_rect)


            # registration
            self.display_surface.blit(self.registration_surf, self.registration_rect)

            registration_text_surf = self.font_enter.render('Registration', True, '#b68962')
            registration_text_rect = registration_text_surf.get_rect(center=(SCREEN_WIDTH // 2 + 108, SCREEN_HEIGHT - 316))
            self.display_surface.blit(registration_text_surf, registration_text_rect)

            # -------------------------------------ОБВОДКА КНОПОК АВТОРИЗАЦИИ И РЕГИСТРАЦИИ-------------------------------------
            if self.authorization_key_status:
                select_enter_slot_rect = self.select_enter_slot_surf.get_rect(center=(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 317))
                self.display_surface.blit(self.select_enter_slot_surf, select_enter_slot_rect)
            if self.registration_key_status:
                select_enter_slot_rect = self.select_enter_slot_surf.get_rect(center=(SCREEN_WIDTH // 2 + 105, SCREEN_HEIGHT - 317))
                self.display_surface.blit(self.select_enter_slot_surf, select_enter_slot_rect)

            # -------------------------------------ТЕКСТ ОШИБКИ-------------------------------------

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

                error_text_rect = error_text_surf.get_rect(center=(SCREEN_WIDTH // 2 + 3, SCREEN_HEIGHT - 375))
                self.display_surface.blit(error_text_surf, error_text_rect)

            # -------------------------------------ОКНО ВХОДА-------------------------------------

        elif self.authorization:
            # background
            background_down_rect = self.background_down_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.display_surface.blit(self.background_down_surf, background_down_rect)

            # play key
            self.play_key_rect = self.play_key_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.display_surface.blit(self.play_key_surf, self.play_key_rect)

            # Обводка кнопки
            if self.play_key_status:
                select_play_rect = self.select_play_key_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.display_surface.blit(self.select_play_key_surf, select_play_rect)

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

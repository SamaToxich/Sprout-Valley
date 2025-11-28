from timer import Timer
from settings import *
from resourse import *
import sys

class Input:
    def __init__(self, Level):
        self.level = Level
        self.start_menu = self.level.start_menu
        self.esc_menu = self.level.esc_menu
        self.player = self.level.player

        self.display_surface = pygame.display.get_surface()

        self.timers = {
            'input_timer_100': Timer(100),
            'input_timer_150': Timer(150),
            'input_timer_200': Timer(200),
            'input_timer_250': Timer(250),
            'input_timer_350': Timer(350),
            'use_seed_timer_250': Timer(250,self.player.use_seed),
            'use_tool_timer_700': Timer(700, self.player.use_tool),
        }

        self.keys_pygame = {
            'W':            pygame.K_w,
            'S':            pygame.K_s,
            'A':            pygame.K_a,
            'D':            pygame.K_d,
            'F':            pygame.K_f,
            'Q':            pygame.K_q,
            'E':            pygame.K_e,
            'R':            pygame.K_r,
            'T':            pygame.K_t,
            'Y':            pygame.K_y,
            'U':            pygame.K_u,
            'I':            pygame.K_i,
            'O':            pygame.K_o,
            'P':            pygame.K_p,
            'L':            pygame.K_l,
            'K':            pygame.K_k,
            'J':            pygame.K_j,
            'H':            pygame.K_h,
            'G':            pygame.K_g,
            'Z':            pygame.K_z,
            'X':            pygame.K_x,
            'C':            pygame.K_c,
            'V':            pygame.K_v,
            'B':            pygame.K_b,
            'N':            pygame.K_n,
            'M':            pygame.K_m,
            '1':            pygame.K_1,
            '2':            pygame.K_2,
            '3':            pygame.K_3,
            '4':            pygame.K_4,
            '5':            pygame.K_5,
            '6':            pygame.K_6,
            '7':            pygame.K_7,
            '8':            pygame.K_8,
            'LSHIFT':       pygame.K_LSHIFT,
            'SPACE':        pygame.K_SPACE,
            'RETURN':       pygame.K_RETURN,
            'ESCAPE':       pygame.K_ESCAPE,
            'BACKSPACE':    pygame.K_BACKSPACE,
            'TAB':          pygame.K_TAB,
            'UP':           pygame.K_UP,
            'DOWN':         pygame.K_DOWN,
            'LEFT':         pygame.K_LEFT,
            'RIGHT':        pygame.K_RIGHT,
            'LCTRL':        pygame.K_LCTRL
        }

        # Флаги для отслеживания состояний клавиш
        self.key_states = {}
        for key_name in self.keys_pygame.keys():
            self.key_states[key_name] = {'pressed': False, 'just_pressed': False}

        self.menus_active = {
            'esc_menu':         self.level.esc_menu_active,
            'inventory_menu':   self.level.inventory_active,
            'shop_menu':        self.level.shop_active,
            'start_menu':       self.level.start_menu_active,
        }

    def handle_events(self):
        """Обрабатывает события (одиночные нажатия)"""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # Находим название клавиши по значению pygame и Обновляем состояние для одиночных нажатий
                for key_name, pygame_key in self.keys_pygame.items():
                    if event.key == pygame_key:
                        self.key_states[key_name]['just_pressed'] = True
                        self.key_states[key_name]['pressed'] = True
                        break

            elif event.type == pygame.KEYUP:
                for key_name, pygame_key in self.keys_pygame.items():
                    if event.key == pygame_key:
                        self.key_states[key_name]['pressed'] = False
                        break

    def get_input(self):
        KEYS = pygame.key.get_pressed()

        # Обновляем состояния непрерывных нажатий
        for key_name, pygame_key in self.keys_pygame.items():
            self.key_states[key_name]['pressed'] = KEYS[pygame_key]

        # ---------------------------------------ПОКА МЕНЮ НЕ АКТИВНЫ---------------------------------------

        # Проверка, что все меню не активны
        if self.check_menus_active_without_target('inventory_menu'):

            # ---------------------------------------ПЕРЕДВИЖЕНИЕ---------------------------------------

            if not self.timers['use_tool_timer_700'].active:
                # Идти вверх
                if KEYS[ self.keys_pygame[ keys_value_list['up'] ] ]:
                    self.player.status = 'up'
                    self.player.direction.y = -1
                # Идти вниз
                elif KEYS[ self.keys_pygame[ keys_value_list['down'] ] ]:
                    self.player.status = 'down'
                    self.player.direction.y = 1
                # Бездействие
                else:
                    self.player.direction.y = 0

                # Идти вправо
                if KEYS[ self.keys_pygame[ keys_value_list['right'] ] ]:
                    self.player.status = 'right'
                    self.player.direction.x = 1
                # Идти влево
                elif KEYS[ self.keys_pygame[ keys_value_list['left'] ] ]:
                    self.player.status = 'left'
                    self.player.direction.x = -1
                # Бездействие
                else:
                    self.player.direction.x = 0

                # Бег
                if KEYS[ self.keys_pygame[ keys_value_list['run'] ] ]:
                    self.player.speed = 300
                    if KEYS[ self.keys_pygame[ keys_value_list['right'] ] ]:
                        self.player.status = 'right_run'
                    elif KEYS[ self.keys_pygame[ keys_value_list['left'] ] ]:
                        self.player.status = 'left_run'
                    elif KEYS[ self.keys_pygame[ keys_value_list['up'] ] ]:
                        self.player.status = 'up_run'
                    elif KEYS[ self.keys_pygame[ keys_value_list['down'] ] ]:
                        self.player.status = 'down_run'
                else:
                    self.player.speed = 200

            # ---------------------------------------ИСТРУМЕНТЫ---------------------------------------

            # Использование инструмента
            if self.key_states[keys_value_list['use']]['pressed'] and not self.timers['use_tool_timer_700'].active:

                self.timers['use_tool_timer_700'].activate()
                if self.player.selected_tool == 'axe':
                    for tree in self.player.tree_sprites.sprites():
                        if tree.rect.collidepoint(self.player.target_pos) and tree.alive and tree.health > 0:
                            self.player.axe_sound.play()

                self.player.direction = pygame.math.Vector2()
                self.player.frame_index = 0
                self.player.wave.play()

            # ---------------------------------------СМЕНА ИНСТРУМЕНТОВ---------------------------------------

            if self.key_states[keys_value_list['switch tool']]['pressed'] and not self.timers['input_timer_200'].active:
                self.player.switch.play()
                self.player.tool_index += 1
                self.player.tool_index = self.player.tool_index if self.player.tool_index < len(self.player.tools) else 0
                self.player.selected_tool = self.player.tools[self.player.tool_index]
                self.timers['input_timer_200'].activate()

            # ---------------------------------------СМЕНА СЕМЯН---------------------------------------

            for i, seed_key in enumerate(['seed_1', 'seed_2', 'seed_3', 'seed_4', 'seed_5', 'seed_6', 'seed_7', 'seed_8']):
                if self.key_states[keys_value_list[seed_key]]['pressed'] and not self.timers['input_timer_200'].active:
                    self.player.switch.play()
                    self.player.seed_index = i
                    self.player.selected_seed = self.player.seeds[self.player.seed_index]
                    self.timers['input_timer_200'].activate()

            # Посадка семян
            if self.key_states[keys_value_list['plant']]['pressed'] and not self.timers['use_seed_timer_250'].active:
                self.player.direction = pygame.math.Vector2()
                self.player.frame_index = 0
                self.timers['use_seed_timer_250'].activate()

        # ---------------------------------------МЕНЮ НАСТРОЕК---------------------------------------

        # Если активно меню настроек
        if self.menus_active['esc_menu'] and not self.timers['input_timer_250'].active:

            # Листаем пункты вверх
            if self.key_states[keys_value_list['up']]['pressed']:
                self.esc_menu.index -= 1
                self.esc_menu.switch.play()
                self.timers['input_timer_250'].activate()

            # Листаем пункты вниз
            if self.key_states[keys_value_list['down']]['pressed']:
                self.esc_menu.index += 1
                self.esc_menu.switch.play()
                self.timers['input_timer_250'].activate()

            # Выбираем пункты меню
            if self.key_states[keys_value_list['accept']]['pressed']:
                current_item = ALL_OPTIONS[self.esc_menu.current_option][self.esc_menu.index]

                # options
                if current_item == 'Play':
                    self.level.toggle_esc_menu()

                # Переходим в настройки
                if current_item == 'Options':
                    self.esc_menu.current_option = 'in_options'

                # Переходим в настройки звука
                if current_item == 'Volume':
                    self.esc_menu.current_option = 'volume'

                # Выходим из игры
                if current_item == 'Exit':
                    pygame.quit()
                    sys.exit()

                self.timers['input_timer_250'].activate()

            # Убавляем звук
            if self.key_states[keys_value_list['left']]['pressed']:
                current_item = ALL_OPTIONS[self.esc_menu.current_option][self.esc_menu.index]

                if self.esc_menu.current_option == 'volume':
                    self.esc_menu.switch.play()
                    self.esc_menu.sound_volume_down(current_item)

                update_all_sound_volume(SOUND_VOLUME)
                self.timers['input_timer_250'].activate()

            # Прибавляем звук
            if self.key_states[keys_value_list['right']]['pressed']:
                current_item = ALL_OPTIONS[self.esc_menu.current_option][self.esc_menu.index]

                if self.esc_menu.current_option == 'volume':
                    self.esc_menu.switch.play()
                    self.esc_menu.sound_volume_up(current_item)

                update_all_sound_volume(SOUND_VOLUME)
                self.timers['input_timer_250'].activate()

            # Возвращение назад или выход из меню
            if self.key_states[keys_value_list['esc']]['pressed']:

                if self.esc_menu.current_option != 'options':
                    if self.esc_menu.current_option == 'volume' or self.esc_menu.current_option == 'hotkeys':
                        self.esc_menu.current_option = 'in_options'
                        self.timers['input_timer_250'].activate()

                    else:
                        self.esc_menu.current_option = 'options'
                        self.timers['input_timer_250'].activate()
                else:
                    self.level.toggle_esc_menu()
                    self.timers['input_timer_250'].activate()

        # ---------------------------------------МЕНЮ ИНВЕНТАРЯ---------------------------------------

        # Если активно меню инвентаря
        elif self.menus_active['inventory_menu']:
            pass

        # ---------------------------------------МЕНЮ АВТОРИЗАЦИИ---------------------------------------

        # Если активно меню авторизации
        elif self.menus_active['start_menu']:
            mouse = pygame.mouse.get_pressed()[0]
            mouse_pos = pygame.mouse.get_pos()

            # Обводка кнопок на которые наводится мышка
            if not self.start_menu.authorization:
                if self.start_menu.entry_rect.collidepoint(mouse_pos):
                    self.start_menu.authorization_key_status = True
                else:
                    self.start_menu.authorization_key_status = False

                if self.start_menu.registration_rect.collidepoint(mouse_pos):
                    self.start_menu.registration_key_status = True
                else:
                    self.start_menu.registration_key_status = False
            else:
                if self.start_menu.play_key_rect.collidepoint(mouse_pos):
                    self.start_menu.play_key_status = True
                else:
                    self.start_menu.play_key_status = False

            # ---------------------------------------ОБРАБОТКА КЛИКОВ МЫШИ---------------------------------------

            # mouse click
            if not self.timers['input_timer_150'].active:
                if mouse:
                    if self.start_menu.login_rect.collidepoint(mouse_pos):
                        self.start_menu.login_active = True
                        self.start_menu.password_active = False

                        self.start_menu.index = 0

                    elif self.start_menu.password_rect.collidepoint(mouse_pos):
                        self.start_menu.login_active = False
                        self.start_menu.password_active = True

                        self.start_menu.index = 1

                    if self.start_menu.authorization:
                        if self.start_menu.play_key_rect.collidepoint(mouse_pos):
                            self.level.transition.play()
                            self.start_menu.toggle()

                    if self.start_menu.entry_rect.collidepoint(mouse_pos):
                        status = self.start_menu.check_account()
                        if status == 'entry':
                            self.start_menu.authorization = True
                        if status == 'empty':
                            self.start_menu.authorization_status = 'empty'
                        if status == 'invalid':
                            self.start_menu.authorization_status = 'invalid'
                        if status == 'none':
                            self.start_menu.authorization_status = 'none'

                        self.timers['input_timer_150'].activate()

                    elif self.start_menu.registration_rect.collidepoint(mouse_pos):
                        status = self.start_menu.registrate()
                        if status == 'true':
                            self.start_menu.authorization_status = 'true'
                        if status == 'empty':
                            self.start_menu.authorization_status = 'empty'
                        if status == 'exists':
                            self.start_menu.authorization_status = 'exists'

                        self.timers['input_timer_150'].activate()

            # ---------------------------------------ВВОД---------------------------------------

            # Обработка клавиш
            if any(KEYS):
                if not self.timers['input_timer_150'].active:
                    for i in self.start_menu.keys:
                        key_backspace = pygame.key.key_code('BACKSPACE')
                        key_name = pygame.key.key_code(i)

                        if self.start_menu.login_active:

                            if KEYS[key_backspace]:
                                self.start_menu.login_text = self.start_menu.login_text[:-1]
                                self.timers['input_timer_150'].activate()
                                break
                            elif KEYS[key_name]:
                                if len(self.start_menu.login_text) < 14:
                                    self.start_menu.login_text += i
                                    self.timers['input_timer_150'].activate()
                                    break

                        if self.start_menu.password_active:

                            if KEYS[key_backspace]:
                                self.start_menu.password_text = self.start_menu.password_text[:-1]
                                self.start_menu.password_text_copy = self.start_menu.password_text_copy[:-1]
                                self.timers['input_timer_150'].activate()
                                break
                            elif KEYS[key_name]:
                                if len(self.start_menu.password_text) < 14:
                                    self.start_menu.password_text_copy += i
                                    self.start_menu.password_text += '#'
                                    self.timers['input_timer_150'].activate()
                                    break

        # ---------------------------------------ИНВЕНТАРЬ---------------------------------------

        # Инвентарь
        if self.key_states[keys_value_list['inventory']]['pressed'] and self.check_menus_active_without_target('inventory_menu') and not self.timers['input_timer_250'].active:
            self.player.toggle_inventory()
            self.timers['input_timer_250'].activate()

        # ---------------------------------------МАГАЗИН И КРОВАТЬ---------------------------------------

        # Магазин и кровать
        if KEYS[self.keys_pygame[keys_value_list['interaction']]] and self.check_menus_active_without_target() and not self.timers['input_timer_250'].active:
            collided_interaction_sprite = pygame.sprite.spritecollide(self.player, self.player.interaction, False)

            if collided_interaction_sprite and self.check_menus_active_without_target():
                if collided_interaction_sprite[0].name == 'Trader':
                    self.player.toggle_shop()

                if collided_interaction_sprite[0].name == 'Bed' and self.check_menus_active_without_target():
                    self.player.status = 'left_idle'
                    self.player.sleep = True

        # ---------------------------------------ВЫЗОВ ESC МЕНЮ---------------------------------------

        # Esc меню
        if self.key_states[keys_value_list['esc']]['pressed'] and self.check_menus_active_without_target() and not self.timers['input_timer_250'].active:
            self.player.esc_menu()
            self.timers['input_timer_250'].activate()

        # Обновляем состояние меню
        self.update_menus_state()

        # Сбрасываем флаги just_pressed после обработки
        for key_state in self.key_states.values():
            key_state['just_pressed'] = False

    # Обновление состояния меню
    def update_menus_state(self):
        self.menus_active = {
            'esc_menu': self.level.esc_menu_active,
            'inventory_menu': self.level.inventory_active,
            'shop_menu': self.level.shop_active,
            'start_menu': self.level.start_menu_active,
        }

    # Обновление состояния игрока
    def get_status(self):
        # if the player is not moving:
        if self.player.direction.magnitude() == 0:
            # add _idle to the status
            self.player.status = self.player.status.split('_')[0] + '_idle'

        # Смена анимации
        if self.timers['use_tool_timer_700'].active:
            self.player.status = self.player.status.split('_')[0] + '_' + self.player.selected_tool

    # Проверка, что все меню кроме нужного не активны
    def check_menus_active_without_target(self, target_menu=''):
        return not any(value for key,value in self.menus_active.items() if key != target_menu)

    # Обновление таймера
    def update_timer(self):
        for timer in self.timers.values():
            timer.update()

    def update(self):
        self.handle_events()
        self.get_status()
        self.update_timer()
        self.get_input()
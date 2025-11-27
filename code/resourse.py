import pygame
from settings import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

sound_list = {
    'Axe':          pygame.mixer.Sound('../audio/axe.mp3'),
    'Switch tool':  pygame.mixer.Sound('../audio/switch_tool1.mp3'),
    'Water':        pygame.mixer.Sound('../audio/water.mp3'),
    'Wave':         pygame.mixer.Sound('../audio/Wave.mp3'),
    'Choice':       pygame.mixer.Sound('../audio/switch.mp3'),
    'Hoe':          pygame.mixer.Sound('../audio/hoe.mp3'),
    'Plant':        pygame.mixer.Sound('../audio/boarding3.mp3'),
    'Success':      pygame.mixer.Sound('../audio/success3.mp3'),
    'Bye or Sell':  pygame.mixer.Sound('../audio/buy or sell.mp3'),
    'Music':        pygame.mixer.Sound('../audio/bg_music2.mp3'),
    'Rain':         pygame.mixer.Sound('../audio/rain.mp3'),
}

def sound_volume(sound, volume):
    sound.set_volume(volume)

def all_sound_volume(sound_list_update):
    for sound, volume in sound_list_update.items():
        if sound in sound_list.keys():
            sound_list[sound].set_volume(volume)
            SOUND_VOLUME[sound] = volume


sprite_list = {
    'sound_on':             pygame.image.load(f'../graphics/overlay/sound_on.png').convert_alpha(),
    'sound_off':            pygame.image.load(f'../graphics/overlay/sound_off.png').convert_alpha(),
    'slot_menu':            pygame.image.load(f'../graphics/overlay/slot_menu.png').convert_alpha(),
    'select_slot_menu':     pygame.image.load(f'../graphics/overlay/select_slot_menu.png').convert_alpha(),
    'setting':              pygame.image.load(f'../graphics/overlay/setting.png').convert_alpha(),
    'back_text':            pygame.image.load(f'../graphics/overlay/back_text.png').convert_alpha(),
    'select':               pygame.image.load(f'../graphics/overlay/select.png').convert_alpha(),
    'select_slot':          pygame.image.load(f'../graphics/start menu/select_slot.png').convert_alpha(),
    'cursor':               pygame.image.load(f'../graphics/overlay/cursor.png').convert_alpha(),
    'inventory_back':       pygame.image.load(f'../graphics/overlay/inventory_back.png').convert_alpha(),
    'shop_back':            pygame.image.load(f'../graphics/overlay/shop_back.png').convert_alpha(),
    'slot':                 pygame.image.load(f'../graphics/overlay/slot.png').convert_alpha(),
    'slot_surf':            pygame.image.load(f'../graphics/start menu/slot.png').convert_alpha(),
    'back':                 pygame.image.load(f'../graphics/overlay/back.png').convert_alpha(),
    'hp_money_bar':         pygame.image.load(f'../graphics/overlay/hp_money_bar.png').convert_alpha(),
    'enter_slot':           pygame.image.load(f'../graphics/start menu/enter_slot.png').convert_alpha(),
    'select_enter_slot':    pygame.image.load(f'../graphics/start menu/select_enter_slot.png').convert_alpha(),
    'background_down':      pygame.image.load(f'../graphics/start menu/background_down.png').convert_alpha(),
    'background_up':        pygame.image.load(f'../graphics/start menu/background_up.png').convert_alpha(),
    'play_key':             pygame.image.load(f'../graphics/start menu/play_up.png').convert_alpha(),
    'select_play_key':      pygame.image.load(f'../graphics/start menu/select_play.png').convert_alpha(),
    'hoe':                  pygame.image.load(f'../graphics/overlay/hoe.png').convert_alpha(),
    'axe':                  pygame.image.load(f'../graphics/overlay/axe.png').convert_alpha(),
    'water':                pygame.image.load(f'../graphics/overlay/water.png').convert_alpha(),
    'corn':                 pygame.image.load(f'../graphics/overlay/corn.png').convert_alpha(),
    'tomato':               pygame.image.load(f'../graphics/overlay/tomato.png').convert_alpha(),
    'cabbage':              pygame.image.load(f'../graphics/overlay/cabbage.png').convert_alpha(),
    'carrot':               pygame.image.load(f'../graphics/overlay/carrot.png').convert_alpha(),
    'pumpkin':              pygame.image.load(f'../graphics/overlay/pumpkin.png').convert_alpha(),
    'turnip':               pygame.image.load(f'../graphics/overlay/turnip.png').convert_alpha(),
    'zucchini':             pygame.image.load(f'../graphics/overlay/zucchini.png').convert_alpha(),
    'cucumber':             pygame.image.load(f'../graphics/overlay/cucumber.png').convert_alpha(),
    'apple':                pygame.image.load(f'../graphics/fruit/apple.png').convert_alpha(),

}


font_list = {
    'font_110': pygame.font.Font('../font/Pixeltype.ttf', 110),
    'font_75': pygame.font.Font('../font/Pixeltype.ttf', 75),
    'font_55': pygame.font.Font('../font/Pixeltype.ttf', 55),
    'font_50': pygame.font.Font('../font/Pixeltype.ttf', 50),
    'font_40': pygame.font.Font('../font/Pixeltype.ttf', 40),
    'font_35': pygame.font.Font('../font/Pixeltype.ttf', 35),
    'font_30': pygame.font.Font('../font/Pixeltype.ttf', 30),
    'font_25': pygame.font.Font('../font/Pixeltype.ttf', 25),
    'font_20': pygame.font.Font('../font/Pixeltype.ttf', 20),
}
import pygame
from pygame.math import Vector2

# screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 64

# volume
SOUND_VOLUME = {
    'Tools':        0.1,
    'Music':        0.0,
    'Water':        0.1,
    'Hoe':          0.4,
    'Axe':          0.3,
    'Wave':         0.1,
    'Plant':        0.5,
    'Success' :     0.1,
    'Switch tool' : 0.2,
    'Bye or Sell' : 0.1,
    'Rain':         1
}

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 75

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

ALL_OPTIONS = {
    'options': ['Play', 'Options', 'Exit'],
    'in_options': ['Volume'],
    'volume': ['Tools', 'Plant', 'Music', 'Success', 'Switch tool', 'Bye or Sell'],
}

# overlay positions
op = 62
OVERLAY_POSITIONS = {
    'hp_money_bar': (10, 10),
    'tool': (50, SCREEN_HEIGHT - 50),
    'corn': (389, SCREEN_HEIGHT - 60),
    'tomato': (389 + op * 1, SCREEN_HEIGHT - 60),
    'cabbage': (389 + op * 2, SCREEN_HEIGHT - 60),
    'carrot': (389 + op * 3, SCREEN_HEIGHT - 60),
    'pumpkin': (389 + op * 4, SCREEN_HEIGHT - 60),
    'turnip': (389 + op * 5, SCREEN_HEIGHT - 60),
    'zucchini': (389 + op * 6, SCREEN_HEIGHT - 60),
    'cucumber': (389 + op * 7, SCREEN_HEIGHT - 60),
    'slot1': (340 + 50, SCREEN_HEIGHT - 59),
    'slot2': (402 + 50, SCREEN_HEIGHT - 59),
    'slot3': (464 + 50, SCREEN_HEIGHT - 59),
    'slot4': (526 + 50, SCREEN_HEIGHT - 59),
    'slot5': (588 + 50, SCREEN_HEIGHT - 59),
    'slot6': (650 + 50, SCREEN_HEIGHT - 59),
    'slot7': (712 + 50, SCREEN_HEIGHT - 59),
    'slot8': (774 + 50, SCREEN_HEIGHT - 59),
    'slot9': (836 + 50, SCREEN_HEIGHT - 59),
    'background' : (SCREEN_WIDTH // 2 - 600 / 2 + 50, SCREEN_HEIGHT - 13)
}

PLAYER_TOOL_OFFSET = {
    'left': Vector2(-50, 40),
    'right': Vector2(50, 40),
    'up': Vector2(0, -10),
    'down': Vector2(0, 50)
}

LAYERS = {
    'water': 0,
    'ground': 1,
    'soil': 2,
    'soil water': 3,
    'rain floor': 4,
    'house bottom': 5,
    'ground plant': 6,
    'main': 7,
    'house top': 8,
    'fruit': 9,
    'rain drops': 10
}

APPLE_POS = {
    'Small': [(18, 17), (30, 37), (12, 50), (30, 45), (20, 30), (30, 10)],
    'Large': [(30, 24), (60, 65), (50, 50), (16, 40), (45, 50), (42, 70)]
}

GROW_SPEED = {
    'corn':     1.2,
    'tomato':   0.7,
    'cabbage':  0.4,
    'carrot':   1,
    'pumpkin':  0.3,
    'turnip':   0.8,
    'zucchini': 0.6,
    'cucumber': 1.2

}

SALE_PRICES = {
    'wood': 4,
    'apple': 2,
    'corn': 10,
    'tomato': 20
}
PURCHASE_PRICES = {
    'corn': 4,
    'tomato': 5
}

GRID = []

# KEYS = {
# 	'plant' : pygame.KEYDOWN[pygame.K_TAB]
# }
#
# def set_key():
#

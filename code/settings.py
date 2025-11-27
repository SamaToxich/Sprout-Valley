from pygame.math import Vector2

# screen
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
TILE_SIZE = 64

# volume - теперь загружается из сохранения
SOUND_VOLUME = {
    'Choice':       0.03,
    'Tools':        0.1,
    'Water':        0.1,
    'Hoe':          0.4,
    'Axe':          0.3,
    'Wave':         0.1,
    'Plant':        0.5,
    'Affects':      0.1,
    'Success':      0.1,
    'Switch tool':  0.2,
    'Bye or Sell':  0.1,
    'Music':        0.0,
    'Rain':         1
}

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
    'in_options': ['Volume', 'Input', 'Op'],
    'volume': ['Tools', 'Affects', 'Music'],
}

# overlay positions
op = 62
OVERLAY_POSITIONS = {
    'hp_money_bar':                                             (10, 10),
    'tool':                                     (50, SCREEN_HEIGHT - 50),
    'corn':                                    (389, SCREEN_HEIGHT - 60),
    'tomato':                         (389 + op * 1, SCREEN_HEIGHT - 60),
    'cabbage':                        (389 + op * 2, SCREEN_HEIGHT - 60),
    'carrot':                         (389 + op * 3, SCREEN_HEIGHT - 60),
    'pumpkin':                        (389 + op * 4, SCREEN_HEIGHT - 60),
    'turnip':                         (389 + op * 5, SCREEN_HEIGHT - 60),
    'zucchini':                       (389 + op * 6, SCREEN_HEIGHT - 60),
    'cucumber':                       (389 + op * 7, SCREEN_HEIGHT - 60),
}

PLAYER_WATER_OFFSET = {'left': Vector2(-90, 40), 'right': Vector2(90, 40), 'up': Vector2(0, -15), 'down': Vector2(0, 70)}
PLAYER_AXE_OFFSET = {'left': Vector2(-20, 40), 'right': Vector2(20, 40), 'up': Vector2(0, 5), 'down': Vector2(0, 50)}
PLAYER_HOE_OFFSET = {'left': Vector2(-50, 40), 'right': Vector2(50, 40), 'up': Vector2(0, -5), 'down': Vector2(0, 60)}
PLAYER_SEED_OFFSET = {'left': Vector2(-10, 40), 'right': Vector2(10, 40), 'up': Vector2(0, -5), 'down': Vector2(0, 40)}

LAYERS = {
    'water':         0,
    'ground':        1,
    'soil':          3,
    'soil water':    2,
    'rain floor':    4,
    'house bottom':  5,
    'ground plant':  6,
    'main':          7,
    'house top':     8,
    'fruit':         9,
    'rain drops':   10
}

APPLE_POS = {
    'Small': [(18, 17), (30, 37), (12, 50), (30, 45), (20, 30), (30, 10)],
    'Large': [(30, 24), (60, 65), (50, 50), (16, 40), (45, 50), (42, 70)]
}

GROW_SPEED = {
    'corn':     1,
    'tomato':   0.7,
    'cabbage':  0.4,
    'carrot':   1,
    'pumpkin':  0.2,
    'turnip':   0.8,
    'zucchini': 0.6,
    'cucumber': 0.7
}

SALE_PRICES = {
    'corn':     7,
    'tomato':   10,
    'cabbage':  25,
    'carrot':   7,
    'pumpkin':  40,
    'turnip':   9,
    'zucchini': 13,
    'cucumber': 10,
    'wood':    3,
    'apple':   2,
}

PURCHASE_PRICES = {
    'corn':     4,
    'tomato':   5,
    'cabbage':  12,
    'carrot':   4,
    'pumpkin':  15,
    'turnip':   3,
    'zucchini': 5,
    'cucumber': 5,
}

collision_list = ['Collision', 'Collision up', 'Collision down', 'Collision left', 'Collision right', 'Collision corner']

# Инициализация пустых инвентарей
item_inventory = {
    'corn': 0,
    'tomato': 0,
    'cabbage': 0,
    'carrot': 0,
    'pumpkin': 0,
    'turnip': 0,
    'zucchini': 0,
    'cucumber': 0,
    'wood': 0,
    'apple': 0,
}

seed_inventory = {
    'corn': 0,
    'tomato': 0,
    'cabbage': 0,
    'carrot': 0,
    'pumpkin': 0,
    'turnip': 0,
    'zucchini': 0,
    'cucumber': 0
}

MONEY = 0
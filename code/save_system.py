import json
import os
from settings import *


class SaveSystem:
    def __init__(self):
        self.save_path = '../save/game_save.json'
        self.settings_path = '../save/settings.txt'
        self.ensure_directories()

    def ensure_directories(self):
        """Создает необходимые директории если их нет"""
        os.makedirs('../save', exist_ok=True)

    def save_game(self, level, player, soil_layer, overlay, sky, sound_volume):
        """Сохраняет все данные игры"""
        save_data = {
            'player': {
                'money': player.money,
                'item_inventory': player.item_inventory,
                'seed_inventory': player.seed_inventory,
                'selected_tool': player.selected_tool,
                'selected_seed': player.selected_seed,
                'tool_index': player.tool_index,
                'seed_index': player.seed_index,
                'seed_select_index': player.seed_select_index
            },
            'level': {
                'current_day': level.current_day,
                'raining': level.raining,
            },
            'soil_layer': {
                'grid': soil_layer.grid,
                'plants': self.get_plants_data(soil_layer.plant_sprites)
            },
            'trees': self.get_trees_data(level.tree_sprites),
            'sky': {
                'now_color': sky.now_color,
                'day_flag': sky.day_flag
            },
            'audio': sound_volume
        }

        with open(self.save_path, 'w') as f:
            json.dump(save_data, f, indent=4)

    def get_plants_data(self, plant_sprites):
        """Сохраняет данные растений"""
        plants_data = []
        for plant in plant_sprites.sprites():
            plants_data.append({
                'plant_type': plant.plant_type,
                'age': plant.age,
                'position': [plant.rect.centerx, plant.rect.centery],
                'harvestable': plant.harvestable,
                'soil_position': [plant.soil.rect.x, plant.soil.rect.y]
            })
        return plants_data

    def get_trees_data(self, tree_sprites):
        """Сохраняет данные деревьев с ID"""
        trees_data = []
        for tree in tree_sprites.sprites():
            trees_data.append({
                'tree_id': tree.tree_id,  # Сохраняем ID
                'health': tree.health,
                'alive': tree.alive,
                'days_since_cut': tree.days_since_cut
            })
        return trees_data

    def load_game(self):
        """Загружает сохранение игры"""
        try:
            with open(self.save_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def save_settings(self):
        """Сохраняет настройки в текстовый файл"""
        settings_data = f"money {MONEY}\n"

        for item, count in item_inventory.items():
            settings_data += f"{item} {count}\n"

        for seed, count in seed_inventory.items():
            settings_data += f"{seed} {count}\n"

        with open(self.settings_path, 'w') as f:
            f.write(settings_data)

    def load_settings(self):
        """Загружает настройки из текстового файла"""
        try:
            with open(self.settings_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return None

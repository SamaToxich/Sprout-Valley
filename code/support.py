import pygame
from os import walk
import os


def import_folder(path):
    surface_list = []

    # Проверяем существует ли папка
    if not os.path.exists(path):
        print(f"Warning: Folder {path} does not exist")
        return surface_list

    for _, __, img_files in walk(path):
        for image in img_files:
            # Пропускаем системные файлы
            if image.startswith('.'):
                continue

            full_path = path + '/' + image
            try:
                image_surf = pygame.image.load(full_path).convert_alpha()
                surface_list.append(image_surf)
            except pygame.error as e:
                print(f"Error loading image {full_path}: {e}")

    # Сортируем файлы по имени для правильного порядка анимации
    surface_list.sort(key=lambda x: x.get_size())

    return surface_list


def import_folder_dict(path):
    surface_dict = {}

    # Проверяем существует ли папка
    if not os.path.exists(path):
        print(f"Warning: Folder {path} does not exist")
        return surface_dict

    for _, __, img_files in walk(path):
        for image in img_files:
            # Пропускаем системные файлы
            if image.startswith('.'):
                continue

            full_path = path + '/' + image
            try:
                image_surf = pygame.image.load(full_path).convert_alpha()
                surface_dict[image.split('.')[0]] = image_surf
            except pygame.error as e:
                print(f"Error loading image {full_path}: {e}")

    return surface_dict
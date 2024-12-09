import os
import pygame
import csv
from pathlib import Path
from importlib import util
from random import choice, choices

def load_animation(path, size):
    if isinstance(size, int):
        size_x = size
        size_y = size
    else:
        size_x = size[0]
        size_y = size[1]

    # Adding every frame image to the list to run through
    name_list = []
    image_list = []

    for filename in os.listdir(path):
        name_list.append(filename)

    # Important to keep it from 1 to n organized
    name_list.sort()

    for filename in name_list:
        if filename.endswith('.png'):
            image = pygame.image.load(path + f'/{filename}').convert_alpha()
            image = pygame.transform.scale(image, (size_x, size_y))

            image_list.append(image)

    return image_list

def load_text(txt_name):
    with open(f'text_files/{txt_name}.txt', 'r') as file:
        reader = csv.reader(file)
        return [row[0] for row in reader]

def load_random_word(words_list):
    return choice(words_list).lower()

def load_filelist(path, size):
    # Adding every image to the list to run through
    name_list = []
    image_list = []

    for filename in os.listdir(path):
        name_list.append(filename)

    # Important to keep it from 1 to n organized
    name_list.sort()

    for filename in name_list:
        if filename.endswith('.png'):
            image = pygame.image.load(path + f'/{filename}').convert_alpha()
            image = pygame.transform.scale(image, size)

            image_list.append(image)

    if len(image_list) < 1: image_list = None

    return image_list

def weight_choices(given_list):
    spawns = []
    chances = []

    for item in given_list:
        spawns.append(given_list[item][0])
        chances.append(given_list[item][1])

    return choices(population=spawns, weights=chances)[0]

def load_class(file_path, class_name):
    file_path = Path(os.getcwd() + file_path)
    module_name = file_path.stem

    # Loading module
    spec = util.spec_from_file_location(module_name, str(file_path))
    module = util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        raise ImportError(f"Error while loading module {module_name}: {e}")

    return getattr(module, class_name)
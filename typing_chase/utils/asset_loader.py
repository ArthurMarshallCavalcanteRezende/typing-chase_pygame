import os
import pygame
import csv

def load_animation(path, size):
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
            image = pygame.transform.scale(image, (size, size))

            image_list.append(image)

    return image_list

def load_text(txt_name):
    with open(f'text_files/{txt_name}.txt', 'r') as file:
        reader = csv.reader(file)
        return [row[0] for row in reader]


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
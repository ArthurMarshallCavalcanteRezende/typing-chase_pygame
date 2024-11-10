import pygame
import random

def run_level0():
    game.tutorial_stage = pygame.transform.scale(
        pygame.image.load("./game_assets/stages/tutorial_stage.png").convert_alpha(),
        (800, 600))
    print("Tutorial")

def run_level1():
    print("Level 1")

def run_level2():
    print("Level 2/Final level")

def check_level(insert_level):
    if insert_level == 0:
        run_level0()

    elif insert_level == 1:
        run_level1()

    elif insert_level == 2:
        run_level2()



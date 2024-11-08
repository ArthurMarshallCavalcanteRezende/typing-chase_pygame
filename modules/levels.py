import pygame
import random

def run_level(inform_level):
    if inform_level == 0:
        print("Run a new level with diferent rules here")
    elif inform_level == 1:
        print("Run a new level with other rules here")
    elif inform_level == 2:
        print("Run a new level with same rules here")

def check_level(insert_level):
    if insert_level == 0:
        print("Tutorial stage here")
        game.tutorial_stage = pygame.transform.scale(pygame.image.load("./game_assets/stages/tutorial_stage.png").convert_alpha(),
                                                 (800, 600))
        run_level(0)

    elif insert_level == 1:
        print("Stage 1 here, only minibot enemy")
        run_level(1)

    elif insert_level == 2:
        print("Stage 2 here, only classes: B, C and D robots")
        run_level(2)


game.SCREEN_WIDTH, game.SCREEN_HEIGHT = 800, 600
game.FPS = 60

class levels:
    def __init__(self):
        super().__init__()
        self.phase = 0



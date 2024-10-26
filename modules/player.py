import pygame

SCREEN_WIDTH = 800

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.lives = 3
        self.max_points = 25
        self.closest_enemy = None
import pygame

SCREEN_WIDTH = 800

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.lives = 3
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.closest_enemy = None
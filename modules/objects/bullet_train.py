import pygame
import constants as c
from utils.colors import Colors
from modules.sprite import Sprite
from modules.game_object import GameObject
colors = Colors()

class BulletTrain(GameObject):
    def __init__(self):
        super().__init__('bullet_train', Sprite('idle', c.bullet_train_sprite), (-200, 450))
        self.speed_x = -9

    def move_to_track(self, new_rect):
        self.speed_x = -9
        self.rect.center = new_rect

    def decelerate(self):
        self.speed_x *= 0.97

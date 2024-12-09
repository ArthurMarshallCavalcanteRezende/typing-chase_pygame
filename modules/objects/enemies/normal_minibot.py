import pygame
import constants as c

from random import randint
from modules.objects.enemy_model import EnemyModel
from modules.sprite import Sprite
from utils.colors import Colors
colors = Colors()

class Enemy(EnemyModel):
    NAME = 'normal_minibot'
    SPRITE_LIST = Sprite('idle', c.normal_minibot_sprite)
    TEXT_LIST = [c.left_letters, c.right_letters]

    def __init__(self, game, custom_pos=None):
        super().__init__(self.NAME, self.SPRITE_LIST)
        self.is_word = False
        self.rect.x = c.SCREEN_WIDTH
        self.rect.y = randint(80, 350)

        self.difficulty = 1
        self.text_frame = False
        self.speed_x = randint(game.level.enemy_speed - 1, game.level.enemy_speed + 1)
        self.speed_y = 0

        super().load(game, self.TEXT_LIST, custom_pos)

    def update(self, game):
        super().get_highlight(game)
        super().update(game)

        if self.reached_player:
            direction_x = game.player.rect.x - self.rect.x
            direction_y = game.player.rect.y - self.rect.y
            distance = (direction_x ** 2 + direction_y ** 2) ** 0.5

            if distance != 0:
                self.speed_x = self.reach_speed * (direction_x / distance)
                self.speed_y = -self.reach_speed * (direction_y / distance)

        # Damage player when colliding
        if self.rect.colliderect(game.player.hitbox) and not self.hit_player:
            self.touch_player = True
            super().damage_player(game)


    def draw(self, game):
        super().draw(game)


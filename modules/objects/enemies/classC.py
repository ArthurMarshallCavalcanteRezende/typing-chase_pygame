import pygame
import constants as c

from random import randint
from modules.objects.enemy_model import EnemyModel
from modules.sprite import Sprite
from utils.colors import Colors
colors = Colors()

class Enemy(EnemyModel):
    NAME = 'classC'
    SPRITE_LIST = Sprite('idle', c.classC_sprite)
    TEXT_LIST = [c.words_2, c.words_3, c.words_4, c.words_5,
                c.words_6, c.words_7, c.words_8]

    def __init__(self, game, custom_pos=None):
        super().__init__(self.NAME, self.SPRITE_LIST)
        self.is_word = True
        self.rect.x = c.SCREEN_WIDTH
        self.rect.y = randint(80, 350)

        self.difficulty = 1
        self.text_frame = True
        self.speed_x = randint(game.level.enemy_speed - 1, game.level.enemy_speed + 1)
        self.speed_y = 0

        new_text = super().get_text(game, self.TEXT_LIST)
        super().load(game, new_text, custom_pos)

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


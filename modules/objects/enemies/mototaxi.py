import pygame
import constants as c

from random import randint
from modules.objects.enemy_model import EnemyModel
from modules.sprite import Sprite
from utils.colors import Colors

colors = Colors()

class Enemy(EnemyModel):
    NAME = 'mototaxi'
    SPRITE_LIST = Sprite('idle', c.mototaxi_sprite)
    TEXT_LIST = [[c.words_2], [c.words_3], [c.words_4]]

    def __init__(self, game, custom_pos=None):
        super().__init__(self.NAME, self.SPRITE_LIST)
        self.is_word = True
        self.rect.x = c.SCREEN_WIDTH
        self.rect.y = game.level.floor_y - self.size[1] * 1.6

        self.difficulty = 1
        self.text_frame = True
        self.speed_x = game.level.difficulty
        self.speed_y = 0

        if self.speed_x < 5: self.speed_x = 5
        elif self.speed_x > 9: self.speed_x = 9

        if game.level.difficulty < 4:
            choosen_txt = self.TEXT_LIST[0]
        elif 4 <= game.level.difficulty < 7:
            choosen_txt = self.TEXT_LIST[randint(0, 1)]
        else:
            choosen_txt = self.TEXT_LIST[randint(1, 2)]

        super().load(game, choosen_txt, custom_pos)

    def update(self, game):
        super().get_highlight(game)
        super().update(game)

        # Damage player when colliding
        if self.rect.colliderect(game.player.hitbox) and not self.hit_player:
            self.touch_player = True

            if not game.player.dodge and not self.touch_player:
                super().damage_player(game, True)

    def draw(self, game):
        super().draw(game)


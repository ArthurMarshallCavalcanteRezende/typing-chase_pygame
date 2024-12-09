import pygame
import constants as c

from random import randint
from modules.objects.enemy_model import EnemyModel
from modules.sprite import Sprite
from utils.colors import Colors
colors = Colors()

class Enemy(EnemyModel):
    NAME = 'target'
    SPRITE_LIST =  Sprite('idle', c.target_sprite)
    TEXT_LIST = [c.left_letters, c.right_letters]

    def __init__(self, game, custom_pos=None):
        super().__init__(self.NAME, self.SPRITE_LIST)
        self.is_word = False
        self.rect.x = c.SCREEN_WIDTH
        self.rect.y = game.level.floor_y - 255

        self.difficulty = 1
        self.text_frame = True
        self.speed_x = 2
        self.speed_y = 0

        super().load(game, self.TEXT_LIST, custom_pos)

    def update(self, game):
        super().get_highlight(game)
        super().update(game)

        # Damage player when colliding
        if self.rect.colliderect(game.player.hitbox) and not self.hit_player:
            self.touch_player = True
            super().damage_player(game)
            game.level.enemy_list.remove(self)


    def draw(self, game):
        super().draw(game)


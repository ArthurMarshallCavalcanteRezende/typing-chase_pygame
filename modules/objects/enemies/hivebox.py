import pygame
import constants as c

from random import randint
from modules.objects.enemy_model import EnemyModel
from modules.objects.enemies.normal_minibot import Enemy as Minibot
from modules.sprite import Sprite
from utils.colors import Colors
colors = Colors()

class Enemy(EnemyModel):
    NAME = 'hivebox'
    SPRITE_LIST = Sprite('idle', c.hivebox_sprite)
    TEXT_LIST = [[c.words_3], [c.words_4], [c.words_5]]

    def __init__(self, game, custom_pos=None):
        super().__init__(self.NAME, self.SPRITE_LIST)
        self.is_word = True
        self.rect.x = c.SCREEN_WIDTH
        self.rect.y = randint(80, 320)

        self.difficulty = 1
        self.text_frame = True
        self.speed_x = 6
        self.speed_y = 0

        if game.level.difficulty < 4:
            choosen_txt = self.TEXT_LIST[0]
        elif 4 <= game.level.difficulty < 7:
            choosen_txt = self.TEXT_LIST[1]
        else:
            choosen_txt = self.TEXT_LIST[2]

        super().load(game, choosen_txt, custom_pos)

    def update(self, game):
        super().get_highlight(game)

        if not self.reached_player:
            super().update(game)

            if self.rect.centerx > self.random_static_x:
                current_interval = int(self.hivebox_interval * 1.5)
            else:
                self.speed_x = 0
                current_interval = self.hivebox_interval

            if self.tick % current_interval == 0:
                # Hivebox will spawn an enemy on it's position after a period
                new_pos = (self.rect.centerx - 15, self.rect.centery + 15)
                new_enemy = Minibot(game, new_pos)

                game.level.enemy_list.append(new_enemy)


    def draw(self, game):
        super().draw(game)


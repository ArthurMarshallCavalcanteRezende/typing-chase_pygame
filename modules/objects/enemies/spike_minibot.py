import pygame
import constants as c

from random import randint
from modules.objects.enemy_model import EnemyModel
from modules.sprite import Sprite
from utils.colors import Colors
colors = Colors()

class Enemy(EnemyModel):
    NAME = 'spike_minibot'
    SPRITE_LIST = Sprite('idle', c.spike_minibot_sprite)
    TEXT_LIST = [c.left_letters, c.right_letters]

    def __init__(self, game, custom_pos=None):
        super().__init__(self.NAME, self.SPRITE_LIST)
        self.is_word = False
        self.rect.x = c.SCREEN_WIDTH
        self.rect.centery = -20

        self.difficulty = 1
        self.reach_speed = -8
        self.text_frame = False
        self.speed_x = 0
        self.speed_y = 0

        super().load(game, self.TEXT_LIST, custom_pos)

    def update(self, game):
        super().get_highlight(game)
        super().update(game)

        if self.lifetime >= 5 and not self.reached_player:
            super().target_player()
            game.sound.miss.play()

        if not self.reached_player:
            can_move_y = False

            # Detecting collision with other spike robots
            for bot in game.level.enemy_list:
                if bot.name == 'spike_minibot' and bot != self:
                    if self.rect.colliderect(bot.rect):
                        can_move_y = True

            self.rect.centerx = game.player.rect.centerx

            if can_move_y or self.rect.centery < self.size[0] + 10:
                self.rect.centery += 3
        else:
            direction_x = game.player.rect.x - self.rect.x
            direction_y = game.player.rect.y - self.rect.y
            distance = (direction_x ** 2 + direction_y ** 2) ** 0.5

            if distance != 0:
                self.speed_y = -self.reach_speed * (direction_y / distance)

        # Damage player when colliding
        if self.rect.colliderect(game.player.hitbox) and not self.hit_player:
            self.touch_player = True
            super().damage_player(game)


    def draw(self, game):
        super().draw(game)


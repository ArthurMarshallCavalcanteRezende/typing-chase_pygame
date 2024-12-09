import pygame
import constants as c
from math import sin

from modules.objects.obstacle_model import ObstacleModel
from utils.colors import Colors
from modules.sprite import Sprite

colors = Colors()


class Obstacle(ObstacleModel):
    NAME = 'tumbleweed'
    SPRITE_LIST = Sprite('idle', c.tumbleweed_sprite)

    def __init__(self, game, custom_pos=None):
        super().__init__(self.NAME, self.SPRITE_LIST)
        self.speed_x = 3
        self.rect.x = c.SCREEN_WIDTH + self.size[0]
        self.rect.y = game.player.rect.centery - (self.size[0] // 1.2)
        self.has_tip = True

        self.distance_warn = 100

        if custom_pos:
            self.rect.x = custom_pos[0]
            self.rect.y = custom_pos[1]

        game.sound.tumbleweed.stop()
        game.sound.tumbleweed.parent = self
        game.sound.tumbleweed.play(-1)

    def update(self, game):
        super().update(game)

        # Damage player when colliding
        if self.rect.colliderect(game.player.hitbox) and self.can_hit:
            if not game.player.dodge:
                game.sound.wrong_input.play()

                if game.sound.tumbleweed.parent == self:
                    game.sound.tumbleweed.stop(True)

                game.level.obstacle_list.remove(self)
            else:
                self.can_hit = False

        if self.rect.x < -100 or self.lifetime >= 30:
            game.sound.tumbleweed.stop()

    def draw(self, game):
        super().draw(game)
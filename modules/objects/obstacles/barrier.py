import pygame
import constants as c

from modules.objects.obstacle_model import ObstacleModel
from utils.colors import Colors
from modules.sprite import Sprite

colors = Colors()


class Obstacle(ObstacleModel):
    NAME = 'barrier'
    SPRITE_LIST = Sprite('idle', c.barrier_sprite)

    def __init__(self, game, custom_pos=None):
        super().__init__(self.NAME, self.SPRITE_LIST)
        self.speed_x = 4 + game.level.floor_speed
        self.rect.x = c.SCREEN_WIDTH + self.size[0]
        self.rect.y = game.player.rect.centery - self.size[1] // 1.55
        self.update_interval = 4

        if custom_pos:
            self.rect.x = custom_pos[0]
            self.rect.y = custom_pos[1]

        if self.speed_x > 10: self.speed_x = 10

    def update(self, game):
        self.speed_x = game.level.floor_speed
        self.distance_warn = 15 * game.level.floor_speed

        super().update(game)

        # Damage player when colliding
        if self.rect.colliderect(game.player.hitbox) and self.can_hit:
            if not game.player.dodge:
                super().damage_player(game)
                game.sound.metal_hit.play()
            else:
                self.can_hit = False

    def draw(self, game):
        super().draw(game)
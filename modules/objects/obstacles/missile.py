import pygame
import constants as c

from modules.objects.obstacle_model import ObstacleModel
from utils.colors import Colors
from modules.sprite import Sprite
colors = Colors()

class Obstacle(ObstacleModel):
    NAME = 'missile'
    SPRITE_LIST = Sprite('idle', c.missile_sprite)

    def __init__(self, game, custom_pos=None):
        super().__init__(self.NAME, self.SPRITE_LIST)
        self.speed_x = 4 + game.level.difficulty
        self.rect.x = c.SCREEN_WIDTH + self.size[0]
        self.rect.y = game.player.rect.centery - (self.size[0] // 1.5)

        if custom_pos:
            self.rect.x = custom_pos[0]
            self.rect.y = custom_pos[1]

        if self.speed_x > 10: self.speed_x = 10
        game.sound.rocket.stop()
        game.sound.rocket.parent = self
        game.sound.rocket.play(-1)


    def update(self, game):
        super().update(game)

        # Damage player when colliding
        if self.rect.colliderect(game.player.hitbox) and self.can_hit:
            if not game.player.dodge:
                super().damage_player(game)

                if game.sound.rocket.parent == self:
                    game.sound.rocket.stop(True)

                game.sound.explode.play()
                game.level.obstacle_list.remove(self)
            else:
                self.can_hit = False

        if self.rect.x < -100 or self.lifetime >= 30:
            game.sound.rocket.stop()

    def draw(self, game):
        super().draw(game)
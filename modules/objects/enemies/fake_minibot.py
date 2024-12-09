import pygame
import constants as c

from random import randint
from modules.objects.enemy_model import EnemyModel
from modules.sprite import Sprite
from utils.colors import Colors
colors = Colors()

class Enemy(EnemyModel):
    NAME = 'fake_minibot'
    SPRITE_LIST = Sprite('idle', c.fake_minibot_sprite)
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
        self.reach_speed = -10

        self.evil_face = c.evil_face.copy()
        self.evil_face_rect = self.evil_face.get_rect()
        self.fake_triggered = False

        super().load(game, self.TEXT_LIST, custom_pos)
        self.text.set_color(colors.red)

    def update(self, game):
        super().get_highlight(game)
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

            if self.fake_triggered:
                super().damage_player(game)

        if self.reached_player and not self.fake_triggered:
            self.fake_triggered = True
            game.sound.trigger.play()

        self.evil_face_rect.center = self.rect.center
        self.evil_face_rect.y += 6

    def draw(self, game):
        super().draw(game)

        if self.fake_triggered:
            self.text.toggle(False)
            game.screen.blit(self.evil_face, self.evil_face_rect)




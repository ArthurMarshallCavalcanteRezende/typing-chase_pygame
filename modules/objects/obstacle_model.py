import pygame
import constants as c

from math import sin
from modules.game_object import GameObject
from utils.colors import Colors
from utils.text import Text
colors = Colors()

class ObstacleModel(GameObject):
    def __init__(self, name, sprite_list):
        super().__init__(name, sprite_list)
        self.reached_player = False
        self.distance_warn = 150
        self.bounce_height = 20
        self.bounce_tick = 0
        self.update_interval = 3

        self.text_frame = c.text_frame.copy()
        self.text_frame = pygame.transform.scale(self.text_frame, (140, 80))
        self.text_frame_rect = self.text_frame.get_rect()
        self.text_frame_rect.x = self.rect.x - self.size[0] // 2.2
        self.text_frame_rect.y = self.rect.y - self.size[0]

        self.tip_text = Text('SPACE', self.text_frame_rect.center, c.text_font, colors.bright_yellow)
        self.has_tip = False
        self.can_hit = True
        self.alarm_on = True


    def damage_player(self, game):
        self.can_hit = False
        game.player.damage(game)
        game.player.dodge_warned = False

    def update(self, game):
        super().update(game)

        self.text_frame_rect.x = self.rect.x - self.size[0] // 2.2
        self.text_frame_rect.y = self.rect.y - self.size[0]

        # Remove if offscreen
        if self.rect.x < -100 or self.lifetime >= 30:
            game.level.obstacle_list.remove(self)
            game.player.dodge_warned = False

        warn_magnitude = game.player.rect.x + self.size[0] + self.distance_warn
        if self.rect.x < warn_magnitude and self.alarm_on:
            game.sound.caution.play()
            self.alarm_on = False
            game.player.dodge_warned = True


    def draw(self, game):
        super().draw(game)

        if self.has_tip:
            game.screen.blit(self.text_frame, self.text_frame_rect)
            text_rect = (self.text_frame_rect.centerx - 35,
                        self.text_frame_rect.centery - 4)

            self.tip_text.set_text(None, text_rect)
            self.tip_text.draw(game)

import pygame
import math
from modules.sprite import Sprite

class Obstacle:
    def __init__(self, game, name, sprite_list, size):
        self.reached_player = False
        self.size = size

        self.name = name
        self.sprite = Sprite('idle', sprite_list)
        self.rect = None
        self.base_interval = 2
        self.update_interval = self.base_interval

        self.rect = self.sprite.current_image.get_rect()

        self.lifetime = 0
        self.tick = 0
        self.speed = 0
        self.direction_x = 0
        self.direction_y = 0
        self.base_y = 0
        self.offset = 0
        self.distance_warn = 150

        self.bounce_height = 20
        self.bounce_tick = 0

        self.text_frame = game.text_frame.copy()
        self.text_frame = pygame.transform.scale(self.text_frame, (140, 80))
        self.text_frame_rect = self.text_frame.get_rect()
        self.tip_text = game.text_font.render(f'SPACE', True, game.COLORS.white)

        self.has_tip = True

        if self.name == 'missile':
            self.speed = 4 + game.player.difficulty
            self.rect.x = game.SCREEN_WIDTH + self.size
            self.rect.y = game.player.rect.centery - (self.size // 1.5)

            if self.speed > 10: self.speed = 10
            game.sound.rocket.stop()
            game.sound.rocket.parent = self
            game.sound.rocket.play(-1)
        elif self.name == 'barrier':
            self.rect.x = game.SCREEN_WIDTH + self.size
            self.rect.y = game.player.rect.centery - self.size * 1.2
        if self.name == 'tumbleweed':
            self.speed = 3
            self.rect.x = game.SCREEN_WIDTH + self.size
            self.rect.y = game.player.rect.centery - (self.size // 1.5)

            self.distance_warn = 100

            self.text_frame_rect.x = self.rect.x - self.size // 2.2
            self.text_frame_rect.y = self.rect.y - self.size

            game.sound.tumbleweed.stop()
            game.sound.tumbleweed.parent = self
            game.sound.tumbleweed.play(-1)

        self.can_hit = True
        self.alarm_on = True
        self.base_y = self.rect.y


    def update(self, game):
        self.tick += 1
        self.sprite.update(self)

        if self.tick % game.FPS == 0:
            self.lifetime += 1

        # Obstacle movements
        if self.name == 'missile':
            self.direction_x = -self.speed
        elif self.name == 'barrier':
            self.direction_x = -game.floor_speed
            self.distance_warn = 15 * game.floor_speed
        elif self.name == 'tumbleweed':
            self.direction_x = -self.speed
            self.direction_y = self.bounce_height * math.sin(self.bounce_tick)

            self.bounce_tick += 0.1
            self.text_frame_rect.x = self.rect.x - self.size // 2.2
            self.text_frame_rect.y = self.rect.y - self.size

        self.rect.x += self.direction_x
        self.rect.y = self.base_y + self.direction_y

        # Remove if offscreen
        if self.rect.x < -100 or self.lifetime >= 30:
            game.level.obstacle_list.remove(self)
            game.player.dodge_warned = False

            if self.name == 'missile' and game.sound.rocket.parent == self:
                game.sound.rocket.stop()
            if self.name == 'tumbleweed' and game.sound.tumbleweed.parent == self:
                game.sound.tumbleweed.stop()

        warn_magnitude = game.player.rect.x + self.size + self.distance_warn
        if self.rect.x < warn_magnitude and self.alarm_on:
            game.sound.caution.play()
            self.alarm_on = False
            game.player.dodge_warned = True

        # Damage player when colliding
        if self.rect.colliderect(game.player.hitbox) and self.can_hit:
            if not game.player.dodge:
                self.can_hit = False
                if self.name != 'tumbleweed':
                    game.player.damage(game)
                    game.sound.destroy.play()
                else:
                    game.sound.wrong_input.play()

                game.player.combo = 0
                game.player.dodge_warned = False

                if self.name == 'missile':
                    game.level.obstacle_list.remove(self)
                    if self.name == 'missile' and game.sound.rocket.parent == self:
                        game.sound.rocket.stop(True)
                    game.sound.explode.play()
                if self.name == 'barrier':
                    game.sound.metal_hit.play()
                if self.name == 'tumbleweed':
                    game.sound.tumbleweed.stop(True)
            else:
                self.can_hit = False


    def draw(self, game):
        self.update_interval = self.base_interval
        self.sprite.draw(game, self)

        if self.name == 'tumbleweed' and self.has_tip:
            text_rect = (
                self.text_frame_rect.centerx - 35,
                self.text_frame_rect.centery - 4
            )

            game.screen.blit(self.text_frame, self.text_frame_rect)
            game.screen.blit(self.tip_text, text_rect)

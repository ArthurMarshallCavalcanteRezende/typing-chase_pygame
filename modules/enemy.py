import pygame
import random
import math

ENEMY_SIZE = 80
ENEMY_IMG = './game_assets/enemy_sprites/minibot.png'
TEXT_BG = './game_assets/enemy_sprites/target_warning.png'

class Enemy():
    def __init__(self, game, text, speed):
        self.image = pygame.image.load(ENEMY_IMG).convert_alpha()
        self.image = pygame.transform.scale(self.image, (ENEMY_SIZE, ENEMY_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = game.SCREEN_WIDTH
        self.rect.y = random.randint(80, game.SCREEN_HEIGHT // 1.8)

        self.target_text = text
        self.remaining_text = text

        bg_size_x = int(game.header_font.get_height() * math.ceil(len(self.target_text) / 2)) + 10
        bg_sized_y = int(game.header_font.get_height() * 1.5)
        self.bg = pygame.image.load(TEXT_BG).convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (bg_size_x, bg_sized_y))
        self.bg_rect = self.bg.get_rect()
        self.bg_rect.center = self.rect.center
        self.bg_rect.y -= ENEMY_SIZE

        self.text = game.header_font.render(f'{self.remaining_text}', True, game.COLORS.white)
        self.text_rect = self.bg.get_rect()
        self.text_rect.center = self.bg_rect.center
        self.finger_highlight = None

        self.speed = speed
        self.spawn_time = 0

    def update(self, game):
        self.rect.x -= self.speed
        self.bg_rect.center = self.rect.center
        self.bg_rect.y = self.rect.y - ENEMY_SIZE

        self.text_rect.center = self.bg_rect.center

        text_lengh = int(len(self.target_text) ** 1.5)

        if len(self.target_text) > 1:
            self.text_rect.centerx += game.header_font.get_height() // 2 + text_lengh
        else:
            self.text_rect.centerx += game.header_font.get_height() // 2

        self.text_rect.y += game.header_font.get_height() // 1.75
        self.text = game.header_font.render(f'{self.remaining_text}', True, game.COLORS.white)

        found_finger = None

        if self == game.player.closest_enemy:
            for hand in game.HAND_KEYS:
                if found_finger: break
                for finger in hand:
                    if found_finger: break

                    for current_key in finger[2]:
                        if current_key == self.remaining_text[0]:
                            found_finger = finger
                            break

        if found_finger: self.finger_highlight = found_finger

    def update_lvl2(self, game):
        direction_x = game.player.rect.x - self.rect.x
        direction_y = game.player.rect.y - self.rect.y
        distance = (direction_x ** 2 + direction_y ** 2) ** 0.5

        elapsed_time = (pygame.time.get_ticks() - self.spawn_time) / 1000

        if elapsed_time == 7:
            self.rect.x += self.speed * (direction_x / distance)
            self.rect.y += self.speed * (direction_y / distance)
        if elapsed_time > 8:
            game.level.enemy_list.remove(self)

    def draw(self, game):
        game.screen.blit(self.image, self.rect)

        game.screen.blit(self.bg, self.bg_rect)
        game.screen.blit(self.text, self.text_rect)


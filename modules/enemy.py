import pygame
import random
import math

ENEMY_FOLDER = './game_assets/enemy_sprites'
TEXT_BG = f'{ENEMY_FOLDER}/target_warning.png'

class Enemy:
    def __init__(self, game, text, speed):
        self.is_word = False
        self.image = None
        self.size = 80
        possible_enemies = []
        y_pos = 0

        if len(text) > 1: self.is_word = True

        if game.level.stage == 0:
            possible_enemies.append('target')
            self.size = 150
            y_pos = game.level.floor_y - int(self.size * 1.7)
        elif game.level.stage == 1:
            if self.is_word and game.player.difficulty >= 2:
                possible_enemies.append('classB_robot')
                self.size = 120
                y_pos = game.level.floor_y - (self.size * 2)
            else:
                possible_enemies.append('minibot')
                self.size = 80
                y_pos = random.randint(80, game.SCREEN_HEIGHT // 1.8)
        elif game.level.stage == 2:
            y_pos = random.randint(80, game.SCREEN_HEIGHT // 1.8)

            if self.is_word:
                possible_enemies.append('classB_robot')
                possible_enemies.append('classC_robot')
                possible_enemies.append('classD_robot')
            else:
                possible_enemies.append('minibot')

        self.name = random.choice(possible_enemies)

        if self.name == 'classD_robot':
            self.size = 200

        self.image = pygame.image.load(f'{ENEMY_FOLDER}/{self.name}.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.x = game.SCREEN_WIDTH + random.randint(0, 150)
        self.rect.y = y_pos

        self.target_text = text
        self.remaining_text = text

        bg_size_x = int(game.header_font.get_height() * math.ceil(len(self.target_text) / 2)) + 10
        bg_sized_y = int(game.header_font.get_height() * 1.5)
        self.bg = pygame.image.load(TEXT_BG).convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (bg_size_x, bg_sized_y))
        self.bg_rect = self.bg.get_rect()
        self.bg_rect.center = self.rect.center
        self.bg_rect.y -= 80

        self.text = game.header_font.render(f'{self.remaining_text}', True, game.COLORS.white)
        self.text_rect = self.bg.get_rect()
        self.text_rect.center = self.bg_rect.center
        self.finger_highlight = None

        self.speed = speed
        self.spawn_time = 0

    def update(self, game):
        self.rect.x -= self.speed
        self.bg_rect.center = self.rect.center
        self.bg_rect.y = self.rect.y - 80

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


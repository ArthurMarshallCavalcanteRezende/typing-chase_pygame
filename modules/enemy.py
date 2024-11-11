import pygame
import random

ENEMY_SIZE = 80
ENEMY_IMG = './game_assets/enemy_sprites/minibot.png'
TEXT_BG = './game_assets/enemy_sprites/target.png'

class Enemy():
    def __init__(self, game, text, speed):
        self.image = pygame.image.load(ENEMY_IMG).convert_alpha()
        self.image = pygame.transform.scale(self.image, (ENEMY_SIZE, ENEMY_SIZE))
        self.bg = pygame.image.load(TEXT_BG).convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (ENEMY_SIZE - 20, ENEMY_SIZE - 20))
        self.rect = self.image.get_rect()
        self.rect.x = game.SCREEN_WIDTH
        self.rect.y = random.randint(80, game.SCREEN_HEIGHT // 1.8)
        self.bg_rect = self.rect

        self.bg_rect.y -= ENEMY_SIZE
        self.target_text = text
        self.remaining_text = text

        self.text = game.large_font.render(f'{text}', True, game.COLORS.white)
        self.finger_highlight = None

        self.speed = speed
        self.spawn_time = 0

    def update(self, game):
        self.rect.x -= self.speed
        self.bg_rect.x = self.rect.x

        found_finger = None

        if self == game.player.closest_enemy:
            for hand in game.HAND_KEYS:
                if found_finger: break
                for finger in hand:
                    if found_finger: break

                    for current_key in finger[2]:
                        if current_key == self.remaining_text[-1]:
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
        game.screen.blit(self.text, self.bg_rect)


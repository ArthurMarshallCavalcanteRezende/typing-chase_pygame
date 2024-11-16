import pygame
import random
import math

ENEMY_FOLDER = './game_assets/enemy_sprites'

def load_random_word(words_list):
    return random.choice(words_list).lower()

class Sprite:
    def __init__(self, name, image_list, oneshot=False, custom_interval=None):
        self.name = name
        self.image_list = image_list
        self.current_image = None
        self.oneshot = oneshot

        # Values for updating the animation frame per update interval
        self.index = 0
        self.max_index = len(self.image_list) - 1
        self.tick = 0
        self.custom_interval = custom_interval

        self.visible = True
        self.shot_enabled = False

        self.current_image = self.image_list[self.index]

    def update(self, enemy):
        self.tick += 1

        # Checking if image can update to next shot depending on interval
        if self.custom_interval:
            can_update = self.tick > self.custom_interval
        else:
            can_update = self.tick > enemy.update_interval

        if can_update:
            # Oneshot mode only runs the animation once, used for single actions.
            if self.oneshot:
                if self.shot_enabled:
                    self.tick = 0
                    self.index = 0
                    self.current_image = self.image_list[self.index]
                    self.shot_enabled = False

                self.tick = 0

                if not self.index > self.max_index:
                    self.current_image = self.image_list[self.index]
                    self.index += 1

            # Plays animation constantly if not oneshot mode
            else:
                self.tick = 0
                self.index += 1
                if self.index > self.max_index: self.index = 0

                self.current_image = self.image_list[self.index]

    def draw(self, game, enemy):
        if self.visible:
            game.screen.blit(self.current_image, enemy.rect)


class Enemy:
    def __init__(self, game, name, sprite_list, size, difficulty, has_frame=False):
        self.loaded = False
        self.is_word = False
        self.reached_player = False
        self.has_frame = has_frame
        self.size = size
        self.difficulty = difficulty

        self.name = name
        self.sprite = Sprite('idle', sprite_list)
        self.rect = None
        self.finger_highlight = None
        self.base_interval = 2
        self.update_interval = self.base_interval

        self.rect = self.sprite.current_image.get_rect()
        self.rect.x = game.SCREEN_WIDTH + 500
        self.rect.y = game.SCREEN_HEIGHT // 2

        self.target_text = ''
        self.remaining_text = ''

        self.bg = game.text_frame.copy()
        self.bg_rect = None
        self.text = None
        self.text_rect = None

        self.lifetime = 0
        self.speed = 0


    def load(self, game, speed):
        letter_list = [game.left_letters, game.right_letters]

        if self.difficulty > 1:
            choosen_txt = game.all_words
        else:
            choosen_txt = random.choice(letter_list)

        new_word = load_random_word(choosen_txt)

        if len(new_word) > 1:
            if len(new_word) <= 5:
                speed = 2
            else:
                speed = 1

        y_pos = 0

        if len(new_word) > 1: self.is_word = True

        if game.level.stage == 0:
            y_pos = game.level.floor_y - int(self.size * 1.7)
        elif game.level.stage == 1:
            if self.is_word and game.player.difficulty >= 2:
                y_pos = game.level.floor_y - (self.size * 2)
            else:
                y_pos = random.randint(80, game.SCREEN_HEIGHT // 1.8)
        elif game.level.stage == 2:
            y_pos = random.randint(80, game.SCREEN_HEIGHT // 1.8)

        self.speed = speed

        self.rect.x = game.SCREEN_WIDTH + random.randint(0, 150)
        self.rect.y = y_pos

        self.target_text = new_word
        self.remaining_text = new_word

        bg_size_x = int(game.header_font.get_height() * math.ceil(len(self.target_text) / 2)) + 10
        bg_sized_y = int(game.header_font.get_height() * 1.5)
        self.bg = pygame.transform.scale(self.bg, (bg_size_x, bg_sized_y))
        self.bg_rect = self.bg.get_rect()
        self.bg_rect.x = game.SCREEN_WIDTH + 200

        self.text = game.header_font.render(f'{self.remaining_text}', True, game.COLORS.white)
        self.text_rect = self.bg.get_rect()
        self.text_rect.center = self.rect.center

        self.loaded = True


    def update(self, game):
        if not self.loaded: return

        self.sprite.update(self)

        if not self.reached_player:
            self.rect.x -= self.speed
        else:
            # Moving to the player if reached far enough
            direction_x = game.player.current_rect.x - self.rect.x
            direction_y = game.player.current_rect.y - self.rect.y
            distance = (direction_x ** 2 + direction_y ** 2) ** 0.5

            self.rect.x += self.speed * (direction_x / distance)
            self.rect.y += self.speed * (direction_y / distance)

        # Remove if offscreen
        if self.rect.x < -100:
            game.level.enemy_list.remove(self)

        # Damage player when colliding
        if self.rect.colliderect(game.player.hitbox) and self in game.level.enemy_list:
            if game.level.stage != 0:
                game.player.lives -= 1
                game.damage_sound.play()
                game.destroy_sound.play()
            else:
                game.wrong_sound.play()

            game.player.combo = 0
            game.level.enemy_list.remove(self)

        self.bg_rect.center = self.rect.center
        self.bg_rect.y = self.rect.y - 80

        if self.has_frame:
            self.text_rect.center = self.bg_rect.center
            text_lengh = int(len(self.target_text) ** 1.5)

            if len(self.target_text) > 1:
                self.text_rect.centerx += game.header_font.get_height() // 2 + text_lengh
            else:
                self.text_rect.centerx += game.header_font.get_height() // 2

            self.text_rect.y += game.header_font.get_height() // 1.75
        else:
            self.text_rect.center = self.rect.center
            self.text_rect.centerx += game.header_font.get_height() // 2.25
            self.text_rect.y += game.header_font.get_height() // 3

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


    def draw(self, game):
        if not self.loaded: return

        self.update_interval = self.base_interval
        self.sprite.draw(game, self)

        if self.has_frame:
            game.screen.blit(self.bg, self.bg_rect)
        game.screen.blit(self.text, self.text_rect)
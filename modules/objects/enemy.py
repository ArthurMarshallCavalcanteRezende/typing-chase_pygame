import pygame
import random
import math

ENEMY_FOLDER = './assets/enemies'

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
        self.touch_player = False
        self.hit_player = False

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
        self.evil_face = game.evil_face.copy()
        self.evil_face_rect = None
        self.bg_rect = None
        self.text = None
        self.text_rect = None
        self.text_color = game.COLORS.white

        self.lifetime = 0
        self.tick = 0
        self.speed = 0
        self.direction_x = 0
        self.direction_y = 0
        self.offset = 0

        self.fake_triggered = False
        self.random_static_x = random.randint(530, 650)
        self.hivebox_interval = max(150 - (15 * game.player.difficulty), 30)


    def load(self, game, speed, custom_pos=None):
        letter_list = [game.left_letters, game.right_letters]

        if self.difficulty > 1:
            if self.name == 'hivebox':
                if game.player.difficulty < 4:
                    choosen_txt = game.words_3
                elif 4 <= game.player.difficulty < 7:
                    choosen_txt = game.words_4
                else:
                    choosen_txt = game.words_5

            elif self.name == 'mototaxi':
                if game.player.difficulty < 5:
                    choosen_txt = game.words_2
                else:
                    choosen_txt = game.words_3
            else:
                # For class B, C and D type robots
                text_files = [
                    game.words_2, game.words_3, game.words_4, game.words_5,
                    game.words_6, game.words_7, game.words_8,
                ]

                word_size_range = game.player.difficulty // 3
                if word_size_range > 3: word_size_range = 3

                word_min_range = self.difficulty - 1
                word_size_range += word_min_range
                if word_size_range > len(text_files) - 1:
                    word_size_range = len(text_files) - 1

                choosen_txt = text_files[random.randint(word_min_range, word_size_range)]
        else:
            choosen_txt = random.choice(letter_list)

        new_word = load_random_word(choosen_txt)

        if len(new_word) > 1:
            speed = 6 - len(new_word)
            if speed < 1: speed = 1
            if self.name == 'hivebot': speed = 6
            if self.name == 'mototaxi':
                speed = game.player.difficulty
                if speed < 5: speed = 5
                elif speed > 9: speed = 9

                speed = random.randint(5, speed)

        x_pos = game.SCREEN_WIDTH
        y_pos = 0

        if len(new_word) > 1: self.is_word = True

        # Defining possible Y positions depending on level
        if game.level.stage == 0:
            y_pos = game.level.floor_y - int(self.size * 1.7)
        elif game.level.stage >= 1:
            y_pos = random.randint(80, int(game.SCREEN_HEIGHT // 1.8))

        self.speed = speed

        if self.name == 'mototaxi':
            y_pos = game.level.floor_y - int(self.size * 3.7)

        if not custom_pos:
            self.rect.x = x_pos
            self.rect.y = y_pos
        else:
            self.rect.center = custom_pos

        self.target_text = new_word
        self.remaining_text = new_word

        # Creating the text frame background and text
        bg_size_x = int(game.header_font.get_height() * math.ceil(len(self.target_text) / 2)) + 10
        if len(self.target_text) == 2:
            bg_size_x = int(bg_size_x) * 1.5

        bg_sized_y = int(game.header_font.get_height() * 1.5)
        self.bg = pygame.transform.scale(self.bg, (bg_size_x, bg_sized_y))
        self.bg_rect = self.bg.get_rect()
        self.bg_rect.x = game.SCREEN_WIDTH + 200

        self.evil_face_rect = self.evil_face.get_rect()

        # Different enemy configurations
        if self.name == 'wild_minibot':
            if self.speed <= 3: self.speed += 1
            self.direction_y = random.randint(2, self.speed + 2)

        if self.name == 'spike_minibot':
            self.rect.centery = -20
            self.offset = -10

        if self.name == 'fake_minibot':
            self.text_color = game.COLORS.red

        self.text = game.header_font.render(f'{self.remaining_text}', True, self.text_color)
        self.text_rect = self.bg.get_rect()
        self.text_rect.center = self.rect.center

        self.loaded = True


    def update(self, game):
        if not self.loaded: return

        self.tick += 1
        self.sprite.update(self)

        if (self.name == 'fake_minibot' and self.reached_player
                and not self.fake_triggered):
            self.fake_triggered = True
            game.sound.trigger.play()

        if self.tick % game.FPS == 0:
            self.lifetime += 1

        if not self.reached_player:
            # Normal minibot movement
            if (self.name == 'normal_minibot'
                or self.name == 'fake_minibot'
                or self.name == 'target'
                or self.name == 'mototaxi'
                or self.name == 'classB'
                or self.name == 'classC'
                or self.name == 'classD'
            ):
                self.direction_x = -self.speed

            # Wild minibot movement
            if self.name == 'wild_minibot':
                self.direction_x = -self.speed

                if self.rect.bottom >= game.level.floor_y // 1.3:
                    self.direction_y = -self.speed
                elif self.rect.top <= 0:
                    self.direction_y = self.speed

            # Spike minibot movement
            if self.name == 'spike_minibot':
                self.direction_x = 0
                can_move_y = False

                # Detecting collision with other spike robots
                for bot in game.level.enemy_list:
                    if bot.name == 'spike_minibot' and bot != self:
                        if self.rect.colliderect(bot.rect):
                            can_move_y = True

                self.rect.centerx = game.player.rect.centerx
                if can_move_y or self.rect.centery < self.size + self.offset:
                    self.rect.centery += 3

            # Hivebox movement
            if self.name == 'hivebox':
                if self.rect.centerx > self.random_static_x:
                    self.direction_x = -self.speed
                    current_interval = int(self.hivebox_interval * 1.5)
                else:
                    self.direction_x = 0
                    current_interval = self.hivebox_interval

                if self.tick % current_interval == 0:
                    # Hivebox will spawn an enemy on it's position after a period
                    enemy_values = game.enemies['normal_minibot']
                    new_enemy = Enemy(
                        game, 'normal_minibot', enemy_values[0], enemy_values[1],
                        enemy_values[2], enemy_values[3])

                    new_pos = (self.rect.centerx - 15, self.rect.centery + 15)
                    new_enemy.load(game, 3, new_pos)

                    game.level.enemy_list.append(new_enemy)

        else:
            if self.name != 'mototaxi':
                # Moving to the player if reached far enough
                direction_x = game.player.rect.x - self.rect.x
                direction_y = game.player.rect.y - self.rect.y
                distance = (direction_x ** 2 + direction_y ** 2) ** 0.5
                if self.name == 'spike_minibot': distance = distance // 5
                if self.name == 'fake_minibot': distance = distance // 6

                if distance != 0:
                    if self.name != 'spike_minibot':
                        self.direction_x = self.speed * (direction_x / distance)
                    self.direction_y = self.speed * (direction_y / distance)

        self.rect.x += self.direction_x
        self.rect.y += self.direction_y
        # Remove if offscreen
        if self.rect.x < -self.size or self.lifetime >= 30:
            game.level.enemy_list.remove(self)

        # Damage player when colliding
        if self.rect.colliderect(game.player.hitbox) and self in game.level.enemy_list:
            can_hit = True

            # Various conditions to detect if enemy can hit player
            if (self.hit_player
                or (self.touch_player and self.name == 'mototaxi')
                or (game.player.dodge and self.name == 'mototaxi')
                or (self.name == 'fake_minibot' and not self.reached_player)):
                can_hit = False

            self.touch_player = True

            if can_hit:
                if game.level.stage != 0:
                    game.player.damage(game)
                    game.sound.destroy.play()
                    game.sound.explode.play()
                else:
                    game.sound.wrong_input.play()

                game.player.combo = 0
                self.hit_player = True

                if self.name != 'mototaxi':
                    game.level.enemy_list.remove(self)

        self.evil_face_rect.center = self.rect.center
        self.evil_face_rect.y += 6

        self.render_text(game)

    def render_text(self, game):
        self.bg_rect.center = self.rect.center
        self.bg_rect.centerx -= self.size // 6
        self.bg_rect.y = self.rect.y - 70

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

        self.text = game.header_font.render(f'{self.remaining_text}', True, self.text_color)

        found_finger = None

        if self == game.player.closest_enemy and self.name != 'fake_minibot':
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

        if self.name == 'fake_minibot' and self.reached_player:
            game.screen.blit(self.evil_face, self.evil_face_rect)
        else:
            game.screen.blit(self.text, self.text_rect)

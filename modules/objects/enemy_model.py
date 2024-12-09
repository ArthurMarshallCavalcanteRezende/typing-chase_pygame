import pygame
import constants as c

from math import ceil
from random import choice, randint
from modules.game_object import GameObject
from utils.asset_loader import load_random_word
from utils.colors import Colors
from utils.text import Text
colors = Colors()

class EnemyModel(GameObject):
    def __init__(self, name, sprite_list):
        super().__init__(name, sprite_list)
        self.is_word = False
        self.reached_player = False
        self.touch_player = False
        self.hit_player = False

        self.text_frame = False
        self.difficulty = 1
        self.finger_highlight = None
        self.update_interval = 3
        self.reach_speed = -4

        self.target_text = ''
        self.remaining_text = ''
        self.text = Text(self.remaining_text, self.rect.center, c.header_font, colors.white)

        self.bg = c.text_frame.copy()
        self.bg_rect = None

        self.random_static_x = randint(530, 650)
        self.hivebox_interval = 150

    # This function chooses the texts automatically depending on difficulty
    def get_text(self, game, text_files):
        word_size_range = game.level.difficulty // 3
        if word_size_range > 3: word_size_range = 3

        word_min_range = self.difficulty - 1
        word_size_range += word_min_range
        if word_size_range > len(text_files) - 1:
            word_size_range = len(text_files) - 1

        new_file = text_files[randint(word_min_range, word_size_range)]
        return [new_file]

    def load(self, game, text_list, custom_pos=None):
        if custom_pos:
            self.rect.x = custom_pos[0]
            self.rect.y = custom_pos[1]

        # Getting new text/word from file given
        choosen_txt = choice(text_list)
        new_word = load_random_word(choosen_txt)

        self.target_text = new_word
        self.remaining_text = new_word

        # Setting text frame background]
        bg_size_x = int(c.header_font.get_height() * ceil(len(self.target_text) / 2)) + 10
        if len(self.target_text) == 2:
            bg_size_x = int(bg_size_x) * 1.5

        bg_size_y = int(c.header_font.get_height() * 1.5)
        self.bg = pygame.transform.scale(self.bg, (bg_size_x, bg_size_y))
        self.bg_rect = self.bg.get_rect()
        self.bg_rect.x = c.SCREEN_WIDTH + 200

        if self.is_word and (self.name != 'hivebox' and self.name != 'mototaxi'):
            self.speed_x = 6 - len(new_word)
            if self.speed_x < 1: self.speed_x = 1

    def update(self, game):
        super().update(game)

        # Remove if offscreen
        if self.rect.x < -self.size[0] or self.lifetime >= 30:
            game.level.enemy_list.remove(self)

        self.render_text(game)

    def target_player(self):
        self.reached_player = True
    
    def damage_player(self, game, keep_alive=False):
        if game.level.stage != 0:
            game.player.damage(game)
            game.sound.destroy.play()
            game.sound.explode.play()

            if not keep_alive:
                game.level.enemy_list.remove(self)
        else:
            game.sound.wrong_input.play()

        self.hit_player = True

    def render_text(self, game):
        self.bg_rect.center = self.rect.center
        self.bg_rect.y = self.rect.y - 70

        if self.text_frame:
            text_size = len(self.target_text)

            if len(self.target_text) > 1:
                new_x = int(text_size ** 2.4)
                if text_size == 2: new_x += 8
                if text_size > 5: new_x -= int(text_size ** 1.8)
                if text_size > 7: new_x -= int(text_size ** 1.8)
            else:
                new_x = 6
                self.bg_rect.centerx -= self.size[0] // 6

            new_text_rect = (self.bg_rect.centerx - new_x,
                             self.bg_rect.centery - 9)
        else:
            new_x = 9
            new_y = 23
            if self.remaining_text[0] == 'i':
                new_x -= 5

            new_text_rect = (self.rect.centerx - new_x,
                             self.rect.centery - new_y)

        self.text.set_text(f'{self.remaining_text}', new_text_rect)

    def remove_text(self):
        self.remaining_text = self.remaining_text[1:]
    
    def get_highlight(self, game):
        found_finger = None

        if self == game.player.closest_enemy:
            for hand in c.HAND_KEYS:
                if found_finger: break
                for finger in hand:
                    if found_finger: break

                    for current_key in finger[2]:
                        if current_key == self.remaining_text[0]:
                            found_finger = finger
                            break

        if found_finger: self.finger_highlight = found_finger

    def draw(self, game):
        super().draw(game)

        if self.text_frame:
            game.screen.blit(self.bg, self.bg_rect)

        self.text.draw(game)

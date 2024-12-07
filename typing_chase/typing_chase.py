import pygame
import sys
import os
import json

from modules import levels
from modules.objects import player as plr

from utils import sound
from utils import particles
from utils import colors

from interfaces import menu
from interfaces import player_select
from interfaces import game_over
from interfaces import pause
from interfaces import rewards
from interfaces import loading

import constants as c

class Game:
    def __init__(self):
        # Data is the current player data
        self.data = {}
        self.loaded = False
        self.account_names = {}
        self.account_check_index = 0
        self.player_name = ''

        self.FPS = 60
        self.tick = 0
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))

        # State is what defines what part of the game to run through (menu, level, pause, etc.)
        self.state = 'player_select'
        self.running = True
        self.paused = False
        self.on_select = False

        # Input attributes
        self.key_down = False
        self.digit_pressed = None

        # Level attributes
        self.level = None
        self.level_index = -1

        # Classes
        self.sound = sound.Sound('assets/music/', 'mp3')
        self.colors = colors.RBG
        self.player = plr.Player(self)
        self.bullet_train = None
        self.stars_emitter = particles.ParticleEmitter(self, c.star_image, (200, 200, 200, 130))

        self.stars_emitter.size = [8, 16]
        self.stars_emitter.random_alpha = [True, 80]


    def save_data(self):
        if len(self.player_name) > 0:
            file_path = os.path.join(c.DATA_FILENAME, f'{self.player_name}.json')

            if not os.path.exists(file_path):
                self.data = c.DATA_FORMAT.copy()
                self.data["name"] = self.player_name

            with open(file_path, 'w') as file:
                json.dump(self.data, file, indent=4)
            print(f"> Data for {self.player_name} saved.")

    def load_data(self):
        file_path = os.path.join(c.DATA_FILENAME, f'{self.player_name}.json')

        # Check if filepath doesn't exist and create new file
        if not os.path.exists(file_path):
            print(f'> {self.player_name} is not part of "{c.DATA_FILENAME}", new data file will be created.')
            self.save_data()

        # Try to load existing data without errors
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                print(f"> Data for {self.player_name} loaded.")
        except json.JSONDecodeError:
            print("Error reading player file. Creating new data.")
            self.data = c.DATA_FORMAT.copy()

        # Check and update missing keys
        updated_data = self.sort_data(data, c.DATA_FORMAT)
        self.data = updated_data

    def sort_data(self, data, template):
        # Recursively update missing keys based on the template
        if not isinstance(data, dict):
            print("> Invalid data format. Resetting to default.")
            return template.copy()

        for key, value in template.items():
            if key not in data:
                print(f"> Adding missing key: {key}")
                data[key] = value
            elif isinstance(value, dict):
                # Recursively check nested dictionaries
                data[key] = self.sort_data(data.get(key, {}), value)

        return data

    def initialize(self):
        pygame.init()


        self.running = True
        self.player.reset_anim()
        self.sound.play('menu', -1)


    def reset_game(self, reset_music=True):
        """RESET ALL GAME VARIABLES FOR RESTART OR NEW LEVEL"""
        if reset_music:
            self.sound.play('menu', -1)

        # Updating every data value, including checking new max reached
        self.data["cash"] += self.player.run_cash

        if self.data["max_cash"] < self.data["cash"]:
            self.data["max_cash"] = self.data["cash"]

        if self.data[f"level{self.level.stage}"]["max_combo"] < self.player.max_combo:
            self.data[f"level{self.level.stage}"]["max_combo"] = self.player.max_combo

        if self.data[f"level{self.level.stage}"]["max_cash"] < self.player.run_cash:
            self.data[f"level{self.level.stage}"]["max_cash"] = self.player.run_cash

        if self.data[f"level{self.level.stage}"]["max_distance"] < self.player.distance:
            self.data[f"level{self.level.stage}"]["max_distance"] = self.player.distance

        self.player.reset_values()

        self.level = levels.Level(self, self.level.stage)
        self.state = 'menu'
        self.paused = False

        self.save_data()

    def change_level(self, value):
        self.level_index += value

        # Minimium and maximum level indexes possible
        if self.level_index < 0:
            self.level_index = 0
        elif self.level_index > 2:
            self.level_index = 2
    def run(self):
        self.initialize()

        while self.running:
            self.tick += 1
            self.handle_events()
            self.draw()

        # In case of problems with the loop
        self.save_data()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                # Saving data before leaving game
                self.save_data()

                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and not self.key_down:
                self.key_down = True
                self.digit_pressed = event.unicode.lower()

                ''' HANDLING MENU CONTROLS '''
                if self.state == 'menu':
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.change_level(1)
                        self.level = levels.Level(self, self.level_index)
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.change_level(-1)
                        self.level = levels.Level(self, self.level_index)

                    if event.key == pygame.K_0:
                        self.level = levels.Level(self, 0)
                    if event.key == pygame.K_1:
                        self.level = levels.Level(self, 1)
                    if event.key == pygame.K_2:
                        self.level = levels.Level(self, 2)

                    if event.key == pygame.K_RETURN:
                        if self.level:
                            if self.data[f'level{self.level.stage}']['unlocked']:
                                self.state = 'level'
                            else:
                                if self.data['cash'] >= c.LV_COSTS[f'level{self.level.stage}']:
                                    self.data['cash'] -= c.LV_COSTS[f'level{self.level.stage}']

                                    self.data[f'level{self.level.stage}']['unlocked'] = True
                                    self.sound.trigger.play()
                                    self.sound.levelup.play()
                                else:
                                    self.sound.wrong_input.play()

                        else:
                            self.level_index = 0
                    elif event.key == pygame.K_ESCAPE:
                        self.level = None
                        self.level_index = -1

                ''' HANDLING PAUSED GAME '''
                if self.state == 'pause':
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.state = 'level'
                        self.paused = False
                        self.sound.pause_sfx(False)
                        pygame.mixer.music.set_volume(0.3)
                    elif event.key == pygame.K_ESCAPE:
                        self.reset_game()

                ''' HANDLING LEVEL CONTROLS '''
                if self.state == 'level':
                    self.player.key_pressed = event.unicode

                    if event.key == pygame.K_ESCAPE:
                        self.paused = True
                        self.state = 'pause'
                        self.sound.pause_sfx(True)

                    if not self.paused and self.player.lives > 0:
                        # Checking if player hit enemy and returns the action

                        if self.player.key_pressed in c.left_letters:
                            self.player.action = 'shoot_left'
                        elif self.player.key_pressed in c.right_letters:
                            self.player.action = 'shoot_right'

                        if event.key == pygame.K_SPACE:
                            self.player.action = 'dodge'

                ''' HANDLING RETURN TO MENU SCREENS '''
                if self.state == 'gameover':
                    if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                        self.reset_game()
                if self.state == 'tutorial_end':
                    if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                        self.reset_game()

                ''' HANDLING ACCOUNT SCREEN CONTROLS '''
                if self.state == 'player_select':
                    if event.key == pygame.K_LEFT or event.key == pygame.KSCAN_LEFT:
                        self.account_check_index -= 1
                        if self.account_check_index <= -len(self.account_names):
                            self.account_check_index = 0

                    if event.key == pygame.K_RIGHT or event.key == pygame.KSCAN_RIGHT:
                        self.account_check_index += 1
                        if self.account_check_index >= len(self.account_names):
                            self.account_check_index = 0

                    if event.key == pygame.K_RETURN:
                        if len(self.player_name) >= 2:
                            # Loading player data or creating new data file
                            self.load_data()
                            self.state = 'menu'

                    if event.key == pygame.K_BACKSPACE:
                        self.digit_pressed = 'backspace'
                    if event.key == pygame.K_UNDERSCORE:
                        self.digit_pressed = '_'

            elif event.type == pygame.KEYUP:
                self.key_down = False
            elif self.state == 'menu' and self.key_down:
                self.key_down = False

    def draw(self):
        # Loading different things depending on game state
        if self.state == 'menu':
            menu.display(self)
        if self.state == 'player_select':
            player_select.display(self)
            self.on_select = True
        elif self.level and self.state == 'level':
            self.level.run(self)
        elif self.level and self.state == 'pause':
            pause.display(self)
        elif self.level and self.state == 'gameover':
            game_over.display(self)
        elif self.level and self.state == 'tutorial_end':
            rewards.tutorial_finish(self)

        if self.state == 'menu' or self.state == 'player_select':
            self.stars_emitter.toggle(True)
        else:
            self.stars_emitter.toggle(False)

        # Updating the screen
        pygame.display.flip()
        self.clock.tick(self.FPS)
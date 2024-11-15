"""
Module to load every starter asset when initializing the game,
separated from the game module to find every variable easily.

Always try to create constants or important game assets here,
so you don't have to constantly get them from other scripts.
"""

import pygame
import csv
import os
import random

from modules import player as plr
from modules import hands
from modules import sound
from modules import enemy

class colors:
    black = (0, 0, 0),
    white = (255, 255, 255),
    grey = (128, 128, 128),
    dark_grey = (60, 60, 60),

    red = (255, 0, 0),
    bright_red = (255, 150, 150),
    yellow = (255, 255, 0),
    bright_yellow = (255, 255, 150),
    orange = (255, 180, 0),
    dark_orange = (120, 50, 0),
    magenta = (255, 0, 255),
    green = (0, 255, 0),
    lime = (100, 255, 130),
    green_yellow = (180, 255, 0),
    blue = (0, 0, 255),
    cyan = (0, 255, 255),
    bright_cyan = (120, 255, 255)


ENEMY_FOLDER = './game_assets/enemy_sprites'

def update_loading(game, loaded=False):
    game.loading_percent += random.randint(7, 15)
    if game.loading_percent > 100 or loaded: game.loading_percent = 100
    message = f'Loading... ({game.loading_percent}%)'
    if loaded: message = 'Game Loaded!'

    game.loading_text = game.large_font.render(message, True, game.COLORS.white[0])
    game.loadint_text_pos = (game.SCREEN_WIDTH // 3.5, game.SCREEN_HEIGHT // 2.5)

    game.screen.fill(game.COLORS.black[0])
    game.screen.blit(game.loading_text, game.loadint_text_pos)
    pygame.display.flip()


def load_animation(game, path, size):
    # Adding every frame image to the list to run through
    name_list = []
    image_list = []

    for filename in os.listdir(path):
        name_list.append(filename)

    # Important to keep it from 1 to n organized
    name_list.sort()

    for filename in name_list:
        if filename.endswith('.png'):
            image = pygame.image.load(path + f'/{filename}').convert_alpha()
            image = pygame.transform.scale(image, (size, size))

            image_list.append(image)

    return image_list

def load_game(game):
    game.loaded = False
    game.loading_percent = 0

    # Screen size and frames per second
    game.SCREEN_WIDTH, game.SCREEN_HEIGHT = 800, 600
    game.FPS = 60
    game.tick = 0
    game.screen = pygame.display.set_mode((game.SCREEN_WIDTH, game.SCREEN_HEIGHT))
    game.COLORS = colors()
    game.level = None
    game.sound = sound.Sound('./game_assets/music/', 'mp3')

    game.screen = pygame.display.set_mode(
        (game.SCREEN_WIDTH, game.SCREEN_HEIGHT))
    pygame.display.set_caption("Typing Chase - PyGame Edition - 2024-10-26")

    # Fonts
    game.title_font = pygame.font.Font('./game_assets/font.otf', 90)
    game.large_font = pygame.font.Font('./game_assets/font.otf', 60)
    game.header_font = pygame.font.Font('./game_assets/font.otf', 40)
    game.text_font = pygame.font.Font('./game_assets/font.otf', 32)

    update_loading(game)

    # game loop
    game.clock = pygame.time.Clock()
    game.running = True
    game.paused = False
    game.game_state = 'menu'
    game.level = None

    game.LV0_NAME = '0 - TUTORIAL'
    game.LV1_NAME = '1 - Chapter 1'
    game.LV2_NAME = '2 - Chapter 2'

    game.BASE_FLOOR_SPEED = 3
    game.BASE_BG_SPEED = 1
    game.BASE_FLOOR_LIGHTS_COLOR = game.COLORS.bright_cyan
    game.floor_speed = game.BASE_FLOOR_SPEED
    game.bg_speed = game.BASE_BG_SPEED

    game.key_down = False

    update_loading(game)

    # Screen filters
    game.DARK_FILTER = pygame.Surface(
        (game.SCREEN_WIDTH, game.SCREEN_HEIGHT), pygame.SRCALPHA)
    game.DARK_FILTER.fill((0, 0, 0, 100))

    game.GAMEOVER_FILTER = pygame.Surface(
        (game.SCREEN_WIDTH, game.SCREEN_HEIGHT), pygame.SRCALPHA)
    game.GAMEOVER_FILTER.fill((30, 10, 0, 200))

    # Color for each finger on the guide hands
    game.HAND_COLORS = {
        'left': {
            'thumb': (255, 0, 0),
            'index': (0, 200, 0),
            'middle': (50, 50, 255),
            'ring': (255, 180, 180),
            'pinkie': (255, 255, 0),
        },
        'right': {
            'thumb': (255, 0, 0),
            'index': (150, 180, 255),
            'middle': (255, 180, 0),
            'ring': (180, 180, 180),
            'pinkie': (180, 255, 128),
        },
    }

    update_loading(game)

    # Enemy sprites
    game.text_frame = pygame.image.load(f'./game_assets/text_frame.png').convert_alpha()

    game.target_sprite = load_animation(game, ENEMY_FOLDER + '/target', 150)
    game.fake_minibot_sprite = load_animation(game, ENEMY_FOLDER + '/fake_minibot', 80)
    game.normal_minibot_sprite = load_animation(game, ENEMY_FOLDER + '/normal_minibot', 80)
    game.wild_minibot_sprite = load_animation(game, ENEMY_FOLDER + '/wild_minibot', 80)
    game.spike_minibot_sprite = load_animation(game, ENEMY_FOLDER + '/spike_minibot', 80)

    game.enemies = {
        # Index meaning: 1 = sprite, 2 = size, 3 = difficulty, 4 = has_frame
        'target': [game.target_sprite, 150, 1, True],
        'fake_minibot': [game.fake_minibot_sprite, 80, 1, False],
        'normal_minibot': [game.normal_minibot_sprite, 80, 1, False],
        'wild_minibot': [game.wild_minibot_sprite, 80, 1, False],
        'spike_minibot': [game.spike_minibot_sprite, 80, 1, False],
    }

    update_loading(game)

    # Keys lists for each hand
    game.HAND_KEYS = [
        [  # Left Hand
            ['left', 'thumb', [' ']],
            ['left', 'index', ['v', 'b', 'f', 'g', 'r', 't', '4', '5']],
            ['left', 'middle', ['c', 'd', 'e', '3']],
            ['left', 'ring', ['x', 's', 'w', '2']],
            ['left', 'pinkie', ['z', 'a', 'q', '1']],
        ],
        [  # Right Hand
            ['right', 'thumb', [' ']],
            ['right', 'index', ['n', 'm', 'h', 'j', 'y', 'u', '6', '7']],
            ['right', 'middle', [',', 'k', 'i', '8']],
            ['right', 'ring', ['.', 'l', 'o', '9']],
            ['right', 'pinkie', [';', 'ç', 'p', '0']],
        ]
    ]

    # Left and right keys list by rows
    with open('text_files/left_letters.txt', 'r') as file:
        reader = csv.reader(file)
        game.left_letters = [row[0] for row in reader]

    with open('text_files/right_letters.txt', 'r') as file:
        reader = csv.reader(file)
        game.right_letters = [row[0] for row in reader]

    with open('text_files/all_words.txt', 'r') as file:
        reader = csv.reader(file)
        game.all_words = [row[0] for row in reader]

    update_loading(game)

    # Creating player
    game.player_pos = ((game.SCREEN_WIDTH // 3) - 100,
                    game.SCREEN_HEIGHT - 235)

    game.player = plr.Player(game.player_pos)
    update_loading(game)

    # Hands Sprites
    left_hand_path = "./game_assets/hands/left_hand"
    right_hand_path = "./game_assets/hands/right_hand"
    x_padding = 280
    y_padding = 90

    left_hand_pos = (x_padding, game.SCREEN_HEIGHT - y_padding)
    right_hand_pos = (game.SCREEN_WIDTH - x_padding, game.SCREEN_HEIGHT - y_padding)

    game.left_hand = hands.Hands(left_hand_path, left_hand_pos, game.HAND_COLORS['left'])
    game.right_hand = hands.Hands(right_hand_path, right_hand_pos, game.HAND_COLORS['right'])
    game.left_hand.side = 'left'
    game.right_hand.side = 'right'
    update_loading(game)

    game.menu_ui = pygame.image.load(f"./game_assets/side_interface.png").convert_alpha()
    game.menu_ui = pygame.transform.scale(game.menu_ui, (game.SCREEN_WIDTH, game.SCREEN_HEIGHT))
    game.menu_ui.fill(game.COLORS.black[0], special_flags=pygame.BLEND_RGBA_MULT)

    score_path = f"./game_assets/coins.png"
    game.score_image = pygame.image.load(score_path).convert_alpha()
    game.score_image = pygame.transform.scale(game.score_image, (40, 40))

    game.menu_score_image = pygame.image.load(score_path).convert_alpha()
    game.menu_score_image = pygame.transform.scale(game.score_image, (50, 50))

    game.death_score_image = pygame.image.load(score_path).convert_alpha()
    game.death_score_image = pygame.transform.scale(game.score_image, (60, 60))

    game.bullet_train = pygame.image.load(f"./game_assets/stages/2/bullet_train.png").convert_alpha()
    game.bullet_train_rect = game.bullet_train.get_rect()
    game.bullet_train = pygame.transform.scale(game.bullet_train, (750, 450))
    game.bullet_train_rect.center = (game.SCREEN_WIDTH // 3, game.SCREEN_HEIGHT // 1.5)
    update_loading(game)

    # Sounds
    game.destroy_sound = pygame.mixer.Sound('./game_assets/sfx/explosion.wav')
    game.destroy_sound.set_volume(0.3)
    game.points_sound = pygame.mixer.Sound('./game_assets/sfx/points.wav')
    game.points_sound.set_volume(0.7)
    game.damage_sound = pygame.mixer.Sound('./game_assets/sfx/damage.wav')
    game.damage_sound.set_volume(0.6)
    game.levelup_sound = pygame.mixer.Sound('./game_assets/sfx/levelup.wav')
    game.levelup_sound.set_volume(0.5)
    game.wrong_sound = pygame.mixer.Sound('./game_assets/sfx/wrong_input.wav')
    game.wrong_sound.set_volume(0.4)
    game.get_life_sound = pygame.mixer.Sound('./game_assets/sfx/get_life.wav')
    game.get_life_sound.set_volume(0.5)
    game.shoot_sound = pygame.mixer.Sound('./game_assets/sfx/shoot.wav')
    game.shoot_sound.set_volume(0.3)
    update_loading(game)

    # ZH4R0V Dubs
    game.zharov_speech1 = pygame.mixer.Sound('./game_assets/stages/2/zharov_speech1.mp3')
    game.zharov_speech1.set_volume(0.8)
    game.zharov_speech2 = pygame.mixer.Sound('./game_assets/stages/2/zharov_speech2.mp3')
    game.zharov_speech2.set_volume(0.8)
    game.zharov_power = pygame.mixer.Sound('./game_assets/stages/2/zharov_power.mp3')
    game.zharov_power.set_volume(0.8)
    game.zharov_speech3 = pygame.mixer.Sound('./game_assets/stages/2/zharov_speech3.mp3')
    game.zharov_speech3.set_volume(0.8)
    update_loading(game)

    game.loaded = True
    update_loading(game, True)
    print('> game loaded')
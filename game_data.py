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
import json

from modules import player as plr
from modules import hands
from modules import sound
from modules import particles

DATA_FILENAME = 'player_data'
ENEMY_FOLDER = './game_assets/enemy_sprites'
OBSTACLE_FOLDER = './game_assets/obstacle_sprites'
TEXT_FORMAT = "UTF-8"

if os.path.exists(f'./{DATA_FILENAME}'):
    ACCOUNT_FILES = [name for name in os.listdir(f'./{DATA_FILENAME}')]
else:
    ACCOUNT_FILES = []
    os.makedirs(DATA_FILENAME)

DATA_FORMAT = {
    "name": f'player{len(ACCOUNT_FILES)}',
    "cash": 0,
    "max_cash": 0,
    "tutorial_finished": False,

    "level0": {
        "unlocked": True,
        "max_distance": 0,
        "max_cash": 0,
        "max_combo": 0,
    },
    "level1": {
        "unlocked": False,
        "max_distance": 0,
        "max_cash": 0,
        "max_combo": 0,
    },
    "level2": {
        "unlocked": False,
        "cutscene_finished": False,
        "max_distance": 0,
        "max_cash": 0,
        "max_combo": 0,
    },
}


class colors:
    black = (0, 0, 0),
    white = (255, 255, 255),
    bright_grey = (180, 180, 180),
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
    space_blue = (20, 10, 40),


def save_datastore(game):
    file_path = os.path.join(DATA_FILENAME, f'{game.player_name}.json')

    if not os.path.exists(file_path):
        game.data = DATA_FORMAT.copy()
        game.data["name"] = game.player_name

    with open(file_path, 'w') as file:
        json.dump(game.data, file, indent=4)
    print(f"> Data for {game.player_name} saved.")

def update_missing_keys(data, template):
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
            data[key] = update_missing_keys(data.get(key, {}), value)

    return data

def load_datastore(game):
    file_path = os.path.join(DATA_FILENAME, f'{game.player_name}.json')

    # Check if filepath doesn't exist and create new file
    if not os.path.exists(file_path):
        print(f'> {game.player_name} is not part of "{DATA_FILENAME}", new data file will be created.')
        save_datastore(game)


    # Try to load existing data without errors
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            print(f"> Data for {game.player_name} loaded.")
    except json.JSONDecodeError:
        print("Error reading player file. Creating new data.")
        game.data = DATA_FORMAT.copy()

    # Check and update missing keys
    updated_data = update_missing_keys(data, DATA_FORMAT)
    game.data = updated_data


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


def load_text(txt_name):
    with open(f'text_files/{txt_name}.txt', 'r') as file:
        reader = csv.reader(file)
        return [row[0] for row in reader]

def load_game(game):
    game.data = {}

    game.loaded = False
    game.loading_percent = 0
    game.account_names = []
    game.account_string = ''
    game.account_check_index = 0

    game.cutscene_skipped = False
    game.play_cutscene = False

    game.level_index = -1

    for file in ACCOUNT_FILES:
        name = file[:-5]
        game.account_names.append(name)

    game.account_names.sort()

    # Screen size and frames per second
    game.SCREEN_WIDTH, game.SCREEN_HEIGHT = 800, 600
    game.FPS = 60
    game.tick = 0
    game.screen = pygame.display.set_mode((game.SCREEN_WIDTH, game.SCREEN_HEIGHT))
    game.COLORS = colors()
    game.level = None
    game.sound = sound.Sound('./game_assets/music/', 'mp3')
    game.player_name = ''
    game.input_blink = False
    game.dodge_color = game.COLORS.red

    game.eligible_names = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
        'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
        'y', 'z',

        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
        
        '_', '-'
    ]

    game.screen = pygame.display.set_mode(
        (game.SCREEN_WIDTH, game.SCREEN_HEIGHT))
    pygame.display.set_caption("Typing Chase - PyGame Edition - 2024-10-26")

    # Fonts
    game.title_font = pygame.font.Font('./game_assets/font.otf', 90)
    game.large_font = pygame.font.Font('./game_assets/font.otf', 60)
    game.header_font = pygame.font.Font('./game_assets/font.otf', 40)
    game.text_font = pygame.font.Font('./game_assets/font.otf', 32)
    game.small_font = pygame.font.Font('./game_assets/font.otf', 24)

    update_loading(game)

    # game loop
    game.clock = pygame.time.Clock()
    game.running = True
    game.paused = False
    game.state = 'player_select'
    game.level = None
    game.on_select = False

    game.TUTORIAL_CASH = 500
    game.LV0_NAME = '0 - TUTORIAL'
    game.LV1_NAME = '1 - Chapter 1'
    game.LV2_NAME = '2 - Chapter 2'

    game.LV_COSTS = {
        'level0': 0,
        'level1': 200,
        'level2': 5000,
    }

    game.BASE_FLOOR_SPEED = 3
    game.BASE_BG_SPEED = 1
    game.BASE_FLOOR_LIGHTS_COLOR = game.COLORS.bright_cyan
    game.floor_speed = game.BASE_FLOOR_SPEED
    game.bg_speed = game.BASE_BG_SPEED

    game.key_down = False
    game.digit_pressed = None

    update_loading(game)

    # Screen filters
    game.TUTORIAL_FILTER = pygame.Surface(
        (game.SCREEN_WIDTH, game.SCREEN_HEIGHT), pygame.SRCALPHA)
    game.TUTORIAL_FILTER.fill((5, 10, 30, 200))

    game.CUTSCENE_FILTER = pygame.Surface(
        (game.SCREEN_WIDTH, game.SCREEN_HEIGHT), pygame.SRCALPHA)
    game.CUTSCENE_FILTER.fill((255, 255, 255, 180))

    game.LV0_FILTER = pygame.Surface(
        (game.SCREEN_WIDTH, game.SCREEN_HEIGHT), pygame.SRCALPHA)
    game.LV0_FILTER.fill((255, 180, 0, 40))

    game.LV1_FILTER = pygame.Surface(
        (game.SCREEN_WIDTH, game.SCREEN_HEIGHT), pygame.SRCALPHA)
    game.LV1_FILTER.fill((0, 0, 0, 70))

    game.DARK_FILTER = pygame.Surface(
        (game.SCREEN_WIDTH, game.SCREEN_HEIGHT), pygame.SRCALPHA)
    game.DARK_FILTER.fill((0, 0, 0, 100))

    game.LOCKED_FILTER = pygame.Surface(
        (game.SCREEN_WIDTH, game.SCREEN_HEIGHT), pygame.SRCALPHA)
    game.LOCKED_FILTER.fill((0, 0, 0, 200))

    game.GAMEOVER_FILTER = pygame.Surface(
        (game.SCREEN_WIDTH, game.SCREEN_HEIGHT), pygame.SRCALPHA)
    game.GAMEOVER_FILTER.fill((30, 10, 0, 200))

    game.star_image = pygame.image.load(f'game_assets/star.png').convert_alpha()

    # Particles
    game.stars_emitter = particles.ParticleEmitter(game, game.star_image, (200, 200, 200, 130))
    game.stars_emitter.size = [8, 16]
    game.stars_emitter.random_alpha = [True, 80]

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

    game.hivebox_sprite = load_animation(game, ENEMY_FOLDER + '/hivebox', 160)
    game.mototaxi_sprite = load_animation(game, ENEMY_FOLDER + '/mototaxi', 160)

    game.classB_sprite = load_animation(game, ENEMY_FOLDER + '/classB', 120)
    game.classC_sprite = load_animation(game, ENEMY_FOLDER + '/classC', 120)
    game.classD_sprite = load_animation(game, ENEMY_FOLDER + '/classD', 160)

    update_loading(game)

    # Obstacle sprites
    game.missile_sprite = load_animation(game, OBSTACLE_FOLDER + '/missile', 80)
    game.barrier_sprite = load_animation(game, OBSTACLE_FOLDER + '/barrier', 150)
    game.tumbleweed_sprite = load_animation(game, OBSTACLE_FOLDER + '/tumbleweed', 80)

    game.enemies = {
        # Index meaning: 1 = sprite, 2 = size, 3 = difficulty, 4 = has_frame
        'target': [game.target_sprite, 150, 1, True],
        'fake_minibot': [game.fake_minibot_sprite, 80, 1, False],
        'normal_minibot': [game.normal_minibot_sprite, 80, 1, False],
        'wild_minibot': [game.wild_minibot_sprite, 80, 1, False],
        'spike_minibot': [game.spike_minibot_sprite, 80, 1, False],

        'hivebox': [game.hivebox_sprite, 80, 2, True],
        'mototaxi': [game.mototaxi_sprite, 80, 2, True],

        'classB': [game.classB_sprite, 120, 2, True],
        'classC': [game.classC_sprite, 120, 3, True],
        'classD': [game.classD_sprite, 160, 5, True],
    }

    game.obstacles = {
        'missile': [game.missile_sprite, 80, 0, False],
        'barrier': [game.barrier_sprite, 80, 0, False],
        'tumbleweed': [game.tumbleweed_sprite, 80, 0, False],
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

    # Lists of letters and words from txt files
    game.left_letters = load_text('left_letters')
    game.right_letters = load_text('right_letters')
    game.all_words = load_text('all_words')

    game.words_2 = load_text('words_2')
    game.words_3 = load_text('words_3')
    game.words_4 = load_text('words_4')
    game.words_5 = load_text('words_5')
    game.words_6 = load_text('words_6')
    game.words_7 = load_text('words_7')
    game.words_8 = load_text('words_8')

    update_loading(game)

    # Creating player
    game.player_pos = ((game.SCREEN_WIDTH // 3) - 100,
                    game.SCREEN_HEIGHT - 235)

    game.player = plr.Player(game)
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

    game.locked_score_image = pygame.image.load(score_path).convert_alpha()
    game.locked_score_image = pygame.transform.scale(game.score_image, (40, 40))

    game.death_score_image = pygame.image.load(score_path).convert_alpha()
    game.death_score_image = pygame.transform.scale(game.score_image, (60, 60))

    game.evil_face = pygame.image.load(f"./game_assets/evil_face.png").convert_alpha()
    game.evil_face = pygame.transform.scale(game.evil_face, (45, 45))

    game.stage2_bg = pygame.image.load(f"./game_assets/stages/2/bg1.png").convert_alpha()
    game.stage2_floor = pygame.image.load(f"./game_assets/stages/2/floor.png").convert_alpha()

    game.bullet_train = pygame.image.load(f"./game_assets/stages/2/bullet_train.png").convert_alpha()
    game.bullet_train_rect = game.bullet_train.get_rect()
    game.bullet_train_size = (750, 450)
    game.bullet_train = pygame.transform.scale(game.bullet_train, game.bullet_train_size)
    game.bullet_train_rect.center = (-10, game.SCREEN_HEIGHT // 1.5)
    game.bullet_train_speed = 5
    update_loading(game)

    # ZH4R0V Dubs
    game.zharov_speech1 = pygame.mixer.Sound('./game_assets/stages/2/zharov_speech1.wav')
    game.zharov_speech1.set_volume(1.0)
    game.zharov_speech2 = pygame.mixer.Sound('./game_assets/stages/2/zharov_speech2.wav')
    game.zharov_speech2.set_volume(1.0)
    game.zharov_power = pygame.mixer.Sound('./game_assets/stages/2/zharov_power.wav')
    game.zharov_power.set_volume(1.0)
    game.zharov_speech3 = pygame.mixer.Sound('./game_assets/stages/2/zharov_speech3.wav')
    game.zharov_speech3.set_volume(1.0)
    update_loading(game)

    game.loaded = True
    update_loading(game, True)
    print('> game loaded')
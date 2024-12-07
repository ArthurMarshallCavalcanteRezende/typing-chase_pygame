import pygame
import os
from utils import colors
from utils.asset_loader import load_text
from utils.asset_loader import load_animation
from utils.asset_loader import load_filelist

DATA_FILENAME = 'data_storage'
ENEMY_FOLDER = './assets/enemies'

OBSTACLE_FOLDER = './assets/obstacles'
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

COLORS = colors.RBG()
account_names = []
account_string = ''

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

level_index = -1

for file in ACCOUNT_FILES:
    name = file[:-5]
    account_names.append(name)

account_names.sort()

# Screen size and frames per second
input_blink = False
dodge_color = COLORS.red

eligible_names = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
    'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
    'y', 'z',

    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'

                                                 '_', '-'
]

# Fonts
title_font = pygame.font.Font('assets/font.otf', 90)
large_font = pygame.font.Font('assets/font.otf', 60)
header_font = pygame.font.Font('assets/font.otf', 40)
text_font = pygame.font.Font('assets/font.otf', 32)
small_font = pygame.font.Font('assets/font.otf', 24)

TUTORIAL_CASH = 500
LV0_NAME = '0 - TUTORIAL'
LV1_NAME = '1 - Chapter 1'
LV2_NAME = '2 - Chapter 2'

LV_COSTS = {
    'level0': 0,
    'level1': 200,
    'level2': 5000,
}

BASE_FLOOR_SPEED = 3
BASE_BUILD_SPEED = 2
BASE_BG_SPEED = 1
floor_speed = BASE_FLOOR_SPEED
build_speed = BASE_BUILD_SPEED
bg_speed = BASE_BG_SPEED

key_down = False
digit_pressed = None

# Screen filters
TUTORIAL_FILTER = pygame.Surface(
    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
TUTORIAL_FILTER.fill((5, 10, 30, 200))

CUTSCENE_FILTER = pygame.Surface(
    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
CUTSCENE_FILTER.fill((255, 255, 255, 180))

LV0_FILTER = pygame.Surface(
    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
LV0_FILTER.fill((255, 180, 0, 40))

LV1_FILTER = pygame.Surface(
    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
LV1_FILTER.fill((0, 0, 0, 70))

LV2_FILTER = pygame.Surface(
    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
LV2_FILTER.fill((255, 190, 200, 60))

DARK_FILTER = pygame.Surface(
    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
DARK_FILTER.fill((0, 0, 0, 100))

LOCKED_FILTER = pygame.Surface(
    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
LOCKED_FILTER.fill((0, 0, 0, 200))

selfOVER_FILTER = pygame.Surface(
    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
selfOVER_FILTER.fill((30, 10, 0, 200))

star_image = pygame.image.load(f'assets/star.png').convert_alpha()

# Enemy sprites
text_frame = pygame.image.load(f'assets/text_frame.png').convert_alpha()

target_sprite = load_animation(ENEMY_FOLDER + '/target', 150)
fake_minibot_sprite = load_animation(ENEMY_FOLDER + '/fake_minibot', 80)
normal_minibot_sprite = load_animation(ENEMY_FOLDER + '/normal_minibot', 80)
wild_minibot_sprite = load_animation(ENEMY_FOLDER + '/wild_minibot', 80)
spike_minibot_sprite = load_animation(ENEMY_FOLDER + '/spike_minibot', 80)

hivebox_sprite = load_animation(ENEMY_FOLDER + '/hivebox', 160)
mototaxi_sprite = load_animation(ENEMY_FOLDER + '/mototaxi', 160)

classB_sprite = load_animation(ENEMY_FOLDER + '/classB', 120)
classC_sprite = load_animation(ENEMY_FOLDER + '/classC', 120)
classD_sprite = load_animation(ENEMY_FOLDER + '/classD', 160)

# Obstacle sprites
missile_sprite = load_animation(OBSTACLE_FOLDER + '/missile', 80)
barrier_sprite = load_animation(OBSTACLE_FOLDER + '/barrier', 150)
tumbleweed_sprite = load_animation(OBSTACLE_FOLDER + '/tumbleweed', 80)

enemies = {
    # Index meaning: 1 = sprite, 2 = size, 3 = difficulty, 4 = has_frame
    'target': [target_sprite, 150, 1, True],
    'fake_minibot': [fake_minibot_sprite, 80, 1, False],
    'normal_minibot': [normal_minibot_sprite, 80, 1, False],
    'wild_minibot': [wild_minibot_sprite, 80, 1, False],
    'spike_minibot': [spike_minibot_sprite, 80, 1, False],

    'hivebox': [hivebox_sprite, 80, 2, True],
    'mototaxi': [mototaxi_sprite, 80, 2, True],

    'classB': [classB_sprite, 120, 2, True],
    'classC': [classC_sprite, 120, 3, True],
    'classD': [classD_sprite, 160, 5, True],
}

obstacles = {
    'missile': [missile_sprite, 80, 0, False],
    'barrier': [barrier_sprite, 80, 0, False],
    'tumbleweed': [tumbleweed_sprite, 80, 0, False],
}

# Keys lists for each hand
HAND_KEYS = [
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
left_letters = load_text('left_letters')
right_letters = load_text('right_letters')
all_words = load_text('all_words')

words_2 = load_text('words_2')
words_3 = load_text('words_3')
words_4 = load_text('words_4')
words_5 = load_text('words_5')
words_6 = load_text('words_6')
words_7 = load_text('words_7')
words_8 = load_text('words_8')

# Player configuration
player_pos = ((SCREEN_WIDTH // 3) - 100,
                   SCREEN_HEIGHT - 235)

# Hands configuration
x_padding = 280
y_padding = 90

left_hand_pos = (x_padding, SCREEN_HEIGHT - y_padding)
right_hand_pos = (SCREEN_WIDTH - x_padding, SCREEN_HEIGHT - y_padding)

menu_ui = pygame.image.load(f"assets/side_interface.png").convert_alpha()
menu_ui = pygame.transform.scale(menu_ui, (SCREEN_WIDTH, SCREEN_HEIGHT))
menu_ui.fill(COLORS.black[0], special_flags=pygame.BLEND_RGBA_MULT)

score_path = f"assets/coins.png"
score_image = pygame.image.load(score_path).convert_alpha()
score_image = pygame.transform.scale(score_image, (40, 40))

menu_score_image = pygame.image.load(score_path).convert_alpha()
menu_score_image = pygame.transform.scale(score_image, (50, 50))

locked_score_image = pygame.image.load(score_path).convert_alpha()
locked_score_image = pygame.transform.scale(score_image, (40, 40))

death_score_image = pygame.image.load(score_path).convert_alpha()
death_score_image = pygame.transform.scale(score_image, (60, 60))

evil_face = pygame.image.load(f"assets/evil_face.png").convert_alpha()
evil_face = pygame.transform.scale(evil_face, (45, 45))

bullet_train = pygame.image.load(f"assets/stages/2/bullet_train.png").convert_alpha()
bullet_train_rect = bullet_train.get_rect()
bullet_train_size = (750, 450)
bullet_train = pygame.transform.scale(bullet_train, bullet_train_size)
bullet_train_rect.center = (-10, SCREEN_HEIGHT // 1.5)
bullet_train_speed = 5

# ZH4R0V Dubs
zharov_speech1 = pygame.mixer.Sound('assets/stages/2/zharov_speech1.wav')
zharov_speech1.set_volume(1.0)
zharov_speech2 = pygame.mixer.Sound('assets/stages/2/zharov_speech2.wav')
zharov_speech2.set_volume(1.0)
zharov_power = pygame.mixer.Sound('assets/stages/2/zharov_power.wav')
zharov_power.set_volume(1.0)
zharov_speech3 = pygame.mixer.Sound('assets/stages/2/zharov_speech3.wav')
zharov_speech3.set_volume(1.0)
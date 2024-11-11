"""
Module to load every starter asset when initializing the game,
separated from the game module to find every variable easily.

Always try to create constants or important game assets here,
so you don't have to constantly get them from other scripts.
"""

import pygame

from modules import player as plr
from modules import hands

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

def load_game(game):
    # Screen size and frames per second
    game.SCREEN_WIDTH, game.SCREEN_HEIGHT = 800, 600
    game.FPS = 60
    game.tick = 0
    game.screen = pygame.display.set_mode((800, 600))
    game.COLORS = colors()
    game.level = None

    # game loop
    game.clock = pygame.time.Clock()
    game.running = True
    game.paused = False
    game.game_state = 'menu'
    game.level = None

    game.LV0_NAME = '0 - TUTORIAL'
    game.LV1_NAME = '1 - Chapter 1'
    game.LV2_NAME = '2 - Chapter 2'

    game.BASE_FLOOR_SPEED = 5
    game.BASE_BG_SPEED = 2
    game.BASE_FLOOR_LIGHTS_COLOR = game.COLORS.bright_cyan
    game.floor_speed = game.BASE_FLOOR_SPEED
    game.bg_speed = game.BASE_BG_SPEED

    game.DARK_FILTER = pygame.Surface(
        (game.SCREEN_WIDTH, game.SCREEN_HEIGHT), pygame.SRCALPHA)
    game.DARK_FILTER.fill((0, 0, 0, 100))

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

    # Initialize sprite groups
    game.all_sprites = pygame.sprite.Group()
    game.enemies = pygame.sprite.Group()

    game.screen = pygame.display.set_mode(
        (game.SCREEN_WIDTH, game.SCREEN_HEIGHT))
    pygame.display.set_caption("Typing Chase - PyGame Edition - 2024-10-26")

    # Enemy sprites
    game.target = '/game_assets/enemy_sprites/target.png'
    game.minibot = './game_assets/enemy_sprites/minibot.png'
    game.type1_robot = '/game_assets/enemy_sprites/classB_robot.png'
    game.type2_robot = '/game_assets/enemy_sprites/classC_robot.png'
    game.type1_robot = '/game_assets/enemy_sprites/classD_robot.png'

    game.enemy_sprites = './game_assets/enemy_sprites/'

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

    # Left keys list by rows
    game.left_top_row = ["q", "w", "e", "r", "t"]
    game.left_middle_row = ["a", "s", "d", "f", "g"]
    game.left_bottom_row = ["z", "x", "c", "v", "b"]

    # Right keys list by rows
    game.right_top_row = ["y", "u", "i", "o", "p"]
    game.right_middle_row = ["h", "j", "k", "l", "ç"]
    game.right_bottom_row = ["n", "m", ",", ".", ";"]

    # Creating player
    game.player_pos = ((game.SCREEN_WIDTH // 3) - 100,
                    game.SCREEN_HEIGHT - 235)

    game.player = plr.Player(game.player_pos)

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

    game.menu_ui = pygame.image.load(f"./game_assets/side_interface.png").convert_alpha()
    game.menu_ui = pygame.transform.scale(game.menu_ui, (game.SCREEN_WIDTH, game.SCREEN_HEIGHT))
    game.menu_ui.fill(game.COLORS.black[0], special_flags=pygame.BLEND_RGBA_MULT)

    game.score_image = pygame.image.load(f"./game_assets/coins.png").convert_alpha()
    game.score_image = pygame.transform.scale(game.score_image, (40, 40))

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

    # Musics
    game.menu_music = pygame.mixer.Sound('./game_assets/music/Jesse James.mp3')
    game.menu_music.set_volume(0.5)
    game.lvl0_music = pygame.mixer.music.load('./game_assets/music/level0.mp3')
    game.lvl1_music = pygame.mixer.Sound('./game_assets/music/level1.mp3')
    game.menace_music = pygame.mixer.Sound('./game_assets/music/The Ring - Klonoa.mp3')
    game.menace_music.set_volume(0.5)
    game.lvl2_music = pygame.mixer.Sound('./game_assets/music/level2.mp3')

    # ZH4R0V Dubs
    game.zharov_speech1 = pygame.mixer.Sound('./game_assets/stages/2/zharov_speech1.mp3')
    game.zharov_speech1.set_volume(0.8)
    game.zharov_speech2 = pygame.mixer.Sound('./game_assets/stages/2/zharov_speech2.mp3')
    game.zharov_speech2.set_volume(0.8)
    game.zharov_power = pygame.mixer.Sound('./game_assets/stages/2/zharov_power.mp3')
    game.zharov_power.set_volume(0.8)
    game.zharov_speech3 = pygame.mixer.Sound('./game_assets/stages/2/zharov_speech3.mp3')
    game.zharov_speech3.set_volume(0.8)

    # Fonts
    game.title_font = pygame.font.Font('./game_assets/font.otf', 90)
    game.large_font = pygame.font.Font('./game_assets/font.otf', 60)
    game.header_font = pygame.font.Font('./game_assets/font.otf', 40)
    game.text_font = pygame.font.Font('./game_assets/font.otf', 32)
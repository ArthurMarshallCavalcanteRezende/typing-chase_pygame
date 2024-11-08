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
    red = (255, 0, 0),
    bright_red = (255, 150, 150),
    yellow = (255, 255, 0),
    bright_yellow = (255, 255, 150),
    magenta = (255, 0, 255),
    green = (255, 0, 0),
    blue = (0, 0, 255),
    cyan = (0, 255, 255),


def load_game(game):
    # Screen size and frames per second
    game.SCREEN_WIDTH, game.SCREEN_HEIGHT = 800, 600
    game.FPS = 60

    # game loop
    game.clock = pygame.time.Clock()
    game.running = True
    game.paused = False
    game.enemy_spawn_time = 0
    game.spawn_interval = 2000
    game.enemy_speed = 2
    game.level = 1

    game.COLORS = colors()

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

    # Enemy images mapping
    game.all_keys = [
        # Left keys
        'q', 'w', 'e', 'r', 't', 'a', 's', 'd', 'f', 'g'
        'z', 'x', 'c', 'v', 'b'

        # Right keys
        'y', 'u', 'i', 'o', 'p', 'h', 'j', 'k',
        'l',  # 'ç' -- not working yet
        'n', 'm', ',', '.', ';'
    ]

    game.enemy_left = {
        'q': './game_assets/left_enemies/Qrobot.png',
        'w': './game_assets/left_enemies/Wrobot.png',
        'e': './game_assets/left_enemies/Erobot.png',
        'r': './game_assets/left_enemies/Rrobot.png',
        't': './game_assets/left_enemies/Trobot.png',
        'a': './game_assets/left_enemies/Arobot.png',
        's': './game_assets/left_enemies/Srobot.png',
        'd': './game_assets/left_enemies/Drobot.png',
        'f': './game_assets/left_enemies/Frobot.png',
        'g': './game_assets/left_enemies/Grobot.png',
        'z': './game_assets/left_enemies/Zrobot.png',
        'x': './game_assets/left_enemies/Xrobot.png',
        'c': './game_assets/left_enemies/Crobot.png',
        'v': './game_assets/left_enemies/Vrobot.png',
        'b': './game_assets/left_enemies/Brobot.png',
    }

    game.enemy_right = {
        'y': './game_assets/right_enemies/Yrobot.png',
        'u': './game_assets/right_enemies/Urobot.png',
        'i': './game_assets/right_enemies/Irobot.png',
        'o': './game_assets/right_enemies/Orobot.png',
        'p': './game_assets/right_enemies/Probot.png',
        'h': './game_assets/right_enemies/Hrobot.png',
        'j': './game_assets/right_enemies/Jrobot.png',
        'k': './game_assets/right_enemies/Krobot.png',
        'l': './game_assets/right_enemies/Lrobot.png',
        # This keys doesn't seem to work with pygame for some reason
        # 'ç': './game_assets/right_enemies/CEDrobot.png',
        'n': './game_assets/right_enemies/Nrobot.png',
        'm': './game_assets/right_enemies/Mrobot.png',
        ',': './game_assets/right_enemies/COMMArobot.png',
        '.': './game_assets/right_enemies/DOTrobot.png',
        ';': './game_assets/right_enemies/SemiColon_robot.png',
    }

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
                    game.SCREEN_HEIGHT - 250)

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

    # Stage image
    game.stage_back = pygame.transform.scale(pygame.image.load("./game_assets/hunt_stage.png").convert_alpha(),
                                          (800, 600))
    game.tutorial_stage = pygame.transform.scale(
        pygame.image.load("./game_assets/stages/tutorial_stage.png").convert_alpha(),
        (800, 600))

    # Sounds
    game.chase_music = pygame.mixer.Sound('./game_assets/Too Good Too Bad.mp3')
    game.chase_music.set_volume(0.2)

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

    game.chase_music.play(-1)

    # Fonts
    game.font = pygame.font.Font(None, 36)
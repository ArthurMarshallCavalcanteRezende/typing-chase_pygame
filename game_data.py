"""
Module to load every starter asset when initializing the game,
separated from the game module to find every variable easily.

Always try to create constants or important game assets here,
so you don't have to constantly get them from other scripts.
"""

import pygame

from modules import player as plr
from modules import hands
from modules import background as bg

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
    game.COLORS = colors()
    game.level = None

    # game loop
    game.clock = pygame.time.Clock()
    game.running = True
    game.paused = False
    game.enemy_spawn_time = 0
    game.spawn_interval = 2000
    game.enemy_speed = 2
    game.game_state = 'menu'
    game.level = 1

    game.BASE_FLOOR_SPEED = 5
    game.BASE_BG_SPEED = 2
    game.BASE_FLOOR_LIGHTS_COLOR = game.COLORS.bright_cyan[0]
    game.floor_speed = game.BASE_FLOOR_SPEED
    game.bg_speed = game.BASE_BG_SPEED

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

    # Stage terrain images and values
    game.floor_image = pygame.image.load(
        "./game_assets/background/floor.png").convert_alpha()
    game.floor_image = pygame.transform.scale(game.floor_image, (250, 250))

    game.bg_image = pygame.image.load(
        "./game_assets/background/background.png").convert_alpha()
    game.bg_image = pygame.transform.scale(
        game.bg_image, (game.SCREEN_HEIGHT, game.SCREEN_HEIGHT))

    game.bg_pillar_image = pygame.image.load(
        "./game_assets/background/background_pillar.png").convert_alpha()
    game.bg_pillar_image = pygame.transform.scale(
        game.bg_pillar_image, (game.SCREEN_HEIGHT, game.SCREEN_HEIGHT))

    game.floor_lights = pygame.Surface((game.SCREEN_WIDTH, game.floor_image.get_size()[1] // 10))
    game.floor_lights.fill(game.BASE_FLOOR_LIGHTS_COLOR)

    game.floor_neon = pygame.Surface((game.SCREEN_WIDTH, game.floor_image.get_size()[1]))
    game.floor_neon.fill(game.COLORS.black[0])

    game.floor_index = 0
    game.bg_index = 0
    game.max_floor = None
    game.max_bg = None

    game.floor_y = game.SCREEN_HEIGHT - (game.floor_image.get_size()[1] // 4)
    game.bg_y = (game.bg_image.get_size()[1] // 2)
    new_floor_pos = (0, game.floor_y)
    new_bg_pos = (0, game.bg_y)

    # Adding initial floor chunks
    while new_floor_pos[0] < game.SCREEN_WIDTH:
        new_floor = bg.Terrain(game, 'floor')
        new_floor.rect.center = new_floor_pos
        new_floor_pos = (new_floor_pos[0] + new_floor.size[0], game.floor_y)
        game.max_floor = new_floor

        game.floor_sprites.append(new_floor)
    # Adding initial background chunks
    while new_bg_pos[0] < game.SCREEN_WIDTH:
        new_bg = bg.Terrain(game, 'background')
        new_bg.rect.center = new_bg_pos
        new_bg_pos = (new_bg_pos[0] + new_bg.size[0], game.bg_y)
        game.max_bg = new_bg

        game.background_sprites.append(new_bg)

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

    # Fonts
    game.font = pygame.font.Font(None, 36)
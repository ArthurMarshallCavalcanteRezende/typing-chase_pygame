from unittest.mock import right

import pygame
import random
from modules import enemy as en
from modules import player as plr
from modules import hands

pygame.init()

# Define colors
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

HAND_COLORS = {
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


# Screen size
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

# Initialize sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Typing Chase - PyGame Edition - 2024-10-22")

# Enemy images mapping
enemy_left = {
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

enemy_right = {
    'y': './game_assets/right_enemies/Yrobot.png',
    'h': './game_assets/right_enemies/Hrobot.png',
    'n': './game_assets/right_enemies/Nrobot.png',
    'u': './game_assets/right_enemies/Urobot.png',
    'j': './game_assets/right_enemies/Jrobot.png',
    'm': './game_assets/right_enemies/Mrobot.png',
    'i': './game_assets/right_enemies/Irobot.png',
    'k': './game_assets/right_enemies/Krobot.png',
    ',': './game_assets/right_enemies/COMMArobot.png',
    'o': './game_assets/right_enemies/Orobot.png',
    'l': './game_assets/right_enemies/Lrobot.png',
    '.': './game_assets/right_enemies/DOTrobot.png',
    'p': './game_assets/right_enemies/Probot.png',
    'ç': './game_assets/right_enemies/CEDrobot.png',
    ';': './game_assets/right_enemies/SemiColon_robot.png',
}

# Keys lists for each hand
HAND_KEYS = [
    [   # Left Hand
        ['left', 'thumb', [' ']],
        ['left','index', ['v', 'b', 'f', 'g', 'r', 't', '4', '5']],
        ['left','middle', ['c', 'd', 'e', '3']],
        ['left','ring', ['x', 's', 'w', '2']],
        ['left','pinkie', ['z', 'a', 'q', '1']],
    ],
    [   # Right Hand
        ['right', 'thumb', [' ']],
        ['right', 'index', ['n', 'm', 'h', 'j', 'y', 'u', '6', '7']],
        ['right', 'middle', [',', 'k', 'i', '8']],
        ['right', 'ring', ['.', 'l', 'o', '9']],
        ['right', 'pinkie', [';', 'ç', 'p', '0']],
    ]
]

# Left keys list by rows
left_top_row = ["q", "w", "e", "r", "t"]
left_middle_row = ["a", "s", "d", "f", "g"]
left_bottom_row = ["z", "x", "c", "v", "b"]

# Right keys list by rows
right_top_row = ["y", "u", "i", "o", "p"]
right_middle_row = ["h", "j", "k", "l", "ç"]
right_bottom_row = ["n", "m", ",", ".", ";"]

# Creating player
player = plr.Player()

# Hands Sprites
left_hand_path = "./game_assets/hands/left_hand"
right_hand_path = "./game_assets/hands/right_hand"
x_padding = 280
y_padding = 90

left_hand_pos = (x_padding, SCREEN_HEIGHT - y_padding)
right_hand_pos = (SCREEN_WIDTH - x_padding, SCREEN_HEIGHT - y_padding)

left_hand = hands.Hands(left_hand_path, left_hand_pos, HAND_COLORS['left'])
right_hand = hands.Hands(right_hand_path, right_hand_pos, HAND_COLORS['right'])
left_hand.side = 'left'
right_hand.side = 'right'

# Stage image
stage_back = pygame.transform.scale(pygame.image.load("./game_assets/hunt_stage.png").convert_alpha(), (800, 600))

# Sounds
chase_music = pygame.mixer.Sound('./game_assets/Too Good Too Bad.mp3')
chase_music.set_volume(0.3)
chase_music.play(-1)

# Adding enemies
def spawn_random_enemy(lvl):
    if lvl == 1:
        enemy_key = random.choice(list(enemy_left.keys()))
        enemy_image_path = enemy_left[enemy_key]
    elif lvl == 2:
        enemy_key = random.choice(list(enemy_right.keys()))
        enemy_image_path = enemy_left[enemy_key]
    elif lvl == 3:
        enemy_key = random.choice(list(enemy_left.keys() + enemy_right.keys()))
        if enemy_key in enemy_left:
            enemy_image_path = enemy_left[enemy_key]
        else:
            enemy_image_path = enemy_right[enemy_key]

    enemy = en.Enemy(enemy_image_path)

    # Set the row based on the key
    if enemy_key in left_top_row:
        enemy.rect.y = 30  # Top row
    elif enemy_key in left_middle_row:
        enemy.rect.y = 150  # Middle row
    elif enemy_key in left_bottom_row:
        enemy.rect.y = 300  # Bottom row
    elif enemy_key in right_top_row:
        enemy.rect.y = 30  # Top row
    elif enemy_key in right_middle_row:
        enemy.rect.y = 150  # Middle row
    elif enemy_key in right_bottom_row:
        enemy.rect.y = 300  # Bottom row

    found_finger = None

    for hand in HAND_KEYS:
        if found_finger: break

        for finger in hand:
            if found_finger: break

            for current_key in finger[2]:
                if current_key == enemy_key:
                    found_finger = finger
                    break

    if found_finger: enemy.finger_highlight = found_finger
    enemy.rect.x = SCREEN_WIDTH  # Start at the right edge
    enemies.add(enemy)
    all_sprites.add(enemy)

# Game loop
clock = pygame.time.Clock()
running = True
enemy_spawn_time = 0
spawn_interval = 2000
level = 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for key presses
        if event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)
            print(f"Key pressed: {key}")  # Debugging output
            for enemy in enemies:
                print(f"Checking enemy: {enemy.key}")  # Debugging output
                if enemy.key == key and enemy == player.closest_enemy:
                    print(f"Enemy defeated: {enemy.key}")  # Debugging output
                    enemies.remove(enemy)
                    all_sprites.remove(enemy)
                    break

    current_time = pygame.time.get_ticks()
    if current_time - enemy_spawn_time > spawn_interval:
        spawn_random_enemy(level)
        enemy_spawn_time = current_time

    all_sprites.update()

    closest_to_plr = [None, 99999]

    # Checking enemy conditions
    for enemy in enemies:
        # If enemy is the current to the player
        player_magnitude = enemy.rect.x - (SCREEN_WIDTH // 2) - 50
        if player_magnitude < closest_to_plr[1]:
            closest_to_plr = [enemy, player_magnitude]

        # If enemy passed the limit to damage player
        if enemy.rect.x < (SCREEN_WIDTH // 2) - 50:
            player.lives -= 1
            enemies.remove(enemy)
            all_sprites.remove(enemy)
            player.max_points -= 1

    # Updating the closest enemy to the player
    if closest_to_plr[0]:
        player.closest_enemy = closest_to_plr[0]

    left_hand.update(player.closest_enemy)
    right_hand.update(player.closest_enemy)

    if player.max_points == 0:
        level += 1
        if level == 2:
            player.max_points += 30
        elif level == 3:
            player.max_points += 30

    if player.lives <= 0:
        print("Game Over")
        running = False

    screen.blit(stage_back, (0, 0))
    all_sprites.draw(screen)

    left_hand.draw(screen)
    right_hand.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

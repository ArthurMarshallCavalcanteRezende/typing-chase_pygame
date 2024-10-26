from unittest.mock import right

import pygame
import random
from modules import enemy as en
from modules import hands

pygame.init()

# Define colors
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

# Screen size
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

# Initialize sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
hands_sprites = pygame.sprite.Group()

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

# Left keys list by rows
left_top_row = ["q", "w", "e", "r", "t"]
left_middle_row = ["a", "s", "d", "f", "g"]
left_bottom_row = ["z", "x", "c", "v", "b"]

# Right keys list by rows
right_top_row = ["y", "u", "i", "o", "p"]
right_middle_row = ["h", "j", "k", "l", "ç"]
right_bottom_row = ["n", "m", ",", ".", ";"]

# Hands Sprites
left_hand = hands.Hands("./game_assets/hands/left_hand/hand.png", position=(200, 450))
right_hand = hands.Hands("./game_assets/hands/right_hand/hand.png", position=(550, 450))
hands_sprites.add(left_hand, right_hand)

# Stage image
stage_back = pygame.transform.scale(pygame.image.load("./game_assets/hunt_stage.png").convert_alpha(), (800, 600))

# Sounds
chase_music = pygame.mixer.Sound('./game_assets/Too Good Too Bad.mp3')
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

    enemy.rect.x = SCREEN_WIDTH  # Start at the right edge
    enemies.add(enemy)
    all_sprites.add(enemy)

# Player lives and error counts
lives = 3
max_points = 25

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
                if enemy.key == key:
                    print(f"Enemy defeated: {enemy.key}")  # Debugging output
                    enemies.remove(enemy)
                    all_sprites.remove(enemy)
                    break

    current_time = pygame.time.get_ticks()
    if current_time - enemy_spawn_time > spawn_interval:
        spawn_random_enemy(level)
        enemy_spawn_time = current_time

    all_sprites.update()

    # Check if any enemy has passed the center
    for enemy in enemies:
        if enemy.rect.x < (SCREEN_WIDTH // 2) - 50:
            lives -= 1
            enemies.remove(enemy)
            all_sprites.remove(enemy)
            max_points -= 1

    if max_points == 0:
        level += 1
        if level == 2:
            max_points += 30
        elif level == 3:
            max_points += 30

    if lives <= 0:
        print("Game Over")
        running = False

    screen.blit(stage_back, (0, 0))
    all_sprites.draw(screen)
    hands_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

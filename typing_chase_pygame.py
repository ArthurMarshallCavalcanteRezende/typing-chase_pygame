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

# List of keys by rows
top_row = ["q", "w", "e", "r", "t"]
middle_row = ["a", "s", "d", "f", "g"]
bottom_row = ["z", "x", "c", "v", "b"]

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
def spawn_random_enemy():
    enemy_key = random.choice(list(enemy_left.keys()))
    enemy_image_path = enemy_left[enemy_key]
    enemy = en.Enemy(enemy_image_path)

    # Set the row based on the key
    if enemy_key in top_row:
        enemy.rect.y = 30  # Top row
    elif enemy_key in middle_row:
        enemy.rect.y = 150  # Middle row
    elif enemy_key in bottom_row:
        enemy.rect.y = 300  # Bottom row

    enemy.rect.x = SCREEN_WIDTH  # Start at the right edge
    enemies.add(enemy)
    all_sprites.add(enemy)

# Player lives and error counts
lives = 10

# Game loop
clock = pygame.time.Clock()
running = True
enemy_spawn_time = 0
spawn_interval = 2000

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for key presses
        if event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)
            for enemy in enemies:
                if enemy.key == key:
                    enemies.remove(enemy)
                    all_sprites.remove(enemy)
                    break


    current_time = pygame.time.get_ticks()
    if current_time - enemy_spawn_time > spawn_interval:
        spawn_random_enemy()
        enemy_spawn_time = current_time

    all_sprites.update()

    # Check if any enemy has passed the center
    for enemy in enemies:
        if enemy.rect.x < (SCREEN_WIDTH // 2) - 50:
            lives -= 1
            enemies.remove(enemy)
            all_sprites.remove(enemy)

    if lives <= 0:
        print("Game Over")
        running = False

    screen.blit(stage_back, (0, 0))
    all_sprites.draw(screen)
    hands_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

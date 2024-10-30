from unittest.mock import right

import pygame
import random
import sys
from modules import enemy as en
from modules import player as plr
from modules import hands

pygame.init()

# Define colors
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BRIGHT_YELLOW = (255, 255, 150)

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
pygame.display.set_caption("Typing Chase - PyGame Edition - 2024-10-26")

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

try:
    # Creating player
    player_pos = ((SCREEN_WIDTH // 3) - 100, SCREEN_HEIGHT - 250)

    player = plr.Player(player_pos)

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

    # Soundz
    chase_music = pygame.mixer.Sound('./game_assets/Too Good Too Bad.mp3')
    chase_music.set_volume(0.2)
    chase_music.play(-1)
    destroy_sound = pygame.mixer.Sound('./game_assets/sfx/explosion.wav')
    destroy_sound.set_volume(0.3)
    points_sound = pygame.mixer.Sound('./game_assets/sfx/points.wav')
    points_sound.set_volume(0.7)
    damage_sound = pygame.mixer.Sound('./game_assets/sfx/damage.wav')
    damage_sound.set_volume(0.6)
    levelup_sound = pygame.mixer.Sound('./game_assets/sfx/levelup.wav')
    levelup_sound.set_volume(0.5)
    wrong_sound = pygame.mixer.Sound('./game_assets/sfx/wrong_input.wav')
    wrong_sound.set_volume(0.4)
    get_life_sound = pygame.mixer.Sound('./game_assets/sfx/get_life.wav')
    get_life_sound.set_volume(0.5)



    # Fonts
    font = pygame.font.Font(None, 36)
except Exception as e:
    print(f"Error while loading recourses: {e}")
    print(f"Check if any files have been changed or renamed.")
    pygame.quit()
    sys.exit()

# Game loop
clock = pygame.time.Clock()
running = True
game_paused = False
enemy_spawn_time = 0
spawn_interval = 2000
enemy_speed = 2
level = 1

''' -----========== FUNCTIONS ==========----- '''
# Adding enemies
def spawn_random_enemy(lvl):
    if lvl == 1:
        enemy_dict = enemy_left
    elif lvl == 2:
        enemy_dict = enemy_right
    else:
        enemy_dict = {**enemy_left, **enemy_right}

    enemy_key = random.choice(list(enemy_dict.keys()))
    enemy_image_path = enemy_dict[enemy_key]

    try:
        # Creating the enemy and setting its key
        enemy = en.Enemy(enemy_image_path, enemy_speed)
        enemy.key = enemy_key

        # Set the row based on the key given
        if enemy_key in left_top_row or enemy_key in right_top_row:
            enemy.rect.y = 30
        elif enemy_key in left_middle_row or enemy_key in right_middle_row:
            enemy.rect.y = 150
        elif enemy_key in left_bottom_row or enemy_key in right_bottom_row:
            enemy.rect.y = 300
        enemy.rect.x = SCREEN_WIDTH
        enemies.add(enemy)
        all_sprites.add(enemy)
    except Exception as e:
        print(f"Error while spawning enemy: {e}")

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


def reset_game():
    """RESET ALL GAME VARIABLES FOR RESTART OR NEW LEVEL"""
    global level, spawn_interval, enemy_speed
    player.lives = 3
    player.score = 0
    player.combo = 0
    player.max_combo = 0
    player.levelup_req = 800
    player.level_multi = 1

    enemy_speed = 3
    level = 1
    spawn_interval = 2000

    enemies.empty()
    all_sprites.empty()


def level_player():
    global spawn_interval, level, enemy_speed

    if player.score >= player.levelup_req:
        new_req = 4

        if player.levelup_req < 1000:
            new_req = 4
        elif player.levelup_req < 10000:
            new_req = 3
        elif player.levelup_req < 50000:
            new_req = 2
        elif player.levelup_req < 250000:
            new_req = 1.5

        levelup_sound.play()
        player.levelup_req = int(player.levelup_req * new_req)
        level += 1
        player.level_multi += 1
        player.lives += 1 if player.lives < 10 else 0


    # Updating difficulty every frame
    if level == 2:
        enemy_speed = 3
        spawn_interval = random.randint(1500, 2500)
    elif level == 3:
        spawn_interval = random.randint(1200, 2200)
    elif level >= 4:
        lowest_interval = 1000 - (30 * level)
        highest_interval = 1800 - (20 * level)
        if lowest_interval < 500: lowest_interval = 500
        if highest_interval < 1000: highest_interval = 1000

        spawn_interval = random.randint(lowest_interval, highest_interval)

        # Getting random speed value depending on corresponding weight chance
        speed_values = [3, 4]
        speed_odds = [40, 20]

        if level == 5:
            speed_values = [3, 4, 5]
            speed_odds = [40, 30, 5]
        elif level > 5:
            speed_values = [3, 4, 5, 6]
            speed_odds = [30, 30, 5 + level, level]

        enemy_speed = random.choices(speed_values, speed_odds)[0]


try:
    while running:
        current_time = pygame.time.get_ticks()
        player_action = None

        # Handling all pygame events, including keys pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = not game_paused
                if not game_paused and player.lives > 0:
                    key = pygame.key.name(event.key)
                    enemy_hit = False

                    for enemy in enemies.copy():
                        # Check if enemy is the right key and closest to player
                        if enemy.key == key and enemy == player.closest_enemy:
                            destroy_sound.play()
                            points_sound.play()

                            enemies.remove(enemy)
                            all_sprites.remove(enemy)

                            # Rewarding with score and combo
                            player.score += 10 * (player.combo + 1) * player.level_multi
                            player.combo += 1
                            player.max_combo = max(player.combo, player.max_combo)

                            if (player.combo > 0 and player.combo % 10 == 0
                                    and player.lives < 5):
                                player.lives += 1
                                get_life_sound.play()

                            enemy_hit = True

                            # Getting the right animation for the player to play
                            if enemy.key in left_top_row or enemy.key in right_top_row:
                                player_action = 'right_shoot_top'
                            elif enemy.key in left_middle_row or enemy.key in right_middle_row:
                                player_action = 'right_shoot_middle'
                            elif enemy.key in left_bottom_row or enemy.key in right_bottom_row:
                                player_action = 'right_shoot_down'

                            break
                    if not enemy_hit:
                        wrong_sound.play()
                        player.combo = 0


        player.on_input(player_action)

        if not game_paused and player.lives > 0:
            # Enemy spawning every interval
            if current_time - enemy_spawn_time > spawn_interval:
                spawn_random_enemy(level)
                enemy_spawn_time = current_time

            # Updating all sprites
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
                destroy_sound.play()
                damage_sound.play()

                player.lives -= 1
                player.combo = 0
                enemies.remove(enemy)
                all_sprites.remove(enemy)

        # Updating the closest enemy to the player
        if closest_to_plr[0]:
            player.closest_enemy = closest_to_plr[0]

        left_hand.update(player.closest_enemy)
        right_hand.update(player.closest_enemy)

        # Changing levels based off player score
        level_player()

        screen.blit(stage_back, (0, 0))
        all_sprites.draw(screen)

        left_hand.draw(screen)
        right_hand.draw(screen)
        player.draw(screen)

        # Setting user interface
        score_text = font.render(f'Score: {player.score}', True, COLOR_WHITE)
        lives_text = font.render(f'Lives: {player.lives}', True, COLOR_WHITE)
        combo_text = font.render(f'Combo: {player.combo}', True, COLOR_WHITE)
        level_text = font.render(f'Level: {level}', True, COLOR_WHITE)
        next_level_text = font.render(f'Next level: {player.levelup_req} score',
                                      True, COLOR_BRIGHT_YELLOW)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 40))
        screen.blit(combo_text, (10, 70))
        screen.blit(level_text, (10, 100))
        screen.blit(next_level_text, (10, 180))

        if game_paused:
            pause_text = font.render('PAUSED - Press ESC to continue', True,
                                     COLOR_WHITE)
            screen.blit(pause_text,
                        (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

        # Game Over
        if player.lives <= 0:
            game_over_text = font.render('GAME OVER', True, COLOR_RED)
            final_score_text = font.render(f'Final Score: {player.score}', True,
                                           COLOR_WHITE)
            level_reached_text = font.render(f'Congrats! You reached level {level}!',
                                         True, COLOR_WHITE)
            max_combo_text = font.render(f'Max Combo: {player.max_combo}', True,
                                         COLOR_WHITE)
            restart_text = font.render('Press SPACE to restart or ESC to quit',
                                       True, COLOR_WHITE)
            screen.blit(game_over_text,
                        (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100))
            screen.blit(level_reached_text,
                        (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
            screen.blit(final_score_text,
                        (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20))
            screen.blit(max_combo_text,
                        (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 10))
            screen.blit(restart_text,
                        (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 70))
            pygame.display.flip()

            # Wait for player input
            waiting = True

            while waiting and running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        waiting = False
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            reset_game()
                            waiting = False
                        elif event.key == pygame.K_ESCAPE:
                            waiting = False
                            running = False

        pygame.display.flip()
        clock.tick(FPS)
except Exception as e:
    print(f"Error while trying to run TYPING-CHASE: {e}")
finally:
    pygame.quit()
    sys.exit()

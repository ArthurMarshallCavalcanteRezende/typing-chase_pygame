"""
Module to run every function in the game, most important functions should be here
"""

import pygame
import random

from modules import enemy as en

''' -----========== FUNCTIONS ==========----- '''
# Function to spawn an enemy depending on game level
def spawn_random_enemy(game):
    if game.level == 1:
        enemy_dict = game.enemy_left
    elif game.level == 2:
        enemy_dict = game.enemy_right
    else:
        enemy_dict = {**game.enemy_left, **game.enemy_right}

    enemy_key = random.choice(list(enemy_dict.keys()))
    enemy_image_path = enemy_dict[enemy_key]

    # Creating the enemy and setting its key
    enemy = en.Enemy(enemy_image_path, game.enemy_speed)
    enemy.key = enemy_key

    # Set the row based on the key given
    if enemy_key in game.left_top_row or enemy_key in game.right_top_row:
        enemy.rect.y = 30
    elif enemy_key in game.left_middle_row or enemy_key in game.right_middle_row:
        enemy.rect.y = 150
    elif enemy_key in game.left_bottom_row or enemy_key in game.right_bottom_row:
        enemy.rect.y = 300
    enemy.rect.x = game.SCREEN_WIDTH
    game.enemies.add(enemy)
    game.all_sprites.add(enemy)

    found_finger = None

    for hand in game.HAND_KEYS:
        if found_finger: break

        for finger in hand:
            if found_finger: break

            for current_key in finger[2]:
                if current_key == enemy_key:
                    found_finger = finger
                    break

    if found_finger: enemy.finger_highlight = found_finger
    enemy.rect.x = game.SCREEN_WIDTH  # Start at the right edge
    game.enemies.add(enemy)
    game.all_sprites.add(enemy)


def reset_game(game):
    """RESET ALL GAME VARIABLES FOR RESTART OR NEW LEVEL"""
    game.player.lives = 3
    game.player.score = 0
    game.player.combo = 0
    game.player.max_combo = 0
    game.player.levelup_req = 800
    game.player.level_multi = 1

    game.enemy_speed = 2
    game.level = 1
    game.spawn_interval = 2000

    game.enemies.empty()
    game.all_sprites.empty()


# Function to move to a new level once reached enough points
def level_player(game):
    if game.player.score >= game.player.levelup_req:
        new_req = 4

        if game.player.levelup_req < 1000:
            new_req = 4
        elif game.player.levelup_req < 10000:
            new_req = 3
        elif game.player.levelup_req < 50000:
            new_req = 2
        elif game.player.levelup_req < 250000:
            new_req = 1.5

        game.levelup_sound.play()
        game.player.levelup_req = int(game.player.levelup_req * new_req)
        game.level += 1
        game.player.level_multi += 1
        game.player.lives += 1 if game.player.lives < 10 else 0

    # Updating difficulty every frame
    if game.level == 2:
        game.enemy_speed = 3
        game.spawn_interval = random.randint(1600, 2000)
    elif game.level == 3:
        game.enemy_speed = 3
        game.spawn_interval = random.randint(1200, 1800)
    elif game.level >= 4:
        lowest_interval = 800 - (30 * game.level)
        highest_interval = 1800 - (20 * game.level)
        if lowest_interval < 400: lowest_interval = 400
        if highest_interval < 1000: highest_interval = 1000

        game.spawn_interval = random.randint(lowest_interval, highest_interval)

        # Getting random speed value depending on corresponding weight chance
        speed_values = [1, 2, 3]
        speed_odds = [60, 40, 20]

        if game.level >= 5:
            speed_values = [1, 2, 3, 4, 5]
            speed_odds = [40, 40, 30, 20, game.level]

        game.enemy_speed = random.choices(speed_values, speed_odds)[0]


def check_enemy_hit(game, event):
    key = pygame.key.name(event.key)
    enemy_hit = False
    player_action = None

    for enemy in game.enemies.copy():
        # Check if enemy is the right key
        if enemy.key == key:
            game.destroy_sound.play()
            game.points_sound.play()

            game.enemies.remove(enemy)
            game.all_sprites.remove(enemy)

            # Rewarding with score and combo
            game.player.score += 10 * (game.player.combo + 1) * game.player.level_multi
            game.player.combo += 1
            game.player.max_combo = max(game.player.combo, game.player.max_combo)

            if (game.player.combo > 0 and game.player.combo % 10 == 0
                    and game.player.lives < 5):
                game.player.lives += 1
                game.get_life_sound.play()

            enemy_hit = True

            # Getting the right animation for the player to play
            if enemy.key in game.left_top_row or enemy.key in game.right_top_row:
                player_action = 'right_shoot_top'
            elif enemy.key in game.left_middle_row or enemy.key in game.right_middle_row:
                player_action = 'right_shoot_middle'
            elif enemy.key in game.left_bottom_row or enemy.key in game.right_bottom_row:
                player_action = 'right_shoot_down'

    if enemy_hit:
        return player_action
    else:
        game.wrong_sound.play()
        game.player.combo = 0


# Main function to run the game
def run(game):
    while game.running:
        current_time = pygame.time.get_ticks()
        player_action = None

        # Handling all pygame events, including keys pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.paused = not game.paused
                if not game.paused and game.player.lives > 0:
                    # Checking if player hit enemy and returns the action
                    player_action = check_enemy_hit(game, event)


        game.player.on_input(player_action)

        if not game.paused and game.player.lives > 0:
            # Enemy spawning every interval
            if current_time - game.enemy_spawn_time > game.spawn_interval:
                spawn_random_enemy(game)
                game.enemy_spawn_time = current_time

            # Updating all sprites
            game.all_sprites.update()

        closest_to_plr = [None, 99999]

        # Checking enemy conditions
        for enemy in game.enemies:
            # If enemy is the current to the player
            player_magnitude = enemy.rect.x - (game.SCREEN_WIDTH // 2) - 50
            if player_magnitude < closest_to_plr[1]:
                closest_to_plr = [enemy, player_magnitude]

            # If enemy passed the limit to damage player
            if enemy.rect.x < (game.SCREEN_WIDTH // 2) - 50:
                game.destroy_sound.play()
                game.damage_sound.play()

                game.player.lives -= 1
                game.player.combo = 0
                game.enemies.remove(enemy)
                game.all_sprites.remove(enemy)

        # Updating the closest enemy to the player
        if closest_to_plr[0]:
            game.player.closest_enemy = closest_to_plr[0]

        game.left_hand.update(game.player.closest_enemy)
        game.right_hand.update(game.player.closest_enemy)

        # Changing levels based off player score
        level_player(game)

        game.screen.blit(game.stage_back, (0, 0))
        game.all_sprites.draw(game.screen)

        game.left_hand.draw(game.screen)
        game.right_hand.draw(game.screen)
        game.player.draw(game.screen)

        # Setting user interface
        score_text = game.font.render(f'Score: {game.player.score}', True, game.COLORS.white)
        lives_text = game.font.render(f'Lives: {game.player.lives}', True, game.COLORS.white)
        combo_text = game.font.render(f'Combo: {game.player.combo}', True, game.COLORS.white)
        level_text = game.font.render(f'Level: {game.level}', True, game.COLORS.white)
        next_level_text = game.font.render(f'Next level: {game.player.levelup_req} score',
                                      True, game.COLORS.bright_yellow)
        game.screen.blit(score_text, (10, 10))
        game.screen.blit(lives_text, (10, 40))
        game.screen.blit(combo_text, (10, 70))
        game.screen.blit(level_text, (10, 100))
        game.screen.blit(next_level_text, (10, 180))

        if game.paused:
            pause_text = game.font.render('PAUSED - Press ESC to continue', True,
                                     game.COLORS.white)
            game.screen.blit(pause_text,
                        (game.SCREEN_WIDTH // 2 - 150, game.SCREEN_HEIGHT // 2))

        # Game Over
        if game.player.lives <= 0:
            game_over_text = game.font.render('GAME OVER', True, game.COLORS.red)
            final_score_text = game.font.render(f'Final Score: {game.player.score}', True,
                                           game.COLORS.white)
            level_reached_text = game.font.render(f'Congrats! You reached level {game.level}!',
                                         True, game.COLORS.white)
            max_combo_text = game.font.render(f'Max Combo: {game.player.max_combo}', True,
                                         game.COLORS.white)
            restart_text = game.font.render('Press SPACE to restart or ESC to quit',
                                       True, game.COLORS.white)
            game.screen.blit(game_over_text,
                        (game.SCREEN_WIDTH // 2 - 100, game.SCREEN_HEIGHT // 2 - 100))
            game.screen.blit(level_reached_text,
                        (game.SCREEN_WIDTH // 2 - 100, game.SCREEN_HEIGHT // 2 - 50))
            game.screen.blit(final_score_text,
                        (game.SCREEN_WIDTH // 2 - 100, game.SCREEN_HEIGHT // 2 - 20))
            game.screen.blit(max_combo_text,
                        (game.SCREEN_WIDTH // 2 - 100, game.SCREEN_HEIGHT // 2 + 10))
            game.screen.blit(restart_text,
                        (game.SCREEN_WIDTH // 2 - 100, game.SCREEN_HEIGHT // 2 + 70))
            pygame.display.flip()

            # Wait for player input
            waiting = True

            while waiting and game.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        waiting = False
                        game.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            reset_game(game)
                            waiting = False
                        elif event.key == pygame.K_ESCAPE:
                            waiting = False
                            game.running = False

        pygame.display.flip()
        game.clock.tick(game.FPS)

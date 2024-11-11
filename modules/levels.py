import pygame
import csv
import random
from modules import background as bg

pygame.mixer.init()

menu_music = './game_assets/music/Jesse James.mp3'
lvl0_music = './game_assets/music/level0.mp3'
lvl1_music = './game_assets/music/level1.mp3'
menace_music = './game_assets/music/The Ring - Klonoa.mp3'
lvl2_music = './game_assets/music/level2.mp3'

def load_random_word(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        words = [row[0] for row in reader]
    return random.choice(words)

def level_config(game, level):
    level.assets = f"./game_assets/stages/{level.stage}"
    level.music = f"./game_assets/music/level{level.stage}.mp3"

    # Loading proper images
    level.floor_image = pygame.image.load(f"{level.assets}/floor.png").convert_alpha()
    level.floor_image = pygame.transform.scale(level.floor_image, level.floor_size)

    level.bg1_image = pygame.image.load(f"{level.assets}/bg1.png").convert_alpha()
    level.bg1_image = pygame.transform.scale(level.bg1_image, level.bg_size)

    level.bg2_image = pygame.image.load(f"{level.assets}/bg2.png").convert_alpha()
    level.bg2_image = pygame.transform.scale(level.bg2_image, level.bg_size)

    level.floor_y = game.SCREEN_HEIGHT - (level.floor_size[1] // 4)
    level.bg_y = (level.bg_size[1] // 2)

    if level.stage == 0:
        level.name = game.LV0_NAME
        level.description = "like father, like son"
        level.difficulty_req = 200
    if level.stage == 1:
        level.name = game.LV1_NAME
        level.description = "Coffee for today's task"
        level.difficulty_req = 100
        level.bg_color = game.COLORS.dark_grey

        level.floor_lights = pygame.Surface((game.SCREEN_WIDTH, level.floor_y // 1.25))
        level.floor_lights.fill(game.BASE_FLOOR_LIGHTS_COLOR)
        level.fl_pos = (0, game.SCREEN_HEIGHT - 185)

        level.floor_neon = pygame.Surface((game.SCREEN_WIDTH, level.floor_size[1] // 1.3))
        level.floor_neon.fill(game.COLORS.black[0])
        level.fn_pos = (0, game.SCREEN_HEIGHT - 170)
    if level.stage == 2:
        level.name = game.LV2_NAME
        level.description = "Freeze, ZH4R0V!!!"
        level.difficulty_req = 500

class Level:
    def __init__(self, game, stage):
        self.stage = stage
        self.name = ''
        self.description = ''
        self.assets = ''
        self.music = ''
        self.floor_image = ''
        self.bg1_image = ''
        self.bg2_image = ''
        self.bg_color = (0, 0, 0)

        self.difficulty_req = 100
        self.enemy_spawn_time = 0
        self.spawn_interval = 2000
        self.enemy_speed = 2

        self.floor_size = (250, 250)
        self.bg_size = (game.SCREEN_HEIGHT, game.SCREEN_HEIGHT)

        self.floor_sprites = []
        self.bg_sprites = []
        self.floor_lights = None
        self.floor_neon = None
        self.floor_lights_pos = None
        self.floor_neon_pos = None

        self.floor_index = 0
        self.bg_index = 0
        self.max_floor = None
        self.max_bg = None
        self.floor_y = 0
        self.bg_y = 0
        self.fl_pos = 0
        self.fn_pos = 0

        self.target_word = load_random_word('C:/typing-chase_pygame/all_words/words_test.txt')
        self.remaining_word = self.target_word

        level_config(game, self)

        new_floor_pos = (0, self.floor_y)
        new_bg_pos = (0, self.bg_y)

        # Adding initial floor chunks
        while new_floor_pos[0] < game.SCREEN_WIDTH:
            new_floor = bg.Terrain(self, 'floor')
            new_floor.rect.center = new_floor_pos
            new_floor_pos = (new_floor_pos[0] + new_floor.size[0], self.floor_y)

            self.max_floor = new_floor
            self.floor_sprites.append(new_floor)
        # Adding initial background chunks
        while new_bg_pos[0] < game.SCREEN_WIDTH:
            new_bg = bg.Terrain(self, 'background')
            new_bg.rect.center = new_bg_pos
            new_bg_pos = (new_bg_pos[0] + new_bg.size[0], self.bg_y)

            self.max_bg = new_bg
            self.bg_sprites.append(new_bg)


    # Main function to run the game
    def run(self, game):
        current_time = pygame.time.get_ticks()
        player_action = None
        if self.stage == 0:
            pygame.mixer.music.load(lvl0_music)
            pygame.mixer.music.play(-1)
        elif self.stage == 1:
            pygame.mixer.music.load(lvl1_music)
            pygame.mixer.music.play(-1)
        elif self.stage == 2:
            pygame.mixer.music.load(lvl2_music)
            pygame.mixer.music.play(-1)

        # Handling all pygame events, including keys pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.paused = not game.paused

                elif not game.paused and game.player.lives > 0 and self.remaining_word:
                    if event.unicode == self.remaining_word[0]:
                        self.remaining_word = self.remaining_word[1:]
                        if not self.remaining_word:
                            if game.player.closest_enemy:
                                game.enemies.remove(game.player.closest_enemy)
                                game.all_sprites.remove(game.player.closest_enemy)
                                game.player.score += 100
                            self.target_word = load_random_word('./path/to/words.csv')
                            self.remaining_word = self.target_word

                if not game.paused and game.player.lives > 0:
                    # Checking if player hit enemy and returns the action
                    player_action = None

        game.player.on_input(player_action)

        if not game.paused and game.player.lives > 0:
            # Enemy spawning every interval
            if current_time - self.enemy_spawn_time > self.spawn_interval:
                self.enemy_spawn_time = current_time

            # Updating all sprites
            game.all_sprites.update()

        closest_to_plr = [None, 99999]

        # Checking enemy conditions
        if self.stage == 1:
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

        game.tick += 1
        distance_threshold = 15 - game.player.speed if game.player.speed < 15 else 14

        if game.tick % distance_threshold == 0:
            game.player.distance += 1

        self.draw(game)

        if game.player.lives <= 0: self.game_over(game)

        game.clock.tick(game.FPS)

    def draw(self, game, stopped=False):
        # Drawing everything
        game.screen.fill(self.bg_color)

        bg.update_terrain(game, game.level, stopped)

        game.all_sprites.draw(game.screen)

        game.left_hand.draw(game.screen)
        game.right_hand.draw(game.screen)

        if game.level.stage < 2:
            game.player.draw(game.screen)

        # Setting user interface
        distance_text = game.large_font.render(f'{game.player.distance} m', True, game.COLORS.white)
        score_text = game.header_font.render(f' {game.player.score}', True, game.COLORS.white)
        lives_text = game.text_font.render(f'Lives: {game.player.lives}', True, game.COLORS.white)
        combo_text = game.text_font.render(f'Combo: {game.player.combo}', True, game.COLORS.white)

        # Actual word indicator
        font = pygame.font.Font(None, 36)
        word_text = font.render(self.remaining_word, True, game.COLORS.white)
        game.screen.blit(word_text, (10, game.SCREEN_HEIGHT - 40))

        if game.level.stage > 0:
            game.screen.blit(distance_text, (10, -5))
            game.screen.blit(score_text, (50, 70))
            game.screen.blit(game.score_image, (5, 80))
        game.screen.blit(lives_text, (10, game.SCREEN_HEIGHT - 80))
        game.screen.blit(combo_text, (10, game.SCREEN_HEIGHT - 50))

        if game.level.stage == 2:
            bullet_train = pygame.image.load(f"./game_assets/stages/2/bullet_train.png").convert_alpha()
            bullet_train_rect = bullet_train.get_rect()
            bullet_train = pygame.transform.scale(bullet_train, (750, 450))
            bullet_train_rect.center = (game.SCREEN_WIDTH // 2, game.SCREEN_HEIGHT // 1.5)
            game.screen.blit(bullet_train, bullet_train_rect)
            # Player position
            game.player.draw_2(game.screen)

    def game_over(self, game):
        # Game Over
        self.draw(game, True)

        game_over_text = game.text_font.render('GAME OVER', True, game.COLORS.red)
        final_score_text = game.text_font.render(f'Final Score: {game.player.score}', True,
                                            game.COLORS.white)
        max_combo_text = game.text_font.render(f'Max Combo: {game.player.max_combo}', True,
                                          game.COLORS.white)
        restart_text = game.text_font.render('Press SPACE to restart or ESC to quit',
                                        True, game.COLORS.white)
        game.screen.blit(game_over_text,
                         (game.SCREEN_WIDTH // 2 - 100, game.SCREEN_HEIGHT // 2 - 100))
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
                    if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                        game.game_state = 'menu'
                        waiting = False

    def pause(self, game):
        while game.game_state == 'pause' and game.running:
            self.draw(game, True)
            game.screen.blit(game.DARK_FILTER, (0, 0))

            pause_text1 = game.title_font.render('PAUSED', True, game.COLORS.bright_yellow)
            pause_text2 = game.text_font.render('> SPACE: resume game', True, game.COLORS.white)
            pause_text3 = game.text_font.render('> ESC: back to menu', True, game.COLORS.white)

            game.screen.blit(pause_text1,
                             (game.SCREEN_WIDTH // 2 - 120, 100))
            game.screen.blit(pause_text2,
                             (game.SCREEN_WIDTH // 2 - 120, 220))
            game.screen.blit(pause_text3,
                             (game.SCREEN_WIDTH // 2 - 120, 260))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        game.game_state = 'level'
                    elif event.key == pygame.K_ESCAPE:
                        game.game_state = 'menu'

            pygame.display.flip()
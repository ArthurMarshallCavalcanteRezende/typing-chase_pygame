import pygame
import random
import game_data
import sys

from modules import background as bg
from modules import enemy
from modules import obstacle

pygame.mixer.init()

def reset_game(game, reset_music=True):
    """RESET ALL GAME VARIABLES FOR RESTART OR NEW LEVEL"""
    if reset_music:
        game.sound.play('menu', -1)
    game.data["cash"] += game.player.run_cash

    if game.data["max_cash"] < game.data["cash"]:
        game.data["max_cash"] = game.data["cash"]

    if game.data[f"level{game.level.stage}"]["max_combo"] < game.player.max_combo:
        game.data[f"level{game.level.stage}"]["max_combo"] = game.player.max_combo

    if game.data[f"level{game.level.stage}"]["max_cash"] < game.player.run_cash:
        game.data[f"level{game.level.stage}"]["max_cash"] = game.player.run_cash

    if game.data[f"level{game.level.stage}"]["max_distance"] < game.player.distance:
        game.data[f"level{game.level.stage}"]["max_distance"] = game.player.distance

    game.player.lives = 3
    game.player.combo = 0
    game.player.max_combo = 0
    game.player.difficulty = 1
    game.player.speed = 3
    game.player.distance = 0
    game.player.run_cash = 0
    game.player.dodge_warned = False

    game.player.closest_enemy = None
    game.player.dodge = False
    game.player.invincible = False

    game.enemy_speed = 2
    game.spawn_interval = 2000

    game.level = Level(game, game.level.stage)
    game.state = 'menu'
    game.paused = False
    game.cutscene_skipped = False

    game_data.save_datastore(game)


def level_config(game, level):
    level.assets = f"./game_assets/stages/{level.stage}"
    level.music = f"level{level.stage}"

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
        level.possible_enemies = {
            'target': ['target', 100],
            'normal_minibot': ['normal_minibot', 0],
            'wild_minibot': ['wild_minibot', 0],
            'spike_minibot': ['spike_minibot', 0],
            'fake_minibot': ['fake_minibot', 0],

            'mototaxi': ['mototaxi', 0],
            'hivebox': ['hivebox', 0],
        }

        level.possible_obstacles = {
            'tumbleweed': ['tumbleweed', 100]
        }

        level.name = game.LV0_NAME
        level.description = "like father, like son"
        level.difficulty_req = 200
        level.base_spawn_interval = 1800
        level.enemy_speed = 2
        level.max_enemy_distance = -200
        level.max_enemies = 3
        level.obstacle_chance = 20

        game.player.speed = 0
    if level.stage == 1:
        level.possible_enemies = {
            'normal_minibot': ['normal_minibot', 60],
            'wild_minibot':['wild_minibot', 30],
            'spike_minibot':['spike_minibot', 10],
            'fake_minibot': ['fake_minibot', 0],

            'mototaxi': ['mototaxi', 0],
            'hivebox': ['hivebox', 0],

            'classB': ['classB', 0],
            'classC': ['classC', 0],
            'classD': ['classD', 0],
        }
        level.possible_obstacles = {
            'missile': ['missile', 30],
            'barrier': ['barrier', 70],
        }

        level.name = game.LV1_NAME
        level.description = "Coffee for today's task"
        level.difficulty_req = 100
        level.bg_color = game.COLORS.dark_grey

        level.floor_lights = pygame.Surface((game.SCREEN_WIDTH, level.floor_y // 1.25))
        level.floor_lights.fill(game.BASE_FLOOR_LIGHTS_COLOR)
        level.fl_pos = (0, game.SCREEN_HEIGHT - 185)

        level.max_enemy_distance = 200
        level.spawn_max = 1
        level.max_enemies = 6
        level.obstacle_chance = 20

        game.player.speed = 3

        level.floor_neon = pygame.Surface((game.SCREEN_WIDTH, level.floor_size[1] // 1.3))
        level.floor_neon.fill(game.COLORS.black[0])
        level.fn_pos = (0, game.SCREEN_HEIGHT - 170)
    if level.stage == 2:
        level.floor_y = game.SCREEN_HEIGHT + 30
        game.bullet_train_rect.centery = level.floor_y - 150

        level.possible_enemies = {
            'normal_minibot': ['normal_minibot', 40],
            'wild_minibot':['wild_minibot', 40],
            'spike_minibot':['spike_minibot', 10],
            'fake_minibot': ['fake_minibot', 20],

            'hivebox': ['hivebox', 5],
            'mototaxi': ['mototaxi', 0],

            'classB': ['classB', 10],
            'classC': ['classC', 5],
            'classD': ['classD', 2],
        }
        level.possible_obstacles = {
            'missile': ['missile', 100],
        }

        level.name = game.LV2_NAME
        level.description = "Freeze, ZH4R0V!!!"

        level.difficulty_req = 1500
        level.base_spawn_interval = 3000
        level.spawn_max = 3
        level.enemy_speed = 3
        level.max_enemy_distance = 350
        level.obstacle_chance = 12
        level.nothing_chance = 5
        level.max_enemies = 9
        level.max_hivebox = 2

        game.player.speed = 15


def play_audio_and_show_subtitles(audio_files, subtitles, game):
    background_image = game.stage2_bg.copy()
    background_image = pygame.transform.scale(background_image, (game.SCREEN_WIDTH, game.SCREEN_HEIGHT))
    zharov_sprite = pygame.image.load('./game_assets/stages/2/ZH4R0V.png')
    zharov_sprite = pygame.transform.scale(zharov_sprite, (400, 400))
    speech_panel = pygame.image.load('./game_assets/stages/2/target_warning.png')
    speech_panel = pygame.transform.scale(speech_panel, (1400, 350))

    x_pos = game.SCREEN_WIDTH - zharov_sprite.get_width() - 30
    y_pos = game.SCREEN_HEIGHT // 2 - zharov_sprite.get_height() // 2 - 20
    game.screen.blit(zharov_sprite, (x_pos, y_pos))
    game.screen.blit(speech_panel, (-15, game.SCREEN_HEIGHT - 400))

    pygame.display.update()

    subtitle_pairs = [subtitles[i:i + 2] for i in range(0, len(subtitles), 2)]
    subtitle_index = 0
    subtitle_durations = [25000, 20000, 30000, 30000]

    while subtitle_index < len(audio_files) and not game.cutscene_skipped:
        current_time = pygame.time.get_ticks()
        start_time = current_time

        pygame.mixer.music.load(audio_files[subtitle_index])
        pygame.mixer.music.play()

        game.bullet_train_rect.center = (-100, game.SCREEN_HEIGHT // 1.5)
        game.player.rect.center = game.bullet_train_rect.center

        game.screen.blit(background_image, (0, 0))
        game.screen.blit(game.CUTSCENE_FILTER, (0, 0))

        game.screen.blit(zharov_sprite, (x_pos, y_pos))
        game.screen.blit(speech_panel, (-390, game.SCREEN_HEIGHT - 400))

        for i, subtitle in enumerate(subtitle_pairs[subtitle_index]):
            subtitle_text = game.small_font.render(subtitle, True, game.COLORS.white)
            game.screen.blit(subtitle_text, (game.SCREEN_WIDTH // 7, game.SCREEN_HEIGHT - 180 + (40 * i)))

        pygame.display.flip()
        game.clock.tick(game.FPS)

        if subtitle_index == 2:
            menace_music_started = False
            elapsed_time = pygame.time.get_ticks() - start_time

            while pygame.mixer.music.get_busy():
                elapsed_time = pygame.time.get_ticks() - start_time

                if not menace_music_started and elapsed_time >= 5000:
                    game.sound.play('menace', -1)
                    menace_music_started = True

                pygame.time.delay(100)
        else:
            subtitle_duration = subtitle_durations[subtitle_index]
            while pygame.mixer.music.get_busy() and current_time - start_time < subtitle_duration:
                pygame.time.delay(6000)
                current_time = pygame.time.get_ticks()

        subtitle_index += 1

    game.state = 'level'
    game.data["cutscene_finished"] = True

# Cutscene assets
def level_2_cutscene(game):
    audio_files = [
        './game_assets/stages/2/zharov_speech1.wav',
        './game_assets/stages/2/zharov_speech2.wav',
        './game_assets/stages/2/zharov_power.wav',
        './game_assets/stages/2/zharov_speech3.wav'
    ]

    subtitles = [
        "Que curioso, jovem recrutas para Intercentauri... Que patético!",
        "Eles te encheram de falsas esperanças, não é garoto?",
        "Escute jovem, eu tenho negócios a resolver com meu fornecedor.",
        "Então... EU VOU ACELERAR NOSSA CONVERSA!",
        "*ROBÔ LANÇANDO PODER IRADO.MP3*",
        "*Música épica de fundo*",
        "Você não irá me pegar, cowboy!",
        "Hahahahahahahaha!!!"
    ]

    # function to play the audios with subtitles
    play_audio_and_show_subtitles(audio_files, subtitles, game)
    pygame.mixer.music.stop()
    game.sound.play('level2', -1)

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

        self.time_elapsed = 0
        self.difficulty_req = 100
        self.enemy_spawn_time = 0
        self.base_spawn_interval = 3000
        self.spawn_interval = self.base_spawn_interval
        self.max_enemy_distance = 200
        self.enemy_speed = 2
        self.distance_per_frame = 1

        self.max_enemies = 6
        self.max_hivebox = 1
        self.hivebox_count = 0
        self.obstacles_spawned = 0

        self.possible_enemies = {}
        self.possible_obstacles = {}

        self.floor_size = (250, 250)
        self.bg_size = (game.SCREEN_HEIGHT, game.SCREEN_HEIGHT)

        self.floor_sprites = []
        self.bg_sprites = []
        self.enemy_list = []
        self.obstacle_list = []

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

        self.started = False
        self.word_list = []

        self.spawn_max = 1
        self.obstacle_chance = 20
        self.nothing_chance = 20

        game.bullet_train_rect.centerx = -10
        game.bullet_train_speed = 5

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


    def spawn_enemy(self, game):
        spawn_count = 1
        spawned = 0
        spike_spawned = False
        mototaxi_spawned = False
        new_speed = self.enemy_speed

        if self.stage > 0:
            spawn_count = random.randint(1, self.spawn_max)
            new_speed = random.randint(self.enemy_speed - 1, self.enemy_speed + 1)

        for new_enemy in range(spawn_count):
            if len(self.enemy_list) < self.max_enemies:
                spawned += 1 # Making sure only the first spawned is a word

                # Get a random bandit to spawn depending on chance
                spawns = []
                chances = []

                for enemy_sprite in self.possible_enemies:
                    spawns.append(self.possible_enemies[enemy_sprite][0])
                    chances.append(self.possible_enemies[enemy_sprite][1])

                choosen_enemy = random.choices(population=spawns, weights=chances)[0]

                if choosen_enemy == 'hivebox' and self.hivebox_count >= self.max_hivebox:
                    continue

                if choosen_enemy == 'spike_minibot' and not spike_spawned:
                    spike_spawned = True
                elif choosen_enemy == 'spike_minibot':
                    continue
                if choosen_enemy == 'mototaxi_spawned' and not mototaxi_spawned:
                    spike_spawned = True
                elif choosen_enemy == 'mototaxi':
                    continue

                enemy_values = game.enemies[choosen_enemy]

                new_enemy = enemy.Enemy(
                    game, choosen_enemy, enemy_values[0], enemy_values[1],
                    enemy_values[2], enemy_values[3])
                new_enemy.load(game, new_speed)

                self.enemy_list.append(new_enemy)

    def spawn_obstacle(self, game):
        if self.nothing_chance >= random.randint(1, 100):
            return

        # Get a random bandit to spawn depending on chance
        spawns = []
        chances = []

        for obstacle_sprite in self.possible_obstacles:
            spawns.append(self.possible_obstacles[obstacle_sprite][0])
            chances.append(self.possible_obstacles[obstacle_sprite][1])

        choosen_obstacle = random.choices(population=spawns, weights=chances)[0]
        obstacle_values = game.obstacles[choosen_obstacle]
        new_obstacle = obstacle.Obstacle(
            game, choosen_obstacle, obstacle_values[0], obstacle_values[1])

        if self.obstacles_spawned >= 3:
            new_obstacle.has_tip = False

        self.obstacles_spawned += 1

        self.obstacle_list.append(new_obstacle)

    def update_difficulty(self, game):
        # Increasing difficulty of the game over distances reached
        if game.player.distance > self.difficulty_req:
            self.difficulty_req *= 2
            game.player.difficulty += 1

            if self.stage == 2: self.distance_per_frame += 1

            # Different changes depending on each difficulty until 8
            if game.player.difficulty < 5:
                game.player.speed += 1
                self.possible_enemies['wild_minibot'][1] += 5
                self.possible_enemies['spike_minibot'][1] += 3
            else:
                game.player.speed += 2

            if game.player.difficulty == 2:
                if self.stage != 2:
                    self.possible_enemies['mototaxi'][1] += 5
                else:
                    self.possible_enemies['classB'][1] += 5
            if game.player.difficulty == 3:
                self.spawn_max += 1
                self.enemy_speed += 1

                if self.stage != 2:
                    self.possible_enemies['mototaxi'][1] += 3
                else:
                    self.possible_enemies['classB'][1] += 5
                    self.possible_enemies['classC'][1] += 5
                self.possible_enemies['hivebox'][1] += 5
                self.possible_enemies['fake_minibot'][1] += 3
            if game.player.difficulty == 4:
                self.possible_enemies['fake_minibot'][1] += 5
                if self.stage != 2:
                    self.possible_enemies['mototaxi'][1] += 2
                else:
                    self.possible_enemies['classB'][1] += 10
                    self.possible_enemies['classC'][1] += 5
                    self.possible_enemies['classD'][1] += 2
            if game.player.difficulty == 5:
                self.max_hivebox += 1
                self.possible_enemies['hivebox'][1] += 5
                self.spawn_max += 1
            if game.player.difficulty == 6:
                self.possible_enemies['fake_minibot'][1] += 3
                if self.stage != 2:
                    self.possible_enemies['mototaxi'][1] += 10
                else:
                    self.possible_enemies['classB'][1] += 3
                    self.possible_enemies['classC'][1] += 5
                    self.possible_enemies['classD'][1] += 10
            if game.player.difficulty == 7:
                self.enemy_speed += 1
                self.possible_enemies['fake_minibot'][1] += 5

    # Main function to run the game
    def run(self, game):
        if not self.started:
            if self.stage == 2 and game.play_cutscene:
                level_2_cutscene(game)
            else:
                game.cutscene_skipped = True
                game.sound.play(self.music, -1)

            if self.stage == 0 or self.stage == 2:
                game.player.is_running = False
            else:
                game.player.is_running = True

            game.player.reset_anim()

            self.started = True

        current_time = pygame.time.get_ticks()
        enemy_hit = False
        enemy_killed = False
        closest_to_plr = [None, 99999]

        # Checking enemy conditions
        hiveboxes = 0

        for enemy in self.enemy_list:
            enemy.update(game)
            if enemy.name == 'hivebox':
                hiveboxes += 1

            if (game.player.key_pressed == enemy.remaining_text[0]
                and enemy.rect.x < game.SCREEN_WIDTH):
                if enemy.name == 'fake_minibot':
                    ignore_fake = False

                    # Avoiding triggering if other enemies have letter
                    for other_enemies in self.enemy_list:
                        if (enemy.remaining_text[0] in other_enemies.remaining_text
                            and other_enemies.name != 'fake_minibot'):
                            ignore_fake = True

                    if not ignore_fake:
                        enemy.reached_player = True

                    continue

                enemy_hit = True
                enemy.remaining_text = enemy.remaining_text[1:]

                if not enemy.remaining_text:
                    self.enemy_list.remove(enemy)
                    enemy_killed = True

                    game.player.combo += 1 if len(enemy.target_text) <= 3 else 3
                    if game.player.combo > game.player.max_combo or self.stage == 0:
                        game.player.max_combo += 1 if len(enemy.target_text) <= 3 else 3

                    to_gain = len(enemy.target_text) * game.player.max_combo

                    if self.stage != 0:
                        game.player.run_cash += to_gain * (self.stage + game.player.difficulty)

            if enemy in self.enemy_list:
                # If enemy is the current to the player
                player_magnitude = enemy.rect.x - (game.SCREEN_WIDTH // 2) - 50
                if player_magnitude < closest_to_plr[1]:
                    closest_to_plr = [enemy, player_magnitude]

                # If enemy passed the limit to damage player
                if enemy.name != 'spike_minibot':
                    if (enemy.rect.x < self.max_enemy_distance
                            and enemy.name != 'fake_minibot'):
                        enemy.reached_player = True
                else:
                    if enemy.lifetime >= 5:
                        enemy.reached_player = True

        self.hivebox_count = hiveboxes
        if enemy_hit:
            game.sound.shoot.play()

        if enemy_killed:
            game.sound.destroy.play()
            if self.stage > 0: game.sound.points.play()
        elif game.player.key_pressed and not enemy_hit:
            game.sound.wrong_input.play()
            game.player.combo -= 1 if game.player.combo > 0 else 0

        for obstacle in self.obstacle_list:
            obstacle.update(game)

        game.player.key_pressed = None

        # Updating the closest enemy to the player
        if closest_to_plr[0]:
            game.player.closest_enemy = closest_to_plr[0]

        game.player.on_input(game)

        ''' ===== CHECKING INSTANCES SPAWNING CONDITIONS ===== '''
        if not game.paused and game.player.lives > 0:
            # Enemy spawning every interval
            if (current_time - self.enemy_spawn_time > self.spawn_interval
                    and self.time_elapsed > 1):
                self.enemy_spawn_time = current_time
                lowest_interval = self.base_spawn_interval - game.player.difficulty * 200
                highest_interval = self.base_spawn_interval - game.player.difficulty * 50
                if lowest_interval < 500: lowest_interval = 500
                self.spawn_interval = random.randint(lowest_interval, highest_interval)

                if (self.obstacle_chance >= random.randint(1, 100)
                        and len(self.possible_obstacles) > 0):
                    self.spawn_obstacle(game)
                else:
                    self.spawn_enemy(game)

        game.left_hand.update(game)
        game.right_hand.update(game)
        game.player.update(game)

        if game.tick % game.FPS == 0:
            self.time_elapsed += 1

        if game.bullet_train_rect.centerx < 200:
            game.bullet_train_rect.centerx += game.bullet_train_speed

            # Slowly decreasing intro speed for bullet train
            game.bullet_train_speed *= 0.98

        # Incrementing distance every certain frames
        if self.stage != 0:
            distance_threshold = 10 - (game.player.speed if game.player.speed < 10 else 9)

            if game.tick % distance_threshold == 0:
                game.player.distance += self.distance_per_frame

                self.update_difficulty(game)

        else:
            if game.player.max_combo >= 15 and not game.data["tutorial_finished"]:
                game.state = 'tutorial_end'
                game.player.run_cash += game.TUTORIAL_CASH
                game.data["tutorial_finished"] = True

        game.floor_speed = game.BASE_FLOOR_SPEED + game.player.speed
        game.bg_speed = game.BASE_BG_SPEED + (game.player.speed // 2)

        self.draw(game)

        if game.player.lives <= 0:
            game.sound.rocket.stop(True)
            game.state = 'gameover'
            game.paused = True

    def draw(self, game):
        # Drawing everything
        game.screen.fill(self.bg_color)

        bg.update_terrain(game, game.level)

        if self.stage == 2:
            game.screen.blit(game.bullet_train, game.bullet_train_rect)

        game.left_hand.draw(game.screen)
        game.right_hand.draw(game.screen)

        game.player.draw(game)

        # Setting user interface
        distance_text = game.large_font.render(f'{game.player.distance} m', True, game.COLORS.white)
        score_text = game.header_font.render(f' {game.player.run_cash}', True, game.COLORS.white)
        lives_text = game.text_font.render(f'Lives: {game.player.lives}', True, game.COLORS.white)
        combo_text = game.text_font.render(f'Combo: {game.player.combo}', True, game.COLORS.white)

        if game.tick % 5 == 0:
            if game.dodge_color == game.COLORS.red:
                game.dodge_color = game.COLORS.orange
            elif game.dodge_color == game.COLORS.orange:
                game.dodge_color = game.COLORS.red

        dodge_text = game.header_font.render(f'DODGE!!', True, game.dodge_color)

        # Actual word indicator
        if self.stage > 0:
            game.screen.blit(distance_text, (10, -5))

        game.screen.blit(score_text, (50, 70))
        game.screen.blit(game.score_image, (5, 80))

        # Always drawing fake minibots behind normal enemies to avoid unfair combos
        for enemy in self.enemy_list:
            if enemy.name == 'fake_minibot':
                enemy.draw(game)
        for enemy in self.enemy_list:
            if enemy.name != 'fake_minibot':
                enemy.draw(game)

        for obstacle in self.obstacle_list:
            obstacle.draw(game)

        game.screen.blit(lives_text, (10, game.SCREEN_HEIGHT - 80))
        game.screen.blit(combo_text, (10, game.SCREEN_HEIGHT - 50))

        if game.player.dodge_warned:
            dodge_rect_x = game.player.rect.x + 8
            dodge_rect_y = game.player.rect.y - 60
            game.screen.blit(dodge_text, (dodge_rect_x, dodge_rect_y))

        if self.stage == 0:
            game.screen.blit(game.LV0_FILTER, (0, 0))

    def game_over(self, game):
        # Game Over
        self.draw(game)

        pygame.mixer.music.set_volume(0.1)
        game.screen.blit(game.GAMEOVER_FILTER, (0, 0))

        game_over_text = game.title_font.render('GAME OVER', True, game.COLORS.red)
        distance_text = game.header_font.render(f'Distance Reached: {game.player.distance} M',
                                                 True, game.COLORS.bright_yellow)
        disks_text = game.large_font.render(f'Gained: {game.player.run_cash}!',
                                                 True, game.COLORS.bright_cyan)
        max_combo_text = game.text_font.render(f'Max Combo: {game.player.max_combo}', True,
                                          game.COLORS.white)
        menu_text = game.text_font.render('> SPACE: back to menu',
                                        True, game.COLORS.white)

        game.screen.blit(game_over_text,
                         (game.SCREEN_WIDTH // 2 - 180, 70))
        game.screen.blit(distance_text,
                         (game.SCREEN_WIDTH // 2 - 180, 180))
        game.screen.blit(max_combo_text,
                         (game.SCREEN_WIDTH // 2 - 100, 230))
        game.screen.blit(game.death_score_image,
                         (game.SCREEN_WIDTH // 2 - 180, 300))
        game.screen.blit(disks_text,
                         (game.SCREEN_WIDTH // 2 - 100, 290))
        game.screen.blit(menu_text,
                         (game.SCREEN_WIDTH // 2 - 120, 400))

    def tutorial_finish(self, game):
        # Screen for when done with tutorial on level 0
        self.draw(game)

        pygame.mixer.music.set_volume(0.1)
        game.screen.blit(game.TUTORIAL_FILTER, (0, 0))

        motivate_text = game.large_font.render("You're getting the hang of it!", True, game.COLORS.white)
        freebie_text = game.header_font.render(f"Here, take these freebies:",
                                                 True, game.COLORS.bright_yellow)
        disks_text = game.large_font.render(f'{game.TUTORIAL_CASH}!',
                                                 True, game.COLORS.bright_cyan)
        unlock_text = game.text_font.render(f'Use these to unlock the next level!', True,
                                          game.COLORS.white)
        menu_text = game.text_font.render('> SPACE: back to menu',
                                        True, game.COLORS.white)

        game.screen.blit(motivate_text,
                         (game.SCREEN_WIDTH // 2 - 340, 100))
        game.screen.blit(freebie_text,
                         (game.SCREEN_WIDTH // 2 - 220, 180))
        game.screen.blit(game.death_score_image,
                         (game.SCREEN_WIDTH // 2 - 135, 250))
        game.screen.blit(disks_text,
                         (game.SCREEN_WIDTH // 2 - 50, 240))
        game.screen.blit(unlock_text,
                         (game.SCREEN_WIDTH // 2 - 210, 350))
        game.screen.blit(menu_text,
                         (game.SCREEN_WIDTH // 2 - 120, 420))


    def pause(self, game):
        self.draw(game)

        pygame.mixer.music.set_volume(0.1)
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

        pygame.display.flip()
import pygame
import random

from modules.terrain.background import Terrain
from modules.terrain.background import update_terrain
from utils.asset_loader import load_class, weight_choices
from utils.colors import Colors
colors = Colors()

import constants as c

def level_config(game, level):
    level.assets = f"./assets/stages/{level.stage}"
    level.music = f"level{level.stage}"

    # Loading proper images
    level.floor_sprites = c.level_sprites[str(level.stage)]['floor_sprites']
    level.build_sprites = c.level_sprites[str(level.stage)]['build_sprites']
    level.bg_sprites = c.level_sprites[str(level.stage)]['bg_sprites']
    level.screen_bg = c.level_sprites[str(level.stage)]['screen_bg']

    level.floor_y = c.SCREEN_HEIGHT - (c.floor_size[1] // 4)
    level.bg_y = (c.bg_size[1] // 2)
    level.build_y =(c.build_size[1] // 2)

    # POSSIBLE ENEMIES STRUCTURE:
    # [0: name, 1: chance, 2: number spawned, 3: max allowed to spawn]

    if level.stage == 0:
        level.possible_enemies = {
            'target': ['target', 100, 0, 3],
            'normal_minibot': ['normal_minibot', 0, 0, 30],
            'wild_minibot': ['wild_minibot', 0, 0, 30],
            'spike_minibot': ['spike_minibot', 0, 0, 30],
            'fake_minibot': ['fake_minibot', 0, 0, 30],

            'mototaxi': ['mototaxi', 0, 0, 30],
            'hivebox': ['hivebox', 0, 0, 30],
        }

        level.possible_obstacles = {
            'tumbleweed': ['tumbleweed', 100]
        }

        level.name = c.LV0_NAME
        level.description = "like father, like son"
        level.difficulty_req = 200
        level.base_spawn_interval = 1800
        level.enemy_speed = 2
        level.max_enemy_distance = -200
        level.max_enemies = 3
        level.obstacle_chance = 20

        level.player_speed = 0
    if level.stage == 1:
        level.possible_enemies = {
            'normal_minibot': ['normal_minibot', 60, 0, 10],
            'wild_minibot':['wild_minibot', 30, 0, 6],
            'spike_minibot':['spike_minibot', 10, 0, 3],
            'fake_minibot': ['fake_minibot', 0, 0, 3],

            'mototaxi': ['mototaxi', 0, 0, 1],
            'hivebox': ['hivebox', 0, 0, 1],

            'classB': ['classB', 0, 0, 2],
            'classC': ['classC', 0, 0, 1],
            'classD': ['classD', 0, 0, 1],
        }
        level.possible_obstacles = {
            'missile': ['missile', 30],
            'barrier': ['barrier', 70],
        }

        level.name = c.LV1_NAME
        level.description = "Coffee for today's task"
        level.difficulty_req = 100
        level.bg_color = colors.dark_grey

        level.floor_lights = pygame.Surface((c.SCREEN_WIDTH, level.floor_y // 1.25))
        level.floor_lights.fill(colors.bright_cyan)
        level.fl_pos = (0, c.SCREEN_HEIGHT - 185)

        level.max_enemy_distance = 200
        level.spawn_max = 1
        level.max_enemies = 6
        level.obstacle_chance = 20
        level.player_speed = 3

        level.floor_neon = pygame.Surface((c.SCREEN_WIDTH, c.floor_size[1] // 1.3))
        level.floor_neon.fill(colors.black[0])
        level.fn_pos = (0, c.SCREEN_HEIGHT - 170)
    if level.stage == 2:
        level.floor_y = c.SCREEN_HEIGHT + 30
        game.bullet_train.move_to_track((-100, level.floor_y - 210))

        level.floor_lights = pygame.Surface((c.SCREEN_WIDTH, 30))
        level.floor_lights.fill(colors.yellow)
        level.fl_pos = (0, c.SCREEN_HEIGHT - 90)

        level.possible_enemies = {
            'normal_minibot': ['normal_minibot', 40, 0, 10],
            'wild_minibot':['wild_minibot', 40, 0, 6],
            'spike_minibot':['spike_minibot', 10, 0, 3],
            'fake_minibot': ['fake_minibot', 20, 0, 3],

            'hivebox': ['hivebox', 5, 0, 2],
            'mototaxi': ['mototaxi', 0, 0, 1],

            'classB': ['classB', 10, 0, 3],
            'classC': ['classC', 5, 0, 3],
            'classD': ['classD', 2, 0, 2],
        }
        level.possible_obstacles = {
            'missile': ['missile', 100],
        }

        level.name = c.LV2_NAME
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

        level.player_speed = 15


class Level:
    def __init__(self, game, stage):
        self.stage = stage
        self.name = ''
        self.description = ''
        self.assets = ''
        self.music = ''
        self.bg_color = (0, 0, 0)

        self.time_elapsed = 0
        self.difficulty_req = 100
        self.spawn_time = 0
        self.base_spawn_interval = 3000
        self.spawn_interval = self.base_spawn_interval
        self.max_enemy_distance = 200
        self.enemy_speed = 2
        self.distance_per_frame = 1
        self.player_speed = 3
        self.difficulty = 1

        self.max_enemies = 6
        self.obstacles_spawned = 0

        self.possible_enemies = {}
        self.possible_obstacles = {}

        self.floor_speed = c.BASE_FLOOR_SPEED
        self.build_speed = c.BASE_BUILD_SPEED
        self.bg_speed = c.BASE_BG_SPEED

        self.floor_list = []
        self.build_list = []
        self.bg_list = []

        self.floor_sprites = None
        self.build_sprites = None
        self.bg_sprites = None
        self.screen_bg = None

        self.enemy_list = []
        self.obstacle_list = []

        self.floor_lights = None
        self.floor_neon = None

        self.floor_index = 0
        self.build_index = 0
        self.bg_index = 0
        self.max_floor = None
        self.max_build = None
        self.max_bg = None

        self.floor_y = 0
        self.build_y = 0
        self.bg_y = 0
        self.fl_pos = 0
        self.fn_pos = 0

        self.started = False
        self.word_list = []

        self.spawn_max = 1
        self.obstacle_chance = 20
        self.nothing_chance = 20

        level_config(game, self)

        new_floor_pos = (0, self.floor_y)
        new_bg_pos = (0, self.bg_y)
        new_build_pos = (0, self.build_y)

        # Adding initial floor chunks
        if self.floor_sprites:
            while new_floor_pos[0] < c.SCREEN_WIDTH:
                new_floor = Terrain(self, 'floor')
                new_floor.rect.center = new_floor_pos
                new_floor_pos = (new_floor_pos[0] + new_floor.size[0], self.floor_y)

                self.max_floor = new_floor
                self.floor_list.append(new_floor)

        # Adding initial background chunks
        if self.bg_sprites:
            while new_bg_pos[0] < c.SCREEN_WIDTH:
                new_bg = Terrain(self, 'background')
                new_bg.rect.center = new_bg_pos
                new_bg_pos = (new_bg_pos[0] + new_bg.size[0], self.bg_y)

                self.max_bg = new_bg
                self.bg_list.append(new_bg)

        # Adding initial building chunks
        if self.build_sprites:
            while new_build_pos[0] < c.SCREEN_WIDTH:
                new_build = Terrain(self, 'building')
                new_build.rect.center = new_build_pos
                new_build_pos = (new_build_pos[0] + new_build.size[0], self.build_y)

                self.max_build = new_build
                self.build_list.append(new_build)


    def spawn_enemy(self, game):
        spawn_count = 1

        if self.stage > 0:
            spawn_count = random.randint(1, self.spawn_max)

        for new_enemy in range(spawn_count):
            if len(self.enemy_list) < self.max_enemies:
                choosen_enemy = weight_choices(self.possible_enemies)
                path = c.ENEMY_CLASS_PATH + choosen_enemy + '.py'

                EnemyClass = load_class(path, 'Enemy')
                if not EnemyClass: continue
                new_enemy = EnemyClass(game)

                self.enemy_list.append(new_enemy)

    def spawn_obstacle(self, game):
        if self.nothing_chance >= random.randint(1, 100):
            return

        self.obstacles_spawned += 1
        choosen_obstacle = weight_choices(self.possible_obstacles)
        path = c.OBSTACLE_CLASS_PATH + choosen_obstacle + '.py'

        ObstacleClass = load_class(path, 'Obstacle')
        if ObstacleClass:
            new_obstacle = ObstacleClass(game)

            self.obstacle_list.append(new_obstacle)

    def increase_difficulty(self, game):
        # Increasing difficulty of the game over distances reached
        if game.player.distance > self.difficulty_req:
            self.difficulty_req *= 2
            self.difficulty += 1

            if self.stage == 2: self.distance_per_frame += 1

            # Different changes depending on each difficulty until 8
            if self.difficulty < 5:
                self.player_speed += 1
                self.possible_enemies['wild_minibot'][1] += 5
                self.possible_enemies['spike_minibot'][1] += 3
            else:
                self.player_speed += 2

            if self.difficulty == 2:
                if self.stage != 2:
                    self.possible_enemies['mototaxi'][1] += 5
                else:
                    self.possible_enemies['classB'][1] += 5
            if self.difficulty == 3:
                self.spawn_max += 1
                self.enemy_speed += 1

                if self.stage != 2:
                    self.possible_enemies['mototaxi'][1] += 3
                else:
                    self.possible_enemies['classB'][1] += 5
                    self.possible_enemies['classC'][1] += 5
                self.possible_enemies['hivebox'][1] += 5
                self.possible_enemies['fake_minibot'][1] += 3
            if self.difficulty == 4:
                self.possible_enemies['fake_minibot'][1] += 5
                if self.stage != 2:
                    self.possible_enemies['mototaxi'][1] += 2
                else:
                    self.possible_enemies['classB'][1] += 10
                    self.possible_enemies['classC'][1] += 5
                    self.possible_enemies['classD'][1] += 2
            if self.difficulty == 5:
                self.possible_enemies['hivebox'][1] += 5
                self.possible_enemies['hivebox'][3] += 1
                self.spawn_max += 1
            if self.difficulty == 6:
                self.possible_enemies['fake_minibot'][1] += 3
                if self.stage != 2:
                    self.possible_enemies['mototaxi'][1] += 10
                else:
                    self.possible_enemies['classB'][1] += 3
                    self.possible_enemies['classC'][1] += 5
                    self.possible_enemies['classD'][1] += 10
            if self.difficulty == 7:
                self.enemy_speed += 1
                self.possible_enemies['fake_minibot'][1] += 5

    # Main function to run the game
    def run(self, game):
        if not self.started:
            game.sound.play(self.music, -1)

            if self.stage == 1:
                game.player.toggle_run(True)
            else:
                game.player.toggle_run(False)

            game.player.reset_anim()

            self.started = True

        self.update(game)
        self.draw(game)

    def update(self, game):
        current_time = pygame.time.get_ticks()
        enemy_hit = False
        enemy_killed = False
        closest_to_plr = [None, 99999]

        # resetting enemy amount
        for enemy in self.enemy_list:
            self.possible_enemies[enemy.name][3] = 0

        # Checking enemy conditions
        for enemy in self.enemy_list:
            enemy.update(game)
            self.possible_enemies[enemy.name][3] += 1

            # Checking if you can destroy enemy
            if (game.player.key_pressed == enemy.remaining_text[0]
                    and enemy.rect.x < c.SCREEN_WIDTH):
                if enemy.name == 'fake_minibot':
                    ignore_fake = False

                    # Avoiding triggering if other enemies have letter
                    for other_enemies in self.enemy_list:
                        if (enemy.remaining_text[0] in other_enemies.remaining_text
                                and other_enemies.name != 'fake_minibot'):
                            ignore_fake = True

                    if not ignore_fake:
                        enemy.target_player()

                    continue

                enemy_hit = True
                enemy.remaining_text = enemy.remaining_text[1:]

                if not enemy.remaining_text:
                    self.enemy_list.remove(enemy)
                    enemy_killed = True
                    enemy_value = len(enemy.target_text)
                    game.player.success_hit(game, enemy_value)

                    if self.stage != 0:
                        to_gain = enemy_value * game.player.max_combo
                        game.player.reward(to_gain, (self.stage + self.difficulty))

            if enemy in self.enemy_list:
                # If enemy is the current closest to the player
                player_magnitude = enemy.rect.x - (c.SCREEN_WIDTH // 2) - 50
                if player_magnitude < closest_to_plr[1]:
                    closest_to_plr = [enemy, player_magnitude]

                # If enemy passed the limit to damage player
                if enemy.name != 'spike_minibot':
                    if (enemy.rect.x < self.max_enemy_distance
                            and enemy.name != 'fake_minibot'):
                        enemy.target_player()

        if enemy_hit:
            game.sound.shoot.play()
        if enemy_killed:
            game.sound.destroy.play()
            if self.stage > 0: game.sound.points.play()
        elif game.player.key_pressed and not enemy_hit:
            game.player.wrong_hit(game)

        for obstacle in self.obstacle_list:
            obstacle.update(game)

        # Updating the closest enemy to the player
        if closest_to_plr[0]:
            game.player.closest_enemy = closest_to_plr[0]

        game.player.on_input(game)

        ''' ===== CHECKING INSTANCES SPAWNING CONDITIONS ===== '''
        if not game.paused and game.player.lives > 0:
            # Enemy spawning every interval
            if (current_time - self.spawn_time > self.spawn_interval
                    and self.time_elapsed > 1):
                self.spawn_time = current_time
                lowest_interval = self.base_spawn_interval - self.difficulty * 200
                highest_interval = self.base_spawn_interval - self.difficulty * 50
                if lowest_interval < 500: lowest_interval = 500
                self.spawn_interval = random.randint(lowest_interval, highest_interval)

                if (self.obstacle_chance >= random.randint(1, 100)
                        and len(self.possible_obstacles) > 0):
                    self.spawn_obstacle(game)
                else:
                    self.spawn_enemy(game)

        # Updating instances
        game.left_hand.update(game)
        game.right_hand.update(game)
        game.player.update(game)

        if game.tick % game.FPS == 0:
            self.time_elapsed += 1

        if game.bullet_train.rect.centerx < 200:
            # Slowly decreasing intro speed for bullet train
            game.bullet_train.decelerate()
            game.bullet_train.update(game)

        # Incrementing distance every certain frames
        if self.stage != 0:
            distance_threshold = 10 - (self.player_speed if self.player_speed < 10 else 9)

            if game.tick % distance_threshold == 0:
                game.player.increase_distance(self.distance_per_frame)

                self.increase_difficulty(game)

        else:
            if game.player.max_combo >= 15 and not game.data["tutorial_finished"]:
                game.state = 'tutorial_end'
                game.player.reward(c.TUTORIAL_CASH)
                game.data["tutorial_finished"] = True

        self.floor_speed = c.BASE_FLOOR_SPEED + self.player_speed
        self.build_speed = c.BASE_BUILD_SPEED + (self.player_speed // 1.5)
        self.bg_speed = c.BASE_BG_SPEED + (self.player_speed // 2)

        if game.player.lives <= 0:
            game.sound.rocket.stop(True)
            game.state = 'gameover'
            game.paused = True

    def draw(self, game):
        # Drawing everything
        game.screen.fill(self.bg_color)
        update_terrain(game, game.level)

        if self.stage == 2:
            game.bullet_train.draw(game)

        game.left_hand.draw(game.screen)
        game.right_hand.draw(game.screen)

        game.player.draw(game)

        # Setting user interface
        game.text.levelUI_distance.set_text(f'{game.player.distance} m')
        game.text.levelUI_cash.set_text(f' {game.player.run_cash}')
        game.text.levelUI_lives.set_text(f'Lives: {game.player.lives}')
        game.text.levelUI_combo.set_text(f'Combo: {game.player.combo}')

        if self.stage > 0:
            game.text.levelUI_distance.draw(game)

        game.text.levelUI_cash.draw(game)
        game.text.levelUI_lives.draw(game)
        game.text.levelUI_combo.draw(game)

        # Always drawing fake minibots behind normal enemies to avoid unfair combos
        for enemy in self.enemy_list:
            if enemy.name == 'fake_minibot':
                enemy.draw(game)
        for enemy in self.enemy_list:
            if enemy.name != 'fake_minibot':
                enemy.draw(game)

        for obstacle in self.obstacle_list:
            obstacle.draw(game)

        if game.player.dodge_warned:
            dodge_rect_x = game.player.rect.x + 8
            dodge_rect_y = game.player.rect.y - 60
            game.text.levelUI_dodge.set_text(None, (dodge_rect_x, dodge_rect_y))
            game.text.levelUI_dodge.draw(game)

        if self.stage == 0:
            game.screen.blit(c.LV0_FILTER, (0, 0))
        if self.stage == 2:
            game.screen.blit(c.LV2_FILTER, (0, 0))
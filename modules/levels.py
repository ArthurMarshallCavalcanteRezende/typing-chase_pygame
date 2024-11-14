import pygame
import csv
import random
from modules import background as bg
from modules import enemy

pygame.mixer.init()

menace_music = './game_assets/music/The Ring - Klonoa.mp3'

def load_random_word(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        words = [row[0] for row in reader]
    return random.choice(words).lower()


def reset_game(game):
    """RESET ALL GAME VARIABLES FOR RESTART OR NEW LEVEL"""
    game.sound.play('menu', -1)

    if game.game_state == 'gameover':
        game.player.score += game.player.run_score

    game.player.lives = 3
    game.player.combo = 0
    game.player.max_combo = 0
    game.player.difficulty = 1
    game.player.speed = 3
    game.player.distance = 0
    game.player.run_score = 0

    game.enemy_speed = 2
    game.spawn_interval = 2000

    game.level = Level(game, game.level.stage)
    game.game_state = 'menu'
    game.paused = False


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
        level.name = game.LV0_NAME
        level.description = "like father, like son"
        level.difficulty_req = 200
        level.spawn_interval = 2500
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
        level.difficulty_req = 2500

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
        self.distance_per_frame = 1

        self.floor_size = (250, 250)
        self.bg_size = (game.SCREEN_HEIGHT, game.SCREEN_HEIGHT)

        self.floor_sprites = []
        self.bg_sprites = []
        self.enemy_list = []

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
        self.has_words = False

        self.spawn_max = 1
        self.word_chance = 0

        if self.stage == 0:
            self.word_list = [
                './all_words/left.txt',
                './all_words/right.txt'
            ]
            game.player.speed = 0
            self.enemy_speed = 1

        elif self.stage == 1:
            self.word_list = [
                './all_words/left.txt',
                './all_words/right.txt',
                './all_words/words_test.txt',
            ]
            self.word_chance = 10
            self.spawn_max = 1
            self.has_words = True
            game.player.speed = 3
        elif self.stage == 2:
            self.word_list = [
                './all_words/left.txt',
                './all_words/right.txt',
                './all_words/words_test.txt',
            ]
            self.word_chance = 40
            self.spawn_max = 2
            self.enemy_speed = 3
            self.has_words = True
            self.distance_per_frame = 3
            game.player.speed = 15

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
        new_speed = self.enemy_speed

        if self.stage > 0:
            spawn_count = random.randint(0, self.spawn_max)
            new_speed = random.randint(self.enemy_speed - 1, self.enemy_speed + 1)

        for new_enemy in range(spawn_count):
            spawned += 1 # Making sure only the first spawned is a word

            if self.has_words and spawned == 1:
                if random.randint(1, 100) <= self.word_chance:
                    choosen_txt = self.word_list[2]
                else:
                    choosen_txt = self.word_list[random.randint(0, 1)]
            else:
                choosen_txt = self.word_list[random.randint(0, 1)]

            new_word = load_random_word(choosen_txt)

            if len(new_word) > 1:
                if len(new_word) <= 5:
                    new_speed = 2
                else:
                    new_speed = 1

            new_enemy = enemy.Enemy(game, new_word, new_speed)

            self.enemy_list.append(new_enemy)


    # Main function to run the game
    def run(self, game):
        if not self.started:
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
        for enemy in self.enemy_list:
            enemy.update(game)

            if (game.player.key_pressed == enemy.remaining_text[0]
                and enemy.rect.x < game.SCREEN_WIDTH):
                enemy.remaining_text = enemy.remaining_text[1:]
                enemy_hit = True

                if not enemy.remaining_text:
                    self.enemy_list.remove(enemy)
                    enemy_killed = True

                    game.player.combo += 1 if len(enemy.target_text) <= 3 else 3
                    if game.player.combo > game.player.max_combo:
                        game.player.max_combo += 1 if len(enemy.target_text) <= 3 else 3

                    to_gain = len(enemy.target_text) * 10 * game.player.max_combo
                    game.player.run_score += to_gain * self.stage

                game.shoot_sound.play()

            if enemy in self.enemy_list:
                # If enemy is the current to the player
                player_magnitude = enemy.rect.x - (game.SCREEN_WIDTH // 2) - 50
                if player_magnitude < closest_to_plr[1]:
                    closest_to_plr = [enemy, player_magnitude]

                # If enemy passed the limit to damage player
                if enemy.rect.x < 200:
                    game.destroy_sound.play()
                    game.damage_sound.play()

                    game.player.lives -= 1
                    game.player.combo = 0
                    self.enemy_list.remove(enemy)
                    game.all_sprites.remove(enemy)

        if enemy_killed:
            game.destroy_sound.play()
            game.points_sound.play()
        elif game.player.key_pressed and not enemy_hit:
            game.wrong_sound.play()
            game.player.combo -= 1 if game.player.combo > 0 else 0

        game.player.key_pressed = None

        # Updating the closest enemy to the player
        if closest_to_plr[0]:
            game.player.closest_enemy = closest_to_plr[0]

        game.player.on_input(game)

        if not game.paused and game.player.lives > 0:
            # Enemy spawning every interval
            if current_time - self.enemy_spawn_time > self.spawn_interval:
                self.enemy_spawn_time = current_time
                self.spawn_enemy(game)

            # Updating all sprites
            game.all_sprites.update()

        game.left_hand.update(game.player.closest_enemy)
        game.right_hand.update(game.player.closest_enemy)

        game.tick += 1

        # Incrementing distance every certain frames
        if self.stage != 0:
            distance_threshold = 10 - (game.player.speed if game.player.speed < 10 else 9)

            if game.tick % distance_threshold == 0:
                game.player.distance += self.distance_per_frame

                # Increasing difficulty of the game over distances reached
                if game.player.distance > self.difficulty_req:
                    self.difficulty_req *= 2
                    game.player.difficulty += 1

                    if game.player.difficulty < 4:
                        game.player.speed += 1
                    elif 6 <= game.player.difficulty < 10:
                        game.player.speed += 2

                    if self.stage == 2: self.distance_per_frame += 1

                    if game.player.difficulty == 3: self.spawn_max += 1
                    if game.player.difficulty == 7: self.spawn_max += 1

                    print(f'DIFFICULTY {game.player.difficulty} REACHED! '
                          f'SPEED INCREASED TO {game.player.speed}')

        game.floor_speed = game.BASE_FLOOR_SPEED + game.player.speed
        game.bg_speed = game.BASE_BG_SPEED + (game.player.speed // 2)

        self.draw(game)

        if game.player.lives <= 0:
            game.game_state = 'gameover'
            game.paused = True

        game.clock.tick(game.FPS)

    def draw(self, game):
        # Drawing everything
        game.screen.fill(self.bg_color)

        bg.update_terrain(game, game.level)

        game.all_sprites.draw(game.screen)
        for enemy in self.enemy_list:
            enemy.draw(game)

        game.left_hand.draw(game.screen)
        game.right_hand.draw(game.screen)

        game.player.draw(game)

        # Setting user interface
        distance_text = game.large_font.render(f'{game.player.distance} m', True, game.COLORS.white)
        score_text = game.header_font.render(f' {game.player.run_score}', True, game.COLORS.white)
        lives_text = game.text_font.render(f'Lives: {game.player.lives}', True, game.COLORS.white)
        combo_text = game.text_font.render(f'Combo: {game.player.combo}', True, game.COLORS.white)

        # Actual word indicator
        if self.stage > 0:
            game.screen.blit(distance_text, (10, -5))

        if not game.paused:
            game.screen.blit(score_text, (50, 70))
            game.screen.blit(game.score_image, (5, 80))
            game.screen.blit(lives_text, (10, game.SCREEN_HEIGHT - 80))
            game.screen.blit(combo_text, (10, game.SCREEN_HEIGHT - 50))

        if self.stage == 2:
            game.screen.blit(game.bullet_train, game.bullet_train_rect)

    def game_over(self, game):
        # Game Over
        self.draw(game)

        pygame.mixer.music.set_volume(0.1)
        game.screen.blit(game.GAMEOVER_FILTER, (0, 0))

        game_over_text = game.title_font.render('GAME OVER', True, game.COLORS.red)
        distance_text = game.header_font.render(f'Distance Reached: {game.player.distance} M',
                                                 True, game.COLORS.bright_yellow)
        disks_text = game.large_font.render(f'Gained: {game.player.run_score}!',
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
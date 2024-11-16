import pygame
import os

PLR_ASSETS_PATH = './game_assets/player'

# Class for creating a spritesheet for animated sprites
class Sprite:
    def __init__(self, player, name, path, oneshot=False, custom_interval=None):
        self.name = name
        self.image_list = []
        self.image_path = PLR_ASSETS_PATH + f'/{path}'
        self.current_image = None
        self.oneshot = oneshot

        # Adding every frame image to the list to run through
        name_list = []

        for filename in os.listdir(self.image_path):
            name_list.append(filename)

        # Important to keep it from 1 to n organized
        name_list.sort()

        for filename in name_list:
            if filename.endswith('.png'):
                image = pygame.image.load(self.image_path + f'/{filename}').convert_alpha()
                image = pygame.transform.scale(image, (player.size, player.size))

                self.image_list.append(image)

        # Values for updating the animation frame per update interval
        self.index = 0
        self.max_index = len(self.image_list) - 1
        self.tick = 0
        self.custom_interval = custom_interval

        self.visible = False
        self.shot_enabled = False

        player.sprite_list.append(self)
        self.current_image = self.image_list[self.index]


    def update(self, player):
        self.tick += 1

        # Checking if image can update to next shot depending on interval
        if self.custom_interval:
            can_update = self.tick > self.custom_interval
        else:
            can_update = self.tick > player.update_interval

        if can_update:
            # Oneshot mode only runs the animation once, used for single actions.
            if self.oneshot:
                if self.shot_enabled:
                    self.tick = 0
                    self.index = 0
                    self.current_image = self.image_list[self.index]
                    self.shot_enabled = False

                self.tick = 0

                if not self.index > self.max_index:
                    self.current_image = self.image_list[self.index]
                    self.index += 1

            # Plays animation constantly if not oneshot mode
            else:
                self.tick = 0
                self.index += 1
                if self.index > self.max_index: self.index = 0

                self.current_image = self.image_list[self.index]

    def draw(self, game):
        if self.visible:
            # Position on top of bullet train on level 2
            if game.level.stage == 2:
                game.player.rect = game.player.train_rect
            else:
                game.player.rect = game.player.base_rect

            game.screen.blit(self.current_image, game.player.rect)


class Player:
    def __init__(self, game):
        super().__init__()
        self.sprite_list = []
        self.running_list = []
        self.oneshot_list = []
        self.size = 120

        # Left sprites put first so the game always draws them behind others
        self.run_left = Sprite(self, 'run_left', 'run/left_run')
        self.left_shoot = Sprite(self, 'left_shoot', 'shoot/left', True, 5)
        self.run_left_shoot = Sprite(self, 'run_left_shoot', 'run/left_shoot')
        self.running_list.append(self.run_left)
        self.oneshot_list.append(self.left_shoot)

        # Main body sprites
        self.idle = Sprite(self, 'idle', 'idle')
        self.run_body = Sprite(self, 'run_body', 'run/body')

        # Right sprites put last so the game always draws them on top of others
        self.run_right = Sprite(self, 'run_right', 'run/right_run')
        self.right_shoot = Sprite(self, 'right_shoot', 'shoot/right', True, 5)
        self.run_right_shoot = Sprite(self, 'run_right_shoot', 'run/right_shoot')
        self.running_list.append(self.run_body)
        self.running_list.append(self.run_right)
        self.oneshot_list.append(self.right_shoot)

        self.base_rect = pygame.Rect(0, 0, self.size, self.size)
        self.base_rect.center = game.player_pos
        self.shoot_visual_cd = [0, 32, False]
        self.is_running = False
        self.train_rect = pygame.Rect(
                    0,
                    self.base_rect.y - 150,
                    self.size, self.size)

        self.rect = self.base_rect
        self.hitbox = pygame.Rect(0, 0, self.size // 4, self.size // 2)

        self.lives = 3
        self.combo = 0
        self.max_combo = 0
        self.speed = 3
        self.base_interval = 8
        self.update_interval = self.base_interval

        # Game currency values
        self.score = 0
        self.run_score = 0

        self.distance = 0
        self.difficulty = 1
        self.closest_enemy = None
        self.action = None
        self.key_pressed = None

        self.letter_frame = game.text_frame.copy()
        self.letter_frame = pygame.transform.scale(self.letter_frame, (140, 140))
        self.letter_frame_rect = self.letter_frame.get_rect()
        self.letter_frame_rect.center = (game.SCREEN_WIDTH // 2, game.SCREEN_HEIGHT - 100)

        self.closest_letter = game.large_font.render('...', True, game.COLORS.white)
        self.closest_letter_rect = self.letter_frame.get_rect()
        self.closest_letter_rect.topleft = self.letter_frame_rect.center
        self.closest_letter_rect.y -= 12
        self.closest_letter_rect.x -= 12

        self.dots_text = '.'
        self.dots_interval = 15

        self.dodge = False
        self.invincible = False
        self.dodge_period = [0, 30]
        self.iv_frames = 0
        self.invincibility_time = 90
        self.iv_blink = [False, 0, 30]

        self.tick = 0

        self.reset_anim()


    def reset_anim(self):
        for sprite in self.sprite_list:
            sprite.visible = False

        if self.is_running:
            for sprite in self.running_list:
                sprite.visible = True
        else:
            self.idle.visible = True

    # Handle the basics of shooting animation
    def shoot_anim(self, side):
        self.shoot_visual_cd[0] = 0
        self.shoot_visual_cd[2] = True

        for sprite in self.sprite_list:
            sprite.visible = False

        if self.is_running:
            self.run_body.visible = True

            if side == 'left':
                self.run_left_shoot.visible = True
                self.run_right.visible = True
            elif side == 'right':
                self.run_right_shoot.visible = True
                self.run_left.visible = True
        else:
            if side == 'left':
                self.left_shoot.visible = True
                self.left_shoot.shot_enabled = True
            elif side == 'right':
                self.right_shoot.visible = True
                self.right_shoot.shot_enabled = True

    # Toggling dodge mode if not on cooldown
    def dodge_anim(self):
        if self.dodge:
            for sprite in self.sprite_list:
                sprite.visible = False

            self.left_shoot.visible = True
            self.dodge_period[0] += 1

            if self.dodge_period[0] > self.dodge_period[1]:
                self.dodge = False
                self.reset_anim()

    def on_input(self, game):
        if game.player.action:
            if game.player.action == 'shoot_left':
                self.shoot_anim('left')
            elif game.player.action == 'shoot_right':
                self.shoot_anim('right')
            elif game.player.action == 'dodge':
                if not self.dodge:
                    self.dodge = True
                    self.dodge_period[0] = 0

            game.player.action = None
        else:
            # Dealing with changing visuals back to idle or action form after some time
            if self.shoot_visual_cd[2]: self.shoot_visual_cd[0] += 1

            if (self.shoot_visual_cd[0] > self.shoot_visual_cd[1]
                and self.shoot_visual_cd[2]):
                self.shoot_visual_cd[0] = 0
                self.shoot_visual_cd[2] = False

                self.reset_anim()

    def damage(self, game):
        if not self.invincible:
            self.lives -= 1
            self.invincible = True
            self.iv_frames = 0

            game.damage_sound.play()

    def update(self, game):
        self.tick += 1
        self.hitbox.center = self.rect.center
        self.dodge_anim()

        if self.invincible:
            self.iv_frames += 1
            self.iv_blink[1] += 1

            if self.iv_frames > self.invincibility_time // 2:
                self.iv_blink[2] = 4
            else:
                self.iv_blink[2] = 8

            if self.iv_blink[1] > self.iv_blink[2]:
                self.iv_blink[1] = 0
                self.iv_blink[0] = not self.iv_blink[0]

            if self.iv_frames >= self.invincibility_time:
                self.invincible = False
        else:
            self.iv_blink[0] = False

        if self.closest_enemy and len(self.closest_enemy.remaining_text) > 0:
            new_color = game.COLORS.white
            if self.closest_enemy.name == 'fake_minibot':
                new_color = game.COLORS.red

            first_letter = self.closest_enemy.remaining_text[0]
            self.closest_letter = game.large_font.render(first_letter, True, new_color)
        else:
            if self.tick % self.dots_interval == 0:
                self.dots_text += '.'
                if len(self.dots_text) > 3: self.dots_text = '.'
            self.closest_letter = game.large_font.render(self.dots_text, True, game.COLORS.white)

        if game.level.stage == 2:
            self.train_rect.x = game.bullet_train_rect.centerx - self.size
            self.train_rect.y = game.bullet_train_rect.y + self.size // 2.2

    def draw(self, game):
        # Drawing visible sprites and positioning them with offsets
        self.update_interval = self.base_interval - self.difficulty
        if self.update_interval < 3: self.update_interval = 3

        for sprite in self.sprite_list:
            if not game.paused:
                sprite.update(self)

            if not self.iv_blink[0]:
                sprite.draw(game)

        game.screen.blit(self.letter_frame, self.letter_frame_rect)
        game.screen.blit(self.closest_letter, self.closest_letter_rect)
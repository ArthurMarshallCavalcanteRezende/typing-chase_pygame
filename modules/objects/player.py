import pygame
import constants as c
from utils.colors import Colors
from modules.sprite import Sprite
from modules.game_object import GameObject
colors = Colors()

class Player(GameObject):
    def __init__(self):
        super().__init__('player', Sprite('idle', c.plr_sprites['idle']), c.player_pos)

        # Left sprites put first so the game always draws them behind others
        self.run_left = Sprite('run_left', c.plr_sprites['run_left'], self.sprite_list)
        self.left_shoot = Sprite('left_shoot', c.plr_sprites['left_shoot'], self.sprite_list, True, 5)
        self.run_left_shoot = Sprite('run_left_shoot', c.plr_sprites['run_left_shoot'], self.sprite_list)
        self.moving_list.append(self.run_left)
        self.oneshot_list.append(self.left_shoot)

        # Main body sprites
        self.run_body = Sprite('run_body', c.plr_sprites['run_body'], self.sprite_list)
        self.dodge_idle = Sprite('dodge_idle', c.plr_sprites['dodge_idle'], self.sprite_list)
        self.dodge_run = Sprite('dodge_run', c.plr_sprites['dodge_run'], self.sprite_list)

        # Right sprites put last so the game always draws them on top of others
        self.run_right = Sprite('run_right', c.plr_sprites['run_right'], self.sprite_list)
        self.right_shoot = Sprite('right_shoot', c.plr_sprites['right_shoot'], self.sprite_list, True, 5)
        self.run_right_shoot = Sprite('run_right_shoot', c.plr_sprites['run_right_shoot'], self.sprite_list)
        self.moving_list.append(self.run_body)
        self.moving_list.append(self.run_right)
        self.oneshot_list.append(self.right_shoot)

        self.shoot_visual_cd = [0, 32, False]
        self.train_rect = pygame.Rect((0, self.base_rect.y - 150), self.size)
        self.hitbox = pygame.Rect((0, 0), (self.size[0] // 4, self.size[1] // 2))

        # PLayer values
        self.lives = 3
        self.run_cash = 0
        self.combo = 0
        self.max_combo = 0
        self.distance = 0

        self.closest_enemy = None
        self.action = None
        self.key_pressed = None

        self.letter_frame = c.text_frame.copy()
        self.closest_letter_rect = self.letter_frame.get_rect()

        self.dots_text = '.'
        self.dots_interval = 15

        self.dodge = False
        self.dodge_period = [0, 30]
        self.dodge_warned = False

        self.invincible = False
        self.iv_frames = 0
        self.invincibility_time = 90
        self.iv_blink = [False, 0, 30]

        self.reset_anim()

        # Setting values
        self.letter_frame = pygame.transform.scale(self.letter_frame, (140, 140))
        self.letter_frame_rect = self.letter_frame.get_rect()
        self.letter_frame_rect.center = (c.SCREEN_WIDTH // 2, c.SCREEN_HEIGHT - 100)

        self.closest_letter_rect.topleft = self.letter_frame_rect.center
        self.closest_letter_rect.y -= 12
        self.closest_letter_rect.x -= 12


    def reset_values(self):
        self.lives = 3
        self.combo = 0
        self.max_combo = 0
        self.distance = 0
        self.run_cash = 0
        self.dodge_warned = False

        self.closest_enemy = None
        self.dodge = False
        self.invincible = False

    def reset_anim(self):
        for sprite in self.sprite_list:
            sprite.visible = False

        if self.is_moving:
            for sprite in self.moving_list:
                sprite.visible = True
        else:
            self.base_sprite.visible = True

    def toggle_run(self, toggle):
        self.is_moving = toggle

    # Handle the basics of shooting animation
    def shoot_anim(self, side):
        self.shoot_visual_cd[0] = 0
        self.shoot_visual_cd[2] = True

        for sprite in self.sprite_list:
            sprite.visible = False

        if self.is_moving:
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

            if self.is_moving:
                self.dodge_run.visible = True
            else:
                self.dodge_idle.visible = True

            self.dodge_period[0] += 1

            if self.dodge_period[0] > self.dodge_period[1]:
                self.dodge = False
                self.reset_anim()

    def on_input(self, game):
        self.key_pressed = None

        if game.player.action:
            if game.player.action == 'shoot_left':
                self.shoot_anim('left')
            elif game.player.action == 'shoot_right':
                self.shoot_anim('right')
            elif game.player.action == 'dodge':
                if not self.dodge:
                    self.dodge = True
                    self.dodge_period[0] = 0
                    game.sound.dodge.play()

            game.player.action = None
        else:
            # Dealing with changing visuals back to idle or action form after some time
            if self.shoot_visual_cd[2]: self.shoot_visual_cd[0] += 1

            if (self.shoot_visual_cd[0] > self.shoot_visual_cd[1]
                and self.shoot_visual_cd[2]):
                self.shoot_visual_cd[0] = 0
                self.shoot_visual_cd[2] = False

                self.reset_anim()

    def damage(self, game, harmless=False):
        if not self.invincible:
            if not harmless:
                self.lives -= 1
                self.invincible = True
                self.iv_frames = 0
                game.sound.damage.play()

            self.combo = 0

    def reward(self, cash, multiplier=1):
        self.run_cash += cash * multiplier

    def success_hit(self, game, value):
        if value > 3: value = 3
        self.combo += value

        if self.combo > self.max_combo:
            self.max_combo = self.combo
        elif game.level.stage == 0:
            self.max_combo += value

    def wrong_hit(self, game):
        if self.key_pressed != ' ':
            self.combo -= 1 if self.combo > 0 else 0
            game.sound.wrong_input.play()

    def increase_distance(self, amount):
        self.distance += amount

    def update(self, game):
        self.hitbox.center = self.rect.center
        self.dodge_anim()
        game.text.playerUI_closest.set_color()

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
            if self.closest_enemy.name == 'fake_minibot':
                game.text.playerUI_closest.set_color(colors.red)

            first_letter = self.closest_enemy.remaining_text[0]
            game.text.playerUI_closest.set_text(first_letter, self.closest_letter_rect)
        else:
            if self.tick % self.dots_interval == 0:
                self.dots_text += '.'
                if len(self.dots_text) > 3: self.dots_text = '.'
            game.text.playerUI_closest.set_text(self.dots_text, self.closest_letter_rect)

        if game.level.stage == 2:
            self.train_rect.x = game.bullet_train.rect.centerx - self.size[0]
            self.train_rect.y = game.bullet_train.rect.y + self.size[0] // 2.2
            self.rect = self.train_rect
        else:
            self.rect = self.base_rect

        super().update(game)

    def draw(self, game):
        if not self.iv_blink[0]:
            super().draw(game)

        game.screen.blit(self.letter_frame, self.letter_frame_rect)
        game.text.playerUI_closest.draw(game)
import pygame
import os

IMG_SIZE = 120
PLR_ASSETS_PATH = './game_assets/player'

# Class for creating a spritesheet for animated sprites
class Sprite:
    def __init__(self, player, name, path):
        self.name = name
        self.image_list = []
        self.image_path = PLR_ASSETS_PATH + f'/{path}'
        self.current_image = None

        # Adding every frame image to the list to run through
        name_list = []

        for filename in os.listdir(self.image_path):
            name_list.append(filename)

        # Important to keep it from 1 to n organized
        name_list.sort()

        for filename in name_list:
            image = pygame.image.load(self.image_path + f'/{filename}').convert_alpha()
            image = pygame.transform.scale(image, (IMG_SIZE, IMG_SIZE))

            self.image_list.append(image)

        # Values for updating the animation frame per update interval
        self.index = 0
        self.max_index = len(self.image_list) - 1
        self.tick = 0

        self.visible = False

        player.sprite_list.append(self)
        self.current_image = self.image_list[self.index]


    def update(self, player):
        self.tick += 1

        if self.tick > player.update_interval:
            self.tick = 0
            self.index += 1
            if self.index > self.max_index: self.index = 0

            self.current_image = self.image_list[self.index]

    def draw(self, game):
        if self.visible:
            new_rect = game.player.rect

            if game.level.stage == 2:
                new_rect = pygame.Rect(
                    game.player.rect.x + 50,
                    game.player.rect.y - 150,
                    IMG_SIZE, IMG_SIZE)

            game.screen.blit(self.current_image, new_rect)


class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.sprite_list = []
        self.running_list = []

        # Left sprites put first so the game always draws them behind others
        self.run_left = Sprite(self, 'run_left', 'run/left_run')
        self.left_shoot = Sprite(self, 'left_shoot', 'shoot/left')
        self.run_left_shoot = Sprite(self, 'run_left_shoot', 'run/left_shoot')
        self.running_list.append(self.run_left)

        # Main body sprites
        self.idle = Sprite(self, 'idle', 'idle')
        self.run_body = Sprite(self, 'run_body', 'run/body')

        # Right sprites put last so the game always draws them on top of others
        self.run_right = Sprite(self, 'run_right', 'run/right_run')
        self.right_shoot = Sprite(self, 'right_shoot', 'shoot/right')
        self.run_right_shoot = Sprite(self, 'run_right_shoot', 'run/right_shoot')
        self.running_list.append(self.run_body)
        self.running_list.append(self.run_right)

        self.rect = pygame.Rect(0, 0, IMG_SIZE, IMG_SIZE)
        self.rect.center = position
        self.shoot_visual_cd = [0, 30, False]
        self.is_running = False
        self.shooting = False

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

        self.reset_anim()


    def reset_anim(self):
        self.shooting = False

        for sprite in self.sprite_list:
            sprite.visible = False

        if self.is_running:
            for sprite in self.running_list:
                sprite.visible = True
        else:
            self.idle.visible = True

    # Handle the basics of shooting animation
    def shoot_anim(self, side):
        self.shooting = True

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
            elif side == 'right':
                self.right_shoot.visible = True

        self.shoot_visual_cd[2] = True

    def on_input(self, game):
        if game.player.action:
            if game.player.action == 'shoot_left':
                self.shoot_anim('left')
            elif game.player.action == 'shoot_right':
                self.shoot_anim('right')

            game.player.action = None
        else:
            # Dealing with changing visuals back to idle or action form after some time
            if self.shoot_visual_cd[2]: self.shoot_visual_cd[0] += 1

            if (self.shoot_visual_cd[0] > self.shoot_visual_cd[1]
                and self.shoot_visual_cd[2]):
                self.shoot_visual_cd[0] = 0
                self.shoot_visual_cd[2] = False

                self.reset_anim()


    def draw(self, game):
        # Drawing visible sprites and positioning them with offsets
        self.update_interval = self.base_interval - self.difficulty
        if self.update_interval < 3: self.update_interval = 3

        for sprite in self.sprite_list:
            if not game.paused: sprite.update(self)

            if sprite.visible:
                sprite.draw(game)
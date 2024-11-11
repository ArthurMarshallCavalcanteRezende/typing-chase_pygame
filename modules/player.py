import pygame

IMG_SIZE = 120
PLR_ASSETS_PATH = './game_assets/player'

# Creating a sprite with various custom properties
def create_sprite(player, name, path):
    image = pygame.image.load(path + f'/{name}.png').convert_alpha()
    image = pygame.transform.scale(image, (IMG_SIZE, IMG_SIZE))

    sprite = {
        'name': name,
        'image': image,
        'visible': False,
        'offset_x': 0,
        'offset_y': 0
    }

    player.sprite_list.append(sprite)
    return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.sprite_list = []

        self.body = create_sprite(self, 'body', PLR_ASSETS_PATH)
        self.glasses = create_sprite(self, 'glasses', PLR_ASSETS_PATH)

        # Separated limbs for each side of the player
        self.left_action = create_sprite(self, 'left_action', PLR_ASSETS_PATH)
        self.left_idle = create_sprite(self, 'left_idle', PLR_ASSETS_PATH)
        self.left_shoot = create_sprite(self, 'left_shoot', PLR_ASSETS_PATH)

        self.right_action = create_sprite(self, 'right_action', PLR_ASSETS_PATH)
        self.right_idle = create_sprite(self, 'right_idle', PLR_ASSETS_PATH)
        self.right_shoot_down = create_sprite(self, 'right_shoot_down', PLR_ASSETS_PATH)
        self.right_shoot_middle = create_sprite(self, 'right_shoot_middle', PLR_ASSETS_PATH)
        self.right_shoot_top = create_sprite(self, 'right_shoot_top', PLR_ASSETS_PATH)

        self.rect = self.body['image'].get_rect()
        self.rect.center = position
        self.shoot_visual_cd = [0, 30, False]
        self.click_visual_cd = [0, 30, False]
        self.action_mode = True

        self.lives = 3
        self.score = 0
        self.combo = 0
        self.max_combo = 0

        self.distance = 0
        self.difficulty = 1
        self.closest_enemy = None

        for sprite in self.sprite_list:
            # Making only action sprites visible
            if (sprite['name'] != 'left_idle'
                    and sprite['name'] != 'right_action'
                    and sprite['name'] != 'body'
                    and sprite['name'] != 'glasses'):

                sprite['visible'] = False
            else:
                sprite['visible'] = True

    # Handle the basics of shooting animation
    def shoot_anim(self, to_visible, glasses_offset):
        self.right_shoot_top['visible'] = False
        self.right_shoot_middle['visible'] = False
        self.right_shoot_down['visible'] = False
        self.right_action['visible'] = False
        self.right_idle['visible'] = False
        self.left_idle['visible'] = False
        self.left_action['visible'] = False

        to_visible['visible'] = True

        self.glasses['offset_y'] = glasses_offset
        self.click_visual_cd[2] = True
        self.shoot_visual_cd[2] = True

    def on_input(self, action):
        if action:

            # Running through every sprite to check key conditions
            for sprite in self.sprite_list:
                if action == sprite['name']:

                    if sprite['name'] == 'right_shoot_down':
                        self.shoot_anim(self.left_action, 1)
                    elif sprite['name'] == 'right_shoot_middle':
                        self.shoot_anim(self.left_action, -3)
                    elif sprite['name'] == 'right_shoot_top':
                        self.shoot_anim(self.left_action, -6)

                    sprite['visible'] = True
                    break

        else:
            # Dealing with changing limb pressing "keyboard" visually after some time
            if self.click_visual_cd[2]: self.click_visual_cd[0] += 1

            if (self.click_visual_cd[0] > self.click_visual_cd[1]
                and self.click_visual_cd[2]):
                self.click_visual_cd[0] = 0
                self.click_visual_cd[2] = False
                self.left_action['visible'] = False
                self.left_idle['visible'] = True


            # Dealing with changing visuals back to idle or action form after some time
            if self.shoot_visual_cd[2]: self.shoot_visual_cd[0] += 1

            if (self.shoot_visual_cd[0] > self.shoot_visual_cd[1]
                and self.shoot_visual_cd[2]):
                self.shoot_visual_cd[0] = 0
                self.shoot_visual_cd[2] = False
                self.glasses['offset_y'] = 0

                for sprite in self.sprite_list:

                    if self.action_mode:
                        # Making only idle sprites visible
                        if (sprite['name'] != 'left_idle'
                                and sprite['name'] != 'right_action'
                                and sprite['name'] != 'body'
                                and sprite['name'] != 'glasses'):

                            sprite['visible'] = False
                        else:
                            sprite['visible'] = True
                    else:
                        # Making only idle sprites visible
                        if (sprite['name'] != 'left_idle'
                            and sprite['name'] != 'right_idle'
                            and sprite['name'] != 'body'
                            and sprite['name'] != 'glasses'):

                            sprite['visible'] = False
                        else:
                            sprite['visible'] = True


    def draw(self, screen):
        # Drawing visible sprites and positioning them with offsets
        for sprite in self.sprite_list:
            if sprite['visible']:
                new_rect = pygame.Rect(
                    self.rect.x + sprite['offset_x'],
                    self.rect.y + sprite['offset_y'],
                    IMG_SIZE, IMG_SIZE)
                screen.blit(sprite['image'], new_rect)

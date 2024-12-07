import pygame

HAND_SIZE = 120

# Color for each finger on the guide hands
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

def create_finger(hand, name, path, color):
    image = pygame.image.load(path + f'/{name}.png').convert_alpha()
    image = pygame.transform.scale(image, (HAND_SIZE, HAND_SIZE))
    image.fill(color[name], special_flags=pygame.BLEND_RGBA_MULT)

    # Making a library of properties for easy access in code
    finger = {
        'name': name,
        'image': image,
        'color': color[name],
        'pressed': False,
    }

    hand.finger_list.append(finger)
    return finger

class Hands():
    def __init__(self, image_path, position, side):
        self.side = side
        self.hand_sprite = pygame.image.load(image_path + '/hand.png').convert_alpha()
        self.hand_sprite = pygame.transform.scale(self.hand_sprite, (HAND_SIZE, HAND_SIZE))
        self.hand_base = pygame.image.load(image_path + '/base.png').convert_alpha()
        self.hand_base = pygame.transform.scale(self.hand_base, (HAND_SIZE, HAND_SIZE))
        self.finger_list = []

        # Creating each finger with its defined properties as a list
        # This means that each finger is a list, not just a sprite
        self.hand_thumb = create_finger(self, 'thumb', image_path, HAND_COLORS[side])
        self.hand_index = create_finger(self, 'index', image_path, HAND_COLORS[side])
        self.hand_middle = create_finger(self, 'middle', image_path, HAND_COLORS[side])
        self.hand_ring = create_finger(self, 'ring', image_path, HAND_COLORS[side])
        self.hand_pinkie = create_finger(self, 'pinkie', image_path, HAND_COLORS[side])
        self.highlighted = None

        self.rect = self.hand_base.get_rect()
        self.rect.center = position

    def update(self, game):
        closest = game.player.closest_enemy

        if (not closest or not closest.finger_highlight or
                not closest in game.level.enemy_list):
            self.highlighted = None

            return

        for finger in self.finger_list:
            if closest and (finger['name'] == closest.finger_highlight[1]
                and self.side == closest.finger_highlight[0]):
                self.highlighted = finger


    def draw(self, screen):
        # Drawing every finger
        screen.blit(self.hand_sprite, self.rect)
        screen.blit(self.hand_base, self.rect)

        # Desenhar cor de cada dedo se tiver
        if self.highlighted:
            screen.blit(self.highlighted['image'], self.rect)
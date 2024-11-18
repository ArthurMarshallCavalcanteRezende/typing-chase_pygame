import pygame

HAND_SIZE = 120

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
    def __init__(self, image_path, position, colors):
        self.side = ''
        self.hand_sprite = pygame.image.load(image_path + '/hand.png').convert_alpha()
        self.hand_sprite = pygame.transform.scale(self.hand_sprite, (HAND_SIZE, HAND_SIZE))
        self.hand_base = pygame.image.load(image_path + '/base.png').convert_alpha()
        self.hand_base = pygame.transform.scale(self.hand_base, (HAND_SIZE, HAND_SIZE))
        self.finger_list = []

        # Creating each finger with its defined properties as a list
        # This means that each finger is a list, not just a sprite
        self.hand_thumb = create_finger(self, 'thumb', image_path, colors)
        self.hand_index = create_finger(self, 'index',image_path, colors)
        self.hand_middle = create_finger(self, 'middle',image_path, colors)
        self.hand_ring = create_finger(self, 'ring',image_path, colors)
        self.hand_pinkie = create_finger(self, 'pinkie',image_path, colors)
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
import pygame

class GameObject:
    def __init__(self, name, sprite_path, width, height, x, y, up_down, left_right):

        # Object form
        self.name = name
        self.sprite_list = []
        self.base_x = x
        self.base_y = y
        self.base_rect = pygame.Rect(0, 0, width, height)
        self.object_rect = pygame.Rect(x, y, width, height)

        # Object movement
        self.speed_x = up_down
        self.speed_y = left_right

        # Object update
        self.update_interval = 1
        self.tick = 1
        self.is_moving = False
        self.alive = True
        self.lifetime = 10
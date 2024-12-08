import pygame
from pygame.math import Vector2


def collides_with():
    player_damage = 1
    return player_damage


class GameObject:
    def __init__(self, name, sprite_path, width, height, x, y, up_down, left_right):

        # Object form
        self.name = name
        self.sprite_list = []
        self.base_x = x
        self.base_y = y
        self.position = Vector2(x, y)
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

    def draw(self):
        blit_position = self.position - Vector2(width / 2)
        surface.blit(self.sprite_list, blit_position)

    def update(self):
        if self.alive:
            self.is_moving = True
            self.object_rect.x += self.speed_x
            self.object_rect.y += self.speed_y

            self.tick += 1

            if self.tick % self.update_interval == 0:
                if self.sprite_list:
                    self.sprite_list.append(self.sprite_list.pop(0))


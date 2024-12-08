import pygame

class GameObject:
    def __init__(self, name, base_sprite, position=(0, 0), speed_x=0, speed_y=0):
        # Object form
        self.name = name
        self.sprite_list = []
        self.moving_list = []
        self.oneshot_list = []

        self.position = position
        self.base_sprite = base_sprite
        self.sprite_list.append(base_sprite)

        self.size = self.base_sprite.current_image.get_size()
        self.base_rect = pygame.Rect(self.position, self.size)
        self.rect = self.base_rect

        # Object movement
        self.speed_x = speed_x
        self.speed_y = speed_y

        # Object update
        self.update_interval = 8
        self.tick = 0
        self.can_collide = True
        self.is_moving = False
        self.alive = True
        self.lifetime = 0
        self.max_lifetime = 0   # Must be set to 0 or lower if lives forever

    def set_collision(self, toggle):
        self.can_collide = toggle

    def kill(self):
        self.alive = False

    def change_interval(self, value):
        self.update_interval = value
        if self.update_interval < 3: self.update_interval = 3

    def update(self, game):
        self.tick += 1

        if self.max_lifetime > 0:
            if game.FPS % self.tick == 0:
                self.lifetime += 1

            if self.lifetime > self.max_lifetime:
                self.kill()

        if self.alive:
            self.is_moving = True
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

    def draw(self, game):
        # Drawing visible sprites and positioning them with offsets
        for sprite in self.sprite_list:
            if not game.paused:
                sprite.update(self)

            sprite.draw(game, self)

    def collides_with(self, other_rect):
        if self.rect.colliderect(other_rect) and self.can_collide:
            return True
        else:
            return False


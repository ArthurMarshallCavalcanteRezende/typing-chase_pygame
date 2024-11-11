import pygame

SCREEN_WIDTH = 800

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image_path, speed):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.key = self.extract_key(image_path)
        self.finger_highlight = None
        self.speed = speed

    def extract_key(self, image_path):
        filename = image_path.split('/')[-1]
        return filename[0].lower()

    def update_lvl1(self):
        self.rect.x -= self.speed
        if self.rect.x < -self.rect.width:
            self.kill()

    def update_lvl2(self):
        direction_x = self.player.rect.x - self.rect.x
        direction_y = self.player.rect.y - self.rect.y
        distance = (direction_x ** 2 + direction_y ** 2) ** 0.5

        elapsed_time = (pygame.time.get_ticks() - self.spawn_time) / 1000
        if elapsed_time == 7:
            self.rect.x += self.speed * (direction_x / distance)
            self.rect.y += self.speed * (direction_y / distance)
        if elapsed_time > 8:
            self.kill()



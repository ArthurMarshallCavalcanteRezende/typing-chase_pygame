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

    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -self.rect.width:
            self.kill()



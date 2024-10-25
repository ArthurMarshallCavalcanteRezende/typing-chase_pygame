import pygame

SCREEN_WIDTH = 800


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image_path):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.key = image_path.split('/')[-1][5]  # Exemplo: 'robotq' -> 'q'

    def update(self):
        self.rect.x -= 3
        if self.rect.x < -self.rect.width:
            self.kill()


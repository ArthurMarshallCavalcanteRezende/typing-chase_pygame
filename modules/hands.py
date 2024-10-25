import pygame

class Hands(pygame.sprite.Sprite):
    def __init__(self, image_path, position):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.topleft = position
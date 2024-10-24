import pygame
import time

pygame.init()
pygame.mixer.init()

BORDER_THICKNESS = 0
FIELD_WIDTH = 0
FIELD_HEIGHT = 0

class Enemy(pygame.sprite):
    def __init__(self):
        super().__init__()
        self.images = {
            'robotQ': pygame.transform.scale(pygame.image.load(images['robotQ']).convert_alpha(), (60, 60)),
            'robotA': pygame.trandform.scale(pygame.image.load(images['robotA']).convert_alpha(), (60, 60)),
            'robotZ': pygame.transform.scale(pygame.image.load(images['robotZ']).convert_alpha(), (60, 60)),
        }

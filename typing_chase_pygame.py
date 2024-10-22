import pygame

pygame.init()

# Define colors
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_DARK_GRAY = (50, 50, 50)

# Screen size
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 900
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Typing Chase - PyGame Edition - 2024-10-22")

# Loop
running = True

while running:
    screen.fill(COLOR_BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
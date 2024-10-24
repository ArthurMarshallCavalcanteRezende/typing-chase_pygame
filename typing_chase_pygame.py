import pygame

pygame.init()

# Define colors
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_DARK_GRAY = (50, 50, 50)

# Screen size
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Typing Chase - PyGame Edition - 2024-10-22")


enemy_left = {
    'robotQ': './game_assets/Qrobot.png',
    'robotA': './game_assets/Arobot.png',
    'robotZ': './game_assets/Zrobot.png',
    'robotW': './game_assets/Wrobot.png',
    'robotS': './game_assets/Srobot.png',
    'robotX': './game_assets/Xrobot.png',
    'robotE': './game_assets/Erobot.png',
    'robotD': './game_assets/Drobot.png',
    'robotC': './game_assets/Crobot.png',
    'robotR': './game_assets/Rrobot.png',
    'robotF': './game_assets/Frobot.png',
    'robotV': './game_assets/Vrobot.png',
    'robotT': './game_assets/Trobot.png',
    'robotG': './game_assets/Grobot.png',
    'robotB': './game_assets/Brobot.png',
}

# stage images
stage_back = pygame.transform.scale(pygame.image.load("./game_assets/hunt_stage.png").convert_alpha(), (800, 600))

# Sounds
chase_music = pygame.mixer.Sound('./game_assets/Too Good Too Bad.mp3')
chase_music.play(-1)

# Loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(stage_back, (0, 0))

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
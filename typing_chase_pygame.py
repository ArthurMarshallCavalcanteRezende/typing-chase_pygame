import pygame
import sys
from modules import level_0 as lvl_0
from modules import level_1 as lvl_1
from modules import level_2 as lvl_2

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Typing Chase - Beta edition - 2024-11-11")


def menu_interface():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 30)

    # Texto para cada fase
    phrase_0 = font.render("0 - Like father, like son...", True, (255, 255, 255))
    phrase_1 = font.render("1 - Coffee for today task.", True, (255, 255, 255))
    phrase_2 = font.render("2 - Freeze ZH4R0V!!!", True, (255, 255, 255))
    screen.blit(phrase_0, (300, 200))
    screen.blit(phrase_1, (300, 300))
    screen.blit(phrase_2, (300, 400))

    pygame.display.flip()


def run(game):
    running = True
    while running:
        menu_interface()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    lvl_0.run_game0()
                elif event.key == pygame.K_1:
                    lvl_1.run_game1()
                elif event.key == pygame.K_2:
                    lvl_2.run_game2()

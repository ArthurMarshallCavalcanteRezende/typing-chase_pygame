""" LOADING SCREEN INTERFACES """

import pygame
import random

def display(game, loaded=False):
    game.loading_percent += random.randint(7, 15)
    if game.loading_percent > 100 or loaded: game.loading_percent = 100
    message = f'Loading... ({game.loading_percent}%)'
    if loaded: message = 'Game Loaded!'

    game.loading_text = game.large_font.render(message, True, game.COLORS.white[0])
    game.loadint_text_pos = (game.SCREEN_WIDTH // 3.5, game.SCREEN_HEIGHT // 2.5)

    game.screen.fill(game.COLORS.black[0])
    game.screen.blit(game.loading_text, game.loadint_text_pos)
    pygame.display.flip()
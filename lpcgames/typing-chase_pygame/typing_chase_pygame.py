import pygame
import sys
from modules import levels

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

def reset_game(game):
    """RESET ALL GAME VARIABLES FOR RESTART OR NEW LEVEL"""
    game.player.lives = 3
    game.player.score = 0
    game.player.combo = 0
    game.player.max_combo = 0
    game.player.levelup_req = 800
    game.player.level_multi = 1

    game.enemy_speed = 2
    game.level = 1
    game.spawn_interval = 2000

    game.enemies.empty()
    game.all_sprites.empty()

def load_level(game, level):
    reset_game(game)
    game.level = levels.Level(game, 1)
    game.game_state = 'level'
    level.start_game(game)

def run(game):
    game.running = True

    while game.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    load_level(game, 1)
                elif event.key == pygame.K_1:
                    lvl_1.run_game1()
                elif event.key == pygame.K_2:
                    lvl_2.run_game2()

        # Loading different things depending on game state
        if game.game_state == 'menu':
            menu_interface()
        elif game.game_state == 'level':
            game.level.run(game)

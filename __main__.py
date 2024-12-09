"""
    Main module to load the game and run the primary loops
"""
import pygame
import traceback
import sys
from typing_chase import Game

DEBUG = True

if __name__ == '__main__':
    game = Game()

    try:
        # Running the game
        game.run()
    except Exception as e:
        print(f"Error while trying to run TYPING-CHASE: {e}")
        if DEBUG: traceback.print_exc()
    finally:
        game.save_data()
        pygame.quit()
        sys.exit()

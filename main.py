"""
    Main module to load the game and run the primary loops
"""
import traceback

import pygame
import sys
import typing_chase_pygame
from game_data import load_game

''' 
    !!! IMPORTANT !!! ALWAYS CREATE CONSTANTS/VARIABLES IN "game_data.py" TO ACCESS THEM ANYWHERE 
    If you don't know how to access them, just send the game class to any other place 
    and use it to get all of the juicy values inside it!

    Ex: send this class to player.py and name it "game" there, then you can use
    game.COLORS or game.FPS and access the values in there.
'''

DEBUG = True

class game:
    def __init__(self):
        # Loading every constant or important variable for the game
        # Access 'game_data.py' to find or add variables

        try:
            load_game(self)
        except Exception as e:
            print(f"Error while loading recourses: {e}")
            print(f"Check if any files have been changed or renamed.")
            if DEBUG: traceback.print_exc()
            pygame.quit()
            sys.exit()


if __name__ == '__main__':
    pygame.init()

    # Getting the game class and everything preloaded
    game = game()

    try:
        # Running the game
        game.menu_music.play(-1)
        typing_chase_pygame.run(game)
    except Exception as e:
        print(f"Error while trying to run TYPING-CHASE: {e}")
        if DEBUG: traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()

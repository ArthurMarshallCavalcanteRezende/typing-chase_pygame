""" LOADING SCREEN INTERFACES """
import constants as c

def display(game):
    game.screen.fill(c.LOCKED_FILTER)
    game.text.loading.draw(game)
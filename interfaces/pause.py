""" PAUSE SCREEN INTERFACES """
import constants as c

def display(game):
    game.level.draw(game)
    game.screen.blit(c.DARK_FILTER, (0, 0))

    game.text.pause_title.draw(game)
    game.text.pause_option1.draw(game)
    game.text.pause_option2.draw(game)
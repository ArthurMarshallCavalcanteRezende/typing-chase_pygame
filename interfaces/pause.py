""" PAUSE SCREEN INTERFACES """
import constants as c

def display(game):
    game.level.draw(game)
    game.screen.blit(c.DARK_FILTER, (0, 0))

    game.text.pauseUI_title.draw(game)
    game.text.pauseUI_option1.draw(game)
    game.text.pauseUI_option2.draw(game)
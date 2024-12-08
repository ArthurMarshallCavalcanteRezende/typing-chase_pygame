""" GAME OVER SCREEN INTERFACES """
import constants as c
from utils.colors import Colors
colors = Colors()

def display(game):
    # Game Over
    game.level.draw(game)
    game.screen.blit(c.GAMEOVER_FILTER, (0, 0))

    game.text.gameoverUI_title.draw(game)
    game.text.gameoverUI_distance.draw(game)
    game.text.gameoverUI_disks.draw(game)
    game.text.gameoverUI_combo.draw(game)
    game.text.gameoverUI_option1.draw(game)


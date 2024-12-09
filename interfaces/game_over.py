""" GAME OVER SCREEN INTERFACES """
import constants as c
from utils.colors import Colors
colors = Colors()

def display(game):
    # Game Over
    game.level.draw(game)
    game.screen.blit(c.GAMEOVER_FILTER, (0, 0))

    game.text.gameoverUI_distance.set_text(f'Distance Reached: {game.player.distance}m')
    game.text.gameoverUI_cash.set_text(f'Gained: {game.player.run_cash}')
    game.text.gameoverUI_combo.set_text(f'Max Combo: {game.player.max_combo}')

    game.text.gameoverUI_title.draw(game)
    game.text.gameoverUI_distance.draw(game)
    game.text.gameoverUI_cash.draw(game)
    game.text.gameoverUI_combo.draw(game)
    game.text.gameoverUI_option1.draw(game)


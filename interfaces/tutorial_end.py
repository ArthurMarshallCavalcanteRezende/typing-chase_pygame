""" INTERFACES FOR REWARD SCREENS """
import constants as c

def display(game):
    # Screen for when done with tutorial on level 0
    game.level.draw(game)
    game.screen.blit(c.TUTORIAL_FILTER, (0, 0))

    game.text.tutorialUI_title.draw(game)
    game.text.tutorialUI_freebies.draw(game)
    game.text.tutorialUI_disks.draw(game)
    game.text.tutorialUI_unlock.draw(game)
    game.text.tutorialUI_option1.draw(game)

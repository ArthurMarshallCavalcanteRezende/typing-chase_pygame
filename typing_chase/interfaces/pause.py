""" PAUSE SCREEN INTERFACES """

def display(game):
    game.level.draw(game)
    game.screen.blit(game.DARK_FILTER, (0, 0))

    pause_text1 = game.title_font.render('PAUSED', True, game.COLORS.bright_yellow)
    pause_text2 = game.text_font.render('> SPACE: resume game', True, game.COLORS.white)
    pause_text3 = game.text_font.render('> ESC: back to menu', True, game.COLORS.white)

    game.screen.blit(pause_text1,
                     (game.SCREEN_WIDTH // 2 - 120, 100))
    game.screen.blit(pause_text2,
                     (game.SCREEN_WIDTH // 2 - 120, 220))
    game.screen.blit(pause_text3,
                     (game.SCREEN_WIDTH // 2 - 120, 260))
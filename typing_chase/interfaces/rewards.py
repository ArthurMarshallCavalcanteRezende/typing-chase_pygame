""" INTERFACES FOR REWARD SCREENS """

def tutorial_finish(game):
    # Screen for when done with tutorial on level 0
    game.level.draw(game)
    game.screen.blit(game.TUTORIAL_FILTER, (0, 0))

    motivate_text = game.large_font.render("You're getting the hang of it!", True, game.COLORS.white)
    freebie_text = game.header_font.render(f"Here, take these freebies:",
                                           True, game.COLORS.bright_yellow)
    disks_text = game.large_font.render(f'{game.TUTORIAL_CASH}!',
                                        True, game.COLORS.bright_cyan)
    unlock_text = game.text_font.render(f'Use these to unlock the next level!', True,
                                        game.COLORS.white)
    menu_text = game.text_font.render('> SPACE: back to menu',
                                      True, game.COLORS.white)

    game.screen.blit(motivate_text,
                     (game.SCREEN_WIDTH // 2 - 340, 100))
    game.screen.blit(freebie_text,
                     (game.SCREEN_WIDTH // 2 - 220, 180))
    game.screen.blit(game.death_score_image,
                     (game.SCREEN_WIDTH // 2 - 135, 250))
    game.screen.blit(disks_text,
                     (game.SCREEN_WIDTH // 2 - 50, 240))
    game.screen.blit(unlock_text,
                     (game.SCREEN_WIDTH // 2 - 210, 350))
    game.screen.blit(menu_text,
                     (game.SCREEN_WIDTH // 2 - 120, 420))
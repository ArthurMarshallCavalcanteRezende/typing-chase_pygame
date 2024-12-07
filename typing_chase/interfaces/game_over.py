""" GAME OVER SCREEN INTERFACES """

def display(game):
    # Game Over
    game.level.draw(game)
    game.screen.blit(game.GAMEOVER_FILTER, (0, 0))

    game_over_text = game.title_font.render('GAME OVER', True, game.COLORS.red)
    distance_text = game.header_font.render(f'Distance Reached: {game.player.distance} M',
                                            True, game.COLORS.bright_yellow)
    disks_text = game.large_font.render(f'Gained: {game.player.run_cash}!',
                                        True, game.COLORS.bright_cyan)
    max_combo_text = game.text_font.render(f'Max Combo: {game.player.max_combo}', True,
                                           game.COLORS.white)
    menu_text = game.text_font.render('> SPACE: back to menu',
                                      True, game.COLORS.white)

    game.screen.blit(game_over_text,
                     (game.SCREEN_WIDTH // 2 - 180, 70))
    game.screen.blit(distance_text,
                     (game.SCREEN_WIDTH // 2 - 180, 180))
    game.screen.blit(max_combo_text,
                     (game.SCREEN_WIDTH // 2 - 100, 230))
    game.screen.blit(game.death_score_image,
                     (game.SCREEN_WIDTH // 2 - 180, 300))
    game.screen.blit(disks_text,
                     (game.SCREEN_WIDTH // 2 - 100, 290))
    game.screen.blit(menu_text,
                     (game.SCREEN_WIDTH // 2 - 120, 400))

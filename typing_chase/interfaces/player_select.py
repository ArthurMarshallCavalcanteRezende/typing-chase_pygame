""" PLAYER SELECT INTERFACES """

def display(game):
    game.screen.fill(game.COLORS.space_blue)
    game.stars_emitter.update(game)

    input_name = game.large_font.render('input your name:', True, game.COLORS.white)
    data_text = game.text_font.render('the game will save your data, just type', True, game.COLORS.bright_yellow)
    data_text2 = game.text_font.render('the same name you used to load it!', True, game.COLORS.bright_yellow)

    game.account_string = ''
    final_dots = False
    if game.account_check_index != 0:
        game.account_string +=  f'|   ...   '

    # Creating a string list of the names for players
    # User will be able to search through them with the left and right arrow keys
    for index in range(len(game.account_names)):
        if index < 6 and index + game.account_check_index < len(game.account_names):
            game.account_string += f'|   {game.account_names[game.account_check_index + index]}   '
        else:
            if index < len(game.account_names) - 1 and not final_dots:
                game.account_string += f'|   ...'
                final_dots = True

    accounts_created = game.text_font.render('ACCOUNTS CREATED:', True, game.COLORS.white)
    search_tip = game.small_font.render('( left or right arrow keys to search through them )',
                                        True, game.COLORS.bright_grey)
    previous_data = game.small_font.render(f'{game.account_string}', True, game.COLORS.white)

    if game.tick % 30 == 0:
        game.input_blink = not game.input_blink

    if (game.digit_pressed
        and game.digit_pressed in game.eligible_names
        or game.digit_pressed == '_'):

        if len(game.player_name) <= 12:
            if game.digit_pressed.isalpha() or len(game.player_name) > 0:
                game.player_name += game.digit_pressed
                game.digit_pressed = None
        else:
            game.input_blink = False
    elif game.digit_pressed == 'backspace':
        game.player_name = game.player_name[:-1]
        game.digit_pressed = None

    new_name = game.player_name + ('_' if game.input_blink else '')
    name_text = game.large_font.render(new_name, True, game.COLORS.white)

    game.screen.blit(input_name, (200, 100))
    game.screen.blit(name_text, (200, 180))
    game.screen.blit(data_text, (150, 300))
    game.screen.blit(data_text2, (180, 335))
    game.screen.blit(accounts_created, (20, 425))
    game.screen.blit(search_tip, (20, 460))
    game.screen.blit(previous_data, (20, 500))
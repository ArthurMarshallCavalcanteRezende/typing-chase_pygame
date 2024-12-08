""" PLAYER SELECT INTERFACES """
import constants as c
from utils.colors import Colors
colors = Colors()

accounts_string = ''
input_blink = False

def display(game):
    global accounts_string, input_blink
    
    game.screen.fill(colors.space_blue)
    game.stars_emitter.update(game)

    accounts_string = ''
    final_dots = False
    if game.account_check_index != 0:
        accounts_string +=  f'|   ...   '

    # Creating a string list of the names for players
    # User will be able to search through them with the left and right arrow keys
    acc_count = len(c.account_names)

    for index in range(acc_count):
        if index < 6 and index + game.account_check_index < acc_count:
            current_name = c.account_names[game.account_check_index + index]
            accounts_string += f'|   {current_name}   '
        else:
            if index < acc_count - 1 and not final_dots:
                accounts_string += f'|   ...'
                final_dots = True

    # Making the input underscore blink every 30 frames
    if game.tick % 30 == 0:
        input_blink = not input_blink

    # Change player name depending on input
    if (game.digit_pressed
        and game.digit_pressed in c.eligible_names
        or game.digit_pressed == '_'):

        if len(game.player_name) <= 12:
            if game.digit_pressed.isalpha() or len(game.player_name) > 0:
                game.player_name += game.digit_pressed
                game.digit_pressed = None
        else:
            input_blink = False
    elif game.digit_pressed == 'backspace':
        game.player_name = game.player_name[:-1]
        game.digit_pressed = None

    new_name = game.player_name + ('_' if input_blink else '')

    game.text.selectUI_name.set_text(new_name)
    game.text.selectUI_data.set_text(accounts_string)

    game.text.selectUI_input.draw(game)
    game.text.selectUI_name.draw(game)
    game.text.selectUI_text1.draw(game)
    game.text.selectUI_text2.draw(game)
    game.text.selectUI_accounts.draw(game)
    game.text.selectUI_tip.draw(game)
    game.text.selectUI_data.draw(game)
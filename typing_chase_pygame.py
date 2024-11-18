import pygame
import sys
from modules import levels
import game_data

pygame.init()
pygame.display.set_caption("Typing Chase - Beta edition - 2024-11-11")

DODGE_KEYTABLE = [
    pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.KMOD_LSHIFT, pygame.KMOD_RSHIFT,
    pygame.KSCAN_LSHIFT, pygame.KSCAN_RSHIFT,

    pygame.K_LCTRL, pygame.K_RCTRL, pygame.KMOD_LCTRL, pygame.KMOD_RCTRL,
    pygame.KSCAN_LCTRL, pygame.KSCAN_RCTRL,

    pygame.K_SPACE, pygame.KSCAN_SPACE
]

def menu_interface(game):
    game.screen.fill(game.COLORS.space_blue)
    game.stars_emitter.update(game)

    lv0_color = game.COLORS.white
    lv1_color = game.COLORS.white
    lv2_color = game.COLORS.white

    # Adding level background and changes if there is a level choosen
    if game.level:
        game.screen.fill(game.COLORS.dark_grey)

        for sprite in game.level.bg_sprites:
            sprite.draw(game)

        if game.level.floor_lights: game.screen.blit(game.level.floor_lights, game.level.fl_pos)
        if game.level.floor_neon: game.screen.blit(game.level.floor_neon, game.level.fn_pos)

        for sprite in game.level.floor_sprites:
            sprite.draw(game)

        description = game.text_font.render(f'- - - - =|  {game.level.description}  |',
                                            True, game.COLORS.white)

        level_locked = False
        price = game.LV_COSTS[f'level{game.level.stage}']

        if game.level.stage == 0:
            lv0_color = game.COLORS.yellow
            if not game.data['level0']['unlocked']:
                game.data['level0']['unlocked'] = True
        if game.level.stage == 1:
            lv1_color = game.COLORS.yellow
            if not game.data['level1']['unlocked']:
                lv1_color = game.COLORS.grey
                level_locked = True
        if game.level.stage == 2:
            lv2_color = game.COLORS.yellow
            if not game.data['level2']['unlocked']:
                lv2_color = game.COLORS.grey
                level_locked = True

        locked_text = game.large_font.render(f'[ LOCKED ]', True, game.COLORS.bright_red)

        if game.data['cash'] >= price:
            cost_text = game.header_font.render(f'COST: {price}', True, game.COLORS.lime)
        else:
            cost_text = game.header_font.render(f'COST: {price}', True, game.COLORS.red)

        if level_locked:
            game.screen.blit(game.LOCKED_FILTER, (0, 0))
            game.screen.blit(locked_text, (120, 170))
            game.screen.blit(cost_text, (170, 270))
            game.screen.blit(game.locked_score_image, (120, 280))

    else:
        description = game.text_font.render(f'- - - - =|  CHOOSE A LEVEL!  |',
                                            True, game.COLORS.white)

    # Anything under here is for UI
    game.screen.blit(game.menu_ui, (0, 0))
    game.screen.blit(description, (20, game.SCREEN_HEIGHT - 40))

    title_text1 = game.title_font.render('TYPING ]', True, game.COLORS.bright_yellow)
    title_text2 = game.title_font.render('CHASE ]', True, game.COLORS.bright_yellow)
    game.screen.blit(title_text1, (510, 40))
    game.screen.blit(title_text2, (520, 120))

    choose_text = game.text_font.render('> Choose a level! ( ENTER to play)', True, game.COLORS.white)
    game.screen.blit(choose_text, (20, 20))

    score_text = game.large_font.render(f' {game.data["cash"]}', True, game.COLORS.bright_cyan)
    game.screen.blit(score_text, (70, 470))
    game.screen.blit(game.menu_score_image, (10, 487))

    lv0_text = game.header_font.render(game.LV0_NAME, True, lv0_color)
    lv1_text = game.header_font.render(game.LV1_NAME, True, lv1_color)
    lv2_text = game.header_font.render(game.LV2_NAME, True, lv2_color)
    game.screen.blit(lv0_text, (500, 400))
    game.screen.blit(lv1_text, (500, 330))
    game.screen.blit(lv2_text, (500, 260))


def player_select_interface(game):
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


def change_level(game, value):
    game.level_index += value

    # Minimium and maximum level indexes possible
    if game.level_index < 0:
        game.level_index = 0
    elif game.level_index > 2:
        game.level_index = 2

def run(game):
    game.running = True
    game.player.reset_anim()
    game.sound.play('menu', -1)

    while game.running:
        game.tick += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
                # Saving data before leaving game
                game_data.save_datastore(game)

                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and not game.key_down:
                game.key_down = True
                game.digit_pressed = event.unicode.lower()

                ''' HANDLING MENU CONTROLS '''
                if game.state == 'menu':
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        change_level(game, 1)
                        game.level = levels.Level(game, game.level_index)
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        change_level(game, -1)
                        game.level = levels.Level(game, game.level_index)

                    if event.key == pygame.K_0: game.level = levels.Level(game, 0)
                    if event.key == pygame.K_1: game.level = levels.Level(game, 1)
                    if event.key == pygame.K_2: game.level = levels.Level(game, 2)

                    if event.key == pygame.K_RETURN:
                        if game.level:
                            if game.data[f'level{game.level.stage}']['unlocked']:
                                game.state = 'level'
                            else:
                                if game.data['cash'] >= game.LV_COSTS[f'level{game.level.stage}']:
                                    game.data['cash'] -= game.LV_COSTS[f'level{game.level.stage}']

                                    game.data[f'level{game.level.stage}']['unlocked'] = True
                                    game.sound.trigger.play()
                                    game.sound.levelup.play()
                                else:
                                    game.sound.wrong_input.play()

                        else:
                            game.level_index = 0j
                    elif event.key == pygame.K_ESCAPE:
                        game.level = None
                        game.level_index = -1

                ''' HANDLING PAUSED GAME '''
                if game.state == 'pause':
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        game.state = 'level'
                        game.paused = False
                        game.sound.pause_sfx(False)
                        pygame.mixer.music.set_volume(0.3)
                    elif event.key == pygame.K_ESCAPE:
                        levels.reset_game(game)

                ''' HANDLING LEVEL CONTROLS '''
                if game.state == 'level':
                    game.player.key_pressed = event.unicode

                    if event.key == pygame.K_ESCAPE:
                        game.paused = True
                        game.state = 'pause'
                        game.sound.pause_sfx(True)

                    if not game.paused and game.player.lives > 0:
                        # Checking if player hit enemy and returns the action

                        if game.player.key_pressed in game.left_letters:
                            game.player.action = 'shoot_left'
                        elif game.player.key_pressed in game.right_letters:
                            game.player.action = 'shoot_right'

                        if event.key in DODGE_KEYTABLE:
                            game.player.action = 'dodge'


                ''' HANDLING RETURN TO MENU SCREENS '''
                if game.state == 'gameover':
                    if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                        levels.reset_game(game)
                if game.state == 'tutorial_end':
                    if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                        levels.reset_game(game, False)

                ''' HANDLING ACCOUNT SCREEN CONTROLS '''
                if game.state == 'player_select':
                    if event.key == pygame.K_LEFT or event.key == pygame.KSCAN_LEFT:
                        game.account_check_index -= 1
                        if game.account_check_index <= -len(game.account_names):
                            game.account_check_index = 0

                    if event.key == pygame.K_RIGHT or event.key == pygame.KSCAN_RIGHT:
                        game.account_check_index += 1
                        if game.account_check_index >= len(game.account_names):
                            game.account_check_index = 0

                    if event.key == pygame.K_RETURN:
                        if len(game.player_name) >= 2:
                            # Loading player data or creating new data file
                            game_data.load_datastore(game)
                            game.state = 'menu'

                    if event.key == pygame.K_BACKSPACE:
                        game.digit_pressed = 'backspace'
                    if event.key == pygame.K_UNDERSCORE:
                        game.digit_pressed = '_'

            elif event.type == pygame.KEYUP:
                game.key_down = False
            elif game.state == 'menu' and game.key_down:
                game.key_down = False


        # Loading different things depending on game state
        if game.state == 'menu':
            menu_interface(game)
        if game.state == 'player_select':
            player_select_interface(game)
            game.on_select = True
        elif game.level and game.state == 'level':
            game.level.run(game)
        elif game.level and game.state == 'pause':
            game.level.pause(game)
        elif game.level and game.state == 'gameover':
            game.level.game_over(game)
        elif game.level and game.state == 'tutorial_end':
            game.level.tutorial_finish(game)

        if game.state == 'menu' or game.state == 'player_select':
            game.stars_emitter.enabled = True
        else:
            game.stars_emitter.enabled = False

        # Updating the screen
        pygame.display.flip()
        game.clock.tick(game.FPS)

    # In case of problems with the loop
    game_data.save_datastore(game)
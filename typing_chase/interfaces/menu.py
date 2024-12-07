""" MENU SCREEN INTERFACES """
from utils import constants as c

def display(game):
    game.screen.fill(game.colors.space_blue)
    game.stars_emitter.update(game)

    lv0_color = game.colors.white
    lv1_color = game.colors.white
    lv2_color = game.colors.white

    # Adding level background and changes if there is a level choosen
    if game.level:
        game.screen.fill(game.colors.dark_grey)

        if game.level.screen_bg:
            game.screen.blit(game.level.screen_bg, (0, 0))

        for sprite in game.level.bg_list:
            sprite.draw(game)

        for sprite in game.level.build_list:
            sprite.draw(game)

        if game.level.floor_lights: game.screen.blit(game.level.floor_lights, game.level.fl_pos)
        if game.level.floor_neon: game.screen.blit(game.level.floor_neon, game.level.fn_pos)

        for sprite in game.level.floor_list:
            sprite.draw(game)

        description = c.text_font.render(f'- - - - =|  {game.level.description}  |',
                                            True, game.colors.white)

        level_locked = False
        price = c.LV_COSTS[f'level{game.level.stage}']

        if game.level.stage == 0:
            lv0_color = game.colors.yellow
            if not game.data['level0']['unlocked']:
                game.data['level0']['unlocked'] = True
        if game.level.stage == 1:
            lv1_color = game.colors.yellow
            if not game.data['level1']['unlocked']:
                lv1_color = game.colors.grey
                level_locked = True
        if game.level.stage == 2:
            lv2_color = game.colors.yellow
            if not game.data['level2']['unlocked']:
                lv2_color = game.colors.grey
                level_locked = True

        locked_text = c.large_font.render(f'[ LOCKED ]', True, game.colors.bright_red)

        if game.data['cash'] >= price:
            cost_text = c.header_font.render(f'COST: {price}', True, game.colors.lime)
        else:
            cost_text = c.header_font.render(f'COST: {price}', True, game.colors.red)

        if level_locked:
            game.screen.blit(game.LOCKED_FILTER, (0, 0))
            game.screen.blit(locked_text, (120, 170))
            game.screen.blit(cost_text, (170, 270))
            game.screen.blit(game.locked_score_image, (120, 280))

    else:
        description = game.text_font.render(f'- - - - =|  CHOOSE A LEVEL!  |',
                                            True, game.colors.white)

    # Anything under here is for UI
    game.screen.blit(c.menu_ui, (0, 0))
    game.screen.blit(description, (20, c.SCREEN_HEIGHT - 40))

    title_text1 = c.title_font.render('TYPING ]', True, game.colors.bright_yellow)
    title_text2 = c.title_font.render('CHASE ]', True, game.colors.bright_yellow)
    game.screen.blit(title_text1, (510, 40))
    game.screen.blit(title_text2, (520, 120))

    choose_text = c.text_font.render('> Choose a level! ( ENTER to play)', True, game.colors.white)
    game.screen.blit(choose_text, (20, 20))

    score_text = c.large_font.render(f' {game.data["cash"]}', True, game.colors.bright_cyan)
    game.screen.blit(score_text, (70, 470))
    game.screen.blit(game.menu_score_image, (10, 487))

    lv0_text = c.header_font.render(c.LV0_NAME, True, lv0_color)
    lv1_text = c.header_font.render(c.LV1_NAME, True, lv1_color)
    lv2_text = c.header_font.render(c.LV2_NAME, True, lv2_color)
    game.screen.blit(lv0_text, (500, 400))
    game.screen.blit(lv1_text, (500, 330))
    game.screen.blit(lv2_text, (500, 260))
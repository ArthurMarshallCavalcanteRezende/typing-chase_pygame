""" MENU SCREEN INTERFACES """
import constants as c
from utils.colors import Colors
colors = Colors()

def display(game):
    game.screen.fill(colors.space_blue)
    game.stars_emitter.update(game)

    # Adding level background and changes if there is a level choosen
    if game.level:
        game.screen.fill(colors.dark_grey)

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

        game.text.menuUI_level_desc.set_text(f'- - - - =|  {game.level.description}  |')

        level_locked = False
        price = c.LV_COSTS[f'level{game.level.stage}']

        # resetting the color of each
        game.text.menuUI_lv0.set_color()
        game.text.menuUI_lv0.set_color()
        game.text.menuUI_lv0.set_color()

        if game.level.stage == 0:
            game.text.menuUI_lv0.set_color(colors.yellow)
            if not game.data['level0']['unlocked']:
                game.data['level0']['unlocked'] = True
        if game.level.stage == 1:
            game.text.menuUI_lv1.set_color(colors.yellow)
            if not game.data['level1']['unlocked']:
                game.text.menuUI_lv1.set_color(colors.grey)
                level_locked = True
        if game.level.stage == 2:
            game.text.menuUI_lv2.set_color(colors.yellow)
            if not game.data['level2']['unlocked']:
                game.text.menuUI_lv2.set_color(colors.grey)
                level_locked = True

        game.text.menuUI_level_cost.set_text(f'COST: {price}')
        if game.data['cash'] >= price:
            game.text.menuUI_level_cost.set_color(colors.lime)
        else:
            game.text.menuUI_level_cost.set_color(colors.red)

        if level_locked:
            game.screen.blit(c.LOCKED_FILTER, (0, 0))
            game.text.menuUI_level_locked.draw(game)
            game.text.menuUI_level_cost.draw(game)

    else:
        game.text.menuUI_level_desc.set_text('- - - - =|  CHOOSE A LEVEL!  |')

    game.screen.blit(c.log_ui, (0, c.log_ui.get_height() // 3))
    game.text.menuUI_account.set_text(f'> Logged as: {game.player_name}')
    game.text.menuUI_cash.set_text(f'{game.data["cash"]}')

    # Anything under here is for UI
    game.screen.blit(c.menu_ui, (0, 0))

    game.text.menuUI_level_desc.draw(game)

    game.text.menuUI_title1.draw(game)
    game.text.menuUI_title2.draw(game)

    game.text.menuUI_account.draw(game)
    game.text.menuUI_cash.draw(game)

    game.text.menuUI_lv0.draw(game)
    game.text.menuUI_lv1.draw(game)
    game.text.menuUI_lv2.draw(game)
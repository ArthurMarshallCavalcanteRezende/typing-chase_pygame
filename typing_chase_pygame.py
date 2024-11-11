import pygame
import sys
from modules import levels

pygame.init()
pygame.display.set_caption("Typing Chase - Beta edition - 2024-11-11")

def menu_interface(game):
    game.screen.fill(game.COLORS.dark_orange)

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
        game.screen.blit(description, (20, game.SCREEN_HEIGHT - 40))
        if game.level.stage == 0: lv0_color = game.COLORS.yellow
        if game.level.stage == 1: lv1_color = game.COLORS.yellow
        if game.level.stage == 2: lv2_color = game.COLORS.yellow

    # Anything under here is for UI
    game.screen.blit(game.menu_ui, (0, 0))

    title_text1 = game.title_font.render('TYPING ]', True, game.COLORS.bright_yellow)
    title_text2 = game.title_font.render('CHASE ]', True, game.COLORS.bright_yellow)
    game.screen.blit(title_text1, (510, 40))
    game.screen.blit(title_text2, (520, 120))

    choose_text = game.text_font.render('> press 0, 1, or 2 to choose level!', True, game.COLORS.white)
    choose_text2 = game.text_font.render('> ENTER to play', True, game.COLORS.white)
    game.screen.blit(choose_text, (20, 20))
    game.screen.blit(choose_text2, (20, 60))

    lv0_text = game.header_font.render(game.LV0_NAME, True, lv0_color)
    lv1_text = game.header_font.render(game.LV1_NAME, True, lv1_color)
    lv2_text = game.header_font.render(game.LV2_NAME, True, lv2_color)
    game.screen.blit(lv0_text, (500, 400))
    game.screen.blit(lv1_text, (500, 330))
    game.screen.blit(lv2_text, (500, 260))



def reset_game(game):
    """RESET ALL GAME VARIABLES FOR RESTART OR NEW LEVEL"""
    game.player.lives = 3
    game.player.combo = 0
    game.player.max_combo = 0
    game.player.difficulty = 1
    game.player.speed = 3
    game.player.distance = 0

    game.enemy_speed = 2
    game.spawn_interval = 2000

    game.enemies.empty()
    game.all_sprites.empty()
    game.game_state = 'menu'


def run(game):
    game.running = True

    while game.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game.game_state == 'menu':
                    if event.key == pygame.K_0:
                        game.level = levels.Level(game, 0)
                        game.menu_music.stop()
                    elif event.key == pygame.K_1:
                        game.level = levels.Level(game, 1)
                        game.menu_music.stop()
                    elif event.key == pygame.K_2:
                        game.level = levels.Level(game, 2)
                        game.menu_music.stop()

                    if event.key == pygame.K_RETURN:
                        game.game_state = 'level'

                if game.game_state == 'level':
                    if event.key == pygame.K_ESCAPE:
                        game.game_state = 'pause'

        # Loading different things depending on game state
        if game.game_state == 'menu':
            menu_interface(game)
        elif game.level and game.game_state == 'level':
            game.level.run(game)
        elif game.level and game.game_state == 'pause':
            game.level.pause(game)

        # Updating the screen
        pygame.display.flip()
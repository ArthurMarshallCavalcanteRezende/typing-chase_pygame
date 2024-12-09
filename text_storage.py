"""
    This module is used solely for storing all the pre-made text for the game,
    utilizing a custom text class for better customization and control.
"""

import constants as c
from utils.text import Text
from utils.colors import Colors
colors = Colors()

class TextStorage:
    def __init__(self):
        self.loading = Text('Loading', (c.SCREEN_WIDTH // 3.5, c.SCREEN_HEIGHT // 2.5),
                            c.large_font, colors.white)

        # ============ MENU TEXT ============
        self.menuUI_title1 = Text('TYPING ]', (510, 40), c.title_font, colors.bright_yellow)
        self.menuUI_title2 = Text('CHASE ]', (520, 120), c.title_font, colors.bright_yellow)
        self.menuUI_cash = Text(' nil', (70, 470), c.large_font, colors.bright_cyan)

        self.menuUI_cash.set_icon(c.cash_image, 60, (-8, 13))

        self.menuUI_account = Text('> Logged as: nil', (20, 20), c.text_font, colors.white)
        self.menuUI_level_desc =  Text('- - - - =|  CHOOSE A LEVEL!  |', (20, 560), c.text_font, colors.white)
        self.menuUI_level_cost =  Text('nil', (170, 270), c.header_font, colors.red)
        self.menuUI_level_locked = Text('[ LOCKED ]', (120, 170), c.large_font, colors.bright_red)

        self.menuUI_level_cost.set_icon(c.cash_image, 50, (-8, 5))

        self.menuUI_lv0 = Text(c.LV0_NAME,  (500, 400), c.header_font, colors.white)
        self.menuUI_lv1 = Text(c.LV1_NAME,  (500, 330), c.header_font, colors.white)
        self.menuUI_lv2 = Text(c.LV2_NAME,  (500, 260), c.header_font, colors.white)

        # ============ LEVEL TEXT ============
        self.levelUI_distance = Text('nil', (10, -5), c.large_font, colors.white)
        self.levelUI_cash = Text('nil', (45, 70), c.header_font, colors.bright_cyan)
        self.levelUI_lives = Text('Lives: nil', (10, 550), c.text_font, colors.white)
        self.levelUI_combo = Text('Combo: nil', (10, 520), c.text_font, colors.white)
        self.levelUI_dodge = Text('DODGE!!', (10, 350), c.header_font, colors.red)

        self.levelUI_dodge.set_color_blink(True, colors.orange, 5)
        self.levelUI_cash.set_icon(c.cash_image, 35, (-3, 9))

        # ============ PAUSE TEXT ============
        self.pauseUI_title = Text('PAUSED', (280, 100), c.title_font, colors.bright_yellow)
        self.pauseUI_option1 = Text('> SPACE: resume game', (280, 220), c.text_font, colors.white)
        self.pauseUI_option2 = Text('> ESC: back to menu', (280, 260), c.text_font, colors.white)

        # ============ GAME OVER TEXT ============
        self.gameoverUI_title = Text('GAME OVER', (220, 70), c.title_font, colors.red)
        self.gameoverUI_distance = Text('Distance Reached: nil', (220, 180), c.header_font, colors.bright_yellow)
        self.gameoverUI_cash = Text('Gained: nil', (230, 240), c.large_font, colors.bright_cyan)
        self.gameoverUI_combo = Text('Max Combo: nil', (220, 320), c.text_font, colors.white)
        self.gameoverUI_option1 = Text('> SPACE: back to menu', (280, 400), c.text_font, colors.white)

        self.gameoverUI_cash.set_icon(c.cash_image, 60, (-8, 13))

        # ============ PLAYER SELECT TEXT ============
        self.selectUI_input = Text('Input your name:', (200, 100), c.large_font, colors.white)
        self.selectUI_name = Text('', (200, 180), c.large_font, colors.white)
        self.selectUI_text1 = Text('the game will save your data, just type',
                                   (150, 300), c.text_font, colors.bright_yellow)
        self.selectUI_text2 = Text('the same name you used to load it!',
                                   (180, 335), c.text_font, colors.bright_yellow)
        self.selectUI_accounts = Text('ACCOUNTS CREATED:', (20, 425), c.text_font, colors.white)
        self.selectUI_tip = Text('( left or right arrow keys to search through them )',
                                 (20, 460), c.small_font, colors.bright_grey)
        self.selectUI_data = Text('',
                                 (20, 500), c.small_font, colors.white)

        # ============ TUTORIAL END TEXT ============
        self.tutorialUI_title = Text("You're getting the hang of it!", (60, 100), c.large_font, colors.white)
        self.tutorialUI_freebies = Text("Here, take these freebies:", (180, 180), c.header_font, colors.bright_yellow)
        self.tutorialUI_cash = Text(str(c.TUTORIAL_CASH), (350, 250), c.large_font, colors.bright_cyan)
        self.tutorialUI_unlock= Text('Use these to unlock the next level!', (190, 100), c.text_font, colors.white)
        self.tutorialUI_option1 = Text('> SPACE: back to menu', (280, 100), c.text_font, colors.white)

        self.tutorialUI_cash.set_icon(c.cash_image, 60, (0, 0))

        # ============ PLAYER TEXT ============
        self.playerUI_closest = Text('...', (0, 0), c.large_font, colors.white)
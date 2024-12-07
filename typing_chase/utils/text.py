"""
Class made to handle managing text and applying effects or changes
"""

class Text:
    def __init__(self, text, rect, font, base_color=(255, 255, 255), background=False,
                 background_color=(0, 0, 0), blink_interval=15, blink_color=(255, 255, 200)):
        self.string = text
        self.rect = rect
        self.font = font
        self.enabled = True
        self.visible = True

        # Visual effects for text
        self.blink = False
        self.color_blink = False
        self.background = background

        self.base_color = base_color
        self.current_color = base_color
        self.blink_color = blink_color
        self.background_color = background_color

        self.blink_tick = 0
        self.blink_interval = blink_interval


    def toggle(self, enable):
        self.enabled = enable

    def toggle_blink(self, blink, interval=None):
        self.blink = blink
        if interval: self.blink_interval = interval

    def toggle_color_blink(self, color_blink, color=None, interval=None):
        self.color_blink = color_blink
        if color: self.blink_color = color
        if interval: self.blink_interval = interval

    def update_text(self, new_text, new_rect=None):
        self.string = new_text
        if new_rect: self.rect = new_rect

    def blink_text(self):
        if not self.enabled: return

        # Visibility blinking check
        if self.blink and self.blink_tick >= self.blink_interval:
            self.visible = not self.visible
            self.blink_tick = 0

        # Color blinking check
        if self.color_blink and self.blink_tick >= self.blink_interval:
            self.blink_tick = 0
            if self.current_color != self.blink_color:
                self.current_color = self.blink_color
            else:
                self.current_color = self.base_color


    def draw(self, game):
        self.blink_tick += 1
        self.blink_text()

        if self.enabled and self.visible:
            # Applying built-in background for text is enabled
            if self.background:
                render_text = self.font.render(self.string, True, self.current_color, self.background_color)
            else:
                render_text = self.font.render(self.string, True, self.current_color)

            render_rect = render_text.get_rect(center=self.rect)
            game.screen.blit(render_text, render_rect)
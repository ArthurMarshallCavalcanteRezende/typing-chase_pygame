class Sprite:
    def __init__(self, name, image_list, sprite_list=None, oneshot=False, custom_interval=None):
        self.name = name
        self.image_list = image_list
        self.current_image = None
        self.oneshot = oneshot

        # Values for updating the animation frame per update interval
        self.index = 0
        self.max_index = len(self.image_list) - 1
        self.tick = 0
        self.custom_interval = custom_interval

        self.visible = True
        self.shot_enabled = False

        self.current_image = self.image_list[self.index]

        if sprite_list:
            sprite_list.append(self)

    def update(self, instance):
        self.tick += 1

        # Checking if image can update to next shot depending on interval
        if self.custom_interval:
            can_update = self.tick > self.custom_interval
        else:
            can_update = self.tick > instance.update_interval

        if can_update:
            # Oneshot mode only runs the animation once, used for single actions.
            if self.oneshot:
                if self.shot_enabled:
                    self.tick = 0
                    self.index = 0
                    self.current_image = self.image_list[self.index]
                    self.shot_enabled = False

                self.tick = 0

                if not self.index > self.max_index:
                    self.current_image = self.image_list[self.index]
                    self.index += 1

            # Plays animation constantly if not oneshot mode
            else:
                self.tick = 0
                self.index += 1
                if self.index > self.max_index: self.index = 0

                self.current_image = self.image_list[self.index]

    def draw(self, game, instance):
        if self.visible:
            game.screen.blit(self.current_image, instance.rect)

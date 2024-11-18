class Sprite:
    def __init__(self, name, image_list, oneshot=False, custom_interval=None):
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

    def update(self, enemy):
        self.tick += 1

        # Checking if image can update to next shot depending on interval
        if self.custom_interval:
            can_update = self.tick > self.custom_interval
        else:
            can_update = self.tick > enemy.update_interval

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

    def draw(self, game, enemy):
        if self.visible:
            game.screen.blit(self.current_image, enemy.rect)


class Obstacle:
    def __init__(self, game, name, sprite_list, size):
        self.reached_player = False
        self.size = size

        self.name = name
        self.sprite = Sprite('idle', sprite_list)
        self.rect = None
        self.base_interval = 2
        self.update_interval = self.base_interval

        self.rect = self.sprite.current_image.get_rect()

        self.lifetime = 0
        self.tick = 0
        self.speed = 0
        self.direction_x = 0
        self.direction_y = 0
        self.offset = 0

        if self.name == 'missile':
            self.speed = 4 + game.player.difficulty
            self.rect.x = game.SCREEN_WIDTH + self.size
            self.rect.y = game.player.rect.centery - (self.size // 1.5)

            if self.speed > 10: self.speed = 10
            game.sound.rocket.stop()
            game.sound.rocket.parent = self
            game.sound.rocket.play(-1)
        elif self.name == 'barrier':
            self.rect.x = game.SCREEN_WIDTH + self.size
            self.rect.y = game.player.rect.centery - (self.size // 1.2)

        self.can_hit = True
        self.alarm_on = True


    def update(self, game):
        self.tick += 1
        self.sprite.update(self)

        if self.tick % game.FPS == 0:
            self.lifetime += 1

        # Missile movement
        if self.name == 'missile':
            self.direction_x = -self.speed
        elif self.name == 'barrier':
            self.direction_x = -game.floor_speed

        self.rect.x += self.direction_x
        self.rect.y += self.direction_y

        # Remove if offscreen
        if self.rect.x < -100 or self.lifetime >= 30:
            game.level.obstacle_list.remove(self)

            if self.name == 'missile' and game.sound.rocket.parent == self:
                game.sound.rocket.stop()

        if self.rect.x < game.player.rect.x + self.size + 150 and self.alarm_on:
            game.sound.caution.play()
            self.alarm_on = False

        # Damage player when colliding
        if self.rect.colliderect(game.player.hitbox) and self.can_hit:
            if not game.player.dodge:
                self.can_hit = False
                game.player.damage(game)
                game.sound.destroy.play()

                game.player.combo = 0

                if self.name == 'missile':
                    game.level.obstacle_list.remove(self)
                    if self.name == 'missile' and game.sound.rocket.parent == self:
                        game.sound.rocket.stop(True)
                    game.sound.explode.play()
                if self.name == 'barrier':
                    game.sound.metal_hit.play()
            else:
                self.can_hit = False


    def draw(self, game):
        self.update_interval = self.base_interval
        self.sprite.draw(game, self)

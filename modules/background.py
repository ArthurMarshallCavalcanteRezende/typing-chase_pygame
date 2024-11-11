import pygame

def update_terrain(game):
    min_floor = None
    min_bg = None

    for background in game.background_sprites:
        background.update(game)
        background.draw(game.screen)

        if background.name == 'background':
            if not min_bg:
                min_bg = background
            elif min_bg.index > background.index:
                min_bg = background

    # Detect if there should be more background chunks created after fully appearing
    if game.max_bg.rect.centerx <= game.SCREEN_WIDTH + game.max_bg.size[0]:
        new_bg = Terrain(game, 'background')
        new_bg.rect.center = (game.max_bg.rect.centerx + new_bg.size[0], game.bg_y)
        game.background_sprites.append(new_bg)
        game.max_bg = new_bg

    # Detect if you should delete background after fully dissapearing
    if min_bg.rect.x < 0 - min_bg.size[0]:
        game.background_sprites.remove(min_bg)

    # Drawing the lights that fill transparent parts in floors
    game.screen.blit(game.floor_neon, (0, game.floor_y // 1.25))
    game.screen.blit(game.floor_lights, (0, game.floor_y // 1.3))

    for floor in game.floor_sprites:
        floor.update(game)
        floor.draw(game.screen)

        if floor.name == 'floor':
            if not min_floor:
                min_floor = floor
            elif min_floor.index > floor.index:
                min_floor = floor

    # Detect if there should be more floor chunks created after fully appearing
    if game.max_floor.rect.centerx <= game.SCREEN_WIDTH + game.max_floor.size[0]:
        new_floor = Terrain(game, 'floor')
        new_floor.rect.center = (game.max_floor.rect.centerx + new_floor.size[0], game.floor_y)
        game.floor_sprites.append(new_floor)
        game.max_floor = new_floor

    # Detect if should delete floor after fully dissapearing
    if min_floor.rect.x < 0 - min_floor.size[0]:
        game.floor_sprites.remove(min_floor)

class Terrain:
    def __init__(self, level, terrain_type):
        self.name = terrain_type
        self.image = ''
        self.index = 0

        # Choosing what type of terrain is being spawned
        if terrain_type == 'floor':
            level.floor_index += 1
            self.index = level.floor_index
            self.image = self.image = level.floor_image.copy()
        elif terrain_type == 'background':
            level.bg_index += 1
            self.index = level.bg_index

            # Spawn pillar wall every certain walls
            if self.index % 4 == 0:
                self.image = level.bg2_image.copy()
            else:
                self.image = level.bg1_image.copy()

        self.size = self.image.get_size()
        self.rect = self.image.get_rect()

    def update(self, game):
        speed = 0
        if self.name == 'floor':
            speed = game.floor_speed
        if self.name == 'background':
            speed = game.bg_speed

        self.rect.x -= speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

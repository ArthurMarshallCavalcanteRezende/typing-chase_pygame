import random
import constants as c

def update_terrain(game, level):
    min_floor = None
    min_build = None
    min_bg = None

    if game.level.screen_bg:
        game.screen.blit(game.level.screen_bg, (0, 0))

    ''' BACKGROUND SPRITE SYSTEM '''
    if level.bg_list:
        for sprite in level.bg_list:
            if level.stage > 0 and not game.paused: sprite.update(game)
            sprite.draw(game)

            if sprite.name == 'background':
                if not min_bg:
                    min_bg = sprite
                elif min_bg.index > sprite.index:
                    min_bg = sprite

        # Detect if there should be more background chunks created after fully appearing
        can_spawn = level.max_bg.rect.centerx <= c.SCREEN_WIDTH + level.max_bg.size[0]

        if can_spawn and not game.paused:
            new_bg = Terrain(level, 'background')
            new_bg.rect.center = (level.max_bg.rect.centerx + new_bg.size[0], level.bg_y)
            level.bg_list.append(new_bg)
            level.max_bg = new_bg

        # Detect if you should delete background after fully dissapearing
        if min_bg.rect.x < 0 - min_bg.size[0]:
            level.bg_list.remove(min_bg)

        if game.level.stage == 1:
            game.screen.blit(game.LV1_FILTER, (0, 0))

    ''' BUILDING SPRITE SYSTEM '''
    if level.build_list:
        for sprite in level.build_list:
            if level.stage > 0 and not game.paused: sprite.update(game)
            sprite.draw(game)

            if sprite.name == 'building':
                if not min_build:
                    min_build = sprite
                elif min_build.index > sprite.index:
                    min_build = sprite

        # Detect if there should be more floor chunks created after fully appearing
        can_spawn = level.max_build.rect.centerx <= c.SCREEN_WIDTH + level.max_build.size[0]

        if can_spawn and not game.paused:
            new_build = Terrain(level, 'building')
            new_build.rect.center = (level.max_build.rect.centerx + new_build.size[0], level.build_y)
            level.build_list.append(new_build)
            level.max_build = new_build

        # Detect if should delete floor after fully dissapearing
        if min_build.rect.x < 0 - min_build.size[0]:
            level.build_list.remove(min_build)

    ''' FLOOR SPRITE SYSTEM '''
    if level.floor_list:
        # Drawing the lights that fill transparent parts in floors
        if level.floor_lights: game.screen.blit(level.floor_lights, level.fl_pos)
        if level.floor_neon: game.screen.blit(level.floor_neon, level.fn_pos)

        for sprite in level.floor_list:
            if level.stage > 0 and not game.paused: sprite.update(game)
            sprite.draw(game)

            if sprite.name == 'floor':
                if not min_floor:
                    min_floor = sprite
                elif min_floor.index > sprite.index:
                    min_floor = sprite

        # Detect if there should be more floor chunks created after fully appearing
        can_spawn = level.max_floor.rect.centerx <= c.SCREEN_WIDTH + level.max_floor.size[0]

        if can_spawn and not game.paused:
            new_floor = Terrain(level, 'floor')
            new_floor.rect.center = (level.max_floor.rect.centerx + new_floor.size[0], level.floor_y)
            level.floor_list.append(new_floor)
            level.max_floor = new_floor

        # Detect if should delete floor after fully dissapearing
        if min_floor.rect.x < 0 - min_floor.size[0]:
            level.floor_list.remove(min_floor)

class Terrain:
    def __init__(self, level, terrain_type):
        self.name = terrain_type
        self.image = ''
        self.index = 0

        # Choosing what type of terrain is being spawned
        if terrain_type == 'floor':
            level.floor_index += 1
            self.index = level.floor_index
            self.image = level.floor_sprites[random.randint(0, len(level.floor_sprites) - 1)]
        elif terrain_type == 'background':
            level.bg_index += 1
            self.index = level.bg_index

            # Spawn pillar wall every certain walls
            if level.stage == 1:
                if self.index % 4 == 0:
                    self.image = level.bg_sprites[1].copy()
                else:
                    self.image = level.bg_sprites[0].copy()
            else:
                self.image = level.bg_sprites[random.randint(0, len(level.bg_sprites) - 1)]
        elif terrain_type == 'building':
            self.index = level.build_index
            self.image = level.build_sprites[random.randint(0, len(level.build_sprites) - 1)]

        self.size = self.image.get_size()
        self.rect = self.image.get_rect()

    def update(self, game):
        speed = 0
        if self.name == 'floor':
            speed = game.floor_speed
        if self.name == 'background':
            speed = game.bg_speed
        if self.name == 'building':
            speed = game.build_speed

        self.rect.x -= speed

    def draw(self, game):
        game.screen.blit(self.image, self.rect)

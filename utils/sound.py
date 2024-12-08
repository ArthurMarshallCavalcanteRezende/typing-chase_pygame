import pygame
import os

MUSIC_PATH = './assets/music/'
SFX_PATH = './assets/sfx'

POSSIBLE_TYPES = ['wav', 'mp3', 'ogg']

class SFX:
    def __init__(self, sound, sfx, base_volume=0.3, fade_in=0, fade_out=0):
        self.sfx = None
        self.base_volume = base_volume
        self.fade_in = fade_in
        self.fade_out = fade_out
        self.parent = None
        self.channel = None

        for file_type in POSSIBLE_TYPES:
            file_path = f'{SFX_PATH}/{sfx}.{file_type}'

            if os.path.exists(file_path):
                try:
                    self.sfx = pygame.mixer.Sound(file_path)
                    break
                except pygame.error as e:
                    self.sfx = None

        if self.sfx:
            self.sfx.set_volume(self.base_volume)
            sound.sfx_list.append(self)
        else:
            print(f'Could not load "{sfx}", current acceptable files are: {POSSIBLE_TYPES}')


    def play(self, loops=0, max_time=10000):
        if self.sfx:
            self.channel = self.sfx.play(loops, max_time, self.fade_in)

    def stop(self, instant=False):
        if self.sfx:
            if instant:
                self.sfx.stop()
            else:
                self.sfx.fadeout(self.fade_out)

class Sound:
    def __init__(self, file_type='mp3'):
        pygame.mixer.init()
        self.mute = False
        self.volume_offset = 0.3
        self.sfx_offset = 0.5
        self.button_pressed = False
        self.path = MUSIC_PATH
        self.file_type = file_type
        self.sfx_list = []

        ''' ======== SOUND EFFECTS AND AUDIOS ======== '''
        # Action SFX
        self.destroy = SFX(self, 'destroy', 0.3)
        self.explode = SFX(self, 'explode', 0.3)
        self.shoot = SFX(self, 'shoot', 0.3)
        self.caution = SFX(self, 'caution', 0.4)
        self.bomb_alarm = SFX(self, 'bomb_alarm', 0.4)
        self.trigger = SFX(self, 'trigger', 0.3)

        self.metal_hit = SFX(self, 'metal_hit', 0.5)
        self.damage = SFX(self, 'damage', 0.7)
        self.dodge = SFX(self, 'dodge', 0.5)

        self.rocket = SFX(self, 'rocket', 0.25, 1000, 1000)
        self.tumbleweed = SFX(self, 'tumbleweed', 0.3, 1000, 1000)

        # Player SFX
        self.coin = SFX(self, 'coin', 0.5)
        self.points = SFX(self, 'points', 0.7)
        self.levelup = SFX(self, 'levelup', 0.5)
        self.get_life = SFX(self, 'get_life', 0.5)

        # Input SFX
        self.wrong_input = SFX(self, 'wrong_input', 0.4)


    def play(self, song, loop=0):
        pygame.mixer.stop()

        pygame.mixer.music.load(f'{self.path}/{song}.{self.file_type}')
        pygame.mixer.music.set_volume(self.volume_offset)
        pygame.mixer.music.play(loop)

    def mute_music(self):
        self.mute = not self.mute
        self.volume_offset = 0 if self.mute else 0.5
        self.sfx_offset = 0 if self.mute else 0.3
        self.button_pressed = True
        pygame.mixer.music.set_volume(self.volume_offset * 0.5)


    def pause_sfx(self, toggle):
        for sfx in self.sfx_list:
            if not sfx.channel:
                continue

            if toggle:
                sfx.channel.pause()
            else:
                sfx.channel.unpause()

    def change_volume(self, volume_change):
        self.button_pressed = True

        if volume_change == 'increase' and self.volume_offset < 1:
            self.volume_offset = round(self.volume_offset + 0.1, 2)
            pygame.mixer.music.set_volume(self.volume_offset)
        if volume_change == 'decrease' and self.volume_offset > 0:
            self.volume_offset = round(self.volume_offset - 0.1, 2)
            pygame.mixer.music.set_volume(self.volume_offset)
        if self.volume_offset < 0: self.volume_offset = 0
    def change_volume_sfx(self, volume_change):
        self.button_pressed = True

        if volume_change == 'increase' and self.sfx_offset < 1:
            self.sfx_offset = round(self.sfx_offset + 0.1, 2)
        if volume_change == 'decrease' and self.sfx_offset > 0:
            self.sfx_offset = round(self.sfx_offset - 0.1, 2)
        if self.sfx_offset < 0: self.sfx_offset = 0

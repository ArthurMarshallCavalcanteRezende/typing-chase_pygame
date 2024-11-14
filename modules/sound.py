import pygame

class Sound:
    def __init__(self, path, file_type):
        pygame.mixer.init()
        self.mute = False
        self.volume_offset = 0.3
        self.sfx_offset = 0.3
        self.button_pressed = False
        self.path = path
        self.file_type = file_type

    def play(self, song, loop=0):
        pygame.mixer.stop()

        pygame.mixer.music.load(f'{self.path}/{song}.{self.file_type}')
        pygame.mixer.music.set_volume(self.volume_offset)
        pygame.mixer.music.play(loop)

    def play_sfx(self, sfx):
        if self.sfx_offset > 0:
            sfx.set_volume(self.sfx_offset + sfx.get_volume())
            sfx.play()

    def mute_music(self):
        self.mute = not self.mute
        self.volume_offset = 0 if self.mute else 0.5
        self.sfx_offset = 0 if self.mute else 0.3
        self.button_pressed = True
        pygame.mixer.music.set_volume(self.volume_offset * 0.5)

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

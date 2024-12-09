from utils.asset_loader import load_animation

import pygame
import time

class Cutscene:
    def __init__(self):
        self.sprite = None
        self.screen = None
        self.clock = pygame.time.Clock()
        self.idle_frames = load_animation('./assets/player' + '/idle', 120)

    def set_screen(self, screen):
        self.screen = screen

    def play_audio(self, audio_path):
        pygame.mixer.init()
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()

    def play_music(self, music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)

    def run_cutscene(self, images, audios):
        if len(images) != 7:
            raise ValueError("A lista de imagens deve conter exatamente 7 itens.")
        if len(audios) != 4:
            raise ValueError("A lista de áudios deve conter exatamente 4 itens.")


        durations = [5, 6, 12, 7, 8, 17, 5]

        current_frame = 0
        last_update_time = pygame.time.get_ticks()
        animation_speed = 100

        for i in range(7):
            resized_image = pygame.transform.scale(images[i], (800, 530))
            self.screen.blit(resized_image, (0, 0))

            if i == 1 or i == 2:
                if i == 1:
                    self.play_audio(audios[0])
            elif i == 3 or i == 4:
                if i == 3:
                    self.play_audio(audios[1])
            elif i == 5:
                self.play_audio(audios[2])
                self.play_music("./assets/music/menace.mp3")
            elif i == 6:
                self.play_audio(audios[3])

            current_time = pygame.time.get_ticks()
            if current_time - last_update_time > animation_speed:
                current_frame = (current_frame + 1) % len(self.idle_frames)
                last_update_time = current_time

            self.screen.blit(self.idle_frames[current_frame], (50, 250))

            pygame.display.flip()

            for _ in range(durations[i] * 10):
                self.clock.tick(10)

        pygame.mixer.music.stop()


import pygame
import time

class Cutscene:
    def __init__(self):
        self.sprite = None
        self.screen = None
        self.clock = pygame.time.Clock()

    def set_screen(self, screen):
        self.screen = screen

    def play_audio(self, audio_path):
        pygame.mixer.init()
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()

    def run_cutscene(self, images, audios):
        if len(images) != 6:
            raise ValueError("A lista de imagens deve conter exatamente 6 itens.")
        if len(audios) != 4:
            raise ValueError("A lista de áudios deve conter exatamente 4 itens.")

        durations = [5, 6, 12, 7, 8, 15]

        for i in range(6):

            resized_image = pygame.transform.scale(images[i], (850, 550))
            self.screen.blit(resized_image, (0, 0))
            pygame.display.flip()


            if i == 1 or i == 2:

                if i == 1:
                    self.play_audio(audios[0])

            elif i == 3 or i == 4:

                if i == 3:
                    self.play_audio(audios[1])

            elif i == 5:

                self.play_audio(audios[2])

            elif i == 6:
                self.play_audio(audios[3])

            if i == 5:
                self.screen.blit(resized_image, (0, 0))

            time.sleep(durations[i])  

        pygame.mixer.music.stop()

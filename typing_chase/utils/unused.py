def play_audio_and_show_subtitles(audio_files, subtitles, game):
    background_image = game.stage2_bg.copy()
    background_image = pygame.transform.scale(background_image, (game.SCREEN_WIDTH, game.SCREEN_HEIGHT))
    zharov_sprite = pygame.image.load('./assets/stages/2/ZH4R0V.png')
    zharov_sprite = pygame.transform.scale(zharov_sprite, (400, 400))
    speech_panel = pygame.image.load('./assets/icons/target_warning.png')
    speech_panel = pygame.transform.scale(speech_panel, (1400, 350))

    x_pos = game.SCREEN_WIDTH - zharov_sprite.get_width() - 30
    y_pos = game.SCREEN_HEIGHT // 2 - zharov_sprite.get_height() // 2 - 20
    game.screen.blit(zharov_sprite, (x_pos, y_pos))
    game.screen.blit(speech_panel, (-15, game.SCREEN_HEIGHT - 400))

    pygame.display.update()

    subtitle_pairs = [subtitles[i:i + 2] for i in range(0, len(subtitles), 2)]
    subtitle_index = 0
    subtitle_durations = [25000, 20000, 30000, 30000]

    while subtitle_index < len(audio_files) and not game.cutscene_skipped:
        current_time = pygame.time.get_ticks()
        start_time = current_time

        pygame.mixer.music.load(audio_files[subtitle_index])
        pygame.mixer.music.play()

        game.bullet_train_rect.center = (-100, game.SCREEN_HEIGHT // 1.5)
        game.player.rect.center = game.bullet_train_rect.center

        game.screen.blit(background_image, (0, 0))
        game.screen.blit(game.CUTSCENE_FILTER, (0, 0))

        game.screen.blit(zharov_sprite, (x_pos, y_pos))
        game.screen.blit(speech_panel, (-390, game.SCREEN_HEIGHT - 400))

        for i, subtitle in enumerate(subtitle_pairs[subtitle_index]):
            subtitle_text = game.small_font.render(subtitle, True, game.COLORS.white)
            game.screen.blit(subtitle_text, (game.SCREEN_WIDTH // 7, game.SCREEN_HEIGHT - 180 + (40 * i)))

        pygame.display.flip()
        game.clock.tick(game.FPS)

        if subtitle_index == 2:
            menace_music_started = False
            elapsed_time = pygame.time.get_ticks() - start_time

            while pygame.mixer.music.get_busy():
                elapsed_time = pygame.time.get_ticks() - start_time

                if not menace_music_started and elapsed_time >= 5000:
                    game.sound.play('menace', -1)
                    menace_music_started = True

                pygame.time.delay(100)
        else:
            subtitle_duration = subtitle_durations[subtitle_index]
            while pygame.mixer.music.get_busy() and current_time - start_time < subtitle_duration:
                pygame.time.delay(6000)
                current_time = pygame.time.get_ticks()

        subtitle_index += 1

    game.state = 'level'
    game.data["cutscene_finished"] = True

# Cutscene assets
def level_2_cutscene(game):
    audio_files = [
        './assets/stages/2/zharov_speech1.wav',
        './assets/stages/2/zharov_speech2.wav',
        './assets/stages/2/zharov_power.wav',
        './assets/stages/2/zharov_speech3.wav'
    ]

    subtitles = [
        "Que curioso, jovem recrutas para Intercentauri... Que patético!",
        "Eles te encheram de falsas esperanças, não é garoto?",
        "Escute jovem, eu tenho negócios a resolver com meu fornecedor.",
        "Então... EU VOU ACELERAR NOSSA CONVERSA!",
        "*ROBÔ LANÇANDO PODER IRADO.MP3*",
        "*Música épica de fundo*",
        "Você não irá me pegar, cowboy!",
        "Hahahahahahahaha!!!"
    ]

    # function to play the audios with subtitles
    play_audio_and_show_subtitles(audio_files, subtitles, game)
    pygame.mixer.music.stop()
    game.sound.play('level2', -1)
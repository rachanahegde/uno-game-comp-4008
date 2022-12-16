import pygame

screen = pygame.display.set_mode([1400, 800])


class StartGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Uno Game')
        # screen = pygame.display.set_mode([1400, 800])
        pygame.mixer.music.load("./assets/gamemusic.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(loops=-1)

        background = pygame.image.load("./assets/new_start.png")
        screen.blit(background, (0, 0))

        start_button = pygame.image.load("./assets/startbt_up.png")
        rect = start_button.get_rect()
        start_button_x = (screen.get_width() - rect.right) * (1 / 2)
        start_button_y = (screen.get_height() - rect.bottom) * (90 / 100)
        screen.blit(start_button, (start_button_x, start_button_y))

        pygame.display.flip()

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    click = pygame.mouse.get_pos()
                elif event.type == pygame.MOUSEMOTION and \
                        start_button_x < event.pos[0] < start_button_x + rect.right and \
                        start_button_y < event.pos[1] < start_button_y + rect.bottom:
                    start_button2 = pygame.image.load("./assets/startbt_down.png")
                    rect = start_button2.get_rect()
                    start_button2_x = (screen.get_width() - rect.right) * (1 / 2)
                    start_button2_y = (screen.get_height() - rect.bottom) * (90 / 100)
                    screen.blit(start_button2, (start_button2_x, start_button2_y))
                    pygame.display.update()
                    screen.fill((255, 255, 255))
                    return

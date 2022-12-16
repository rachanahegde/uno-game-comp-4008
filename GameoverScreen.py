import pygame
import sys
from main import *


class GameOverScreen:
    def __init__(self, screen, winning_player, losing_player, score_winning, score_losing):
        self.screen = pygame.image.load(f'./assets/scoreboard.jpg')
        screen.blit(self.screen, (0, 0))
        self.score_winning = score_winning
        self.score_losing = score_losing
        self.winning_player = winning_player
        self.losing_player = losing_player

        font = pygame.font.Font('./assets/Montserrat.otf', 32)

        label_win = font.render(f"{self.winning_player} Win!", True, '#1427A4')

        label_winner = font.render(f"{self.winning_player}", True, 'white')
        label_loser = font.render(f"{self.losing_player}", True, 'white')
        winner_score = font.render(f"{self.score_winning}", True, 'white')
        loser_score = font.render(f"{self.score_losing}", True, 'white')

        screen.blit(label_win, [460, 130])
        screen.blit(label_winner, [460, 290])
        screen.blit(label_loser, [460, 390])
        screen.blit(winner_score, [800, 290])
        screen.blit(loser_score, [800, 390])

        close_button = pygame.image.load("./assets/Close1.png")
        rect = close_button.get_rect()
        close_button_x = (screen.get_width() - rect.right) * (1 / 2)
        close_button_y = (screen.get_height() - rect.bottom) * (80 / 100)
        screen.blit(close_button, (close_button_x, close_button_y))

        pygame.display.flip()

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and \
                        close_button_x < event.pos[0] < close_button_x + rect.right and \
                        close_button_y < event.pos[1] < close_button_y + rect.bottom:
                    close_button2 = pygame.image.load("./assets/Close2.png")
                    rect = close_button2.get_rect()
                    close_button2_x = (screen.get_width() - rect.right) * (1 / 2)
                    close_button2_y = (screen.get_height() - rect.bottom) * (80 / 100)
                    screen.blit(close_button2, (close_button2_x, close_button2_y))
                    pygame.display.update()

                    pygame.quit()
                    sys.exit()

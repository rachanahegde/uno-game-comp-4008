import pygame
import random
from Card import *
from Deck import *
from DiscardPile import *
from Player import *
from GameBoard import *
from GameManager import *
from StartGame import *


def main():
    StartGame()

    # Make game_board and game_manager objects and put cards, draw pile, and discard pile on screen
    game_board = GameBoard()
    game_board.setbackground()
    game_manager = GameManager()
    game_board.set_cards(game_manager.players_list)
    game_board.draw_pile()
    game_board.set_discard_pile(game_manager.discard_pile.card_pile)
    game_manager.show_turns()
    

    # Main loop of the game - checking for new events and rendering the window picture
    running = True
    iswin = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif iswin is True:
                pass

            # Check if the human player has clicked and also if it is their turn to play
            elif event.type == pygame.MOUSEBUTTONDOWN and game_manager.current_player == game_manager.human_player:
                click = pygame.mouse.get_pos()
                iswin = game_manager.human_play_game(click, game_board)

            elif game_manager.current_player == game_manager.computer_player:  # Change player to computer player
                iswin = game_manager.computer_play_game(game_board)

        # Render the picture on the screen
        pygame.display.flip()

        # Slow down the main loop
        pygame.time.wait(10)
    pygame.time.wait(2000)
    pygame.quit()


if __name__ == '__main__':
    main()

import pygame
import random
import time
import sys
from Player import *
from StartGame import *
from GameManager import *

screen = pygame.display.set_mode([1400, 800])


class GameBoard:
    def __init__(self):
        self.back_card_rect = None  # Rectangle object associated with draw pile

    def set_cards(self, players_list):
        y = 70
        for player in players_list:
            # Check if player object is a subclass of ComputerPlayer()
            if isinstance(player, ComputerPlayer):
                x = 400
                for card in player.cards_in_hand:
                    image_position = (x, y)
                    card_img = pygame.image.load(f'./assets/cards/uno_card_back.png')
                    card_img = pygame.transform.smoothscale(card_img, (80, 125))
                    screen.blit(card_img, image_position)
                    if len(player.cards_in_hand) > 7:
                        x += ((1010 - 400 - (70 * len(player.cards_in_hand))) / (len(player.cards_in_hand))) + 70
                    else:
                        x += 90
            else:
                # Set cards for human player
                x = 400
                for card in player.cards_in_hand:
                    image_position = (x, 580)
                    # Update the x, y coordinates for the rectangle that represents each card
                    card.rect.x = x
                    card.rect.y = 580
                    screen.blit(card.image, image_position)
                    # Insert cards within a specific x range in the screen
                    if len(player.cards_in_hand) > 7:
                        x += ((1010 - 400 - (70 * len(player.cards_in_hand))) / (len(player.cards_in_hand))) + 70
                    else:
                        x += 90

    def draw_pile(self):
        back_card = pygame.image.load(f'./assets/cards/uno_card_back.png')
        back_card = pygame.transform.smoothscale(back_card, (80, 125))
        # Draw pile must have rectangle object associated with it for user to be able to click it
        self.back_card_rect = back_card.get_rect()
        self.back_card_rect.x = 540
        self.back_card_rect.y = 315
        screen.blit(back_card, (540, 315))


    def set_discard_pile(self, discard_pile):
        # Show card at top of discard pile (the last card added)
        screen.blit(discard_pile[-1].image, (670, 315))


    # Update card images when player gets a new card or plays a card
    def update_card_images(self, discard_pile, players_list):
        self.setbackground()
        self.set_discard_pile(discard_pile)
        self.draw_pile()
        self.set_cards(players_list)

    # Create background screen
    def setbackground(self):
        background_img = pygame.image.load(f'./assets/background.jpg')
        background_img = pygame.transform.smoothscale(background_img, (1400, 800))
        screen.blit(background_img, (0, 0))

import pygame
import random


# Set up a class representing the discarded cards pile


class DiscardPile:
    def __init__(self, card_deck):
        self.card_pile = []
        # Set up discard pile at start of game by drawing one card from the deck and adding it to the discard pile
        self.card_pile.append(card_deck[-1])
        # Remove that card from the card_deck
        card_deck.remove(card_deck[-1])
        while self.card_pile[-1].color == 'black':  # Avoid the top card in the discard pile being a black card
            self.card_pile.append(card_deck[-1])
            card_deck.remove(card_deck[-1])

    # Method called when a player plays a card into the discard pile
    def discard(self, a_card):
        self.card_pile.append(a_card)

import pygame
import random


# Set up a class representing player
class Player:
    def __init__(self):
        self.cards_in_hand = []

    # Player plays a card into the discard pile
    def play(self, a_card, discard_pile):
        self.cards_in_hand.remove(a_card)
        discard_pile.discard(a_card)

    # Used when a player takes top card from the card_deck
    def take_card(self, card_deck, discard_pile):
        self.cards_in_hand.append(card_deck[-1])
        card_deck.remove(card_deck[-1])
        # Updates deck if cards run out
        if len(card_deck) == 0:
            random.shuffle(discard_pile)
            card_deck = discard_pile
            discard_pile.clear()
            # Set up the discard pile again with the top card from the deck
            discard_pile.append(card_deck[-1])
            card_deck.remove(card_deck[-1])

    # Call this method at the start of each turn - the player will choose one card from their hand,
    # put it on the bottom of the discard pile, then take the top card from  draw pile and add it to their hand.
    def swap_card(self, a_card, discard_pile, card_deck):
        self.cards_in_hand.remove(a_card)
        discard_pile.insert(0, a_card)
        self.take_card(card_deck, discard_pile)


class ComputerPlayer(Player):
    # Loop through the cards in the player's hand and check if they match the card at top of the discard pile
    # Computer plays the card that matches the card on the top of the discard pile
    def play(self, a_card, discard_pile):
        self.cards_in_hand.remove(a_card)
        discard_pile.discard(a_card)


class HumanPlayer(Player):
    pass

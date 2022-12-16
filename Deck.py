import pygame
import random
from Card import *

# Card colors and types
cards_color = ["red", "blue", "yellow", "green"]
special_cards = ["skip", "reverse", "draw_2"]
wild_cards = ["wild_draw_4", "wild"]


# Set up a class representing the card deck
class Deck:
    def __init__(self):
        self.card_deck = []
        self.rectangles = []  # Rectangle objects that represent each card and can be clicked on by human player

    # Add all the cards needed for the game to the deck
    def add_cards(self):
        for number in range(0, 10):
            if number != 0:
                for _ in range(2):
                    for color in cards_color:
                        self.card_deck.append(NumberCard(color, number))
                        self.rectangles.append(NumberCard(color, number).rect)

            if number == 0:
                for color in cards_color:
                    self.card_deck.append(NumberCard(color, number))
                    self.rectangles.append(NumberCard(color, number).rect)

        for color in cards_color:
            for _ in range(2):
                for special in special_cards:
                    self.card_deck.append(SpecialCard(color, special))
                    self.rectangles.append(SpecialCard(color, special).rect)

        for wild in wild_cards:
            for _ in range(4):
                self.card_deck.append(SpecialCard("black", wild))
                self.rectangles.append(SpecialCard("black", wild).rect)

    # Shuffle the card deck
    def shuffle_cards(self):
        random.shuffle(self.card_deck)

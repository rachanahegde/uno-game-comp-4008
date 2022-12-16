import pygame


# Set up a class representing different types of cards
class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value
        # Load and transform card images
        self.image = pygame.image.load(f'./assets/cards/{self.color}_{self.value}.png')
        self.image = pygame.transform.smoothscale(self.image, (80, 125))
        self.rect = self.image.get_rect()


class SpecialCard(Card):
    def create_card(self):
        pass


class NumberCard(Card):
    def create_card(self):
        pass

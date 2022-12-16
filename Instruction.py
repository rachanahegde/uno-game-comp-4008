import pygame


# The class representing a text instruction to the human player
class Instruction:
    def __init__(self, screen, text, pos, size, colour):
        self.screen = screen
        self.text = text
        self.pos = pos
        self.font = pygame.font.Font(f'./assets/Montserrat.otf',size)
        self.font_colour = pygame.Color(colour)
        
        img = self.font.render(self.text, True, self.font_colour)
        screen.blit(img, self.pos)

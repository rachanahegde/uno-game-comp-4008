import pygame
import random
from Card import *
from Deck import *
from DiscardPile import *
from Player import *
from GameBoard import *
from GameoverScreen import *
from Instruction import *
from StartGame import *

clock = pygame.time.Clock()


class GameManager:
    def __init__(self):
        # Set font used to draw text
        self.FONT = pygame.font.Font(f'./assets/Montserrat.otf', 20)

        self.turns_left = 25  # Max number of player turns per one round of the game (makes the game more difficult)
        self.font_color = '#BBC4FF'  # lavender

        # Create card deck object, add cards, shuffle the deck, create discard pile, create human and computer players
        self.deck = Deck()
        self.deck.add_cards()
        self.deck.shuffle_cards()
        self.discard_pile = DiscardPile(self.deck.card_deck)
        self.human_player = HumanPlayer()
        self.computer_player = ComputerPlayer()
        self.players_list = [self.human_player, self.computer_player]
        self.direction = 1  # 1 for clockwise, -1 for counterclockwise

        # Deal 7 cards each
        self.deal_card_players(self.players_list, self.deck.card_deck)

        # Randomly choose which player has their turn first
        self.current_player = random.choice(self.players_list)

        # Tell  the user which player is going first
        if self.current_player == self.human_player:
            text = "It's the HUMAN PLAYER's turn, swap a card."
            Instruction(screen, text, (400, 520), 23, 'white')
        else:
            text = "It's the COMPUTER PLAYER's turn, swap a card and then play or draw a new card."
            Instruction(screen, text, (400, 220), 23, 'white')

        self.human_has_swapped_card = False
        self.human_has_played_turn = False

        # Instance variables for calculating player's scores at the end of the game
        self.list_num_human = []
        self.list_num_comp = []
        self.list_draw2_reverse_skip_human = []
        self.list_draw2_reverse_skip_comp = []
        self.list_wild_human = []
        self.list_wild_comp = []
        self.final_score_comp = 0
        self.final_score_human = 0

    def give_instructions(self, instruction):
        text = self.FONT.render(instruction, True, 'WHITE')
        screen.blit(text, [400, 480])

    def hint_instructions(self, instruction):
        new_text = self.FONT.render(instruction, True, 'Red')
        screen.blit(new_text, [400, 450])

    def compare_cards(self, card):
        # Compares card selected by the player to the card on the discard pile
        if card.color == self.discard_pile.card_pile[-1].color or card.value == self.discard_pile.card_pile[-1].value \
                or card.color == "black":
            return True
        else:
            return False

    def human_play_game(self, click, game_board):
        for card in self.human_player.cards_in_hand:
            if card.rect.collidepoint(click) and not self.human_has_swapped_card:
                # Player swaps their card at start of each turn
                self.human_player.swap_card(card, self.discard_pile.card_pile, self.deck.card_deck)
                game_board.update_card_images(self.discard_pile.card_pile, self.players_list)
                self.show_turns()
                self.human_has_swapped_card = True
                Instruction(screen, "Choose a card to play or draw a new card.", (400, 520), 23, 'white')

            elif not self.human_has_played_turn and self.human_has_swapped_card:
                # Check if the card they clicked on matches the card on the discard pile
                if card.rect.collidepoint(click):
                    if self.compare_cards(card):
                        self.human_player.play(card, self.discard_pile)
                        self.human_has_played_turn = True
                        self.track_turns()
                        game_board.update_card_images(self.discard_pile.card_pile, self.players_list)
                        self.calculation_after_round(last_card=card)
                        self.show_turns()
                        return self.declare_winner()
                    else:
                        game_board.update_card_images(self.discard_pile.card_pile, self.players_list)
                        self.show_turns()
                        text = "Pick another card or draw a new card, this doesn't match."
                        Instruction(screen, text, (400, 520), 23, 'white')
                # Check if the player wants to draw a new card
                elif game_board.back_card_rect.collidepoint(click):
                    self.human_player.take_card(self.deck.card_deck, self.discard_pile.card_pile)
                    self.track_turns()
                    game_board.update_card_images(self.discard_pile.card_pile, self.players_list)
                    self.show_turns()

                    # Player plays the card they just got from the deck if it matches
                    if self.compare_cards(self.human_player.cards_in_hand[-1]):
                        card_to_play = self.human_player.cards_in_hand[-1]
                        self.human_player.play(card_to_play, self.discard_pile)
                        game_board.update_card_images(self.discard_pile.card_pile, self.players_list)
                        self.calculation_after_round(last_card=card_to_play)
                        self.show_turns()
                        return self.declare_winner()
                    else:
                        self.calculation_after_round()
                        return self.declare_winner()

    # Method to call when the wild or wild draw 4 cards are played
    def change_color(self):
        # Slow down the game to give the player time to click on a color
        clock.tick(40)

        # Show four different colors in boxes on the screen for the user to click on
        if self.current_player == self.computer_player:
            self.discard_pile.card_pile[-1].color = random.choice(cards_color)
            text = f"The computer player just changed the color: {self.discard_pile.card_pile[-1].color}."
            Instruction(screen, text, (400, 470), 23, 'grey')
            return
        else:
            Instruction(screen, "Pick a color", (930, 240), 23, 'white')

            red_img = pygame.image.load(f'./assets/red.png')
            blue_img = pygame.image.load(f'./assets/blue.png')
            green_img = pygame.image.load(f'./assets/green.png')
            yellow_img = pygame.image.load(f'./assets/yellow.png')

            red_img = pygame.transform.smoothscale(red_img, (120, 120))
            blue_img = pygame.transform.smoothscale(blue_img, (120, 120))
            green_img = pygame.transform.smoothscale(green_img, (120, 120))
            yellow_img = pygame.transform.smoothscale(yellow_img, (120, 120))

            red_rect = red_img.get_rect()
            red_rect.x = 900
            red_rect.y = 260
            blue_rect = blue_img.get_rect()
            blue_rect.x = 980
            blue_rect.y = 260
            green_rect = green_img.get_rect()
            green_rect.x = 900
            green_rect.y = 360
            yellow_rect = yellow_img.get_rect()
            yellow_rect.x = 980
            yellow_rect.y = 360

            screen.blit(red_img, (900, 260))
            screen.blit(blue_img, (980, 260))
            screen.blit(green_img, (900, 360))
            screen.blit(yellow_img, (980, 360))

            pygame.display.flip()

            rect_list = [red_rect, blue_rect, yellow_rect, green_rect]

            # If human player clicks on the color, change color of card at the top of the discard pile to that color
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for x in range(len(rect_list)):
                            if rect_list[x].collidepoint(event.pos):
                                self.discard_pile.card_pile[-1].color = cards_color[x]
                                text = f"The human player just clicked on this color: {self.discard_pile.card_pile[-1].color}."
                                Instruction(screen, text, (400, 480), 23, 'grey')
                                return

    def calculation_after_round(self, last_card=None):
        if last_card is None or type(last_card.value) == int:
            self.current_player = self.players_list[
                (self.players_list.index(self.current_player) + self.direction) % len(self.players_list)]
            if self.current_player == self.human_player:
                text = "It's the HUMAN PLAYER's turn, swap a card"
                Instruction(screen, text, (400, 520), 23, 'white')
            else:
                text = "It's the COMPUTER PLAYER's turn, swap a card and then play or draw a new card."
                Instruction(screen, text, (400, 220), 23, 'white')
        elif last_card.value == 'skip':
            if self.current_player == self.human_player:
                Instruction(screen, "COMPUTER PLAYER's turn is skipped!", (400, 450), 23, 'pink')
            else:
                Instruction(screen, "HUMAN PLAYER's turn is skipped!", (400, 450), 23, 'pink')
            self.current_player = self.players_list[
                (self.players_list.index(self.current_player) + 2 * self.direction) % len(self.players_list)]
            if self.current_player == self.human_player:
                text = "It's the HUMAN PLAYER's turn, swap a card."
                Instruction(screen, text, (400, 520), 23, 'white')
            else:
                text = "It's the COMPUTER PLAYER's turn, swap a card and then play or draw a new card."
                Instruction(screen, text, (400, 220), 23, 'white')
        elif last_card.value == 'reverse':
            if len(self.players_list) == 2:
                Instruction(screen, "Now the turn order is reversed.", (400, 450), 23, 'pink')
                self.direction = -self.direction
                self.current_player = self.players_list[
                    (self.players_list.index(self.current_player) + 2 * self.direction) % len(self.players_list)]
                if self.current_player == self.human_player:
                    text = "It's the HUMAN PLAYER's turn, swap a card."
                    Instruction(screen, text, (400, 520), 23, 'white')
                else:
                    text = "It's the COMPUTER PLAYER's turn, swap a card and then play or draw a new card."
                    Instruction(screen, text, (400, 220), 23, 'white')
            else:
                Instruction(screen, "Now the turn order is reversed.", (400, 450), 23, 'pink')
                self.direction = -self.direction
                self.current_player = self.players_list[
                    (self.players_list.index(self.current_player) + self.direction) % len(self.players_list)]
                if self.current_player == self.human_player:
                    text = "It's the HUMAN PLAYER's turn, swap a card."
                    Instruction(screen, text, (400, 520), 23, 'white')
                else:
                    text = "It's the COMPUTER PLAYER's turn, swap a card and then play or draw a new card."
                    Instruction(screen, text, (400, 220), 23, 'white')
        elif last_card.value == 'draw_2':
            if self.current_player == self.human_player:
                Instruction(screen, "COMPUTER PLAYER, draw 2 cards!", (400, 450), 23, 'pink')
            else:
                Instruction(screen, "HUMAN PLAYER, draw 2 cards!", (400, 450), 23, 'pink')
            self.current_player = self.players_list[
                (self.players_list.index(self.current_player) + self.direction) % len(self.players_list)]
            for i in range(2):
                self.current_player.take_card(self.deck.card_deck, self.discard_pile.card_pile)
            self.current_player = self.players_list[
                (self.players_list.index(self.current_player) + self.direction) % len(self.players_list)]
            if self.current_player == self.human_player:
                text = "It's the HUMAN PLAYER's turn, swap a card."
                Instruction(screen, text, (400, 520), 23, 'white')
            else:
                text = "It's the COMPUTER PLAYER's turn, swap a card and then play or draw a new card."
                Instruction(screen, text, (400, 220), 23, 'white')
        elif last_card.value == 'wild_draw_4':
            self.change_color()
            if self.current_player == self.human_player:
                Instruction(screen, "COMPUTER PLAYER, draw 4 cards!", (400, 445), 23, 'pink')
            else:
                Instruction(screen, "HUMAN PLAYER, draw 4 cards!", (400, 445), 23, 'pink')
            self.current_player = self.players_list[
                (self.players_list.index(self.current_player) + self.direction) % len(self.players_list)]
            for i in range(4):
                self.current_player.take_card(self.deck.card_deck, self.discard_pile.card_pile)
            self.current_player = self.players_list[
                (self.players_list.index(self.current_player) + self.direction) % len(self.players_list)]
            if self.current_player == self.human_player:
                text = "It's the HUMAN PLAYER's turn, swap a card."
                Instruction(screen, text, (400, 520), 23, 'white')
            else:
                text = "It's the COMPUTER PLAYER's turn, swap a card and then play or draw a new card."
                Instruction(screen, text, (400, 220), 23, 'white')
        elif last_card.value == 'wild':
            self.change_color()
            self.current_player = self.players_list[
                (self.players_list.index(self.current_player) + self.direction) % len(self.players_list)]
            if self.current_player == self.human_player:
                text = "It's the HUMAN PLAYER's turn, swap a card."
                Instruction(screen, text, (400, 520), 23, 'white')
            else:
                text = "It's the COMPUTER PLAYER's turn, swap a card and then play or draw a new card."
                Instruction(screen, text, (400, 220), 23, 'white')
        self.human_has_swapped_card = False
        self.human_has_played_turn = False

    # This method is to control the computer as it plays the game
    def computer_play_game(self, game_board):
        pygame.time.wait(1500)
        self.computer_player.swap_card(random.choice(self.computer_player.cards_in_hand), self.discard_pile.card_pile,
                                       self.deck.card_deck)
        game_board.update_card_images(self.discard_pile.card_pile, self.players_list)
        self.show_turns()

        for card in self.computer_player.cards_in_hand:
            if self.compare_cards(card):
                self.computer_player.play(card, self.discard_pile)
                self.track_turns()
                game_board.update_card_images(self.discard_pile.card_pile, self.players_list)
                self.calculation_after_round(last_card=card)
                self.show_turns()
                return self.declare_winner()

        # Computer takes a card from the deck/draw pile if it doesn't have a matching card
        self.computer_player.take_card(self.deck.card_deck, self.discard_pile.card_pile)
        self.track_turns()
        game_board.update_card_images(self.discard_pile.card_pile, self.players_list)
        self.show_turns()

        # If the card that the computer took from the deck matches, it can play it
        if self.compare_cards(self.computer_player.cards_in_hand[-1]):
            card_played = self.computer_player.cards_in_hand[-1]
            self.computer_player.play(card_played, self.discard_pile)
            game_board.update_card_images(self.discard_pile.card_pile, self.players_list)
            self.calculation_after_round(last_card=card_played)
            self.show_turns()
            return self.declare_winner()
        else:
            game_board.update_card_images(self.discard_pile.card_pile, self.players_list)
            self.calculation_after_round()
            self.show_turns()
            return self.declare_winner()

    # Track the number of turns left in the game
    def track_turns(self):
        if self.turns_left > 0:
            self.turns_left -= 1

    def show_turns(self):
        if self.turns_left > 0:
            turn_info = self.FONT.render(f'Turns remaining: {self.turns_left}', True, self.font_color)
            screen.blit(turn_info, [200, 300])
        else:
            return self.declare_winner()

    # Declares winner after a player plays their last card and show scores by creating GameOverScreen object
    def declare_winner(self):
        if len(self.current_player.cards_in_hand) == 0 or self.turns_left == 0:
            self.card_type_filter()
            self.calculation_human()
            self.calculation_comp()
            iswin = True
            if self.final_score_human < self.final_score_comp:
                GameOverScreen(screen, winning_player="Human Player", losing_player="Computer Player",
                               score_winning=self.final_score_human, score_losing=self.final_score_comp)
            else:
                GameOverScreen(screen, winning_player="Computer Player", losing_player="Human Player",
                               score_winning=self.final_score_comp, score_losing=self.final_score_human)
            return iswin
        return False


    def card_type_filter(self):
        for player in self.players_list:
            # Append to the list for human player
            if player == self.human_player:
                for card in self.human_player.cards_in_hand:
                    if type(card.value) == int:
                        self.list_num_human.append(card.value)
                    elif card.value == 'draw_2' or card.value == 'reverse' or card.value == 'skip':
                        self.list_draw2_reverse_skip_human.append(card.value)
                    else:
                        self.list_wild_human.append(card.value)

            # Append to the list for computer player
            elif player == self.computer_player:
                for card in self.computer_player.cards_in_hand:
                    if type(card.value) == int:
                        self.list_num_comp.append(card.value)
                    elif card.value == 'draw_2' or card.value == 'reverse' or card.value == 'skip':
                        self.list_draw2_reverse_skip_comp.append(card.value)
                    else:
                        self.list_wild_comp.append(card.value)

    def calculation_human(self):
        for i in self.list_num_human:
            self.final_score_human += i
        self.final_score_human = self.final_score_human + 20 * (len(self.list_draw2_reverse_skip_human)) + 50 * (
            len(self.list_wild_human))
        return self.final_score_human

    def calculation_comp(self):
        for i in self.list_num_comp:
            self.final_score_comp += i
        self.final_score_comp = self.final_score_comp + 20 * (len(self.list_draw2_reverse_skip_comp)) + 50 * (
            len(self.list_wild_comp))
        return self.final_score_comp

    # Method deals 7 cards to each player and removes those cards from the deck
    def deal_card_players(self, players_list, deck):
        for player in players_list:
            for item in random.sample(deck, 7):
                player.cards_in_hand.append(item)
            for card in player.cards_in_hand:
                deck.remove(card)

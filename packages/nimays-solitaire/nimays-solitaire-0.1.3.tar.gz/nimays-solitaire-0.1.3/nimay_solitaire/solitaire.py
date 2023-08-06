import copy

from nimay_solitaire.card import Card
from nimay_solitaire.gameboard import Gameboard


class Solitaire(object):
    """
    A class to implement the game logic of solitaire.
    """

    """
    Initiates a game of solitaire.
    """
    def __init__(self, num_tableau_piles=7, loop=True):
        self.num_tableau_piles = num_tableau_piles
        self.move_stack = []
        self.gameboard = Gameboard(num_tableau_piles)
        if loop:
            self.game_loop()

    """
    Determines whether a solitaire game is complete. A game is complete when all of the foundation piles are full.
    """
    def game_end(self):
        return all([len(self.gameboard.foundation_piles[i].cards) == 13 for i in range(len(Card.suits))])

    """
    Attempts to make a move and adds it to the history if it was successful
    :param move_str: A string representing the move that should be attempted
    :return: True if the move succeeded False otherwise
    """
    def make_move_with_history(self, move_str):
        gameboard_copy = copy.deepcopy(self.gameboard)
        move_success = self.make_move(move_str)
        if move_success:
            self.move_stack.append(gameboard_copy)
        else:
            self.gameboard = gameboard_copy
        return move_success

    """
    Makes a move specified by the given string.
    :param move_str: A string representing the move the user wants to make, assumed to be in all caps
    :return: True if the move was made successfully, False otherwise
    """
    def make_move(self, move_str):
        tokens = move_str.split()
        if len(tokens) == 2 and tokens[1] == 'D':
            # draw card to waste pile
            return self.gameboard.deck.draw_card_to_waste()
        elif len(tokens) == 3 and tokens[1] == 'W' and tokens[2] == 'F':
            # waste pile to foundation
            card = self.gameboard.deck.waste_pile.remove_card()
            if card:
                return self.gameboard.foundation_piles[card.suit].add_card(card, True, True)
        elif len(tokens) == 4 and tokens[1] == 'W' and tokens[2] == 'T':
            # waste pile to tableau
            try:
                pile_idx = int(tokens[3])
            except ValueError:
                return False
            card = self.gameboard.deck.waste_pile.remove_card()
            if card:
                return self.gameboard.tableau_piles[pile_idx].add_card(card, True, True)
        elif len(tokens) == 4 and tokens[1] == 'T' and tokens[3] == 'F':
            # tableau to foundation
            try:
                pile_idx = int(tokens[2])
            except ValueError:
                return False
            src_tab_pile = self.gameboard.tableau_piles[pile_idx]
            cards = src_tab_pile.remove_card(len(src_tab_pile.cards)-1)
            if cards and len(cards) == 1:
                return self.gameboard.foundation_piles[cards[0].suit].add_card(cards[0], True, True)
        elif len(tokens) == 5:
            # foundation to tableau
            try:
                found_pile_idx = int(tokens[2])
                tab_pile_idx = int(tokens[4])
            except ValueError:
                return False
            card = self.gameboard.foundation_piles[found_pile_idx].remove_card()
            if card:
                return self.gameboard.tableau_piles[tab_pile_idx].add_card(card, True, True)
        elif len(tokens) == 6:
            # tableau to tableau
            try:
                src_tab_pile_idx = int(tokens[2])
                src_tab_pile_card_idx = int(tokens[3])
                dst_tab_pile_idx = int(tokens[5])
            except ValueError:
                return False
            cards = self.gameboard.tableau_piles[src_tab_pile_idx].remove_card(src_tab_pile_card_idx)
            if cards:
                return self.gameboard.tableau_piles[dst_tab_pile_idx].add_cards(cards)
        # Unable to parse move string
        return False

    """
    Undoes the last move (if there is one) by restoring the state of the gameboard to what it was before the last move.
    """
    def undo_move(self):
        if self.move_stack:
            self.gameboard = self.move_stack.pop()

    """
    The loop that drives the game. The game loop continues until the player has won, or a game is restarted.
    """
    def game_loop(self):
        while not self.game_end():
            usr_input = input("Make your move!\n").upper()
            if usr_input == "END GAME":
                break
            elif usr_input == "NEW GAME":
                self.gameboard = Gameboard(self.num_tableau_piles)
            elif usr_input == "SHOW":
                print(self.gameboard)
            elif usr_input.upper() == "UNDO":
                self.undo_move()
            elif usr_input.split()[0] == "MOVE":
                gameboard_copy = copy.deepcopy(self.gameboard)
                move_success = self.make_move(usr_input)
                if move_success:
                    self.move_stack.append(gameboard_copy)
                else:
                    self.gameboard = gameboard_copy
                print(self.gameboard)
            else:
                print("Recognized commands: END GAME, NEW GAME, SHOW, UNDO, MOVE")
        print("Game Over!")

    """
    Move part of a tableau pile to another tableau pile.
    :param src_tab_idx: The index of the tableau pile to take the cards from.
    :param src_tab_card_idx: The index of the first card to take from the tableau pile.
    :param dst_tab_idx: The index of the tableau pile to move the cards to.
    """
    def move_tableau_pile(self, src_tab_idx, src_tab_card_idx, dst_tab_idx):
        src_tab_pile = self.gameboard.tableau_piles[src_tab_idx]
        cards = src_tab_pile.remove_card(src_tab_card_idx)
        for card in cards:
            if not self.gameboard.tableau_piles[dst_tab_idx].add_card(card, True, True):
                raise Exception("Invalid pile state")

    """
    Move a card from a tableau pile to a foundation pile
    :param tab_idx: The index of the tableau pile to take the card from.
    :param found_idx: The index of the foundation pile to move the card to.
    """
    def move_tableau_to_foundation(self, tab_idx, found_idx):
        tab_pile = self.gameboard.tableau_piles[tab_idx]
        card = tab_pile.remove_card(len(tab_pile.cards) - 1)
        if card:
            card = card[0]
            if not self.gameboard.foundation_piles[found_idx].add_card(card, True, True):
                tab_pile.add_card(card, True, True)

    """
    Move a card from a foundation pile to a tableau pile.
    :param tab_idx: The index of the tableau pile to move the card to.
    :param found_idx: The index of the foundation pile to take the card from.
    """
    def move_foundation_to_tableau(self, tab_idx, found_idx):
        found_pile = self.gameboard.foundation_piles[found_idx]
        card = found_pile.remove_card()
        if not self.gameboard.tableau_piles[tab_idx].add_card(card, True, True):
            found_pile.add_card(card, True, True)


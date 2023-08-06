from nimay_solitaire.card import Card
from nimay_solitaire.solitaire import Solitaire
from unittest import TestCase

import copy


class TestSolitaire(TestCase):
    """
    A class for testing Solitaire game logic.
    """

    """
    Test game ending condition
    """
    def test_game_end(self):
        game = Solitaire(loop=False)
        for i in range(4):
            while len(game.gameboard.foundation_piles[i].cards) < 13:
                game.gameboard.foundation_piles[i].add_card(Card(0, 0, True), False, False)
        self.assertTrue(game.game_end())

    """
    Test moving a tableau pile to another tableau pile
    """
    def test_make_move_tableau_to_tableau(self):
        game = Solitaire(loop=False)
        king_of_hearts = Card(Card.HEART, 12, True)
        game.gameboard.tableau_piles[0].cards[0] = king_of_hearts
        queen_of_clubs = Card(Card.CLUB, 11, True)
        jack_of_diamonds = Card(Card.DIAMOND, 10, True)
        game.gameboard.tableau_piles[1].cards = [queen_of_clubs, jack_of_diamonds]
        self.assertTrue(game.make_move("MOVE T 1 0 T 0"))

    """
    Test moving a card from a tableau pile to a foundation pile
    """
    def test_make_move_tableau_to_foundation(self):
        game = Solitaire(loop=False)
        ace_of_hearts = Card(Card.HEART, 0, True)
        game.gameboard.tableau_piles[0].cards[0] = ace_of_hearts
        self.assertTrue(game.make_move("MOVE T 0 F"))
        self.assertEqual(1, len(game.gameboard.foundation_piles[0].cards))

    """
    Test moving a card from a foundation pile to a tableau pile
    """
    def test_make_move_foundation_to_tableau(self):
        game = Solitaire(loop=False)
        two_of_clubs = Card(Card.CLUB, 1, True)
        game.gameboard.tableau_piles[0].cards = [two_of_clubs]
        ace_of_hearts = Card(Card.HEART, 0, True)
        game.gameboard.foundation_piles[0].cards.append(ace_of_hearts)
        self.assertTrue(game.make_move("MOVE F 0 T 0"))
        self.assertEqual(0, len(game.gameboard.foundation_piles[0].cards))
        self.assertEqual(2, len(game.gameboard.tableau_piles[0].cards))

    """
    Test moving a card from the waste pile to a foundation pile
    """
    def test_make_move_waste_to_foundation(self):
        game = Solitaire(loop=False)
        ace_of_hearts = Card(Card.HEART, 0, True)
        game.gameboard.deck.waste_pile.cards = [ace_of_hearts]
        self.assertTrue(game.make_move("MOVE W F"))
        self.assertEqual(1, len(game.gameboard.foundation_piles[0].cards))

    """
    Test moving a card from the waste pile to a tableau pile
    """
    def test_make_move_waste_to_tableau(self):
        game = Solitaire(loop=False)
        two_of_clubs = Card(Card.CLUB, 1, True)
        game.gameboard.tableau_piles[0].cards = [two_of_clubs]
        ace_of_hearts = Card(Card.HEART, 0, True)
        game.gameboard.deck.waste_pile.cards = [ace_of_hearts]
        self.assertTrue(game.make_move("MOVE W T 0"))
        self.assertEqual(0, len(game.gameboard.deck.waste_pile.cards))
        self.assertEqual(2, len(game.gameboard.tableau_piles[0].cards))

    """
    Test a branch of failed move parsing
    """
    def test_make_move_invalid_move0(self):
        game = Solitaire(loop=False)
        self.assertFalse(game.make_move("MOVE W T A"))

    """
    Test a branch of failed move parsing
    """
    def test_make_move_invalid_move1(self):
        game = Solitaire(loop=False)
        self.assertFalse(game.make_move("MOVE T A F"))

    """
    Test a branch of failed move parsing
    """
    def test_make_move_invalid_move2(self):
        game = Solitaire(loop=False)
        self.assertFalse(game.make_move("MOVE T A B T C"))

    """
    Test a branch of failed move parsing
    """
    def test_make_move_invalid_move3(self):
        game = Solitaire(loop=False)
        self.assertFalse(game.make_move("MOVE F T A"))

    """
    Test make move with history
    """
    def test_make_move_with_history(self):
        game = Solitaire(loop=False)
        game.make_move_with_history("MOVE D")
        self.assertEqual(1, len(game.move_stack))

    """
    Test make move with history
    """
    def test_make_move_with_history_invalid_move(self):
        game = Solitaire(loop=False)
        game.make_move_with_history("MOVE F T A")
        self.assertEqual(0, len(game.move_stack))

    """
    Test undoing a move
    """
    def test_undo_move(self):
        game = Solitaire(loop=False)
        game.move_stack.append(copy.deepcopy(game.gameboard))
        game.make_move("MOVE D")
        game.undo_move()
        self.assertEqual(0, len(game.gameboard.deck.waste_pile.cards))

    """
    Test moving a tableau pile to another tableau pile
    """
    def test_move_tableau_pile(self):
        game = Solitaire(loop=False)
        king_of_hearts = Card(Card.HEART, 12, True)
        game.gameboard.tableau_piles[0].cards[0] = king_of_hearts
        queen_of_clubs = Card(Card.CLUB, 11, True)
        jack_of_diamonds = Card(Card.DIAMOND, 10, True)
        game.gameboard.tableau_piles[1].cards = [queen_of_clubs, jack_of_diamonds]
        game.move_tableau_pile(1, 0, 0)
        self.assertEqual(0, len(game.gameboard.tableau_piles[1].cards))
        self.assertEqual(3, len(game.gameboard.tableau_piles[0].cards))

    """
    Test moving a card from a tableau pile to a foundation pile
    """
    def test_move_tableau_to_foundation(self):
        game = Solitaire(loop=False)
        ace_of_hearts = Card(Card.HEART, 0, True)
        game.gameboard.tableau_piles[0].cards[0] = ace_of_hearts
        game.move_tableau_to_foundation(0, Card.HEART)
        self.assertEqual(1, len(game.gameboard.foundation_piles[0].cards))

    """
    Test moving a card from a foundation pile to a tableau pile
    """
    def test_move_foundation_to_tableau(self):
        game = Solitaire(loop=False)
        two_of_clubs = Card(Card.CLUB, 1, True)
        game.gameboard.tableau_piles[0].cards = [two_of_clubs]
        ace_of_hearts = Card(Card.HEART, 0, True)
        game.gameboard.foundation_piles[0].cards.append(ace_of_hearts)
        game.move_foundation_to_tableau(0, 0)
        self.assertEqual(0, len(game.gameboard.foundation_piles[0].cards))
        self.assertEqual(2, len(game.gameboard.tableau_piles[0].cards))


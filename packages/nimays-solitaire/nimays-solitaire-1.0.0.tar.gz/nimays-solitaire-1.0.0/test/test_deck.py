from unittest import TestCase

from nimay_solitaire.card import Card
from nimay_solitaire.deck import Deck


class TestDeck(TestCase):
    """
    Tests the Deck class
    """

    """
    Test deck initialization
    """
    def test_init(self):
        deck = Deck()
        self.assertEqual(52, len(deck.stock_pile.cards))
        self.assertEqual(0, len(deck.waste_pile.cards))

    """
    Test shuffling the deck
    """
    def test_shuffle(self):
        deck = Deck()
        starting_cards = deck.stock_pile.cards[:]
        deck.shuffle()
        self.assertNotEqual(starting_cards, deck.stock_pile.cards)

    """
    Test adding cards to the deck from the waste pile
    """
    def test_add_cards_from_waste(self):
        deck = Deck()
        starting_cards = deck.stock_pile.cards[:]
        card = deck.draw_card()
        deck.waste_pile.add_card(card, False, True)
        deck.add_cards_from_waste()
        self.assertEqual(0, len(deck.waste_pile.cards))
        self.assertEqual(52, len(deck.stock_pile.cards))
        self.assertEqual(starting_cards, deck.stock_pile.cards)

    """
    Test drawing a card deck
    """
    def test_draw_card(self):
        deck = Deck()
        expected_card = Card(Card.SPADE, 12, False)
        self.assertEqual(expected_card, deck.draw_card())

    """
    Test drawing a card to the waste pile
    """
    def test_draw_card_to_waste(self):
        deck = Deck()
        self.assertTrue(deck.draw_card_to_waste())
        self.assertEqual(1, len(deck.waste_pile.cards))
        expected_card = Card(Card.SPADE, 12, False)
        self.assertEqual(expected_card, deck.waste_pile.cards[-1])

    """
    Test draw card to waste with empty deck
    """
    def test_draw_card_to_waste_empty_deck(self):
        deck = Deck()
        for _ in range(52):
            deck.draw_card()
        self.assertFalse(deck.draw_card_to_waste())


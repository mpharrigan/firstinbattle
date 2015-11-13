from unittest import TestCase

from firstinbattle.deck import StandardDeck


class TestCard(TestCase):
    pass


class TestDesk(TestCase):
    def test_get_desk(self):
        deck = StandardDeck.get_deck()
        self.assertEqual(len(deck), 52)

        card = deck.pop()
        self.assertIn(card.suit, StandardDeck.suits)
        self.assertIn(card.number, StandardDeck.numbers)

        self.assertTrue(isinstance(deck, set))

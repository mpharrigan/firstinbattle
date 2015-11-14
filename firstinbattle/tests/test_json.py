from unittest import TestCase

from firstinbattle.deck import Card
from firstinbattle.json_util import js


class TestJson(TestCase):
    def test_encode_loads(self):
        cards = {
            Card(5, 'diamond'),
            Card(9, 'heart'),
        }
        encoded_str = js.encode({
            'message': 'test_msg',
            'cards': cards,
        })

        decoded_obj = js.loads(encoded_str)
        self.assertEqual(decoded_obj['message'], 'test_msg')
        for card in cards:
            self.assertIn(
                {'number': card.number, 'suit': card.suit},
                decoded_obj['cards']
            )

import random
from tornado.testing import gen_test, AsyncHTTPTestCase
from tornado.websocket import websocket_connect
from firstinbattle.gofish import js, Player, Card, Pair
from firstinbattle.main import FIBApplication
from unittest import TestCase


class TestGoFishPython(TestCase):
    def test_consolidate_pairs1(self):
        p1 = Player('p1')
        p1.cards = {
            Card(5, 'diamond'),
            Card(5, 'heart'),
            Card(3, 'heart'),
            Card(5, 'club'),
        }

        new_pairs_could_be = {
            Pair(Card(5, 'diamond'), Card(5, 'heart')),
            Pair(Card(5, 'diamond'), Card(5, 'club')),
            Pair(Card(5, 'heart'), Card(5, 'club')),
        }

        new_pairs = p1.consolidate_pairs()
        self.assertTrue(new_pairs < new_pairs_could_be)
        self.assertSetEqual(p1.pairs, new_pairs)

    def test_consolidate_pairs2(self):
        p1 = Player('p1')
        p1.cards = {
            Card(5, 'diamond'),
            Card(5, 'heart'),
            Card(9, 'heart'),
            Card(9, 'club'),
            Card(2, 'club'),
        }

        new_pairs_should_be = {
            Pair(Card(5, 'diamond'), Card(5, 'heart')),
            Pair(Card(9, 'heart'), Card(9, 'club')),
        }

        cards_should_be = {
            Card(2, 'club'),
        }

        new_pairs = p1.consolidate_pairs()
        self.assertSetEqual(new_pairs, new_pairs_should_be)
        self.assertSetEqual(p1.pairs, new_pairs_should_be)
        self.assertSetEqual(p1.cards, cards_should_be)


class TestGoFish(AsyncHTTPTestCase):
    def get_app(self):
        return FIBApplication()

    @gen_test
    def test_register_player(self):
        ws = yield websocket_connect(
            "ws://localhost:{}/gofish-ws".format(self.get_http_port()),
            io_loop=self.io_loop)

        ws.write_message(js.encode({
            'message': 'register_player',
            'user': {'name': 'p1'}
        }))
        response = yield ws.read_message()
        self.assertTrue(response is not None)
        data = js.loads(response)

        self.assertEqual(data['message'], 'player_registered')
        self.assertEqual(len(data['cards']), 7)
        for card in data['cards']:
            self.assertEqual(set(card.keys()), {'number', 'suit'})
            self.assertTrue(0 <= card['number'] < 13)

    @gen_test
    def test_register_multi_player(self):
        ws1 = yield websocket_connect(
            "ws://localhost:{}/gofish-ws".format(self.get_http_port()),
            io_loop=self.io_loop)
        ws2 = yield websocket_connect(
            "ws://localhost:{}/gofish-ws".format(self.get_http_port()),
            io_loop=self.io_loop)

        ws1.write_message(js.encode({
            'message': 'register_player',
            'user': {'name': 'p1'}
        }))
        _ = yield ws1.read_message()  # player_registered
        _ = yield ws1.read_message()  # return_players

        ws2.write_message(js.encode({
            'message': 'register_player',
            'user': {'name': 'p2'}
        }))
        _ = yield ws2.read_message()  # player_registered

        r1 = yield ws1.read_message()
        r2 = yield ws2.read_message()
        r1 = js.loads(r1)
        r2 = js.loads(r2)
        self.assertEqual(r1['message'], 'return_players')
        self.assertEqual(r1, r2)
        self.assertEqual(len(r1['players']), 2)
        for plyr in r1['players']:
            self.assertEqual(set(plyr.keys()), {'name'})

    @gen_test
    def test_steal_card(self):
        ws1 = yield websocket_connect(
            "ws://localhost:{}/gofish-ws".format(self.get_http_port()),
            io_loop=self.io_loop)
        ws2 = yield websocket_connect(
            "ws://localhost:{}/gofish-ws".format(self.get_http_port()),
            io_loop=self.io_loop)

        ws1.write_message(js.encode({
            'message': 'register_player',
            'user': {'name': 'p1'}
        }))
        _ = yield ws1.read_message()  # player_registered
        _ = yield ws1.read_message()  # return_players

        ws2.write_message(js.encode({
            'message': 'register_player',
            'user': {'name': 'p2'}
        }))
        pr2 = yield ws2.read_message()  # player_registered
        _ = yield ws1.read_message()  # return_players
        _ = yield ws2.read_message()  # return_players

        # Find which card we're going to steal
        pr2 = js.loads(pr2)
        self.assertEqual(pr2['message'], 'player_registered')
        desired_card = pr2['cards'][0]

        # And steal it
        ws1.write_message(js.encode({
            'message': 'request_card',
            'card': desired_card,
            'from': {'name': 'p2'}
        }))
        cr1 = yield ws1.read_message()
        cr1 = js.loads(cr1)

        # Make sure we stole successfully
        self.assertEqual(cr1['message'], 'receive_card')
        self.assertTrue(cr1['success'])
        self.assertEqual(cr1['card'], desired_card)
        self.assertEqual(len(cr1['cards']), 8)

        # p2 should be informed of his loss
        cl2 = yield ws2.read_message()
        cl2 = js.loads(cl2)

        self.assertEqual(cl2['message'], 'card_lost')
        self.assertEqual(cl2['card'], desired_card)
        self.assertEqual(len(cl2['cards']), 6)
        self.assertNotIn(desired_card, cl2['cards'])

    @gen_test
    def test_fish_card(self):
        ws1 = yield websocket_connect(
            "ws://localhost:{}/gofish-ws".format(self.get_http_port()),
            io_loop=self.io_loop)
        ws2 = yield websocket_connect(
            "ws://localhost:{}/gofish-ws".format(self.get_http_port()),
            io_loop=self.io_loop)

        ws1.write_message(js.encode({
            'message': 'register_player',
            'user': {'name': 'p1'}
        }))
        _ = yield ws1.read_message()  # player_registered
        _ = yield ws1.read_message()  # return_players

        ws2.write_message(js.encode({
            'message': 'register_player',
            'user': {'name': 'p2'}
        }))
        pr2 = yield ws2.read_message()  # player_registered
        _ = yield ws1.read_message()  # return_players
        _ = yield ws2.read_message()  # return_players

        # Find which card we're going to steal
        pr2 = js.loads(pr2)
        self.assertEqual(pr2['message'], 'player_registered')
        pr2_cards = pr2['cards']

        # Pick a card that p2 doesn't have
        while True:
            desired_card = {'number': random.randint(0, 13), 'suit': 'heart'}
            if desired_card not in pr2_cards:
                break

        # Ask for it
        ws1.write_message(js.encode({
            'message': 'request_card',
            'card': desired_card,
            'from': {'name': 'p2'}
        }))
        cr1 = yield ws1.read_message()
        cr1 = js.loads(cr1)

        # Make sure we stole successfully
        self.assertEqual(cr1['message'], 'receive_card')
        self.assertFalse(cr1['success'])
        self.assertEqual(len(cr1['cards']), 8)
        self.assertNotIn(cr1['card'], pr2_cards)

        # p2 should not be informed of his loss
        # cl2 = yield ws2.read_message()

    @gen_test
    def test_turn_tracker(self):
        ws1 = yield websocket_connect(
            "ws://localhost:{}/gofish-ws".format(self.get_http_port()),
            io_loop=self.io_loop)
        ws2 = yield websocket_connect(
            "ws://localhost:{}/gofish-ws".format(self.get_http_port()),
            io_loop=self.io_loop)

        ws1.write_message(js.encode({
            'message': 'register_player',
            'user': {'name': 'p1'}
        }))
        _ = yield ws1.read_message()  # player_registered
        _ = yield ws1.read_message()  # return_players

        ws2.write_message(js.encode({
            'message': 'register_player',
            'user': {'name': 'p2'}
        }))
        _ = yield ws2.read_message()  # player_registered
        _ = yield ws1.read_message()  # return_players
        _ = yield ws2.read_message()  # return_players

        # Should be p1's turn
        ws1.write_message(js.encode({
            'message': 'is_turn'
        }))
        it1 = yield ws1.read_message()  # is_turn
        it1 = js.loads(it1)
        self.assertEqual(it1['message'], 'is_turn')
        self.assertTrue(it1['is_turn'])

        # Should not be p2's turn
        ws2.write_message(js.encode({
            'message': 'is_turn'
        }))
        it2 = yield ws2.read_message()  # is_turn
        it2 = js.loads(it2)
        self.assertEqual(it2['message'], 'is_turn')
        self.assertFalse(it2['is_turn'])

        # p1 takes his turn
        ws1.write_message(js.encode({
            'message': 'request_card',
            'card': {'number': 2, 'suit': 'diamond'},
            'from': {'name': 'p2'},
        }))
        rc1 = yield ws1.read_message()  # receive_card
        rc1 = js.loads(rc1)
        self.assertEqual(rc1['message'], 'receive_card')

        # A turn being taken should broadcast turn info.
        it1 = yield ws1.read_message()  # is_turn (broadcast)
        it2 = yield ws2.read_message()  # is_turn (broadcast)
        it1 = js.loads(it1)
        it2 = js.loads(it2)
        self.assertEqual(it1['message'], 'is_turn')
        self.assertEqual(it2['message'], 'is_turn') # TODO: could be lose card
        self.assertFalse(it1['is_turn'])
        self.assertTrue(it2['is_turn'])

        # Should not be p1's turn
        ws1.write_message(js.encode({
            'message': 'is_turn'
        }))
        it1 = yield ws1.read_message()  # is_turn
        it1 = js.loads(it1)
        self.assertEqual(it1['message'], 'is_turn')
        self.assertFalse(it1['is_turn'])

        # Should be p2's turn
        ws2.write_message(js.encode({
            'message': 'is_turn'
        }))
        it2 = yield ws2.read_message()  # is_turn
        it2 = js.loads(it2)
        self.assertEqual(it2['message'], 'is_turn')
        self.assertTrue(it2['is_turn'])

        # Attempting out of turn request should result in a slap
        ws1.write_message(js.encode({
            'message': 'request_card',
            'card': {'number': 3, 'suit': 'diamond'},
            'from': {'name': 'p2'},
        }))
        rc1 = yield ws1.read_message()  # receive_card
        rc1 = js.loads(rc1)
        self.assertEqual(rc1['message'], 'not_your_turn')

    @gen_test
    def test_pair_consolidate1(self):
        ws1 = yield websocket_connect(
            "ws://localhost:{}/gofish-ws".format(self.get_http_port()),
            io_loop=self.io_loop)
        ws1.write_message(js.encode({
            'message': 'register_player',
            'user': {'name': 'p1'}
        }))
        _ = yield ws1.read_message()  # player_registered
        _ = yield ws1.read_message()  # return_players

        ws1.write_message(js.encode({
            'message': 'consolidate_pairs'
        }))
        pc1 = yield ws1.read_message()  # pairs_consolidated
        pc1 = js.loads(pc1)
        self.assertEqual(pc1['message'], 'pairs_consolidated')
        self.assertSetEqual(pc1.keys(),
                            {'message', 'new_pairs', 'all_pairs', 'cards'})
        # we haven't consolidated before, so these should be equal
        self.assertListEqual(pc1['new_pairs'], pc1['all_pairs'])
        self.assertIn(len(pc1['new_pairs']), range(0, 7 // 2 + 1))

        for pair in pc1['new_pairs']:
            self.assertSetEqual(pair.keys(), {'card1', 'card2'})
            self.assertEqual(pair['card1']['number'], pair['card2']['number'])
            self.assertNotEqual(pair['card1']['suit'], pair['card2']['suit'])

    @gen_test
    def test_pair_consolidate2(self):
        ws1 = yield websocket_connect(
            "ws://localhost:{}/gofish-ws".format(self.get_http_port()),
            io_loop=self.io_loop)
        ws1.write_message(js.encode({
            'message': 'register_player',
            'user': {'name': 'p1'}
        }))
        _ = yield ws1.read_message()  # player_registered
        _ = yield ws1.read_message()  # return_players

        # Get all the cards
        for _ in range(52 - 7):
            ws1.write_message(js.encode({
                'message': 'request_card',
                'from': {'name': 'p1'},
                'card': {'suit': 'xxxx', 'number': 0},
            }))
            cr1 = yield ws1.read_message()  # receive_card

        cr1 = js.loads(cr1)
        self.assertEqual(len(cr1['cards']), 52)

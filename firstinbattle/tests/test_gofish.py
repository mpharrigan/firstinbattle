import random

from tornado.testing import gen_test, AsyncHTTPTestCase
from tornado.websocket import websocket_connect

from firstinbattle.gofish import js
from firstinbattle.main import FIBApplication


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
        self.assertEqual(it2['message'], 'is_turn')
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

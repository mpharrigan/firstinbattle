from tornado.websocket import WebSocketHandler
from tornado.web import RequestHandler
import logging
import json as _json
import itertools
import random

log = logging.getLogger(__name__)

SUITS = {'heart', 'spade', 'club', 'diamond'}
COLORS = {
    'heart': 'red',
    'diamond': 'red',
    'spade': 'black',
    'club': 'black',
}
NUMBERS = set(range(13))


class JSON(_json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'json'):
            return obj.json
        # Let the base class default method raise the TypeError
        return _json.JSONEncoder.default(self, obj)

    def loads(self, bytes):
        return _json.loads(bytes, encoding='utf-8')


js = JSON()


def get_deck():
    cards = [Card(number, suit)
             for number, suit
             in itertools.product(NUMBERS, SUITS)]
    return cards


class DontHave(Exception):
    pass


class Card:
    def __init__(self, number, suit):
        self.number = number
        self.suit = suit

    @property
    def json(self):
        return {
            'number': self.number,
            'suit': self.suit
        }

    def __eq__(self, other):
        return self.number == other.number and self.suit == other.suit


class Player:
    def __init__(self, name, ws=None):
        self.name = name
        self.ws = ws
        self.cards = []

    def request(self, req_card):
        """Other players may ask for a card. We have to give it to them
        """
        if req_card is None:
            return self.cards.pop()

        if req_card not in self.cards:
            raise DontHave
        else:
            self.cards.remove(req_card)
            return req_card

    @property
    def json(self):
        return {
            'name': self.name,
            'cards': self.cards,
        }


class GoFish:
    game_name = 'gofish'
    hand_size = 7

    def __init__(self):
        self.dealer = Player('dealer')
        self.dealer.cards = get_deck()
        random.shuffle(self.dealer.cards)
        self.players = []

    def new_player(self, player):
        player.cards = self.dealer.cards[:self.hand_size]
        self.dealer.cards = self.dealer.cards[self.hand_size:]
        self.players += [player]
        return player

    def get_player(self, id):
        # TODO: Use some sort of guid
        for player in self.players:
            if player.name == id:
                return player


class GoFishRh(RequestHandler):
    def post(self, command):
        data = js.loads(self.request.body)
        if command == 'new_game':
            user = data['user']
            print(user)


class GoFishWs(WebSocketHandler):
    game_class = GoFish
    ws_id = 0

    def open(self, *args, **kwargs):
        log.info("Websocket opened")
        games = self.application.games[self.game_class.game_name]

        # TODO: choose game
        if len(games) > 0:
            game = games[0]
        else:
            game = self.game_class()
            games.append(game)

        self.game = game

    def register_player(self, data):
        """Trigger when a new user is entering the game

        This will cause the `return_players` message to be sent to
        all WSs

        Accepts
        -------
        user
            - name

        Responds
        --------
        'player_registered'
            - cards : list
        """
        player = self.game.new_player(Player(
            name=data['user']['name'],
            ws=self,
        ))
        self.player = player
        self.write_message(js.encode({
            'message': 'player_registered',
            'cards': player.cards,
        }))

        for player in self.game.players:
            player.ws.get_players(None)

    def get_players(self, data):
        """Request unconfidential player data

        Responds
        --------
        'return_players'
            - players : list
        """
        self.write_message(js.encode({
            'message': 'return_players',
            'players': [{'name': p.name} for p in self.game.players],
        }))

    def request_card(self, data):
        """Ask another player for a card.

        Accepts
        -------
        from : Player
            - name : str
        card : Card-ish
            - number : int
            - suit : str

        Responds
        --------
        'receive_card'
            - card : Card
            - success : bool
                True if from player, go fish otherwise
        """
        other_player = self.game.get_player(data['from']['name'])
        card = Card(**data['card'])
        try:
            card = other_player.request(card)
            success = True
            other_player.ws.lose_card(card)
        except DontHave:
            # Go fish!
            card = self.game.dealer.request(None)
            success = False

        self.player.cards += [card]
        self.write_message(js.encode({
            'message': 'receive_card',
            'success': success,
            'card': card,
            'cards': self.player.cards
        }))

    def lose_card(self, card):
        self.write_message(js.encode({
            'message': 'card_lost',
            'card': card,
            'cards': self.player.cards
        }))

    def on_message(self, data):
        data = js.loads(data)
        getattr(self, data['message'])(data)

    def on_close(self):
        log.info("Websocket closed")

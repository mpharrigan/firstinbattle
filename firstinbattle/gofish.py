import logging
import random
from collections import defaultdict

from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler

from .deck import StandardDeck, Card, NPair
from .json_util import js

log = logging.getLogger(__name__)


class DontHave(Exception):
    pass


class OutOfTurn(Exception):
    pass


class Pair(NPair):
    N = 2


class Player:
    def __init__(self, name, ws=None):
        self.name = name
        self.ws = ws
        self.cards = set()
        self.pairs = set()

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

    def consolidate_pairs(self):
        """Take our hand and combine pairs."""
        by_number = defaultdict(set)
        for card in self.cards:
            by_number[card.number].add(card)

        new_pairs = set()
        for num, cards in by_number.items():
            while len(cards) >= 2:
                pair = Pair(*(cards.pop() for _ in range(2)))
                new_pairs.add(pair)
                for c in pair.cards:
                    self.cards.remove(c)

        self.pairs |= new_pairs
        return new_pairs

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
        self.dealer.cards = StandardDeck.get_deck()
        self.players = []

        self._turn = 0

    def new_player(self, player):
        player.cards = set(random.sample(self.dealer.cards, self.hand_size))
        self.dealer.cards -= player.cards

        self.players += [player]
        return player

    def get_player(self, id):
        # TODO: Use some sort of guid
        for player in self.players:
            if player.name == id:
                return player
        raise ValueError("Could not find player {}".format(id))

    def is_turn(self, player):
        return player == self.players[self._turn]

    def next_turn(self):
        self._turn += 1
        if self._turn >= len(self.players):
            self._turn = 0

    def request(self, *, card, from_player, to_player):
        if not self.is_turn(to_player):
            raise OutOfTurn

        try:
            card = from_player.request(card)
            success = True
        except DontHave:
            # Go fish!
            card = self.dealer.request(None)
            success = False

        to_player.cards.add(card)
        self.next_turn()
        return card, success


class GoFishRh(RequestHandler):
    def post(self, command):
        data = js.loads(self.request.body)
        # TODO


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

        This will cause the `return_players` message to broadcast
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
        """
        self.write_message(js.encode({
            'message': 'return_players',
            'players': [{'name': p.name} for p in self.game.players],
        }))

    def request_card(self, data):
        """Ask another player for a card.

        Will cause a broadcast of `is_turn`
        """
        other_player = self.game.get_player(data['from']['name'])
        card = Card(**data['card'])

        try:
            card, success = self.game.request(
                card=card,
                from_player=other_player,
                to_player=self.player,
            )
            # Tell current player of his conquests
            self.write_message(js.encode({
                'message': 'receive_card',
                'success': success,
                'card': card,
                'cards': self.player.cards
            }))
            # Tell other player if they lost a card
            if success:
                other_player.ws.lose_card(card)

            # Tell everyone their turn
            for player in self.game.players:
                player.ws.is_turn(None)
        except OutOfTurn:
            self.write_message(js.encode({
                'message': 'not_your_turn',
            }))

    def lose_card(self, card):
        """Called on a player that has lost a card

        The card should have already been removed from the player's hand.
        This serves to notify the user that a card has been stolen.

        """
        self.write_message(js.encode({
            'message': 'card_lost',
            'card': card,
            'cards': self.player.cards
        }))

    def is_turn(self, data):
        """Ask 'is it my turn?'
        """
        self.write_message(js.encode({
            'message': 'is_turn',
            'is_turn': self.game.is_turn(self.player)
        }))

    def consolidate_pairs(self, data):
        """Take hand and consolidate pairs
        """
        new_pairs = self.player.consolidate_pairs()
        self.write_message(js.encode({
            'message': 'pairs_consolidated',
            'all_pairs': self.player.pairs,
            'new_pairs': new_pairs,
            'cards': self.player.cards,
        }))

    def on_message(self, data):
        data = js.loads(data)
        getattr(self, data['message'])(data)

    def on_close(self):
        log.info("Websocket closed")

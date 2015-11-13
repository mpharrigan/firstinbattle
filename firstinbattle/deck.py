import itertools


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

    def __hash__(self):
        return hash((
            self.number,
            self.suit,
        ))

    def __repr__(self):
        return "{number} of {suit}s".format(**self.__dict__)


class NPair:
    # Override below
    N = 0

    def __init__(self, *cards):
        assert len(cards) == self.N
        self.cards = frozenset(cards)

    @property
    def json(self):
        return {'card{}'.format(i): card
                for i, card in enumerate(self.cards)}

    def __eq__(self, other):
        return self.cards == other.cards

    def __hash__(self):
        return hash(self.cards)

    def __repr__(self):
        return "<" + ", ".join(repr(card) for card in self.cards) + ">"


class StandardDeck:
    suits = {'heart', 'spade', 'club', 'diamond'}
    colors = {
        'heart': 'red',
        'diamond': 'red',
        'spade': 'black',
        'club': 'black',
    }
    numbers = set(range(13))

    @classmethod
    def get_deck(cls):
        cards = set(Card(number, suit)
                    for number, suit
                    in itertools.product(cls.numbers, cls.suits))
        return cards

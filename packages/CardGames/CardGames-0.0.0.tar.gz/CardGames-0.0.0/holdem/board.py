from cards import deck

class Board(object):
    """The "board". Holds the community cards (flop, turn, river) and the
    discard pile."""
    def __init__(self):
        self._flop = []
        self._turn = []
        self._river = []
        self._discard_pile = deck.Deck()

    @property
    def flop(self):
        """Get the flop."""
        return self._flop

    @flop.setter
    def flop(self, flop):
        self._flop =  flop

    @property
    def turn(self):
        """Get the turn."""
        return self._turn

    @turn.setter
    def turn(self, turn):
        self._turn = turn

    @property
    def river(self):
        """Get the river."""
        return self._river

    @river.setter
    def river(self, river):
        self._river = river

    @property
    def discard_pile(self):
        """Get the discard pile."""
        return self._discard_pile

    @property
    def community_cards(self):
        """Get the community cards."""
        all_cards = self._flop + [self._turn] + [self._river]
        return [card for card in all_cards
                if card] # if card exists (is not an empty list)

    @property
    def empty(self):
        """Return true if the board is empty."""
        return self.community_cards == []

from . import exceptions

class Dealer(object):
    def __init__(self, board, deck):
        self._board = board
        self._deck = deck

    def deal(self):
        if not self._board.flop:
            self._deal_flop()
        elif not self._board.turn:
            self._deal_turn()
        elif not self._board.river:
            self._deal_river()
        else:
            raise exceptions.BoardFullException

    def _deal_flop(self):
        self._burn_card()
        self._board.flop = [self._deck.draw() for i in range(3)]

    def _deal_turn(self):
        self._burn_card()
        self._board.turn = self._deck.draw()

    def _deal_river(self):
        self._burn_card()
        self._board.river = self._deck.draw()

    def _burn_card(self):
        burned_card = self._deck.draw()
        self._board.discard_pile.insert_to_top(burned_card)


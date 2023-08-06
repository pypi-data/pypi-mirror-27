import pytest

from cards.deck import StandardPlayingCardDeck
from holdem.board import Board
from holdem.dealer import Dealer
from holdem.exceptions import BoardFullException


@pytest.fixture
def dealer_board_deck():
    my_deck = StandardPlayingCardDeck()
    my_deck.shuffle()
    board = Board()
    return (Dealer(board, my_deck), board, my_deck)

def test_init():
    deck = StandardPlayingCardDeck()
    board = Board()
    Dealer(board, deck)

def test_flop(dealer_board_deck):
    dealer, board, deck = dealer_board_deck
    discard = board.discard_pile
    burned_card = deck.draw()
    flop_cards = [deck.draw() for i in range(3)]
    for card in reversed(flop_cards):
        deck.insert_to_top(card)
    deck.insert_to_top(burned_card)
    dealer.deal()
    assert len(discard) == 1
    assert burned_card in discard
    assert board.flop == flop_cards

def test_turn(dealer_board_deck):
    dealer, board, deck = dealer_board_deck
    discard = board.discard_pile
    dealer.deal()
    burned_card = deck.draw()
    turn_card = deck.draw()
    deck.insert_to_top(turn_card)
    deck.insert_to_top(burned_card)
    dealer.deal()
    assert len(discard) == 2
    assert burned_card in discard
    assert board.turn == turn_card

def test_river(dealer_board_deck):
    dealer, board, deck = dealer_board_deck
    discard = board.discard_pile
    dealer.deal()
    dealer.deal()
    burned_card = deck.draw()
    river_card = deck.draw()
    deck.insert_to_top(river_card)
    deck.insert_to_top(burned_card)
    dealer.deal()
    assert len(discard) == 3
    assert burned_card in discard
    assert board.river == river_card

def test_raise_exception_after_third_deal(dealer_board_deck):
    dealer, _, _ = dealer_board_deck
    for i in range(3):
        dealer.deal()
    for i in range(5):
        with pytest.raises(BoardFullException):
            dealer.deal()



import pytest

from cards import deck
from holdem import board

@pytest.fixture
def draw_deck():
    to_return = deck.StandardPlayingCardDeck()
    to_return.shuffle()
    return to_return

@pytest.fixture
def empty_board():
    return board.Board()

def test_empty_board(empty_board):
    assert empty_board.empty

def test_community_cards_on_empty_board(empty_board):
    assert empty_board.community_cards == []

def test_flop(empty_board, draw_deck):
    board = empty_board
    flop = [draw_deck.draw() for i in range(3)]
    board.flop = flop
    assert len(board.flop) == 3
    assert board.flop == flop
    assert board.community_cards == flop

def test_turn(empty_board, draw_deck):
    board = empty_board
    flop = [draw_deck.draw() for i in range(3)]
    board.flop = flop
    turn = draw_deck.draw()
    board.turn = turn
    assert board.turn == turn
    assert board.community_cards == flop + [turn]

def test_river(empty_board, draw_deck):
    board = empty_board
    flop = [draw_deck.draw() for i in range(3)]
    board.flop = flop
    turn = draw_deck.draw()
    board.turn = turn
    river = draw_deck.draw()
    board.river = river
    assert board.river == river
    assert board.community_cards == flop + [turn] + [river]


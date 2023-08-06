import pytest

from cards import playing_cards
from cards import exceptions
from cards import ranks
from cards import suits

class TestCards(object):
    def test_init(self):
        playing_cards.StandardPlayingCard('Ace', 'Spade')

    def test_bad_suit_raises_exception(self):
        with pytest.raises(exceptions.IllegalSuitException):
            playing_cards.StandardPlayingCard('ace', 'bunnies')

    def test_bad_rank_raises_exception(self):
        with pytest.raises(exceptions.IllegalRankException):
            playing_cards.StandardPlayingCard('potato', 'spades')

    def test_rank(self):
        ace = playing_cards.StandardPlayingCard('Ace', 'Spade')
        assert ace.rank == 'Ace'

    def test_suit(self):
        ace = playing_cards.StandardPlayingCard('Ace', 'Spade')
        assert ace.suit == 'Spade'

    def test_text(self):
        ace = playing_cards.StandardPlayingCard('Ace', 'Spade')
        assert ace.name == 'Ace of Spades'

    def test_card_identity_property(self):
        king = playing_cards.StandardPlayingCard('King', 'diamonds')
        assert king == king

    def test_same_cards_equal(self):
        seven = playing_cards.StandardPlayingCard(7, 'Clover')
        seven_2 = playing_cards.StandardPlayingCard(7, 'Clover')
        assert seven == seven_2

    def test_different_cards_unequal(self):
        queen = playing_cards.StandardPlayingCard('queen', 'hearts')
        other_cards = [playing_cards.StandardPlayingCard(rank, suit)
                       for rank in ranks.get_all_ranks()
                       for suit in suits.get_all_suits()]
        other_cards.remove(queen)
        for other_card in other_cards:
            assert queen != other_card


# removed because these are game logic tests, not card object tests
    # def test_ace_beats_2(self):
    #     ace = cards.StandardPlayingCard('Ace', 'Spade')
    #     two = cards.StandardPlayingCard('2', 'spade')
    #     assert ace > two
    #     assert ace >= two
    #     assert two < ace
    #     assert two <= ace
    #
    # def test_all_ranks_beat_smaller_ranks(self):
    #     for rank in ranks.get_all_ranks():
    #         lesser_ranks = ranks.get_smaller_ranks(rank)
    #         big_card = cards.StandardPlayingCard(rank, 'spades')
    #         for lesser_rank in lesser_ranks:
    #             small_card = cards.StandardPlayingCard(lesser_rank, 'spades')
    #             assert big_card > small_card
    #
    # def test_same_rank_different_suit_are_equal(self):
    #     for rank in ranks.get_all_ranks():
    #         for suit in suits.get_all_suits():
    #             base_card = cards.StandardPlayingCard(rank, suit)
    #             other_suits = suits.get_all_suits() - set(suit)
    #             for different_suit in other_suits:
    #                 different_suited_card = cards.StandardPlayingCard(rank, different_suit)
    #                 assert base_card == different_suited_card




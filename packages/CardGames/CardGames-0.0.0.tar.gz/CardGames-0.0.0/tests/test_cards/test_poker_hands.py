import pytest

import cards.classification_utils
import cards.classify_hand
import cards.five_card_hand
from cards import playing_cards
from cards import exceptions
from cards import poker_hands
from cards import ranks
from cards import suits

@pytest.fixture
def royal_flush_diamonds():
    ace_diamonds = playing_cards.StandardPlayingCard(ranks.ACE, suits.DIAMOND)
    king_diamonds = playing_cards.StandardPlayingCard(ranks.KING, suits.DIAMOND)
    queen_diamonds = playing_cards.StandardPlayingCard(ranks.QUEEN, suits.DIAMOND)
    jack_diamonds = playing_cards.StandardPlayingCard(ranks.JACK, suits.DIAMOND)
    ten_diamonds = playing_cards.StandardPlayingCard(ranks.TEN, suits.DIAMOND)
    hand = cards.five_card_hand.FiveCardHand([ace_diamonds, king_diamonds, queen_diamonds, jack_diamonds, ten_diamonds])
    return hand

@pytest.fixture
def four_of_a_kind_9s():
    hand = [playing_cards.StandardPlayingCard(ranks.NINE, suit) for suit in suits.get_all_suits()]
    hand.append(playing_cards.StandardPlayingCard(ranks.FOUR, suits.CLOVER))
    return cards.five_card_hand.FiveCardHand(hand)

@pytest.fixture
def full_house_queens():
    hand = [playing_cards.StandardPlayingCard(ranks.QUEEN, suit) for suit in [suits.DIAMOND, suits.CLOVER, suits.SPADE]]
    hand += [playing_cards.StandardPlayingCard(ranks.SEVEN, suit) for suit in [suits.HEART, suits.SPADE]]
    return poker_hands.FullHouse(hand)

@pytest.fixture
def flush_spades():
    hand = [playing_cards.StandardPlayingCard(rank, suits.SPADE)
            for rank in [ranks.SEVEN, ranks.QUEEN, ranks.ACE, ranks.TWO, ranks.TEN]]
    return poker_hands.Flush(hand)

@pytest.fixture
def straight():
    hand = [playing_cards.StandardPlayingCard(rank, suits.HEART) for rank in ranks.get_all_ranks()[3:7]]
    hand.append(playing_cards.StandardPlayingCard(ranks.NINE, suits.CLOVER))
    return poker_hands.Straight(hand)

@pytest.fixture
def three_of_a_kind():
   hand = [playing_cards.StandardPlayingCard(ranks.SIX, suit) for suit in [suits.SPADE, suits.HEART, suits.DIAMOND]]
   hand += [playing_cards.StandardPlayingCard(ranks.NINE, suits.CLOVER), playing_cards.StandardPlayingCard(ranks.TWO, suits.SPADE)]
   return poker_hands.ThreeOfAKind(hand)

@pytest.fixture
def two_pair():
    hand = [playing_cards.StandardPlayingCard(ranks.THREE, suit) for suit in suits.get_black_suits()]
    hand += [playing_cards.StandardPlayingCard(ranks.FIVE, suit) for suit in suits.get_red_suits()]
    hand += [playing_cards.StandardPlayingCard(ranks.QUEEN, suits.DIAMOND)]
    return poker_hands.TwoPair(hand)

@pytest.fixture
def one_pair():
    hand = [playing_cards.StandardPlayingCard(ranks.TWO, suit) for suit in suits.get_black_suits()]
    hand += [playing_cards.StandardPlayingCard(rank, suits.CLOVER) for rank in [ranks.QUEEN, ranks.FIVE, ranks.TEN]]
    return poker_hands.OnePair(hand)

@pytest.fixture
def high_card():
    hand = [playing_cards.StandardPlayingCard(rank, suits.DIAMOND) for rank in ranks.get_all_ranks()[:4]]
    hand += [playing_cards.StandardPlayingCard(ranks.TEN, suits.CLOVER)]
    return poker_hands.HighCard(hand)

@pytest.fixture
def straight_ace_low():
    hand = [playing_cards.StandardPlayingCard(rank, suits.CLOVER) for rank in [ranks.ACE, ranks.TWO, ranks.THREE, ranks.FOUR]]
    hand.append(playing_cards.StandardPlayingCard(ranks.FIVE, suits.DIAMOND))
    return cards.five_card_hand.FiveCardHand(hand)

@pytest.fixture
def straight_ace_high():
    hand = [playing_cards.StandardPlayingCard(rank, suits.CLOVER) for rank in [ranks.TEN, ranks.JACK, ranks.QUEEN, ranks.KING]]
    hand.append(playing_cards.StandardPlayingCard(ranks.ACE, suits.DIAMOND))
    return cards.five_card_hand.FiveCardHand(hand)

@pytest.fixture
def straight_flush_spades_5_high():
    hand = [playing_cards.StandardPlayingCard(rank, suits.SPADE)
            for rank in [ranks.ACE, ranks.TWO, ranks.THREE, ranks.FOUR, ranks.FIVE]]
    return cards.classify_hand.classify(hand)


class TestFiveCardHand():
    def test_init(self, royal_flush_diamonds):
        pass

    def test_raises_exception_on_4_items(self):
        with pytest.raises(exceptions.NotEnoughCardsException):
            cards.five_card_hand.FiveCardHand([1, 2, 3, 4])

    def test_raises_exception_on_6_items(self):
        with pytest.raises(exceptions.TooManyCardsException):
            cards.five_card_hand.FiveCardHand([1, 2, 3, 4, 5, 6])

    def test_suit_counts_royal_flush(self, royal_flush_diamonds):
        assert royal_flush_diamonds.suit_counts == {suits.DIAMOND: 5}

    def test_suit_counts_four_of_a_kind(self, four_of_a_kind_9s):
        expected_suit_counts = {suit: 1 for suit in suits.get_all_suits()}
        expected_suit_counts[suits.CLOVER] += 1
        assert four_of_a_kind_9s.suit_counts == expected_suit_counts

    def test_rank_counts_four_of_a_kind(self, four_of_a_kind_9s):
        expected_rank_counts = {ranks.NINE: 4, ranks.FOUR: 1}
        assert four_of_a_kind_9s.rank_counts == expected_rank_counts

    def test_rank_counts_royal_flush(self, royal_flush_diamonds):
        ranks_to_expect = [ranks.TEN, ranks.JACK, ranks.QUEEN, ranks.KING, ranks.ACE]
        expected_suit_counts = {rank: 1 for rank in ranks_to_expect}
        assert royal_flush_diamonds.rank_counts == expected_suit_counts

    def test_iterator(self, royal_flush_diamonds):
        ranks_to_expect = reversed([ranks.TEN, ranks.JACK, ranks.QUEEN, ranks.KING, ranks.ACE])
        cards_to_expect = [playing_cards.StandardPlayingCard(rank, suits.DIAMOND) for rank in ranks_to_expect]
        for expected_card, actual_card in zip(cards_to_expect, royal_flush_diamonds):
            assert expected_card == actual_card


class TestHandTrumpMechanics(object):
    def test_straight_flush_beats_four_of_a_kind(self, royal_flush_diamonds, four_of_a_kind_9s):
        straight_flush = poker_hands.StraightFlush([card for card in royal_flush_diamonds])
        four_of_a_kind = poker_hands.FourOfAKind([card for card in four_of_a_kind_9s])
        assert straight_flush > four_of_a_kind
        assert four_of_a_kind < straight_flush

    def test_four_of_a_kind_beats_full_house(self, four_of_a_kind_9s, full_house_queens):
        four_of_a_kind = poker_hands.FourOfAKind([card for card in four_of_a_kind_9s])
        full_house = poker_hands.FullHouse([card for card in full_house_queens])
        assert four_of_a_kind > full_house
        assert full_house < four_of_a_kind

    def test_full_house_beats_flush(self, full_house_queens, flush_spades):
        assert full_house_queens > flush_spades
        assert flush_spades < full_house_queens

    def test_flush_beats_straight(self, flush_spades, straight):
        assert flush_spades > straight
        assert straight < flush_spades

    def test_straight_beats_three_of_a_kind(self, straight, three_of_a_kind):
        assert straight > three_of_a_kind
        assert three_of_a_kind < straight

    def test_three_of_a_kind_beats_two_pair(self, three_of_a_kind, two_pair):
        assert three_of_a_kind > two_pair
        assert two_pair < three_of_a_kind

    def test_two_pair_beats_one_pair(self, two_pair, one_pair):
        assert two_pair > one_pair
        assert one_pair < two_pair

    def test_one_pair_beats_high_card(self, one_pair, high_card):
        assert one_pair > high_card
        assert high_card < one_pair

    def test_same_hands_raise_exception(self, one_pair, royal_flush_diamonds, three_of_a_kind):
        with pytest.raises(exceptions.SamePokerHandClassException):
            assert one_pair > one_pair
        royal_flush_diamonds = cards.classify_hand.classify(royal_flush_diamonds)
        with pytest.raises(exceptions.SamePokerHandClassException):
            assert royal_flush_diamonds < royal_flush_diamonds
        with pytest.raises(exceptions.SamePokerHandClassException):
            assert three_of_a_kind > three_of_a_kind


class TestClassifyRankMatches(object):
    def test_classify_four_of_a_kind(self, four_of_a_kind_9s):
        assert isinstance(cards.classify_hand.classify(four_of_a_kind_9s), poker_hands.FourOfAKind)

    def test_classify_full_house(self, full_house_queens):
        assert isinstance(cards.classify_hand.classify(full_house_queens), poker_hands.FullHouse)

    def test_classify_three_of_a_kind(self, three_of_a_kind):
        assert isinstance(cards.classify_hand.classify(three_of_a_kind), poker_hands.ThreeOfAKind)

    def test_classify_two_pair(self, two_pair):
        assert isinstance(cards.classify_hand.classify(two_pair), poker_hands.TwoPair)

    def test_classify_one_pair(self, one_pair):
        assert isinstance(cards.classify_hand.classify(one_pair), poker_hands.OnePair)


class TestClassifyFlushes(object):
    def test_classify_flush(self, flush_spades):
        assert isinstance(cards.classify_hand.classify(flush_spades), poker_hands.Flush)

    def test_classify_straight_flush_is_flush(self, royal_flush_diamonds):
        assert isinstance(cards.classify_hand.classify(royal_flush_diamonds), poker_hands.Flush)

    def test_classify_straight_flush_is_straight_flush(self, royal_flush_diamonds):
        assert isinstance(cards.classify_hand.classify(royal_flush_diamonds), poker_hands.StraightFlush)

    def test_classify_flush_is_not_straight_flush(self, flush_spades):
        assert not isinstance(cards.classify_hand.classify(flush_spades), poker_hands.StraightFlush)


class TestClassifyStraight(object):
    def test_classify_straight_ace_low(self, straight_ace_low):
        assert cards.classification_utils.is_straight_ace_low(straight_ace_low)

    def test_classify_straight_ace_low_rejects_ace_high(self, straight_ace_high):
        assert not cards.classification_utils.is_straight_ace_low(straight_ace_high)

    def test_classify_straight_ace_high(self, straight_ace_high):
        assert cards.classification_utils.is_straight_ace_high(straight_ace_high)

    def test_classify_straight_ace_high_rejects_ace_low(self, straight_ace_low):
        assert not cards.classification_utils.is_straight_ace_high(straight_ace_low)

    def test_classify_straight(self, straight):
        assert isinstance(cards.classify_hand.classify(straight), poker_hands.Straight)

    def test_classify_straight_default_with_ace_low(self, straight_ace_low):
        assert isinstance(cards.classify_hand.classify(straight_ace_low), poker_hands.Straight)

    def test_classify_straight_default_with_ace_high(self, straight_ace_high):
        assert isinstance(cards.classify_hand.classify(straight_ace_high), poker_hands.Straight)

    def test_straight_flush_is_straight(self, royal_flush_diamonds):
        assert isinstance(cards.classify_hand.classify(royal_flush_diamonds), poker_hands.Straight)


class TestClassifyHighCard(object):
    def test_classify_high_card(self, high_card):
        assert isinstance(cards.classify_hand.classify(high_card), poker_hands.HighCard)

class TestDominantRanks(object):
    def test_straight_flush(self, royal_flush_diamonds, straight_flush_spades_5_high):
        assert cards.classify_hand.classify(royal_flush_diamonds).get_high_card() == ranks.ACE
        assert cards.classify_hand.classify(straight_flush_spades_5_high).get_high_card() == ranks.FIVE

    def test_four_of_a_kind(self, four_of_a_kind_9s):
        four_of_a_kind_9s = cards.classify_hand.classify(four_of_a_kind_9s)
        assert four_of_a_kind_9s.get_dominant_rank() == ranks.NINE
        assert four_of_a_kind_9s.get_kicker() == playing_cards.StandardPlayingCard(ranks.FOUR, suits.CLOVER)

    def test_full_house(self, full_house_queens):
        full_house_queens = cards.classify_hand.classify(full_house_queens)
        assert full_house_queens.get_triple_rank() == ranks.QUEEN
        assert full_house_queens.get_double_rank() == ranks.SEVEN

    def test_flush(self, flush_spades, royal_flush_diamonds, straight_flush_spades_5_high):
        flush_spades = cards.classify_hand.classify(flush_spades)
        royal_flush_diamonds = cards.classify_hand.classify(royal_flush_diamonds)
        straight_flush_spades_5_high = cards.classify_hand.classify(straight_flush_spades_5_high)
        assert flush_spades.get_cards_high_to_low() == [ranks.ACE, ranks.QUEEN, ranks.TEN, ranks.SEVEN, ranks.TWO]
        assert royal_flush_diamonds.get_cards_high_to_low() == [ranks.ACE, ranks.KING, ranks.QUEEN,
                                                                ranks.JACK, ranks.TEN]
        assert straight_flush_spades_5_high.get_cards_high_to_low() == [ranks.FIVE, ranks.FOUR, ranks.THREE,
                                                                        ranks.TWO, ranks.ACE]

    def test_straight(self, straight, straight_flush_spades_5_high, royal_flush_diamonds):
        straight = cards.classify_hand.classify(straight)
        straight_flush_spades_5_high = cards.classify_hand.classify(straight_flush_spades_5_high)
        royal_flush_diamonds = cards.classify_hand.classify(royal_flush_diamonds)
        assert straight.get_high_card() == ranks.NINE
        assert straight_flush_spades_5_high.get_high_card() == ranks.FIVE
        assert royal_flush_diamonds.get_high_card() == ranks.ACE

    def test_three_of_a_kind(self, three_of_a_kind):
        three_of_a_kind = cards.classify_hand.classify(three_of_a_kind)
        assert three_of_a_kind.get_dominant_rank() == ranks.SIX
        assert three_of_a_kind.get_high_kicker() == ranks.NINE
        assert three_of_a_kind.get_low_kicker() == ranks.TWO

    def test_two_pair(self, two_pair):
        two_pair = cards.classify_hand.classify(two_pair)
        assert two_pair.get_high_pair_rank() == ranks.FIVE
        assert two_pair.get_low_pair_rank() == ranks.THREE

    def test_one_pair(self, one_pair):
        one_pair = cards.classify_hand.classify(one_pair)
        assert one_pair.get_pair_rank() == ranks.TWO
        assert one_pair.get_kickers_high_to_low() == [ranks.QUEEN, ranks.TEN, ranks.FIVE]

    def test_high_card(self, high_card):
        high_card = cards.classify_hand.classify(high_card)
        assert high_card.get_cards_high_to_low() == [ranks.TEN, ranks.FIVE, ranks.FOUR, ranks.THREE, ranks.TWO]

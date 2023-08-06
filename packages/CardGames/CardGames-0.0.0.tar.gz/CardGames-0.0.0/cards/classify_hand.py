from cards.classification_utils import is_straight_ace_low_high, is_flush
from cards.five_card_hand import FiveCardHand
from cards.poker_hands import StraightFlush, Straight, Flush, HighCard, FourOfAKind, FullHouse, ThreeOfAKind, TwoPair, \
    OnePair


def classify(hand, is_straight_function=is_straight_ace_low_high):
    """Takes a list of cards or a FiveCardHand and classifies it as one
    of the poker hands, returning an object of that type containing the
    given cards."""
    five_card_hand = FiveCardHand(hand)
    hand_is_straight = is_straight_function(five_card_hand)
    hand_is_flush = is_flush(five_card_hand)
    if hand_is_flush and hand_is_straight:
        return StraightFlush(five_card_hand)
    elif not hand_is_flush and hand_is_straight:
        return Straight(five_card_hand)
    elif hand_is_flush and not hand_is_straight:
        return Flush(five_card_hand)
    elif five_card_hand.has_matches():
        return _classify_hand_with_matches(five_card_hand)
    else:
        return HighCard(five_card_hand)


def _classify_hand_with_matches(five_card_hand):
    first_pass = _classify_hand_with_matches_first_pass(five_card_hand)
    if first_pass is not None:
        return first_pass
    else:
        return _classify_hand_with_matches_second_pass(five_card_hand)


def _classify_hand_with_matches_first_pass(five_card_hand):
    for rank, rank_count in five_card_hand.rank_counts.items():
        if rank_count == 4:
            return FourOfAKind(five_card_hand)
        if rank_count == 3:
            return _classify_card_with_3_of_same_rank(five_card_hand)
    return None


def _classify_card_with_3_of_same_rank(five_card_hand):
    for rank, rank_count in five_card_hand.rank_counts.items():
        if rank_count == 2:
            return FullHouse(five_card_hand)
    return ThreeOfAKind(five_card_hand)


def _classify_hand_with_matches_second_pass(five_card_hand):
    '''Second pass of classifications. hand is guaranteed to not have more
    than two of a kind'''
    num_pairs = 0
    for rank, rank_count in five_card_hand.rank_counts.items():
        if rank_count == 2:
            num_pairs += 1
    if num_pairs == 2:
        return TwoPair(five_card_hand)
    else:
        return OnePair(five_card_hand)
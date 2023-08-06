from cards import ranks, exceptions


def is_straight_ace_low_high(five_card_hand):
    """Returns true if the straight is valid under Ace Low-High rules."""
    return is_straight_ace_high(five_card_hand) or \
           is_straight_ace_low(five_card_hand)


def is_straight_ace_low(five_card_hand):
    """Returns true if the straight is valid under Ace Low rules."""
    return _is_straight_under_ordering(five_card_hand,
                                       ranks.ORDERED_RANKS_ACE_LOW)


def is_straight_ace_high(five_card_hand):
    """Returns true if the straight is valid under Ace High rules."""
    return _is_straight_under_ordering(five_card_hand,
                                       ranks.ORDERED_RANKS_ACE_HIGH)


def _is_straight_under_ordering(five_card_hand, ordering):
    hand_card_ranks = [card.rank for card in five_card_hand]
    lowest_rank = min(hand_card_ranks, key=lambda x: ordering.index(x))
    current_rank = lowest_rank
    try:
        for i in range(4):
            next_rank = ranks.next_larger_rank(current_rank, ordering)
            if next_rank not in hand_card_ranks:
                return False
            current_rank = next_rank
    except exceptions.NoHigherRankException:
        return False
    return True


def is_flush(five_card_hand):
    """Return true if the hand is a flush."""
    for suit, suit_count in five_card_hand.suit_counts.items():
        if suit_count == 5:
            return True
    return False
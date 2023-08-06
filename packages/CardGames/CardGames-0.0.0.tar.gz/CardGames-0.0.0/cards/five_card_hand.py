from collections import defaultdict

from cards import exceptions, ranks


class FiveCardHand(object):
    """General class for hands with five cards."""
    def __init__(self, cards):
        self._cards = list(cards)
        self._check_hand_size()
        self._count_suits_and_ranks()

    def _check_hand_size(self):
        if len(self._cards) < 5:
            raise exceptions.NotEnoughCardsException
        elif len(self._cards) > 5:
            raise exceptions.TooManyCardsException

    def _count_suits_and_ranks(self):
        self._suit_counts = defaultdict(int)
        self._rank_counts = defaultdict(int)
        for card in self._cards:
            self._suit_counts[card.suit] += 1
            self._rank_counts[card.rank] += 1

    def has_matches(self):
        """Return a boolean telling whether or not there are multiple cards of
        the same rank."""
        for rank, rank_count in self._rank_counts.items():
            if rank_count > 1:
                return True
        return False

    def get_cards_high_to_low(self, ordering=ranks.ORDERED_RANKS_ACE_HIGH):
        """Return cards from highest rank to lowest."""
        self._cards.sort(key=lambda x: ordering.index(x), reverse=True)
        return self._cards

    def same_strength(self, other):
        """Evaluates if two poker hands have the same strength."""
        return self.strength == other.strength

    @property
    def suit_counts(self):
        """Get suit counts."""
        return self._suit_counts

    @property
    def rank_counts(self):
        """Get rank counts."""
        return self._rank_counts

    @property
    def strength(self):
        """Get hand strength."""
        return self._strength

    def __repr__(self):
        return '{}:\n{}'.format(self.__class__.__name__,
               self.get_cards_as_string())

    def get_cards_as_string(self):
        """Return a string representing the five-card-hand."""
        return '' \
        '    {}\n' \
        '    {}\n' \
        '    {}\n' \
        '    {}\n' \
        '    {}\n'.format(*self.get_cards_high_to_low())

    def __iter__(self):
        for card in self._cards:
            yield card

    def __gt__(self, other):
        if self.strength == other.strength:
            raise exceptions.SamePokerHandClassException
        return self.strength > other.strength

    def __lt__(self, other):
        if self.strength == other.strength:
            raise exceptions.SamePokerHandClassException
        return self.strength < other.strength
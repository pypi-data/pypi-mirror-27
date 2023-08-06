import random

from . import playing_cards
from . import exceptions
from . import ranks
from . import suits


class Deck(object):
    """A collection of cards that can execute common actions, like drawing,
    inserting, and shuffling."""
    def __init__(self):
        self._cards = []

    def draw(self):
        """Draw the top card of the deck."""
        if self.num_cards <= 0:
            raise exceptions.NoCardsLeftException
        else:
            return self._cards.pop()

    def insert_to_top(self, card):
        """Insert a card at the top of the deck."""
        self._cards.append(card)

    def insert_to_bottom(self, card):
        """Insert a card at the bottom of the deck."""
        self._cards.insert(0, card)

    def shuffle(self):
        """Randomize order of the cards in the deck."""
        random.shuffle(self._cards)

    def remove(self, card_to_remove):
        """Removes the first card that it finds that matches the given
        criteria."""
        for index, card in enumerate(self._cards):
            if card == card_to_remove:
                return self._cards.pop(index)

    def remove_all(self, card_to_remove):
        """Remove all cards matching the given card, suit, or rank."""
        removed_cards = [card for card in self._cards
                         if card == card_to_remove]
        self._cards = [card for card in self._cards if card != card_to_remove]
        return removed_cards

    def __iter__(self):
        for card in self._cards:
            yield card

    def __len__(self):
        return self.num_cards

    @property
    def num_cards(self):
        """Return the number of cards in the deck."""
        return len(self._cards)


class StandardPlayingCardDeck(Deck):
    """A standard 52-card deck of French playing cards."""
    def __init__(self):
        super().__init__()
        for rank in ranks.get_all_ranks():
            for suit in suits.get_all_suits():
                card = playing_cards.StandardPlayingCard(rank, suit)
                self._cards.append(card)

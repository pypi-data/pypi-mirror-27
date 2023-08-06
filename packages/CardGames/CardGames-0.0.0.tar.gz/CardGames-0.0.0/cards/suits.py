DIAMOND = 'Diamond'
CLOVER = 'Clover'
HEART = 'Heart'
SPADE = 'Spade'
SUITS = [DIAMOND, CLOVER, HEART, SPADE]
SUIT_TO_SYMBOL = {
    SPADE: u'\u2664',
    DIAMOND: u'\u2662',
    CLOVER: u'\u2667',
    HEART: u'\u2661'
}

def get_all_suits():
    """Return all suits."""
    return SUITS[:]

def get_black_suits():
    """Return the black suits."""
    return [SPADE, CLOVER]

def get_red_suits():
    """Return the red suits."""
    return [HEART, DIAMOND]

def get_suit_symbol(suit):
    """Return the unicode symbol for the given suit."""
    return SUIT_TO_SYMBOL[suit]


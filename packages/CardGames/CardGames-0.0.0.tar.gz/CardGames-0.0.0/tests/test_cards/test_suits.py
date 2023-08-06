from cards import suits

SUITS = ['Diamond', 'Clover', 'Heart', 'Spade']

def test_get_all_suits():
    all_suits = suits.get_all_suits()
    assert len(all_suits) == 4
    for suit in SUITS:
        assert suit in all_suits


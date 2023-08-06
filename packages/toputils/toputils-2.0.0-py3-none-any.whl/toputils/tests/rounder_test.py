
from toputils.rounder import price_rounder

def test_rounder_no_rolls():
    assert price_rounder(1.9, 0) == 1.9


def test_rounder_plus_rolls():
    assert price_rounder(1.9, 5) == 1.85


def test_rounder_minus_rolls():
    assert price_rounder(1.9, -5) == 1.95

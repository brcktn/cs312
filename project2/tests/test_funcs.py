import pytest

from project2.convex_hull import is_ccw, cross_product


def test_is_ccw():
    assert is_ccw((1, 2), (3, 4), (2, 5))
    assert not is_ccw((1, 2), (3, 4), (3, 2))
    assert not is_ccw((0, 0), (1, 1), (1, 0))

    with pytest.raises(ValueError):
        is_ccw((1, 2), (3, 4), (1, 2))

    with pytest.raises(ValueError):
        is_ccw((1, 2), (5, 6), (3, 4))

    with pytest.raises(ValueError):
        is_ccw((1, 2), (3, 4), (5, 6))


def test_cross_product():
    assert cross_product((1, 2), (3, 4)) == -2
    assert cross_product((3, 4), (1, 2)) == 2
    assert cross_product((1, 2), (1, 2)) == 0
    assert cross_product((3, 0), (0, 2)) == 6



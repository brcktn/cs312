import pytest

from project2.convex_hull import (
    is_ccw,
    cross_product,
    compute_hull,
    split_points,
    keep_between_indecies,
)


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


def test_convex_hull_2_points():
    assert compute_hull([(1, 2), (3, 4)]) == [(1, 2), (3, 4)]
    assert compute_hull([(3, 4), (1, 2)]) == [(3, 4), (1, 2)]
    assert compute_hull([(1, 2), (1, 2)]) == [(1, 2), (1, 2)]


def test_convex_hull_3_points():
    assert sorted(compute_hull([(1, 2), (3, 4), (5, 5)])) == [(1, 2), (3, 4), (5, 5)]
    assert sorted(compute_hull([(1, 2), (5, 5), (3, 4)])) == [(1, 2), (3, 4), (5, 5)]


def test_split_points():
    points = [(1, 2), (3, 4), (5, 5), (2, 1), (4, 3)]
    left, right = split_points(points)
    assert left == [(1, 2), (2, 1)]
    assert right == [(3, 4), (4, 3), (5, 5)]


def test_keep_between_indecies():
    points = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
    assert keep_between_indecies(points, (0, 4)) == [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
    assert keep_between_indecies(points, (4, 0)) == [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0)]
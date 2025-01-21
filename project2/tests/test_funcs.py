from project2.convex_hull import (
    is_ccw,
    cross_product,
    compute_hull,
    split_points,
    keep_between_indecies,
    combine_hulls,
)
from project2.generate import generate_random_points
from test_utils import is_convex_hull


def test_is_ccw():
    assert is_ccw((1, 2), (3, 4), (2, 5))
    assert not is_ccw((1, 2), (3, 4), (3, 2))
    assert not is_ccw((0, 0), (1, 1), (1, 0))
    assert not is_ccw((1, 2), (3, 4), (1, 2))
    assert not is_ccw((1, 2), (5, 6), (3, 4))
    assert not is_ccw((1, 2), (3, 4), (5, 6))


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
    assert keep_between_indecies(points, (0, 4)) == [
        (1, 0),
        (1, 1),
        (0, 1),
        (-1, 1),
        (-1, 0),
    ]
    assert keep_between_indecies(points, (4, 0)) == [
        (-1, 0),
        (-1, -1),
        (0, -1),
        (1, -1),
        (1, 0),
    ]
    assert keep_between_indecies(points, (0, 0)) == [(1, 0)]


def test_combine_hulls():
    left = [(-1, 1), (-1, -1), (0, 0)]
    right = [(1, 1), (1, -1)]

    assert sorted(combine_hulls(left, right)) == [(-1, -1), (-1, 1), (1, -1), (1, 1)]


def test_guassian_distribution_medium():
    points = generate_random_points("uniform", 34, 312)
    candidate_hull = compute_hull(points)
    assert is_convex_hull(candidate_hull, points)

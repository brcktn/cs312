from alignment import NWMatrix
from math import inf

def test_create_matrix():
    matrix = NWMatrix("test1", "test2")
    reference = [[inf, inf, inf, inf, inf, inf],
                 [inf, inf, inf, inf, inf, inf],
                 [inf, inf, inf, inf, inf, inf],
                 [inf, inf, inf, inf, inf, inf],
                 [inf, inf, inf, inf, inf, inf],
                 [inf, inf, inf, inf, inf, inf]]
    assert matrix.get_matrix() == reference


def test_set_and_get():
    matrix = NWMatrix("test1", "a")
    matrix.set_value(2, 1, 1)

    assert matrix.get_matrix()[1][1] == 2


def test_is_match():
    matrix = NWMatrix("abc", "cba")

    assert matrix.is_match(2,2)
    assert not matrix.is_match(1,1)

def test_init_values():
    matrix = NWMatrix("abc", "cba")
    matrix.init_values(1)

    assert matrix.get_value(0, 3) == 3
    assert matrix.get_value(2, 0) == 2
from alignment import Matrix, BandedMatrix, align, align_banded
from math import inf


def test_create_matrix():
    matrix = Matrix("test1", "test2")
    reference = [
        [inf, inf, inf, inf, inf, inf],
        [inf, inf, inf, inf, inf, inf],
        [inf, inf, inf, inf, inf, inf],
        [inf, inf, inf, inf, inf, inf],
        [inf, inf, inf, inf, inf, inf],
        [inf, inf, inf, inf, inf, inf],
    ]
    assert matrix.get_matrix() == reference


def test_create_banded_matrix():
    matrix = BandedMatrix("test1", "test2", banded_width=1)
    reference = [
        [inf, inf, inf],
        [inf, inf, inf],
        [inf, inf, inf],
        [inf, inf, inf],
        [inf, inf, inf],
        [inf, inf, inf],
    ]
    assert matrix.get_matrix() == reference


def test_set_value_banded():
    matrix = BandedMatrix("test1", "test2", banded_width=1)
    matrix.set_value(1, 5, 5)
    matrix.set_value(2, 4, 4)
    matrix.set_value(3, 0, 1)
    matrix.set_value(4, 1, 1)

    reference = [
            [inf, inf, 3],
            [inf, 4, inf],
            [inf, inf, inf],
            [inf, inf, inf],
            [inf, 2, inf],
            [inf, 1, inf],
        ]
    assert matrix.get_matrix() == reference


def test_out_of_bounds_banded():
    matrix = BandedMatrix("test1", "test2", banded_width=1)
    matrix.set_value(1, 5, 0)
    matrix.set_value(1, 0, 5)

    reference = [
        [inf, inf, inf],
        [inf, inf, inf],
        [inf, inf, inf],
        [inf, inf, inf],
        [inf, inf, inf],
        [inf, inf, inf],
    ]
    assert matrix.get_matrix() == reference


def test_set_and_get():
    matrix = Matrix("test1", "a")
    matrix.set_value(2, 1, 1)

    assert matrix.get_matrix()[1][1] == 2


def test_set_banded():
    matrix = BandedMatrix("test1", "a", banded_width=1)
    matrix.set_value(2, 1, 1)

    assert matrix.get_matrix()[1][1] == 2


def test_get_out_of_bounds():
    matrix = Matrix("test1", "a")
    matrix.set_value(2, 1, 1)
    matrix.set_value(3, 1, 1)
    matrix.set_value(4, 1, 1)
    matrix.set_value(5, 1, 1)

    assert matrix.get_value(5,1) == inf


def test_is_match():
    matrix = Matrix("abc", "cba")

    assert matrix.is_match(2, 2)
    assert not matrix.is_match(1, 1)


def test_is_match_banded():
    matrix = BandedMatrix("abc", "cba", banded_width=3)

    assert matrix.is_match(2, 2)
    assert not matrix.is_match(1, 1)


def test_init_values():
    matrix = Matrix("abc", "cba")
    matrix.init_values(1)

    assert matrix.get_value(0, 3) == 3
    assert matrix.get_value(2, 0) == 2


def test_init_values_banded():
    matrix = BandedMatrix("abcde", "edcba", banded_width=2)
    matrix.init_values(1)
    reference = [
        [inf, inf, 0, 1, 2],
        [inf, 1, inf, inf, inf],
        [2, inf, inf, inf, inf],
        [inf, inf, inf, inf, inf],
        [inf, inf, inf, inf, inf],
        [inf, inf, inf, inf, inf],
    ]

    assert matrix.get_matrix() == reference


def test_small_alignment_cost():
    assert align("AGTCGA", "ATCGT")[0] == -6


def test_small_alignment_banded_cost():
    assert align_banded("AGTCG", "ATCGT", banded_width=3)[0] == -2


def test_small_alignment():
    score, aseq1, aseq2 = align("AGTCGA", "ATCGT")
    assert score == -6
    assert aseq1 == "AGTCGA"
    assert aseq2 == "A-TCGT"


def test_small_alignment_banded():
    score, aseq1, aseq2 = align_banded("AGTCG", "ATCGT", banded_width=3)
    assert score == -2
    assert aseq1 == "AGTCG-"
    assert aseq2 == "A-TCGT"


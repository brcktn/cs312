from math import inf


def align(
    seq1: str,
    seq2: str,
    match_award=-3,
    indel_penalty=5,
    sub_penalty=1,
    banded_width=-1,
    gap="-",
) -> tuple[float, str | None, str | None]:
    """
    Align seq1 against seq2 using Needleman-Wunsch
    Put seq1 on left (j) and seq2 on top (i)
    => matrix[i][j]

    :param seq1: the first sequence to align; should be on the "left" of the matrix
    :param seq2: the second sequence to align; should be on the "top" of the matrix
    :param match_award: how many points to award a match
    :param indel_penalty: how many points to award a gap in either sequence
    :param sub_penalty: how many points to award a substitution
    :param banded_width: banded_width * 2 + 1 is the width of the banded alignment; -1 indicates full alignment
    :param gap: the character to use to represent gaps in the alignment strings
    :return: alignment cost, alignment 1, alignment 2

    Time complexity: O(n*m) for unrestricted, O(n*k) for banded
    Space complexity: O(n*m) for unrestricted, O(n*k) for banded
    where n is the length of seq1, m is the length of seq2, and k is the banded width
    """
    if banded_width == -1:
        return align_unrestricted(
            seq1, seq2, match_award, indel_penalty, sub_penalty, gap
        )
    else:
        return align_banded(
            seq1, seq2, match_award, indel_penalty, sub_penalty, banded_width, gap
        )


def align_unrestricted(
    seq1: str, seq2: str, match_award, indel_penalty, sub_penalty, gap
) -> tuple[float, str | None, str | None]:
    """
    Unrestricted verion of Needleman-Wunsch, i.g. banded_width = -1

    :param seq1: the first sequence to align; should be on the "left" of the matrix
    :param seq2: the second sequence to align; should be on the "top" of the matrix
    :param match_award: how many points to award a match
    :param indel_penalty: how many points to award a gap in either sequence
    :param sub_penalty: how many points to award a substitution
    :param gap: the character to use to represent gaps in the alignment strings
    :return: alignment cost, alignment 1, alignment 2

    Time complexity: O(n*m)
    Space complexity: O(n*m)
    """
    matrix = Matrix(seq1, seq2) #O(n*m)
    matrix.init_values(indel_penalty) #O(n+m)
    for row in range(1, len(seq1) + 1): # runs n times: O(n*m)
        for column in range(1, len(seq2) + 1): # runs m times: O(m)
            insert_score = matrix.get_value(row - 1, column) + indel_penalty
            delete_score = matrix.get_value(row, column - 1) + indel_penalty
            if matrix.is_match(row, column):
                sub_match_score = matrix.get_value(row - 1, column - 1) + match_award
            else:
                sub_match_score = matrix.get_value(row - 1, column - 1) + sub_penalty

            min_cost = min(insert_score, delete_score, sub_match_score)
            matrix.set_value(min_cost, row, column)

    alignment1 = ""
    alignment2 = ""
    i = len(seq1)
    j = len(seq2)

    while i > 0 or j > 0: # runs at most n+m times: O(n+m)
        if (
            matrix.get_value(i, j) == matrix.get_value(i - 1, j - 1) + match_award
            and matrix.is_match(i, j)
        ) or matrix.get_value(i, j) == matrix.get_value(i - 1, j - 1) + sub_penalty:
            # if match or substitution
            alignment1 = matrix.seq1[i] + alignment1
            alignment2 = matrix.seq2[j] + alignment2
            i -= 1
            j -= 1
        elif matrix.get_value(i, j) == matrix.get_value(i, j - 1) + indel_penalty:
            # if insertion
            alignment1 = gap + alignment1
            alignment2 = matrix.seq2[j] + alignment2
            j -= 1
        elif matrix.get_value(i, j) == matrix.get_value(i - 1, j) + indel_penalty:
            # if deletion
            alignment1 = matrix.seq1[i] + alignment1
            alignment2 = gap + alignment2
            i -= 1
        else:
            raise Exception("Error in traceback")

    return matrix.get_value(len(seq1), len(seq2)), alignment1, alignment2


def align_banded(
    seq1: str,
    seq2: str,
    match_award=-3,
    indel_penalty=5,
    sub_penalty=1,
    banded_width=-1,
    gap="-",
) -> tuple[float, str | None, str | None]:
    """
    Banded version of Needleman-Wunsch

    :param seq1: the first sequence to align; should be on the "left" of the matrix
    :param seq2: the second sequence to align; should be on the "top" of the matrix
    :param match_award: how many points to award a match
    :param indel_penalty: how many points to award a gap in either sequence
    :param sub_penalty: how many points to award a substitution
    :param banded_width: banded_width * 2 + 1 is the width of the banded alignment
    :param gap: the character to use to represent gaps in the alignment strings
    :return: alignment cost, alignment 1, alignment 2

    Time complexity: O(n*d)
    Space complexity: O(n*d)
    """
    matrix = BandedMatrix(seq1, seq2, banded_width) #O(n*k)
    matrix.init_values(indel_penalty) #O(k)
    for row in range(1, len(seq1) + 1): # runs n times: O(n*k)
        for column in range(row - banded_width, row + banded_width + 1): # runs 2*k times: O(k)
            insert_score = matrix.get_value(row - 1, column) + indel_penalty
            delete_score = matrix.get_value(row, column - 1) + indel_penalty
            if matrix.is_match(row, column):
                sub_match_score = matrix.get_value(row - 1, column - 1) + match_award
            else:   
                sub_match_score = matrix.get_value(row - 1, column - 1) + sub_penalty

            min_cost = min(insert_score, delete_score, sub_match_score)
            matrix.set_value(min_cost, row, column)

    alignment1 = ""
    alignment2 = ""
    i = len(seq1)
    j = len(seq2)
    while i > 0 or j > 0: # runs at most n+m times: O(n+m)
        if (
            matrix.get_value(i, j) == matrix.get_value(i - 1, j - 1) + match_award
            and matrix.is_match(i, j)
        ) or matrix.get_value(i, j) == matrix.get_value(i - 1, j - 1) + sub_penalty:
            alignment1 = matrix.seq1[i] + alignment1
            alignment2 = matrix.seq2[j] + alignment2
            i -= 1
            j -= 1
        elif matrix.get_value(i, j) == matrix.get_value(i, j - 1) + indel_penalty:
            alignment1 = gap + alignment1
            alignment2 = matrix.seq2[j] + alignment2
            j -= 1
        elif matrix.get_value(i, j) == matrix.get_value(i - 1, j) + indel_penalty:
            alignment1 = matrix.seq1[i] + alignment1
            alignment2 = gap + alignment2
            i -= 1
        else:
            raise Exception("Error in traceback")

    return matrix.get_value(len(seq1), len(seq2)), alignment1, alignment2


class Matrix:
    def __init__(self, seq1: str, seq2: str):
        """
        Initialize the matrix with the sequences

        Time complexity: O(n*m)
        Space complexity: O(n*m)
        """
        self.seq1 = " " + seq1
        self.seq2 = " " + seq2
        self.matrix = [
            [inf for _ in range(len(self.seq2))] for _ in range(len(self.seq1))
        ]

    def get_matrix(self):
        """
        returns the matrix

        Time complexity: O(1)
        """
        return self.matrix

    def set_value(self, input: int, index1: int, index2: int):
        """
        sets the value of the matrix at the given indicies

        Time complexity: O(1)
        """
        self.matrix[index1][index2] = input

    def get_value(self, index1: int, index2: int):
        """
        returns the value from the matrix where index1 is the row
        (left side index), and index2 is the column (top side index)

        Time complexity: O(1)
        """
        return self.matrix[index1][index2]

    def is_match(self, index1: int, index2: int):
        """
        returns True if the seq1 and seq 2 have the same value
        at the given indicies

        Time complexity: O(1)
        """
        return self.seq1[index1] == self.seq2[index2]

    def init_values(self, indel_penalty: int):
        """
        initializes the values on the left and top of the matrix

        Time complexity: O(n+m)
        """
        self.set_value(0, 0, 0)
        for i in range(1, len(self.seq1)):
            self.set_value(i * indel_penalty, i, 0)
        for i in range(1, len(self.seq2)):
            self.set_value(i * indel_penalty, 0, i)


class BandedMatrix:
    def __init__(self, seq1: str, seq2: str, banded_width: int):
        """
        Initialize the banded matrix with the sequences and banded width

        Time complexity: O(n*d)
        Space complexity: O(n*d)
        """
        self.seq1 = " " + seq1
        self.seq2 = " " + seq2
        self.banded_width = banded_width
        self.matrix = [
            [inf for _ in range(2 * self.banded_width + 1)] for _ in range(len(self.seq1))
        ]

    def get_matrix(self):
        """
        returns the matrix

        Time complexity: O(1)
        """
        return self.matrix
    
    def set_value(self, input: int, index1: int, index2: int):
        """
        sets the value of the matrix at the given indicies

        Time complexity: O(1)
        """
        if not (-self.banded_width <= index2 - index1 <= self.banded_width):
            return
        if index2-index1+self.banded_width >= 2 * self.banded_width + 1:
            return
        self.matrix[index1][index2-index1+self.banded_width] = input

    def get_value(self, index1: int, index2: int):
        """
        returns the value from the matrix where index1 is the row
        (left side index), and index2 is the column (top side index)

        Time complexity: O(1)
        """
        if not (-self.banded_width <= index2 - index1 <= self.banded_width):
            return inf
        if index2-index1+self.banded_width >= 2 * self.banded_width + 1:
            return inf
        return self.matrix[index1][index2-index1+self.banded_width]
    
    def is_match(self, index1: int, index2: int):
        """
        returns True if the seq1 and seq 2 have the same value
        at the given indicies

        Time complexity: O(1)
        """
        if index1 >= len(self.seq1) or index2 >= len(self.seq2):
            return False
        return self.seq1[index1] == self.seq2[index2]
    
    def init_values(self, indel_penalty: int):
        """
        initializes the values on the left and top of the matrix
        
        Time complexity: O(d)
        """
        self.set_value(0, 0, 0)
        for i in range(1, self.banded_width + 1):
            self.set_value(i * indel_penalty, i, 0)
        for i in range(1, self.banded_width + 1):
            self.set_value(i * indel_penalty, 0, i)

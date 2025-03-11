from math import inf

def align(
        seq1: str,
        seq2: str,
        match_award=-3,
        indel_penalty=5,
        sub_penalty=1,
        banded_width=-1,
        gap='-'
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
    """
    matrix = NWMatrix(seq1, seq2)
    matrix.init_values(sub_penalty)
    for i in range(1, len(seq2)):
        for j in range(1, len(seq1)):
            pass


class NWMatrix:
    def __init__(self, seq1: str, seq2: str):
        self.seq1 = " " + seq1
        self.seq2 = " " + seq2
        self.matrix = [[inf for _ in range(len(self.seq2))] for _ in range(len(self.seq1))]

    def get_matrix(self):
        return self.matrix
    
    def set_value(self, input: int, index1: int, index2: int):
        self.matrix[index1][index2] = input
    
    def get_value(self, index1: int, index2: int):
        """
        returns the value from the matrix where index1 is the row
        (left side index), and index2 is the column (top side index)
        """
        return self.matrix[index1][index2]
    
    def is_match(self, index1: int, index2: int):
        """
        returns True if the seq1 and seq 2 have the same value
        at the given indicies
        """
        return self.seq1[index1] == self.seq2[index2]
    
    def init_values(self, sub_penalty: int):
        for i in range(1, len(self.seq1)):
            self.set_value(i * sub_penalty, i, 0)
        for i in range(1, len(self.seq2)):
            self.set_value(i * sub_penalty, 0, i)

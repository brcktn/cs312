import math

class Solution(object):
    def numSquares(self, n):
        """
        :type n: int
        :rtype: int
        """
        squares = []
        i = 1
        while True:
            j = i**2
            if j > n:
                break
            squares.append(j)
            i += 1

        array = [100 for i in range(n+1)]
        array[0] = 0

        for i in range(len(array)):
            for square in squares:
                if square > i:
                    break
                array[i] = min(array[i], array[i-square] + 1)

        return array[-1]
    

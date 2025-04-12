class Solution(object):
    def numSquares(self, n):
        """
        :type n: int
        :rtype: int
        """
        squares = [i**2 for i in range(1, int(n**0.5) + 1)]

        array = [100 for i in range(n+1)]
        array[0] = 0

        for i in range(len(array)):
            for square in squares:
                if square > i:
                    break
                array[i] = min(array[i], array[i-square] + 1)

        return array[-1]
    

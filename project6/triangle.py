class Solution(object):
    def minimumTotal(self, triangle):
        """
        :type triangle: List[List[int]]
        :rtype: int
        """
        cost_triangle = [[triangle[0][0]]]
        for row in triangle[1:]:
            cost_triangle.append([])
            for i in range(len(row)):
                if i == 0:
                    a = cost_triangle[-1]
                    b = cost_triangle[-2][0]
                    c = row[0]
                    cost_triangle[-1].append(cost_triangle[-2][0] + row[0])
                elif i == len(row) - 1:
                    cost_triangle[-1].append(cost_triangle[-2][-1] + row[-1])
                else:
                    cost_triangle[-1].append(min(cost_triangle[-2][i-1], cost_triangle[-2][i]) + row[i])

        return min(cost_triangle[-1])
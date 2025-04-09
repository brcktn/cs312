from heapq import heappush, heappop

class Solution(object):
    def minCostConnectPoints(self, points):
        """
        :type points: List[List[int]]
        :rtype: int
        """

        heap = []
        visited = {0}
        total = 0

        for i in range(1, len(points)):
            heappush(heap, (self.dist(points[0], points[i]), (0, i)))

        while len(visited) < len(points):
            cost, (point1, point2) = heappop(heap)
            if point2 in visited:
                continue
            visited.add(point2)
            total += cost
            for i in range(len(points)):
                if i not in visited:
                    heappush(heap, (self.dist(points[point2], points[i]), (point2, i)))

        return total


    def dist(self, point1, point2):
        return abs(point1[0]-point2[0]) + abs(point1[1]-point2[1])
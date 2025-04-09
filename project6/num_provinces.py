class Solution(object):
    def findCircleNum(self, isConnected):
        """
        :type isConnected: List[List[int]]
        :rtype: int
        """
        visited = set()
        provinces = 0
        for node in range(len(isConnected)):
            if node not in visited:
                provinces += 1
                self.dfs(isConnected, visited, node)

        return provinces

    def dfs(self, graph, visited, node):
        visited.add(node)
        for i in range(len(graph[node])):
            if i not in visited and graph[node][i]:
                self.dfs(graph, visited, i)
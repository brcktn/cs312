class Solution(object):
    def canFinish(self, numCourses, prerequisites):
        """
        :type numCourses: int
        :type prerequisites: List[List[int]]
        :rtype: bool
        """
        graph = self.make_graph(prerequisites, numCourses)
        path = set()
        visited = set()
        for i in range(numCourses):
            if self.dfs(graph, visited, path, i):
                return False
        return True
    
    def make_graph(self, prereqs, numCourses):
        graph = {i:set() for i in range(numCourses)}
        for prereq in prereqs:
            graph[prereq[0]].add(prereq[1])
        return graph


    def dfs(self, graph, visited, path, node):
        if node in path:
            return True
        if node in visited:
            return False

        path.add(node)
        for i in graph[node]:  # loop over indices
            if self.dfs(graph, visited, path, i):
                return True
        path.remove(node)
        visited.add(node)
        return False
                
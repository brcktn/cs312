from math import inf


def find_shortest_path_with_heap(
    graph: dict[int, dict[int, float]], source: int, target: int
) -> tuple[list[int], float]:
    """
    Find the shortest (least-cost) path from `source` to `target` in `graph`
    using the heap-based algorithm.

    Return:
        - the list of nodes (including `source` and `target`)
        - the cost of the path

    Time complexity: O((V + E) log V)
    Space complexity: O(V)
    """
    dist, prev = dijkstra(graph, source, HeapPriorityQueue)  # O((V + E) log V)
    path = []
    while target is not None:  # O(V)
        path.insert(0, target)
        target = prev[target]
    return path, dist[path[-1]]


def find_shortest_path_with_array(
    graph: dict[int, dict[int, float]], source: int, target: int
) -> tuple[list[int], float]:
    """
    Find the shortest (least-cost) path from `source` to `target` in `graph`
    using the array-based (linear lookup) algorithm.

    Return:
        - the list of nodes (including `source` and `target`)
        - the cost of the path

    Time complexity: O(V^2)
    Space complexity: O(V)
    """
    dist, prev = dijkstra(graph, source, ListPriorityQueue)  # O(V^2)
    path = []
    while target is not None:  # O(V)
        path.insert(0, target)
        target = prev[target]
    return path, dist[path[-1]]


def dijkstra(
    graph: dict[int, dict[int, float]], source: int, priority_queue: type
) -> tuple[dict[int, float], dict[int, int]]:
    """
    Find the shortest (least-cost) path from `source` to all other nodes in `graph`.

    Return:
        - the dictionary of distances from `source` to each node
        - the dictionary of previous nodes on the shortest path from `source` to each node

    Complexities notated in for [ list / heap priority queue ] for V vertices and E edges:

    Time complexity: O(V^2) / O((V + E) log V)
    Space complexity: O(V) / O(V)
    """
    pq = priority_queue()

    # Initialize the distance and previous node dictionaries
    # O(V) / O(V log V)
    dist = {vertex: inf for vertex in graph}  # O(V)
    prev = {vertex: None for vertex in graph}  # O(V)
    dist[source] = 0  # O(1)
    for vertex in graph:
        pq.push(vertex, dist[vertex])  # O(1) / O(log V)

    visited = set()

    # loop breaks when all vertices are visited
    # runs V times in total
    while not pq.is_empty():
        vertex, current_dist = pq.pop()  # O(V) / O(log V)
        visited.add(vertex)  # O(1)

        for neighbor in graph[vertex]:  # inner loop runs E times in total
            if neighbor not in visited and neighbor in graph[vertex]:  # O(log V)
                new_dist = current_dist + graph[vertex][neighbor]  # O(1)
                if new_dist < dist[neighbor]:  # O(1)
                    dist[neighbor] = new_dist  # O(1)
                    prev[neighbor] = vertex  # O(1)
                    pq.decrease_key(neighbor, new_dist)  # O(1) / O(log V)

        if len(visited) == len(graph):
            break

    return dist, prev


class ListPriorityQueue:
    def __init__(self):
        self.queue = []

    def push(self, node, priority):
        """
        Add a new element to the queue.

        Time complexity: O(1)
        Space complexity: O(1)
        """
        self.queue.append((node, priority))  # O(1)

    def pop(self):
        """
        Remove and return the element with the minimum priority from the queue.

        Time complexity: O(n)
        Space complexity: O(1)
        """
        if self.is_empty():
            return None
        min_index = 0
        for i in range(1, len(self.queue)):
            if self.queue[i][1] < self.queue[min_index][1]:
                min_index = i
        return self.queue.pop(min_index)

    def decrease_key(self, node, new_priority):
        """
        Decrease the priority of the given node.

        Time complexity: O(n)
        Space complexity: O(1)
        """
        # if new_priority >= self.queue[0][1]:  # O(1)
        #     raise ValueError(f"New priority is not less than the current priority.\n{self.queue}\n{node}, {new_priority}")

        for i in range(len(self.queue)):  # runs max n times
            if self.queue[i][0] == node:  # O(1)
                self.queue[i] = (node, new_priority)  # O(1)
                break

    def is_empty(self):
        """
        Returns True if the queue is empty, False otherwise.

        Time complexity: O(1)
        Space complexity: O(1)
        """
        return len(self.queue) == 0


class HeapPriorityQueue:
    def __init__(self):
        self.queue = []

    def push(self, node, priority):
        """
        Add a new element to the heap.

        Time complexity: O(log n)
        Space complexity: O(1)
        """
        index = len(self.queue)
        self.queue.append((node, priority))
        while index > 0:
            if self.queue[index][1] < self.queue[(index - 1) // 2][1]:
                self.queue[index], self.queue[(index - 1) // 2] = (
                    self.queue[(index - 1) // 2],
                    self.queue[index],
                )
                index = (index - 1) // 2
            else:
                break

    def pop(self):
        """
        Remove and return the top element from the heap.

        Return:
            - The top element of the heap.

        Time complexity: O(log n) (amortized)
        Space complexity: O(1)
        """

        if self.is_empty():
            return None
        top = self.queue[0]
        self.queue[0] = self.queue[-1]
        self.queue.pop()
        self.heap_down(0)  # O(log n)
        return top

    def heap_down(self, index):
        """
        Heapify the heap from the given index.

        Time complexity: O(log n)
        Space complexity: O(1)
        """
        # calculate children indices, O(1)
        left = 2 * index + 1
        right = 2 * index + 2
        smallest = index

        # compare to left child, O(1)
        if left < len(self.queue) and self.queue[left][1] < self.queue[smallest][1]:
            smallest = left
        # compare to right child, O(1)
        if right < len(self.queue) and self.queue[right][1] < self.queue[smallest][1]:
            smallest = right

        # swap if necessary, O(1) + O(heap_down) = O(log n)
        if smallest != index:
            self.queue[index], self.queue[smallest] = (
                self.queue[smallest],
                self.queue[index],
            )
            self.heap_down(smallest)

    def decrease_key(self, node, new_priority):
        """
        Decrease the priority of the given node.

        Time complexity: O(n)
        """
        for i in range(len(self.queue)):
            if self.queue[i][0] == node:
                if new_priority >= self.queue[i][1]:
                    raise ValueError(
                        "New priority is not less than the current priority."
                    )
                self.queue[i] = (node, new_priority)
                while i > 0:
                    if self.queue[i][1] < self.queue[(i - 1) // 2][1]:
                        self.queue[i], self.queue[(i - 1) // 2] = (
                            self.queue[(i - 1) // 2],
                            self.queue[i],
                        )
                        i = (i - 1) // 2
                    else:
                        break


    def is_empty(self):
        """
        Returns True if the queue is empty, False otherwise.

        Time complexity: O(1)
        Space complexity: O(1)
        """
        return len(self.queue) == 0

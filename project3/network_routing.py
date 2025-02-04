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
    """


def find_shortest_path_with_array(
    graph: dict[int, dict[int, float]], source: int, target: int
) -> tuple[list[int], float]:
    """
    Find the shortest (least-cost) path from `source` to `target` in `graph`
    using the array-based (linear lookup) algorithm.

    Return:
        - the list of nodes (including `source` and `target`)
        - the cost of the path
    """


def dijkstra(
    graph: dict[int, dict[int, float]], source: int
) -> tuple[list[int], float]:
    """"
    Find the shortest (least-cost) path from `source` to all other nodes in `graph`.

    Return:
        - the list of nodes (including `source`) in the order of traversal
        - the cost of the path to each node
    """


class ListPriorityQueue:
    def __init__(self):
        self.queue = []

    def push(self, node, priority):
        self.queue.append((node, priority))
        self.queue.sort(key=lambda x: x[1])

    def pop(self):
        return self.queue.pop(0)

    def is_empty(self):
        return len(self.queue) == 0

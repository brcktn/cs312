from network_routing import ListPriorityQueue, HeapPriorityQueue, dijkstra
from math import inf


def test_list_push_ordered():
    pq = ListPriorityQueue()
    pq.push(1, 1)
    pq.push(2, 2)
    pq.push(3, 3)
    pq.push(4, 4)
    pq.push(5, 5)
    assert pq.queue == [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]


def test_list_push_unordered():
    pq = ListPriorityQueue()
    pq.push(5, 5)
    pq.push(3, 3)
    pq.push(1, 1)
    pq.push(4, 4)
    pq.push(2, 2)
    assert pq.queue == [(5, 5), (3, 3), (1, 1), (4, 4), (2, 2)]


def test_list_pop():
    pq = ListPriorityQueue()
    pq.push(5, 5)
    pq.push(3, 3)
    pq.push(1, 1)
    pq.push(4, 4)
    pq.push(2, 2)
    assert pq.pop() == (1, 1)
    assert pq.pop() == (2, 2)
    assert pq.pop() == (3, 3)
    assert pq.pop() == (4, 4)
    assert pq.pop() == (5, 5)


def test_list_pop_with_inf():
    pq = ListPriorityQueue()
    pq.push(5, 5)
    pq.push(3, 3)
    pq.push(1, 1)
    pq.push(4, 4)
    pq.push(2, 2)
    pq.push(6, inf)
    assert pq.pop() == (1, 1)
    assert pq.pop() == (2, 2)
    assert pq.pop() == (3, 3)
    assert pq.pop() == (4, 4)
    assert pq.pop() == (5, 5)
    assert pq.pop() == (6, inf)


def test_list_is_empty():
    pq = ListPriorityQueue()
    assert pq.is_empty()
    pq.push(5, 5)
    assert not pq.is_empty()


def test_list_decrease_key():
    pq = ListPriorityQueue()
    pq.push(1, 10)
    pq.push(2, 9)
    pq.push(3, 8)
    pq.push(4, 7)
    pq.push(5, 6)
    
    pq.decrease_key(5, 1)
    pq.decrease_key(4, 2)
    pq.decrease_key(3, 3)
    pq.decrease_key(2, 4)
    pq.decrease_key(1, 5)

    assert pq.pop() == (5, 1)
    assert pq.pop() == (4, 2)
    assert pq.pop() == (3, 3)
    assert pq.pop() == (2, 4)
    assert pq.pop() == (1, 5)


def test_list_decrease_key_reverse():
    pq = ListPriorityQueue()
    pq.push(1, 10)
    pq.push(2, 9)
    pq.push(3, 8)
    pq.push(4, 7)
    pq.push(5, 6)
    
    pq.decrease_key(5, 5)
    pq.decrease_key(4, 4)
    pq.decrease_key(3, 3)
    pq.decrease_key(2, 2)
    pq.decrease_key(1, 1)

    assert pq.pop() == (1, 1)
    assert pq.pop() == (2, 2)
    assert pq.pop() == (3, 3)
    assert pq.pop() == (4, 4)
    assert pq.pop() == (5, 5)


def test_heap_push_ordered():
    pq = HeapPriorityQueue()
    pq.push(1, 1)
    pq.push(2, 2)
    pq.push(3, 3)
    pq.push(4, 4)
    pq.push(5, 5)
    assert pq.queue == [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]


def test_heap_push_unordered():
    pq = HeapPriorityQueue()
    pq.push(5, 5)
    pq.push(3, 3)
    pq.push(1, 1)
    pq.push(4, 4)
    pq.push(2, 2)
    assert pq.queue[0] == (1, 1)


def test_heap_push_with_inf():
    pq = HeapPriorityQueue()
    pq.push(5, 5)
    pq.push(3, 3)
    pq.push(1, 1)
    pq.push(4, 4)
    pq.push(2, 2)
    pq.push(6, inf)
    assert pq.queue[0] == (1, 1)


def test_heap_pop():
    pq = HeapPriorityQueue()
    pq.push(5, 5)
    pq.push(3, 3)
    pq.push(1, 1)
    pq.push(4, 4)
    pq.push(2, 2)
    assert pq.pop() == (1, 1)
    assert pq.pop() == (2, 2)
    assert pq.pop() == (3, 3)
    assert pq.pop() == (4, 4)
    assert pq.pop() == (5, 5)


def test_heap_pop_with_duplicates():
    pq = HeapPriorityQueue()
    pq.push(1,1)
    pq.push(2,1)
    pq.push(3,1)
    pq.push(4,1)
    pq.push(5,1)
    pq.push(6,1)
    pq.push(7,1)

    assert pq.queue == [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]

    assert pq.pop() == (1, 1)
    assert pq.pop() == (7, 1)
    assert pq.pop() == (6, 1)
    assert pq.pop() == (5, 1)
    assert pq.pop() == (4, 1)
    assert pq.pop() == (3, 1)
    assert pq.pop() == (2, 1)


def test_heap_is_empty():
    pq = HeapPriorityQueue()
    assert pq.is_empty()
    pq.push(5, 5)
    assert not pq.is_empty()


def test_heap_decrease_key():
    pq = ListPriorityQueue()
    pq.push(2, 2)
    pq.push(3, 3)
    pq.push(4, 4)
    pq.push(5, 5)
    pq.push(6, 6)
    pq.push(7, 7)
    pq.push(8, 8)

    pq.decrease_key(8, 1)

    assert pq.pop() == (8, 1)


def test_heap_decrease_key_reverse():
    pq = ListPriorityQueue()
    pq.push(1, 10)
    pq.push(2, 9)
    pq.push(3, 8)
    pq.push(4, 7)
    pq.push(5, 6)
    
    pq.decrease_key(5, 5)
    pq.decrease_key(4, 4)
    pq.decrease_key(3, 3)
    pq.decrease_key(2, 2)
    pq.decrease_key(1, 1)

    assert pq.pop() == (1, 1)
    assert pq.pop() == (2, 2)
    assert pq.pop() == (3, 3)
    assert pq.pop() == (4, 4)
    assert pq.pop() == (5, 5)


def test_dijkstra_tiny():
    input_graph = {
        1: {2: 1},
        2: {1: 1, 3: 1},
        3: {},
    }

    dist, prev = dijkstra(input_graph, 1, ListPriorityQueue)
    assert dist == {1: 0, 2: 1, 3: 2}
    assert prev == {1: None, 2: 1, 3: 2}


def test_dijkstra_small():
    input_graph = {
        1: {2: 1, 3: 4},
        2: {3: 2, 4: 5},
        3: {4: 1},
        4: {},
    }

    # dist, prev = dijkstra(input_graph, 1, ListPriorityQueue)
    # assert dist == {1: 0, 2: 1, 3: 3, 4: 4}
    # assert prev == {1: None, 2: 1, 3: 2, 4: 3}

    dist, prev = dijkstra(input_graph, 1, HeapPriorityQueue)
    assert dist == {1: 0, 2: 1, 3: 3, 4: 4}
    assert prev == {1: None, 2: 1, 3: 2, 4: 3}



def test_dijkstra_large():
    input_graph = {
        1: {2: 10, 3: 5, 4: 3, 7: 2},
        2: {5: 1, 6: 4},
        3: {2: 2, 4: 2, 5: 2},
        4: {6: 8},
        5: {7: 3},
        6: {7: 1},
        7: {},
    }

    dist, prev = dijkstra(input_graph, 1, ListPriorityQueue)
    assert dist == {1: 0, 2: 7, 3: 5, 4: 3, 5: 7, 6: 11, 7: 2}
    assert prev == {1: None, 2: 3, 3: 1, 4: 1, 5: 3, 6: 4, 7: 1}

    dist, prev = dijkstra(input_graph, 1, HeapPriorityQueue)
    assert dist == {1: 0, 2: 7, 3: 5, 4: 3, 5: 7, 6: 11, 7: 2}
    assert prev == {1: None, 2: 3, 3: 1, 4: 1, 5: 3, 6: 4, 7: 1}

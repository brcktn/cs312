import math
import random

from tsp_core import Tour, SolutionStats, Timer, score_tour, Solver, generate_network
from tsp_cuttree import CutTree
from math import inf
import heapq

def random_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))

    while True:
        if timer.time_out():
            return stats

        tour = random.sample(list(range(len(edges))), len(edges))
        n_nodes_expanded += 1

        cost = score_tour(tour, edges)
        if math.isinf(cost):
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        if stats and cost > stats[-1].score:
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        stats.append(SolutionStats(
            tour=tour,
            score=cost,
            time=timer.time(),
            max_queue_size=1,
            n_nodes_expanded=n_nodes_expanded,
            n_nodes_pruned=n_nodes_pruned,
            n_leaves_covered=cut_tree.n_leaves_cut(),
            fraction_leaves_covered=cut_tree.fraction_leaves_covered()
        ))

    if not stats:
        return [SolutionStats(
            [],
            math.inf,
            timer.time(),
            1,
            n_nodes_expanded,
            n_nodes_pruned,
            cut_tree.n_leaves_cut(),
            cut_tree.fraction_leaves_covered()
        )]


def greedy_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))

    best_tour = None
    best_score = inf
    
    tour = [0]


    while not timer.time_out() and tour[0] < len(edges) - 1:
        if len(tour) == len(edges): # find return path when tour is complete
            if edges[tour[-1]][tour[0]] == inf:
                tour = [tour[0] + 1] # reset tour
                continue
            else: 
                n_nodes_expanded += 1
                cost = score_tour(tour, edges)
                if cost < best_score:
                    best_score = cost
                    best_tour = tour[:]
                    stats.append(SolutionStats(
                        tour=best_tour,
                        score=best_score,
                        time=timer.time(),
                        max_queue_size=1,
                        n_nodes_expanded=n_nodes_expanded,
                        n_nodes_pruned=n_nodes_pruned,
                        n_leaves_covered=cut_tree.n_leaves_cut(),
                        fraction_leaves_covered=cut_tree.fraction_leaves_covered()
                    ))
                tour = [tour[0] + 1] # reset tour
                continue
        # find the next node to visit
        n_nodes_expanded += 1
        next_node = min(
            (i for i in range(len(edges)) if i not in tour),  # Only consider unvisited nodes
            key=lambda i: edges[tour[-1]][i],
            default=None  # Handle the case where no valid nodes are found
        )

        if next_node is None or edges[tour[-1]][next_node] == inf:
            # No valid next node found
            tour = [tour[0] + 1]  # Reset tour
        else:
            # Append the next node to the tour
            if next_node in tour:
                print(edges)
                print(tour)
                raise ValueError("Tour contains duplicate nodes")
            tour.append(next_node)

    if not stats:
        stats.append(SolutionStats(
            [],
            math.inf,
            timer.time(),
            1,
            n_nodes_expanded,
            n_nodes_pruned,
            cut_tree.n_leaves_cut(),
            cut_tree.fraction_leaves_covered()
        ))

    for stat in stats:
        if stat.score != score_tour(stat.tour, edges):
            raise ValueError("Tour score does not match the calculated score")
        if len(stat.tour) != len(edges):
            raise ValueError("Tour length does not match number of nodes")
        if len(stat.tour) != len(set(stat.tour)):
            raise ValueError("Tour contains duplicate nodes")

    return stats[-1:]


def dfs(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    def dfs_helper(tour: list[int]):
        nonlocal best_tour, best_score, n_nodes_expanded, n_nodes_pruned, stats
        if timer.time_out():
            return
        if len(tour) == len(edges):
            if edges[tour[-1]][tour[0]] == inf:
                return
            n_nodes_expanded += 1
            cost = score_tour(tour, edges)
            if cost < best_score:
                best_score = cost
                best_tour = tour[:]
                stats.append(SolutionStats(
                    tour=best_tour,
                    score=best_score,
                    time=timer.time(),
                    max_queue_size=1,
                    n_nodes_expanded=n_nodes_expanded,
                    n_nodes_pruned=n_nodes_pruned,
                    n_leaves_covered=cut_tree.n_leaves_cut(),
                    fraction_leaves_covered=cut_tree.fraction_leaves_covered()
                ))
            return
        for i in range(len(edges)):
            if edges[tour[-1]][i] == inf or i in tour:
                continue
            n_nodes_expanded += 1
            dfs_helper(tour + [i])
            
    best_tour = None
    best_score = inf
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))
    stats = []

    dfs_helper([0])

    if not stats:
        stats.append(SolutionStats(
            [],
            math.inf,
            timer.time(),
            1,
            n_nodes_expanded,
            n_nodes_pruned,
            cut_tree.n_leaves_cut(),
            cut_tree.fraction_leaves_covered()
        ))

    return stats[-1:]


def branch_and_bound(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:

    stats = greedy_tour(edges, timer)
    best_score = stats[0].score
    best_tour = stats[0].tour
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))

    edges_copy = [row[:] for row in edges]
    # set the diagonal to inf before reducing matrices
    for i in range(len(edges_copy)): edges_copy[i][i] = inf
    # reduce the matrix
    edges_copy, lower_bound = reduce_matrix(edges_copy)
    
    def bb_helper(tour: list[int], reduced_edges: list[list[float]], lower_bound: float):
        nonlocal n_nodes_expanded, n_nodes_pruned, stats, cut_tree, best_score, best_tour, edges_copy
        if timer.time_out():
            return
        if len(tour) == len(reduced_edges):
            if reduced_edges[tour[-1]][tour[0]] == inf:
                return
            n_nodes_expanded += 1
            cost = score_tour(tour, edges)
            if cost < best_score:
                best_score = cost
                best_tour = tour[:]
                stats.append(SolutionStats(
                    tour=best_tour,
                    score=best_score,
                    time=timer.time(),
                    max_queue_size=1,
                    n_nodes_expanded=n_nodes_expanded,
                    n_nodes_pruned=n_nodes_pruned,
                    n_leaves_covered=cut_tree.n_leaves_cut(),
                    fraction_leaves_covered=cut_tree.fraction_leaves_covered()
                ))
            return

        for i in range(len(reduced_edges)):
            if reduced_edges[tour[-1]][i] == inf or i in tour:
                continue
            n_nodes_expanded += 1
            new_matrix, path_cost = update_matrix_for_path(reduced_edges, tour[-1], i)
            new_lower_bound = lower_bound + path_cost
            if new_lower_bound < best_score:
                bb_helper(tour + [i], new_matrix, new_lower_bound)
            else:
                n_nodes_pruned += 1
                cut_tree.cut(tour + [i])
    
    bb_helper([0], edges_copy, lower_bound)

    for stat in stats:
        if stat.score != score_tour(stat.tour, edges):
            raise ValueError("Tour score does not match the calculated score")

    return stats


def branch_and_bound_smart(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    
    stats = greedy_tour(edges, timer)
    best_score = stats[0].score
    best_tour = stats[0].tour
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))
    max_queue_size = 1
    edges_copy = [row[:] for row in edges]
    queue = []
    
    # set the diagonal to inf before reducing matrices
    for i in range(len(edges_copy)): edges_copy[i][i] = inf
    # reduce the matrix
    edges_copy, lower_bound = reduce_matrix(edges_copy)
    heapq.heappush(queue, (0, lower_bound, [0], edges_copy))

    while queue:
        if timer.time_out():
            break

        _, current_lower_bound, tour, reduced_edges = heapq.heappop(queue)
        if current_lower_bound >= best_score:
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue
        n_nodes_expanded += 1

        if len(tour) == len(reduced_edges):
            if edges[tour[-1]][tour[0]] == inf:
                continue
            cost = score_tour(tour, edges)
            if cost < best_score:
                best_score = cost
                best_tour = tour[:]
                stats.append(SolutionStats(
                    tour=best_tour,
                    score=best_score,
                    time=timer.time(),
                    max_queue_size=max_queue_size,
                    n_nodes_expanded=n_nodes_expanded,
                    n_nodes_pruned=n_nodes_pruned,
                    n_leaves_covered=cut_tree.n_leaves_cut(),
                    fraction_leaves_covered=cut_tree.fraction_leaves_covered()
                    )
                )
            continue

        for i in range(len(reduced_edges)):
            if reduced_edges[tour[-1]][i] == inf or i in tour:
                continue
            new_matrix, path_cost = update_matrix_for_path(reduced_edges, tour[-1], i)
            new_lower_bound = current_lower_bound + path_cost
            if new_lower_bound < best_score:
                heapq.heappush(queue, (new_lower_bound + 1 * (len(edges) - len(tour)), new_lower_bound, tour + [i], new_matrix))
                max_queue_size = max(max_queue_size, len(queue))
            else:
                n_nodes_pruned += 1
                cut_tree.cut(tour + [i])

    for stat in stats:
        if stat.score != score_tour(stat.tour, edges):
            raise ValueError("Tour score does not match the calculated score")
        
    return stats


def reduce_matrix(matrix: list[list[float]]) -> tuple[list[list[float]], float]:
    """
    Reduces the matrix by subtracting the minimum value from each row and column.
    Returns the reduced matrix and the total reduction value.
    """
    reduced_value = 0

    # Row reduction
    for i in range(len(matrix)):
        row_min = min(matrix[i])
        if row_min != inf:
            reduced_value += row_min
            for j in range(len(matrix)):
                matrix[i][j] -= row_min
    
    # Column reduction
    for j in range(len(matrix)):
        col_min = min(matrix[i][j] for i in range(len(matrix)))
        if col_min != inf:
            reduced_value += col_min
            for i in range(len(matrix)):
                matrix[i][j] -= col_min

    return matrix, reduced_value


def update_matrix_for_path(matrix: list[list[float]], row: int, col: int) -> tuple[list[list[float]], float]:
    """
    Updates the matrix to reflect the inclusion of an edge (row, col) in the path.
    Sets the corresponding row and column to infinity and blocks the reverse edge.
    Reduces the updated matrix and returns the updated matrix and the total cost
    """
    updated_matrix = [row[:] for row in matrix]  # Create a deep copy of the matrix
    edge_cost = updated_matrix[row][col]

    # Set the selected row and column to infinity
    for i in range(len(updated_matrix)):
        updated_matrix[row][i] = inf
        updated_matrix[i][col] = inf

    # Block the reverse edge
    updated_matrix[col][row] = inf

    # Reduce the updated matrix
    updated_matrix, reduction_value = reduce_matrix(updated_matrix)

    return updated_matrix, edge_cost + reduction_value


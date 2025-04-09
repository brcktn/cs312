def test_connect_points():
    from connect_points import Solution

    # Create an instance of the Solution class
    solution = Solution()

    # Test cases
    test_cases = [
        ([(0, 0), (2, 2), (3, 10), (5, 2), (7, 0)], 20),
        ([(3, 12), (-2, 5), (-4, 1)], 18),
    ]

    for points, expected in test_cases:
        result = solution.minCostConnectPoints(points)
        assert result == expected, f"Test failed for points={points}: expected {expected}, got {result}"



def test_perfect_squares():
    from perfect_squares import Solution

    # Create an instance of the Solution class
    solution = Solution()

    # Test cases
    test_cases = [
        (12, 3),   # 4 + 4 + 4
        (13, 2),   # 4 + 9
        (1, 1),    # 1
        (2, 2),    # 1 + 1
        (3, 3),    # 1 + 1 + 1
        (4, 1),    # 4
        (5, 2),    # 4 + 1
        (6, 3),    # 4 + 1 + 1
        (7, 4),    # 4 + 1 + 1 + 1
        (8, 2),    # 4 + 4
        (9, 1)     # 9
    ]

    for n, expected in test_cases:
        result = solution.numSquares(n)
        assert result == expected, f"Test failed for n={n}: expected {expected}, got {result}"


def test_tribonacci():
    from tribonacci import Solution

    # Create an instance of the Solution class
    solution = Solution()

    # Test cases
    test_cases = [
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 4),
        (5, 7),
        (6, 13),
        (7, 24),
        (8, 44),
        (9, 81)
    ]

    for n, expected in test_cases:
        result = solution.tribonacci(n)
        assert result == expected, f"Test failed for n={n}: expected {expected}, got {result}"


def test_num_provinces():
    from num_provinces import Solution

    # Create an instance of the Solution class
    solution = Solution()

    # Test
    test_cases = [
        ([[1, 1, 0], [1, 1, 0], [0, 0, 1]], 2),  # Two provinces
        ([[1, 0, 0], [0, 1, 0], [0, 0, 1]], 3),  # Three provinces
        ([[1, 1, 0], [1, 1, 1], [0, 1, 1]], 1),  # One province
        ([[1]], 1),                            # One city
        ([[1, 0], [0, 1]], 2)                 # Two disconnected cities
    ]
    for isConnected, expected in test_cases:
        result = solution.findCircleNum(isConnected)
        assert result == expected, f"Test failed for isConnected={isConnected}: expected {expected}, got {result}"



def test_course_schedule():
    from course_schedule import Solution

    # Create an instance of the Solution class
    solution = Solution()

    # Test cases
    test_cases = [
        (2, [[1, 0]], True),   # Can finish all courses
        (2, [[1, 0], [0, 1]], False),  # Cannot finish all courses
        (3, [[0, 1], [1, 2], [2, 0]], False),  # Cycle exists
        (4, [[0, 1], [1, 2], [2, 3]], True),   # No cycle
        (5, [[0, 1], [1, 2], [3, 4]], True)    # No cycle
    ]

    for numCourses, prerequisites, expected in test_cases:
        result = solution.canFinish(numCourses, prerequisites)
        assert result == expected, f"Test failed for numCourses={numCourses}, prerequisites={prerequisites}: expected {expected}, got {result}"


def test_triangle():
    from triangle import Solution

    # Create an instance of the Solution class
    solution = Solution()

    # Test cases
    test_cases = [
        ([[2], [3, 4], [5, 6, 7], [4, 1, 8, 3]], 11),  # Four levels
    ]

    for triangle_data, expected in test_cases:
        result = solution.minimumTotal(triangle_data)
        assert result == expected, f"Test failed for triangle={triangle_data}: expected {expected}, got {result}"

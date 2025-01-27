# Uncomment this line to import some functions that can help
# you debug your algorithm
# from plotting import draw_line, draw_hull, circle_point


def compute_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull"""
    if len(points) < 3:
        return points

    if len(points) == 3:
        if is_ccw(points[0], points[1], points[2]):
            return points
        else:
            return [points[2], points[1], points[0]]

    left, right = split_points(points)
    left_hull = compute_hull(left)
    right_hull = compute_hull(right)
    return combine_hulls(left_hull, right_hull)


def split_points(
    points: list[tuple[float, float]]
) -> tuple[list[tuple[float, float]], list[tuple[float, float]]]:
    """Return a tuple of two lists of points split along the y-axis"""
    points.sort(key=lambda x: x[0])
    mid = len(points) // 2
    return points[:mid], points[mid:]


def combine_hulls(
    left: list[tuple[float, float]], right: list[tuple[float, float]]
) -> list[tuple[float, float]]:
    """Return the convex hull of the two provided hulls
    Assumes that both hulls are sorted in ccw order"""
    rigthmost_left_index = max(enumerate(left), key=lambda x: x[1][0])[0]
    leftmost_right_index = min(enumerate(right), key=lambda x: x[1][0])[0]

    i = rigthmost_left_index
    j = leftmost_right_index

    while True:
        if is_ccw(left[(i + 1) % len(left)], left[i], right[j]):
            i = (i + 1) % len(left)
        elif is_ccw(left[i], right[j], right[(j - 1) % len(right)]):
            j = (j - 1) % len(right)
        else:
            top_chord_indecies = (i, j)
            break

    i = rigthmost_left_index
    j = leftmost_right_index

    while True:
        if is_ccw(right[j], left[i], left[(i - 1) % len(left)]):
            i = (i - 1) % len(left)
        elif is_ccw(right[(j + 1) % len(right)], right[j], left[i]):
            j = (j + 1) % len(right)
        else:
            bottom_chord_indecies = (i, j)
            break

    left = keep_between_indecies(
        left, (top_chord_indecies[0], bottom_chord_indecies[0])
    )
    right = keep_between_indecies(
        right, (bottom_chord_indecies[1], top_chord_indecies[1])
    )

    return left + right


def keep_between_indecies(
    points: list[tuple[float, float]], indecies: tuple[int, int]
) -> list[tuple[float, float]]:
    """Return the subset of points that are between the provided indecies"""

    start, end = indecies
    if start <= end:
        return points[start : end + 1]
    else:
        return points[start:] + points[: end + 1]


def is_ccw(
    a: tuple[float, float], b: tuple[float, float], c: tuple[float, float]
) -> bool:
    """Return True if the points a, b, and c are in counter-clockwise
    order and False otherwise

    Also returns False if any two of the points are the same,
    or if the points are collinear"""
    if a == b or b == c or a == c:
        return False
    ba = (a[0] - b[0], a[1] - b[1])
    bc = (c[0] - b[0], c[1] - b[1])
    return cross_product(ba, bc) < 0


def cross_product(a: tuple[float, float], b: tuple[float, float]) -> float:
    """Return the magnitiude of the cross product
    of the planar vectors a and b"""
    return a[0] * b[1] - a[1] * b[0]

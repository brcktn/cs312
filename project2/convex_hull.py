# Uncomment this line to import some functions that can help
# you debug your algorithm
# from plotting import draw_line, draw_hull, circle_point


def compute_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull"""
    return []


def is_ccw(
    a: tuple[float, float], b: tuple[float, float], c: tuple[float, float]
) -> bool:
    """Return True if the points a, b, and c are in counter-clockwise
    order and False otherwise

    Raises a ValueError if any two of the points are the same,
    or if the points are collinear"""
    if a == b or b == c or a == c:
        raise ValueError("Two points are the same")
    ba = (a[0] - b[0], a[1] - b[1])
    bc = (c[0] - b[0], c[1] - b[1])
    if (cross := cross_product(ba, bc)) == 0:
        raise ValueError("Points are collinear")
    return cross <= 0


def cross_product(a: tuple[float, float], b: tuple[float, float]) -> float:
    """Return the cross product of the vectors a and b"""
    return a[0] * b[1] - a[1] * b[0]



from typing import Sequence, List, Optional

from shapely.geometry import LineString, Point, MultiPoint


__all__ = ["unique_line_points", "nearest_neighbor_within"]


def unique_line_points(lines: Sequence[LineString]) -> List[Point]:
    """


    :param lines:
    :return: Return list of unique vertices from list of LineStrings.
    :rtype: List[Point]
    """

    vertices = []

    for line in lines:
        vertices.extend(list(line.coords))

    return [Point(p) for p in set(vertices)]


def nearest_neighbor_within(others: Sequence, point, max_distance) -> Optional[Point]:
    """Find the nearest point among others up to a maximum distance.


    :param others: a list of Points or a MultiPoint
    :param point: a Point
    :param max_distance: maximum distance to search for the nearest neighbor

    :return: A shapely Point if one is within max_distance, None otherwise
    :rtype: Optional[Point]
    """
    search_region = point.buffer(max_distance)
    interesting_points = search_region.intersection(MultiPoint(others))

    if not interesting_points:
        closest_point = None
    elif isinstance(interesting_points, Point):
        closest_point = interesting_points
    else:
        distances = [
            point.distance(ip) for ip in interesting_points if point.distance(ip) > 0
        ]
        closest_point = interesting_points[distances.index(min(distances))]

    return closest_point

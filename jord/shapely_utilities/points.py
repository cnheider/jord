from typing import Sequence, List, Optional

import numpy
from shapely.geometry import LineString, Point, MultiPoint

__all__ = ["unique_line_points", "nearest_neighbor_within", "azimuth"]


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


def azimuth(point1: Point, point2: Point) -> float:
    """
    The clockwise angle from North to line of two points

    :param point1:
    :type point1: Point
    :param point2:
    :type point2: Point
    :return: angle
    :rtype: float
    """

    angle = numpy.arctan2(point2.x - point1.x, point2.y - point1.y)
    # Gets the angle between the first and last coordinate of a linestring

    return (
        numpy.degrees(angle) if angle >= 0 else numpy.degrees(angle) + 360
    ) % 180  # Modulo is used on the angle to produce a result between 0 and 180 degrees

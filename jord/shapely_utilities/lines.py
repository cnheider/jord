#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

           Created on 1/23/23
           """

__all__ = [
    "to_lines",
    "to_single_line",
    "explode_line",
    "strip_multiline_dangles",
    "strip_line_dangles",
]

import collections
from typing import Union, List, Sequence

import shapely.ops
from shapely.geometry import LineString, MultiLineString, Point, MultiPoint, box
from shapely.geometry.base import BaseGeometry

from jord.shapely_utilities.points import (
    unique_line_points,
    nearest_neighbor_within,
)


def to_single_line(s: Union[LineString, MultiLineString]) -> LineString:
    """
    assume that lines are ordered, NOTE closes of gaps!

    :param s:
    :type s: Union[LineString, MultiLineString]
    :return:
    :rtype: LineString
    """
    if isinstance(s, MultiLineString):
        out_coords = [
            list(i.coords) for i in s.geoms
        ]  # Put the subline coordinates into a list of sublists

        return LineString(
            [i for sublist in out_coords for i in sublist]
        )  # Flatten the list of sublists and use it to make a new line

    elif isinstance(s, LineString):
        return s
    else:
        raise NotImplementedError


def to_lines(geoms: Sequence[BaseGeometry]) -> List[LineString]:
    """
    Converts Shapely geoms in to Shapely LineString

    :param geoms:
    :type geoms: Sequence[BaseGeometry]
    :return:
    :rtype: List[LineString]
    """

    lines = []
    for g in geoms:
        if isinstance(g, (LineString)):
            lines.append(g)
        elif isinstance(g, (BaseGeometry)):
            boundary = g.boundary
            if isinstance(boundary, MultiLineString):
                lines.extend(to_lines(boundary.geoms))
            else:
                lines.append(boundary)
        else:
            raise NotImplementedError(f"{g, type(g)}")

    return lines


def strip_line_dangles(
    line: LineString, dangle_length_threshold: float = 0.1, iterations: int = 3
) -> LineString:
    """

    :param line:
    :type line: LineString
    :param dangle_length_threshold:
    :type dangle_length_threshold: float
    :param iterations:
    :type iterations: int
    :return: The LineString without dangles shorter than the dangle_length_threshold
    :rtype: LineString
    """

    working_line = line
    for ith_ in range(iterations):
        working_segments = []
        segments = explode_line(working_line)
        if len(segments) > 2:
            start, *rest, end = segments

            if start.length > dangle_length_threshold:
                working_segments.append(start)

            working_segments.extend(rest)

            if end.length > dangle_length_threshold:
                working_segments.append(end)

        elif len(segments) < 2:
            segment = segments[0]

            if segment.length > dangle_length_threshold:
                working_segments.append(segment)

        else:
            s1, s2 = segments

            if s1.length > dangle_length_threshold:
                working_segments.append(s1)

            if s2.length > dangle_length_threshold:
                working_segments.append(s2)

        working_line = LineString(working_segments)

    return working_line


def line_endpoints(lines: Union[List[LineString], MultiLineString]) -> MultiPoint:
    """

    :param lines:
    :type: Union[List[LineString], MultiLineString]
    :return: Returns a MultiPoint of terminal points from list of LineStrings.
    :rtype: MultiPoint
    """

    all_points = []
    if isinstance(lines, MultiLineString):
        lines = lines.geoms

    for line in lines:
        for i in [0, -1]:  # start and end point
            all_points.append(line.coords[i])

    endpoints = set(
        [item for item, count in collections.Counter(all_points).items() if count < 2]
    )  # Remove duplicates

    return MultiPoint([Point(p) for p in endpoints])


def strip_multiline_dangles(
    multilinestring: MultiLineString,
    dangle_length_threshold: float = 0.1,
    iterations: int = 3,
) -> MultiLineString:
    """

    :param multilinestring:
    :type multilinestring: MultiLineString
    :param dangle_length_threshold:
    :type dangle_length_threshold: float
    :param iterations:
    :type iterations: int
    :return:
    :rtype: MultiLineString
    """
    working_multi = multilinestring
    for ith_ in range(iterations):
        endpoints = line_endpoints(working_multi)
        working_segments = []
        for linestring in working_multi.geoms:
            segments = explode_line(linestring)
            if len(segments) > 2:
                start, *rest, end = segments
                if start.intersects(endpoints):
                    if start.length > dangle_length_threshold:
                        working_segments.append(start)
                else:
                    working_segments.append(start)

                working_segments.extend(rest)

                if end.intersects(endpoints):
                    if end.length > dangle_length_threshold:
                        working_segments.append(end)
                else:
                    working_segments.append(end)
            elif len(segments) < 2:
                segment = segments[0]
                if segment.intersects(endpoints):
                    if segment.length > dangle_length_threshold:
                        working_segments.append(segment)
                else:
                    working_segments.append(segment)
            else:
                s1, s2 = segments
                if s1.intersects(endpoints):
                    if s1.length > dangle_length_threshold:
                        working_segments.append(s1)
                else:
                    working_segments.append(s1)

                if s2.intersects(endpoints):
                    if s2.length > dangle_length_threshold:
                        working_segments.append(s2)
                else:
                    working_segments.append(s2)

        working_multi = MultiLineString(working_segments)

    return working_multi


def explode_line(line: LineString) -> List[LineString]:
    """

    :param line:
    :return:
    """
    out = []
    for pt1, pt2 in zip(
        line.coords, line.coords[1:]
    ):  # iterate from first cord, iterate from second coords to get
        # endpoints of each segment
        out.append(LineString([pt1, pt2]))
    return out


def find_isolated_endpoints(
    lines: Sequence[Union[LineString, MultiLineString]],
) -> Sequence[Point]:
    """
    Find endpoints of lines that don't touch another line.

    :param lines: A list of LineStrings or a MultiLineString
    :return: A list of line end Points that don't touch any other line of lines
    """

    isolated_endpoints = []
    for i, line in enumerate(lines):
        other_lines = lines[:i] + lines[i + 1 :]
        for q in [0, -1]:
            endpoint = Point(line.coords[q])
            if any(endpoint.touches(another_line) for another_line in other_lines):
                continue
            else:
                isolated_endpoints.append(endpoint)
    return isolated_endpoints


def snappy_endings(
    lines: Union[LineString, MultiLineString], max_distance: float
) -> Sequence[Union[LineString, MultiLineString]]:
    """
    Snap endpoints of lines together if they are at most max_length apart.


    :param lines: A list of LineStrings or a MultiLineString
    :param max_distance: maximum distance two endpoints may be joined together
    :return:
    :rtype: Sequence[Union[LineString, MultiLineString]]
    """

    # initialize snapped lines with list of original lines
    # snapping points is a MultiPoint object of all vertices
    snapped_lines = [line for line in lines]
    snapping_points = unique_line_points(snapped_lines)

    # isolated endpoints are going to snap to the closest vertex
    isolated_endpoints = find_isolated_endpoints(snapped_lines)

    # only move isolated endpoints, one by one
    for endpoint in isolated_endpoints:
        # find all vertices within a radius of max_distance as possible
        target = nearest_neighbor_within(snapping_points, endpoint, max_distance)

        # do nothing if no target point to snap to is found
        if not target:
            continue

            # find the LineString to modify within snapped_lines and update it
        for i, snapped_line in enumerate(snapped_lines):
            if endpoint.touches(snapped_line):
                snapped_lines[i] = bend_towards(snapped_line, where=endpoint, to=target)
                break

        # also update the corresponding snapping_points
        for i, snapping_point in enumerate(snapping_points):
            if endpoint.equals(snapping_point):
                snapping_points[i] = target
                break

    # post-processing: remove any resulting lines of length 0
    snapped_lines = [s for s in snapped_lines if s.length > 0]

    return snapped_lines


def bend_towards(line: LineString, where: Point, to: Point) -> LineString:
    """
    Move the point where along a line to the point at location to.

    :param line:
    :param where: a point ON the line (not necessarily a vertex)
    :param to: a point NOT on the line where the nearest vertex will be moved to
    :return: the modified (bent) line
    """

    if not line.contains(where) and not line.touches(where):
        raise ValueError("line does not contain the point where.")

    coords = line.coords[:]
    # easy case: where is (within numeric precision) a vertex of line
    for k, vertex in enumerate(coords):
        if where.almost_equals(Point(vertex)):
            # move coordinates of the vertex to destination
            coords[k] = to.coords[0]
            return LineString(coords)

    # hard case: where lies between vertices of line, so
    # find the nearest vertex and move that one to point to
    _, min_k = min(
        (where.distance(Point(vertex)), k) for k, vertex in enumerate(coords)
    )
    coords[min_k] = to.coords[0]
    return LineString(coords)


def prune_short_lines(
    lines: Sequence[LineString], min_length: float
) -> List[LineString]:
    """
    Remove lines from a LineString shorter than min_length.

    Deletes all lines from a list of LineStrings or a MultiLineString
    that have a total length of less than min_length. Vertices of touching
    lines are contracted towards the centroid of the removed line.


    :param lines: List of LineStrings or a MultiLineString
    :param min_length: minimum length of a single LineString to be preserved
    :return:  the pruned pandas DataFrame
    """
    pruned_lines = [line for line in lines]  # converts MultiLineString to list
    to_prune = []

    for i, line in enumerate(pruned_lines):
        if line.length < min_length:
            to_prune.append(i)
            for n in intersecting_lines_idx(line, pruned_lines):
                contact_point = line.intersection(pruned_lines[n])
                pruned_lines[n] = bend_towards(
                    pruned_lines[n], where=contact_point, to=line.centroid
                )

    return [line for i, line in enumerate(pruned_lines) if i not in to_prune]


def linemerge(
    line_s: Union[LineString, MultiLineString]
) -> Union[LineString, MultiLineString]:
    """
    Merge a list of LineStrings and/or MultiLineStrings.

    Given a list of LineStrings and possibly MultiLineStrings, merge all of
    them to a single MultiLineString.

    :type line_s: LineString|MultiLineString
    :rtype:LineString|MultiLineString
    """
    lines = []
    for line in line_s.geoms:
        if isinstance(line, MultiLineString):
            # line is a multilinestring, so append its components
            lines.extend(line.geoms)
        else:
            # line is a line, so simply append it
            lines.append(line)

    return shapely.ops.linemerge(lines)


def one_linestring_per_intersection(
    lines: Sequence[LineString],
) -> Union[LineString, MultiLineString]:
    """
    Move line endpoints to intersections of line segments.

    Given a list of touching or possibly intersecting LineStrings, return a
     list of LineStrings that have their endpoints at all crossings and
    intersecting points and ONLY there.


    :param lines: A list of LineStrings or a MultiLineString
    :return: a list of LineStrings
    """
    lines_merged = shapely.ops.linemerge(lines)

    # intersecting multiline with its bounding box somehow triggers a first
    bounding_box = box(*lines_merged.bounds)

    # perform linemerge (one linestring between each crossing only)
    # if this fails, write function to perform this on a bbox-grid and then
    # merge the result
    lines_merged = lines_merged.intersection(bounding_box)
    lines_merged = shapely.ops.linemerge(lines_merged)
    return lines_merged


def intersecting_lines_idx(of: LineString, lines: Sequence[LineString]) -> List[int]:
    """Find the indices in a list of LineStrings that touch a given LineString.


    :param lines: List of LineStrings in which to search for neighbors
    :param of: the LineString, which must be touched
    :return: a list of indices, so that all lines[indices] touch the LineString of
    """
    return [k for k, line in enumerate(lines) if line.touches(of)]


def intersecting_lines(of: LineString, lines: Sequence[LineString]) -> List[LineString]:
    """
    Find the indices in a list of LineStrings that touch a given LineString.


    :param of: The LineString which must be touched
    :param lines: List of LineStrings in which to search for neighbors
    :return: list of indices, so that all lines[indices] touch the LineString of
    """
    return [line for line in (lines) if line.touches(of)]


if __name__ == "__main__":

    def iashdh():
        print(
            to_single_line(MultiLineString([[[0, 0], [0, 1]], [[0, 2], [0, 3]]]))
        )  # LINESTRING (0 0, 0 1, 0 2, 0 3)

    def ausdh():
        from shapely.geometry import MultiPolygon, Point

        pol1 = MultiPolygon([Point(0, 0).buffer(2.0), Point(1, 1).buffer(2.0)])
        pol2 = Point(7, 8).buffer(1.0)
        pols = [pol1, pol2]

        print(to_lines(pols))

    ausdh()

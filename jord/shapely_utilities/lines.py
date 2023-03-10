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

from shapely.geometry import LineString, MultiLineString, Point, MultiPoint
from shapely.geometry.base import BaseGeometry


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
        ]  # Put the sub-line coordinates into a list of sublists

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
    :return:
    :rtype: LineString
    """

    working_line = line
    for ith_ in range(iterations):
        endpoints = line_endpoints(working_line)
        working_segments = []
        segments = explode_line(working_line)
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

        working_line = LineString(working_segments)

    return working_line


def line_endpoints(lines: List[LineString] | MultiLineString) -> MultiPoint:
    """Return list of terminal points from list of LineStrings."""

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
    out = []
    for pt1, pt2 in zip(
        line.coords, line.coords[1:]
    ):  # iterate from first cord, iterate from second coords to get
        # endpoints of each segment
        out.append(LineString([pt1, pt2]))
    return out


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

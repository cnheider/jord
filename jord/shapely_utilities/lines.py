#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

           Created on 1/23/23
           """

__all__ = []

from typing import Union

from shapely import LineString, MultiLineString


def to_single_line(s: Union[LineString, MultiLineString]) -> LineString:
    """
    assume that lines are ordered
    :return:
    :rtype:
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


if __name__ == "__main__":
    print(
        to_single_line(MultiLineString([[[0, 0], [0, 1]], [[0, 2], [0, 3]]]))
    )  # LINESTRING (0 0, 0 1, 0 2, 0 3)

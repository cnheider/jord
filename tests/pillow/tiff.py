#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

           Created on 1/27/23
           """

__all__ = []

from jord.pillow_utilities import TIFF_TAG_IDS, TIFF_TAG_V2_IDS


def test_tiff_tags():
    assert len(TIFF_TAG_IDS) > 0, "TIFF_TAG_IDS was empty"


def test_tiff_v2_tags():
    assert len(TIFF_TAG_V2_IDS) > 0, "TIFF_TAG_V2_IDS was empty"


if __name__ == "__main__":
    test_tiff_tags()
    test_tiff_v2_tags()

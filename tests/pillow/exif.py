#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

           Created on 1/27/23
           """

__all__ = []

from jord.pillow_utilities import EXIF_TAG_IDS


def test_exif_tags():
    assert len(EXIF_TAG_IDS) > 0, "EXIF_TAG_IDS was empty"


if __name__ == "__main__":
    test_exif_tags()

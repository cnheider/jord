#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

           Created on 5/5/22
           """

__all__ = [
    "import_qgis",
    # "QGIS"
]

from types import ModuleType


def import_qgis() -> ModuleType:
    try:
        import qgis

    except (ImportError, ModuleNotFoundError) as e:
        raise ImportError(f"gdal is not installed {type(e), e}")

    return qgis


# QGIS = import_qgis()

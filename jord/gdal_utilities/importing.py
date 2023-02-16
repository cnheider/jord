#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

           Created on 5/5/22
           """

__all__ = ["import_gdal", "import_osr", "GDAL", "OSR"]

from types import ModuleType


def import_gdal() -> ModuleType:
    try:
        import gdal

    except (ImportError, ModuleNotFoundError) as e:
        try:
            from osgeo import gdal
        except Exception as e2:
            raise ImportError(f"gdal is not installed {type(e), e, type(e2), e2}")

    gdal.UseExceptions()

    return gdal


def import_osr() -> ModuleType:
    try:
        import ors

    except (ImportError, ModuleNotFoundError) as e:
        try:
            from osgeo import osr
        except Exception as e2:
            raise ImportError(f"osr is not installed {type(e), e, type(e2), e2}")

    osr.UseExceptions()

    return osr


GDAL = import_gdal()
OSR = import_osr()

if __name__ == "__main__":
    import_gdal()
    import_osr()

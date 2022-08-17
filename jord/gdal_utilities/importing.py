#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

           Created on 5/5/22
           """

__all__ = ["import_gdal", "import_osr", "GDAL", "OSR"]


def import_gdal():
    """

    :return:
    :rtype:
    """
    try:
        import gdal
    except ImportError:
        try:
            from osgeo import gdal
        except:
            raise ImportError("gdal is not installed")
    gdal.UseExceptions()
    return gdal


def import_osr():
    """

    :return:
    :rtype:
    """
    try:
        import ors
    except ImportError:
        try:
            from osgeo import osr
        except:
            raise ImportError("osr is not installed")
    osr.UseExceptions()
    return osr


GDAL = import_gdal()
OSR = import_osr()

if __name__ == "__main__":
    import_gdal()
    import_osr()

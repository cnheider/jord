#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"


def test_import_package():
    ...
    if False:
        import jord

        print(jord.__version__)


def test_qgis_import_package():
    ...
    if False:
        from jord import qgis_utilities

        print(qgis_utilities.__doc__)


def test_gdal_import_package():
    ...
    if False:
        from jord import gdal_utilities

        print(gdal_utilities.__doc__)


def test_pil_import_package():
    ...
    if False:
        from jord import pillow_utilities

        print(pillow_utilities.__doc__)


def test_shapely_import_package():
    ...
    if False:
        from jord import shapely_utilities

        print(shapely_utilities.__doc__)


def test_rasterio_import_package():
    ...
    if False:
        from jord import rasterio_utilities

        print(rasterio_utilities.__doc__)


if __name__ == "__main__":
    test_gdal_import_package()
    test_pil_import_package()
    test_gdal_import_package()
    test_import_package()
    test_shapely_import_package()
    test_rasterio_import_package()

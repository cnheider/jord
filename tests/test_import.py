#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"


def test_import_package():
  import jord

  print(jord.__version__)


def test_qgis_import_package():
  from jord import qgis_utilities

  print(qgis_utilities.__doc__)


def test_gdal_import_package():
  from jord import gdal_utilities

  print(gdal_utilities.__doc__)


def test_pil_import_package():
  from jord import pillow_utilities

  print(pillow_utilities.__doc__)


if __name__ == '__main__':
    test_gdal_import_package()
    test_pil_import_package()
    test_gdal_import_package()
    test_import_package()
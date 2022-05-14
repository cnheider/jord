__all__ = [
  "import_gdal",
]


def import_gdal():
  try:
    import gdal
  except ImportError:
    try:
      from osgeo import gdal
    except:
      raise ImportError("gdal is not installed")
  return gdal

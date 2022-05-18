from pathlib import Path
from typing import List

from jord.gdal_utilities.enums import GdalAccessEnum
from jord.gdal_utilities.importing import GDAL, OSR


# __all__ = ['get_gcps_from_file']


def get_georeference_from_file(file: Path) -> List[GDAL.GCP]:
    with GDAL.Open(file) as f:
        # return ds.GetProjection()
        # return f.GetGCPs()
        return f.GetGeoTransform()


def set_georeference_to_file(file: Path, gcps: List[GDAL.GCP]):

    img_path = "/path/to/tif"

    # input values for geotransform
    ulx = 25
    uly = 60
    xres = 0.5
    yres = -0.5
    xrot = 0
    yrot = 0
    geotransform = (ulx, xres, xrot, uly, yrot, yres)

    # find projection
    srs = OSR.SpatialReference()
    srs.ImportFromEPSG(4326)

    # update image georeference
    ds = GDAL.Open(img_path, GdalAccessEnum.update.value)
    ds.SetGeoTransform(geotransform)
    ds.SetProjection(srs.ExportToWkt())
    ds.FlushCache()
    del ds

    # do this for each image and then stack


def copy_gcps_to_file(file: Path, gcps: List[GDAL.GCP]):
    with GDAL.Open(file, GdalAccessEnum.update.value) as f:
        f.SetGCPs(gcps)
        f.FlushCache()


def geotiff_to_tiff(src: Path, dst: Path):
    """
    https://gdal.org/user/translate.html
    """
    GDAL.Translate(
        dst,
        src,
        format="GTiff",
        outputType=GDAL.GDT_Byte,
        creationOptions=["COMPRESS=LZW"],
    )


def tiff_to_geotiff(src: Path, dst: Path):
    """
    https://gdal.org/user/translate.html
    """
    GDAL.Translate(
        dst,
        src,
        format="GTiff",
        outputType=GDAL.GDT_Byte,
        creationOptions=["COMPRESS=LZW"],
    )

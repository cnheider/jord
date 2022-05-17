from jord.gdal_utilities import GDAL
from enum import Enum


class GdalAccessEnum(Enum):
    """
    Enum for GDAL.Access
    """

    read_only = GDAL.GA_ReadOnly  # Default  = 0
    update = GDAL.GA_Update

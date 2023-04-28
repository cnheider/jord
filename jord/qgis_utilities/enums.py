from enum import Enum

from qgis.core import (
    QgsMultiBandColorRenderer,
    QgsPalettedRasterRenderer,
    QgsSingleBandColorDataRenderer,
    QgsSingleBandGrayRenderer,
    QgsSingleBandPseudoColorRenderer,
)

__all__ = ["QgisRendererEnum"]


class QgisRendererEnum(Enum):
    multi_band = QgsMultiBandColorRenderer
    paletted_raster = QgsPalettedRasterRenderer
    single_band_color = QgsSingleBandColorDataRenderer
    single_band_gray = QgsSingleBandGrayRenderer
    single_band_pseudo = QgsSingleBandPseudoColorRenderer

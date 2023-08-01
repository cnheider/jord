import time
import uuid
from enum import Enum
from typing import Mapping, Any, Tuple

import numpy
import shapely.geometry.base
import tqdm
from pandas import DataFrame
from shapely.geometry.base import BaseGeometry
from warg import ensure_existence
from warg import passes_kws_to, Number

from jord import PROJECT_APP_PATH
from jord.qlive_utilities.qgis_layer_creation import add_qgis_geometry

APPEND_TIMESTAMP = True
SKIP_MEMORY_LAYER_CHECK_AT_CLOSE = True
PIXEL_SIZE = 1
DEFAULT_NUMBER = 0
CONTRAST_ENHANCE = True
DEFAULT_LAYER_NAME = "TemporaryLayer"
DEFAULT_LAYER_CRS = "EPSG:4326"
VERBOSE = False

__all__ = [
    "add_raster",
    "add_rasters",
    "add_wkt",
    "add_wkts",
    "add_wkb",
    "add_wkbs",
    "add_dataframe",
    "add_dataframes",
    "add_geojson",
    "add_shapely_geometry",
    "add_shapely_geometries",
    "clear_all",
    "remove_layers",
    "QliveRPCMethodEnum",
    "QliveRPCMethodMap",
]


def add_raster(
    qgis_instance_handle: Any,
    raster: numpy.ndarray,
    name: str = DEFAULT_LAYER_NAME,
    centroid: Tuple[Number, Number] = None,
    extent_tuple: Tuple[Number, Number, Number, Number] = None,
    pixel_size: Tuple[Number, Number] = PIXEL_SIZE,
    crs_str: str = DEFAULT_LAYER_CRS,
    default_value: Number = DEFAULT_NUMBER,
    field: str = None,
    no_data_value: int = -1,
) -> None:
    """
    add a raster

    :param qgis_instance_handle:
    :param raster:
    :param name:
    :param centroid:
    :param extent_tuple:
    :param pixel_size:
    :param crs_str:
    :param default_value:
    :param field:
    :return: None
    :rtype: None
    """
    # noinspection PyUnresolvedReferences
    from qgis.core import (
        QgsRectangle,
        QgsCoordinateReferenceSystem,
        QgsRasterBandStats,
        QgsSingleBandGrayRenderer,
        QgsMultiBandColorRenderer,
        QgsContrastEnhancement,
        QgsRasterLayer,
        QgsRasterFileWriter,
        Qgis,
    )
    from jord.qgis_utilities.numpy_utilities.data_type import get_qgis_type
    from jord.qgis_utilities import RasterDataProviderEditSession

    x_size, y_size, *rest_size = raster.shape

    if len(rest_size) == 0:
        raster = numpy.expand_dims(raster, axis=-1)

    *_, num_bands = raster.shape

    data_type = get_qgis_type(raster.dtype).value

    extent = QgsRectangle()

    if extent_tuple:
        extent.setXMinimum(extent_tuple[0])
        extent.setYMinimum(extent_tuple[1])
        extent.setXMaximum(extent_tuple[2])
        extent.setYMaximum(extent_tuple[3])
    else:
        if centroid is None:
            centroid = (0, 0)  # (x_size, y_size)

        raster_half_size = (PIXEL_SIZE * x_size / 2, PIXEL_SIZE * y_size / 2)

        if False:
            raster_half_size = raster_half_size[1], raster_half_size[0]

        extent.setXMinimum(centroid[0] - raster_half_size[0])
        extent.setYMinimum(centroid[1] - raster_half_size[1])
        extent.setXMaximum(centroid[0] + raster_half_size[0])
        extent.setYMaximum(centroid[1] + raster_half_size[1])

    if APPEND_TIMESTAMP:
        name += f"_{time.time()}"

    temp_file = (
        ensure_existence(PROJECT_APP_PATH.user_data / "rasters") / f"{uuid.uuid4()}.tif"
    )
    writer = QgsRasterFileWriter(temp_file)
    provider = writer.createMultiBandRaster(
        dataType=data_type.value,
        width=x_size,
        height=y_size,
        extent=extent,
        crs=QgsCoordinateReferenceSystem(crs_str),
        nBands=num_bands,
    )

    if VERBOSE:
        print("drawing")

    w_pixels, h_pixels = x_size, y_size

    with RasterDataProviderEditSession(provider):
        progress = range(0, num_bands)

        if VERBOSE:
            progress = tqdm.tqdm(progress)

        for ith_band in progress:
            block = provider.block(
                bandNo=ith_band + 1, boundingBox=extent, width=w_pixels, height=h_pixels
            )
            provider.setNoDataValue(bandNo=ith_band + 1, noDataValue=no_data_value)

            for wp in range(0, w_pixels):
                for hp in range(0, h_pixels):
                    value = raster[wp][hp][ith_band]
                    if value == numpy.nan:
                        block.setIsNoData(wp, hp)
                        continue
                    if False:
                        value = int(value) * 255
                    block.setValue(wp, hp, value)

            if VERBOSE:
                print("writing block on band", ith_band + 1)

            provider.writeBlock(block, band=ith_band + 1, xOffset=0, yOffset=0)

            del block

    layer = QgsRasterLayer(temp_file, name, "gdal")

    if num_bands == 1:
        # this is needed for the min and max value to refresh in the layer panel
        renderer = layer.renderer()

        gray_renderer = QgsSingleBandGrayRenderer(provider, 1)

        if CONTRAST_ENHANCE:
            stats = provider.bandStatistics(1, QgsRasterBandStats.All, extent)
            min_value = stats.minimumValue
            max_value = stats.maximumValue

            my_enhancement = QgsContrastEnhancement()
            my_enhancement.setContrastEnhancementAlgorithm(
                QgsContrastEnhancement.StretchToMinimumMaximum, True
            )
            my_enhancement.setMinimumValue(min_value)
            my_enhancement.setMaximumValue(max_value)
            gray_renderer.setContrastEnhancement(my_enhancement)

        layer.setRenderer(gray_renderer)

    elif num_bands != 4:
        multi_color_renderer = QgsMultiBandColorRenderer(provider, 1, 2, 3)

        layer.setRenderer(multi_color_renderer)
        layer.setDefaultContrastEnhancement()
        layer.triggerRepaint()
        # iface.legendInterface().refreshLayerSymbology(layer)

    else:
        multi_color_renderer = QgsMultiBandColorRenderer(provider, 1, 2, 3)

        layer.setRenderer(multi_color_renderer)
        layer.setDefaultContrastEnhancement()
        layer.triggerRepaint()

    if SKIP_MEMORY_LAYER_CHECK_AT_CLOSE:
        layer.setCustomProperty("skipMemoryLayersCheck", 1)

    qgis_instance_handle.qgis_project.addMapLayer(layer, False)
    qgis_instance_handle.temporary_group.insertLayer(0, layer)


@passes_kws_to(add_raster)
def add_rasters(qgis_instance_handle, rasters: Mapping, **kwargs) -> None:
    """

    :param qgis_instance_handle:
    :param rasters:
    :param kwargs:
    :return:
    """
    for layer_name, raster in rasters.items():
        add_raster(qgis_instance_handle, raster, name=layer_name, **kwargs)


@passes_kws_to(add_qgis_geometry)
def add_wkb(qgis_instance_handle: Any, wkb: str, **kwargs) -> None:
    """

    :param qgis_instance_handle:
    :param wkb:
    :param kwargs:
    :return:
    """
    # noinspection PyUnresolvedReferences
    from qgis.core import QgsGeometry

    add_qgis_geometry(qgis_instance_handle, QgsGeometry.fromWkb(wkb), **kwargs)


@passes_kws_to(add_qgis_geometry)
def add_wkt(qgis_instance_handle: Any, wkt: str, **kwargs) -> None:
    """

    :param qgis_instance_handle:
    :param wkt:
    :param kwargs:
    :return:
    """
    # noinspection PyUnresolvedReferences
    from qgis.core import QgsGeometry

    add_qgis_geometry(qgis_instance_handle, QgsGeometry.fromWkt(wkt), **kwargs)


@passes_kws_to(add_wkb)
def add_wkbs(qgis_instance_handle: Any, wkbs: Mapping[str, str], **kwargs) -> None:
    """

    :param qgis_instance_handle:
    :param wkbs:
    :param kwargs:
    :return:
    """
    for layer_name, wkb in wkbs.items():
        add_wkb(qgis_instance_handle, wkb, name=layer_name, **kwargs)


@passes_kws_to(add_wkt)
def add_wkts(qgis_instance_handle: Any, wkts: Mapping[str, str], **kwargs) -> None:
    """

    :param qgis_instance_handle:
    :param wkts:
    :param kwargs:
    :return:
    """
    for layer_name, wkt in wkts.items():
        add_wkt(qgis_instance_handle, wkt, name=layer_name, **kwargs)


@passes_kws_to(add_qgis_geometry)
def add_dataframes(
    qgis_instance_handle: Any, dataframes: Mapping[str, DataFrame], **kwargs
) -> None:
    ...


@passes_kws_to(add_qgis_geometry)
def add_dataframe(qgis_instance_handle: Any, dataframe: DataFrame, **kwargs) -> None:
    """

    :param qgis_instance_handle:
    :param dataframe:
    :param kwargs:
    :return:
    """
    from geopandas import GeoDataFrame
    from jord.geopandas_utilities import split_on_geom_type

    if isinstance(dataframe, GeoDataFrame):
        columns_to_include = ("layer",)
        geom_dict = split_on_geom_type(dataframe)
        for df in geom_dict.values():
            if False:
                for w in df.geometry.to_wkt():
                    add_wkt(qgis_instance_handle, w)
            else:
                for w in df.geometry.to_wkb():
                    add_wkb(qgis_instance_handle, w)

    elif isinstance(dataframe, DataFrame) and False:
        geometry_column = "geometry"
        if isinstance(
            dataframe[geometry_column][0], shapely.geometry.base.BaseGeometry
        ):
            a = dataframe[geometry_column][0]
            # if a.geom_type == "MultiPolygon":

            wkts = [d.wkt for d in dataframe[geometry_column]]
        elif isinstance(dataframe[geometry_column][0], str):
            wkts = dataframe[geometry_column]
        else:
            raise NotImplemented

        for row in wkts:
            add_wkt(qgis_instance_handle, row)
    else:
        if VERBOSE:
            print("SKIP!")


@passes_kws_to(add_qgis_geometry)
def add_geojson(qgis_instance_handle: Any, geojson: str, **kwargs) -> None:
    """

    :param qgis_instance_handle:
    :param dataframe:
    :param kwargs:
    :return:
    """
    geom = shapely.from_geojson(geojson)
    add_shapely_geometry(geom)


def remove_layers(qgis_instance_handle: Any, *args) -> None:
    """
    clear all the added layers

    :param qgis_instance_handle:
    :param args:
    :return:
    """
    qgis_instance_handle.on_clear_temporary()


def clear_all(qgis_instance_handle: Any, *args) -> None:  # TODO: REMOVE THIS!
    """
    clear all the added layers

    :param qgis_instance_handle:
    :return:
    """
    remove_layers(qgis_instance_handle)
    if VERBOSE:
        print("CLEAR ALL!")


def add_shapely_geometry(
    qgis_instance_handle: Any, geom: BaseGeometry, **kwargs
) -> None:
    """
    Add a shapely geometry

    :param qgis_instance_handle:
    :param args:
    :return:
    """

    add_wkt(qgis_instance_handle, geom.wkt)


@passes_kws_to(add_shapely_geometry)
def add_shapely_geometries(
    qgis_instance_handle: Any, geometries: Mapping, **kwargs
) -> None:
    """

    :param qgis_instance_handle:
    :param wkbs:
    :param kwargs:
    :return:
    """
    for layer_name, geometry in geometries.items():
        add_shapely_geometry(qgis_instance_handle, geometry, name=layer_name, **kwargs)


class QliveRPCMethodEnum(Enum):
    # add_layers = add_layers.__name__
    remove_layers = remove_layers.__name__
    clear_all = clear_all.__name__
    add_wkt = add_wkt.__name__
    add_wkb = add_wkb.__name__
    add_wkts = add_wkts.__name__
    add_wkbs = add_wkbs.__name__
    add_dataframe = add_dataframe.__name__
    add_dataframes = add_dataframes.__name__
    add_shapely_geometry = add_shapely_geometry.__name__
    add_shapely_geometries = add_shapely_geometries.__name__
    add_raster = add_raster.__name__
    add_rasters = add_rasters.__name__


funcs = locals()  # In local scope for name
QliveRPCMethodMap = {e: funcs[e.value] for e in QliveRPCMethodEnum}

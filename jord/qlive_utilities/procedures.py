import json
import time
from enum import Enum

__all__ = ["QliveRPCMethodEnum", "QliveRPCMethodMap"]

from typing import Mapping, Any, Tuple, Optional

import geopandas.geodataframe
import numpy
import shapely.geometry.base
from warg import passes_kws_to, Number
from pandas import DataFrame
from shapely.geometry.base import BaseGeometry
from jord.geopandas_utilities import split_on_geom_type

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
    "add_wkb",
    "add_wkts",
    "add_wkbs",
    "add_rasters",
    "add_wkt",
    "add_dataframe",
    "add_geom_layer",
    "clear_all",
    "remove_layers",
]


def add_raster(
    qgis_instance_handle: Any,
    raster: numpy.ndarray,
    name: str = DEFAULT_LAYER_NAME,
    centroid: Tuple[Number, Number] = None,
    extent_tuple: Tuple[Number, Number, Number, Number] = None,
    pixel_size: Tuple[Number, Number] = PIXEL_SIZE,
    crs_str: str = DEFAULT_LAYER_CRS,
    default_value=DEFAULT_NUMBER,
    field: str = None,
) -> None:
    """

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
    from qgis.core import (
        QgsRectangle,
        QgsCoordinateReferenceSystem,
        QgsRasterBlock,
        QgsRasterBandStats,
        QgsSingleBandGrayRenderer,
        QgsMultiBandColorRenderer,
        QgsContrastEnhancement,
        QgsRasterLayer,
        QgsProcessing,
    )
    from jord.qgis_utilities.numpy_utilities.data_type import get_qgis_type
    from qgis import processing

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

    raster_output = processing.run(
        "qgis:createconstantrasterlayer",
        {
            "EXTENT": extent,
            "TARGET_CRS": QgsCoordinateReferenceSystem(crs_str),  # ("EPSG:2180")
            "PIXEL_SIZE": pixel_size,
            "NUMBER": default_value,
            "OUTPUT_TYPE": data_type.value,
            "IGNORE_NODATA": True,
            "OUTPUT_NODATA_VALUE": DEFAULT_NUMBER,
            "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
        },
    )["OUTPUT"]

    if APPEND_TIMESTAMP:
        name += f"_{time.time()}"

    layer = QgsRasterLayer(raster_output, name, "gdal")
    provider = layer.dataProvider()

    if False:
        location = None
        extent = provider.extent()
        xres = (extent.width()) / provider.xSize()
        yres = (extent.height()) / provider.ySize()
        col = int((location.x() - extent.xMinimum()) / xres)
        row = int((location.y() - extent.yMinimum()) / yres)
    elif False:
        raster_extent = provider.extent()
        raster_width = provider.xSize()
        raster_height = provider.ySize()
        no_data_value = provider.srcNoDataValue(1)
    else:
        w = layer.width()
        h = layer.height()

    provider.setEditable(True)
    block = QgsRasterBlock(data_type, w, h)
    # block = provider.block(1, extent, w, h)

    for ith_band in range(0, num_bands):
        if False:
            for i in range(0, w):
                for j in range(0, h):
                    value = raster[i][j][ith_band]
                    if value == numpy.nan:
                        block.setIsNoData(i, j)
                        continue
                    value = int(value) * 255
                    block.setValue(i, j, value)
        elif True:
            for i in range(0, w):
                for j in range(0, h):
                    block.setValue(i, j, raster[i][j][ith_band])
        else:
            block.setData(bytearray(numpy.array(map(lambda x: int(x * 255), raster))))

        if VERBOSE:
            print("writing block on band", ith_band + 1)

        provider.writeBlock(block, band=ith_band + 1)

    provider.setEditable(False)
    provider.reload()

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


def add_geom_layer(
    qgis_instance_handle: Any,
    geom: BaseGeometry,
    name: Optional[str] = None,
    crs: Optional[str] = None,
    fields: Mapping = None,
    index: bool = False,
    categorise_by_attribute: Optional[str] = None,
) -> None:
    """

    An example url is “Point?crs=epsg:4326&field=id:integer&field=name:string(20)&index=yes”

      :param fields: Field=name:type(length,precision) Defines an attribute of the layer. Multiple field parameters can be added to the data provider definition. Type is one of “integer”, “double”, “string”.
      :param index:     index=yes Specifies that the layer will be constructed with a spatial index
      :param qgis_instance_handle:
      :param geom:
      :param name:
      :param crs: Crs=definition Defines the coordinate reference system to use for the layer. Definition is any string accepted by QgsCoordinateReferenceSystem.createFromString()
      :return: None
      :rtype: None
    """

    from qgis.core import QgsVectorLayer, QgsFeature

    # uri = geom.type()
    # uri = geom.wkbType()
    # uri = geom.wktTypeStr()

    uri = json.loads(geom.asJson())["type"]

    if name is None:
        name = DEFAULT_LAYER_NAME

    if crs is None:
        crs = DEFAULT_LAYER_CRS

    layer_name = f"{name}"
    if APPEND_TIMESTAMP:
        layer_name += f"_{time.time()}"

    if uri == "GeometryCollection":
        gm_group = qgis_instance_handle.temporary_group.addGroup(layer_name)

        for g in geom.asGeometryCollection():  # TODO: Look into recursion?
            uri = json.loads(g.asJson())["type"]
            sub_type = uri

            if crs:
                uri += f"?crs={crs}"

            if fields:
                for k, v in fields.items():
                    uri += f"&field={k}:{v}"

            uri += f'&index={"yes" if index else "no"}'

            feat = QgsFeature()
            feat.setGeometry(g)

            sub_layer = QgsVectorLayer(uri, f"{layer_name}_{sub_type}", "memory")
            sub_layer.dataProvider().addFeatures([feat])

            if SKIP_MEMORY_LAYER_CHECK_AT_CLOSE:
                sub_layer.setCustomProperty("skipMemoryLayersCheck", 1)

            qgis_instance_handle.qgis_project.addMapLayer(sub_layer, False)
            gm_group.insertLayer(0, sub_layer)
    else:
        if crs:
            uri += f"?crs={crs}"

        if fields:
            for k, v in fields.items():
                uri += f"&field={k}:{v}"

        uri += f'&index={"yes" if index else "no"}'

        feat = QgsFeature()
        feat.setGeometry(geom)

        layer = QgsVectorLayer(uri, layer_name, "memory")
        layer.dataProvider().addFeatures([feat])

        if SKIP_MEMORY_LAYER_CHECK_AT_CLOSE:
            layer.setCustomProperty("skipMemoryLayersCheck", 1)

        qgis_instance_handle.qgis_project.addMapLayer(layer, False)
        qgis_instance_handle.temporary_group.insertLayer(0, layer)


@passes_kws_to(add_geom_layer)
def add_wkb(qgis_instance_handle: Any, wkb: str, **kwargs) -> None:
    """

    :param qgis_instance_handle:
    :param wkb:
    :param kwargs:
    :return:
    """
    from qgis.core import QgsGeometry

    add_geom_layer(qgis_instance_handle, QgsGeometry.fromWkb(wkb), **kwargs)


@passes_kws_to(add_geom_layer)
def add_wkt(qgis_instance_handle: Any, wkt: str, **kwargs) -> None:
    """

    :param qgis_instance_handle:
    :param wkt:
    :param kwargs:
    :return:
    """
    from qgis.core import QgsGeometry

    add_geom_layer(qgis_instance_handle, QgsGeometry.fromWkt(wkt), **kwargs)


@passes_kws_to(add_wkb)
def add_wkbs(qgis_instance_handle: Any, wkbs: Mapping, **kwargs) -> None:
    """

    :param qgis_instance_handle:
    :param wkbs:
    :param kwargs:
    :return:
    """
    for layer_name, wkb in wkbs.items():
        add_wkb(qgis_instance_handle, wkb, name=layer_name, **kwargs)


@passes_kws_to(add_wkt)
def add_wkts(qgis_instance_handle: Any, wkts: Mapping, **kwargs) -> None:
    """

    :param qgis_instance_handle:
    :param wkts:
    :param kwargs:
    :return:
    """
    for layer_name, wkt in wkts.items():
        add_wkt(qgis_instance_handle, wkt, name=layer_name, **kwargs)


@passes_kws_to(add_geom_layer)
def add_dataframe(qgis_instance_handle: Any, dataframe: DataFrame, **kwargs) -> None:
    """

    :param qgis_instance_handle:
    :param dataframe:
    :param kwargs:
    :return:
    """
    if isinstance(dataframe, geopandas.geodataframe.GeoDataFrame):
        columns_to_include = ("layer",)
        geom_dict = split_on_geom_type(dataframe)
        for df in geom_dict.values():
            add_wkt(qgis_instance_handle, df.to_wkt())
    elif isinstance(dataframe, DataFrame):
        geometry_column = "geometry"
        if isinstance(
            dataframe[geometry_column][0], shapely.geometry.base.BaseGeometry
        ):
            a = dataframe[geometry_column][0]
            wkts = a.geom_type == "MultiPolygon"
            # TODO: Implement
        elif isinstance(dataframe[geometry_column][0], str):
            wkts = dataframe[geometry_column]
        else:
            raise NotImplemented

        for row in wkts:
            add_geom_layer(qgis_instance_handle, row)


def remove_layers(qgis_instance_handle: Any, *args) -> None:
    """

    :param qgis_instance_handle:
    :param args:
    :return:
    """
    qgis_instance_handle.on_clear_temporary()


def clear_all(qgis_instance_handle: Any) -> None:
    """

    :param qgis_instance_handle:
    :return:
    """
    remove_layers(qgis_instance_handle)
    print("CLEAR ALL!")


class QliveRPCMethodEnum(Enum):
    # add_layers = add_layers.__name__
    add_wkt = add_wkt.__name__
    add_wkb = add_wkb.__name__
    add_wkts = add_wkts.__name__
    add_wkbs = add_wkbs.__name__
    add_dataframe = add_dataframe.__name__
    add_raster = add_raster.__name__
    add_rasters = add_rasters.__name__
    remove_layers = remove_layers.__name__
    clear_all = clear_all.__name__


funcs = locals()  # In local scope for name
QliveRPCMethodMap = {e: funcs[e.value] for e in QliveRPCMethodEnum}

import json
import time
from enum import Enum

__all__ = ["QliveRPCMethodEnum", "QliveRPCMethodMap"]

from typing import Mapping, Any

import numpy
from warg import passes_kws_to

APPEND_TIMESTAMP = True
SKIP_MEMORY_LAYER_CHECK_AT_CLOSE = True
DEFAULT_LAYER_NAME = "TemporaryLayer"
DEFAULT_LAYER_CRS = "EPSG:3857"


def add_raster(
    qgis_instance_handle: Any, raster: numpy.ndarray, name: str, crs: str, field: str
) -> None:
    from qgis.core import (
        QgsRectangle,
        QgsCoordinateReferenceSystem,
        QgsRasterBlock,
        QgsRasterBandStats,
        QgsSingleBandGrayRenderer,
        QgsContrastEnhancement,
        QgsRasterLayer,
        QgsProcessing,
    )
    import Qgis
    from qgis import processing

    extent = QgsRectangle()
    extent.setXMinimum(457552.5)
    extent.setYMinimum(248698.5)
    extent.setXMaximum(459804.5)
    extent.setYMaximum(251031.5)
    crs = QgsCoordinateReferenceSystem("EPSG:2180")
    params = {
        "EXTENT": extent,
        "TARGET_CRS": crs,
        "PIXEL_SIZE": 10,
        "NUMBER": 0.5,
        "OUTPUT_TYPE": Qgis.DataType.Byte,
        "OUTPUT": QgsProcessing.TEMPORARY_OUTPUT,
    }
    r = processing.run("qgis:createconstantrasterlayer", params)["OUTPUT"]
    layer = QgsRasterLayer(r, "temp", "gdal")
    provider = layer.dataProvider()

    w = layer.width()
    h = layer.height()

    # dataType = Qgis.DataType.Byte
    dataType = provider.dataType(1)
    block = QgsRasterBlock(dataType, w, h)

    # this is where you would use your numpy array to set value of each and every pixel
    # arr is a random 2-dimensional array with pixel values
    arr = numpy.random.rand(w, h)
    for i in range(0, w):
        for j in range(0, h):
            block.setValue(i, j, int(arr[i][j] * 255))

    # alternative using setData
    # f = lambda x: int(x * 255)
    # data = bytearray(np.array(map(f, arr)))
    # block.setData(data)

    provider.setEditable(True)
    provider.writeBlock(block, band=1)
    provider.setEditable(False)
    provider.reload()

    # this is needed for the min and max value to refresh in the layer panel
    stats = provider.bandStatistics(1, QgsRasterBandStats.All, extent)
    min = stats.minimumValue
    max = stats.maximumValue

    renderer = layer.renderer()
    myType = renderer.dataType(1)
    GrayRenderer = QgsSingleBandGrayRenderer(provider, 1)
    contrastEnhancement = QgsContrastEnhancement.StretchToMinimumMaximum
    myEnhancement = QgsContrastEnhancement()
    myEnhancement.setContrastEnhancementAlgorithm(contrastEnhancement, True)
    myEnhancement.setMinimumValue(min)
    myEnhancement.setMaximumValue(max)
    layer.setRenderer(GrayRenderer)
    layer.renderer().setContrastEnhancement(myEnhancement)

    qgis_instance_handle.qgis_project.addMapLayer(layer, False)
    qgis_instance_handle.temporary_group.insertLayer(0, layer)


@passes_kws_to(add_raster)
def add_rasters(qgis_instance_handle, rasters: Mapping, **kwargs) -> None:
    for layer_name, raster in rasters.items():
        add_raster(qgis_instance_handle, raster, name=layer_name, **kwargs)


def add_geom(
    qgis_instance_handle: Any,
    geom: Any,
    name=None,
    crs=None,
    fields: Mapping = None,
    index: bool = False,
) -> None:
    """
      crs=definition Defines the coordinate reference system to use for the layer. definition is any string accepted by QgsCoordinateReferenceSystem.createFromString()

    index=yes Specifies that the layer will be constructed with a spatial index

    field=name:type(length,precision) Defines an attribute of the layer. Multiple field parameters can be added to the data provider definition. type is one of “integer”, “double”, “string”.

    An example url is “Point?crs=epsg:4326&field=id:integer&field=name:string(20)&index=yes”

      :param fields:
      :param index:
      :param qgis_instance_handle:
      :param geom:
      :param name:
      :param crs:
      :return:"""

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


@passes_kws_to(add_geom)
def add_wkb(qgis_instance_handle: Any, wkb: str, **kwargs) -> None:
    from qgis.core import QgsGeometry

    add_geom(qgis_instance_handle, QgsGeometry.fromWkb(wkb), **kwargs)


@passes_kws_to(add_geom)
def add_wkt(qgis_instance_handle: Any, wkt: str, **kwargs) -> None:
    from qgis.core import QgsGeometry

    add_geom(qgis_instance_handle, QgsGeometry.fromWkt(wkt), **kwargs)


@passes_kws_to(add_wkb)
def add_wkbs(qgis_instance_handle: Any, wkbs: Mapping, **kwargs) -> None:
    for layer_name, wkb in wkbs.items():
        add_wkb(qgis_instance_handle, wkb, name=layer_name, **kwargs)


@passes_kws_to(add_wkt)
def add_wkts(qgis_instance_handle: Any, wkts: Mapping, **kwargs) -> None:
    for layer_name, wkt in wkts.items():
        add_wkt(qgis_instance_handle, wkt, name=layer_name, **kwargs)


def remove_layers(qgis_instance_handle: Any, *args) -> None:
    qgis_instance_handle.on_clear_temporary()


def clear_all(qgis_instance_handle: Any) -> None:
    remove_layers(qgis_instance_handle)
    print("CLEAR ALL!")


class QliveRPCMethodEnum(Enum):
    # add_layers = add_layers.__name__
    add_wkt = add_wkt.__name__
    add_wkb = add_wkb.__name__
    add_wkts = add_wkts.__name__
    add_wkbs = add_wkbs.__name__
    add_raster = add_raster.__name__
    add_rasters = add_rasters.__name__
    remove_layers = remove_layers.__name__
    clear_all = clear_all.__name__


funcs = locals()  # In local scope for name
QliveRPCMethodMap = {e: funcs[e.value] for e in QliveRPCMethodEnum}

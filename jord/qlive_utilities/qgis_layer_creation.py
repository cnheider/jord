import json
import time
from typing import Any, Optional, Mapping

from warg import passes_kws_to

from jord.geojson_utilities import GeoJsonGeometryTypesEnum

APPEND_TIMESTAMP = True
SKIP_MEMORY_LAYER_CHECK_AT_CLOSE = True
PIXEL_SIZE = 1
DEFAULT_NUMBER = 0
CONTRAST_ENHANCE = True
DEFAULT_LAYER_NAME = "TemporaryLayer"
DEFAULT_LAYER_CRS = "EPSG:4326"
VERBOSE = False


__all__ = ["add_qgis_geometry", "add_qgis_geometries"]


def add_qgis_geometry(
    qgis_instance_handle: Any,
    geom,  #: QgsGeometry,
    name: Optional[str] = None,
    crs: Optional[str] = None,
    fields: Mapping[str, Any] = None,
    index: bool = False,
    categorise_by_attribute: Optional[str] = None,
) -> None:
    """
    An example url is “Point?crs=epsg:4326&field=id:integer&field=name:string(20)&index=yes”

    :param fields: Field=name:type(length,precision) Defines an attribute of the layer. Multiple field parameters can be added to the data provider definition. Type is one of “integer”, “double”, “string”.
    :param index: index=yes Specifies that the layer will be constructed with a spatial index
    :param qgis_instance_handle:
    :param geom:
    :type geom: QgsGeometry
    :param name:
    :type name: Optional[str]
    :param crs: Crs=definition Defines the coordinate reference system to use for the layer. Definition is any string accepted by QgsCoordinateReferenceSystem.createFromString()
    :return: None
    :rtype: None
    """
    # noinspection PyUnresolvedReferences
    from qgis.core import QgsVectorLayer, QgsFeature

    # uri = geom.type()
    # uri = geom.wkbType()
    # uri = geom.wktTypeStr()

    geom_type = json.loads(geom.asJson())["type"]
    uri = geom_type

    if name is None:
        name = DEFAULT_LAYER_NAME

    if crs is None:
        crs = DEFAULT_LAYER_CRS

    layer_name = f"{name}"
    if APPEND_TIMESTAMP:
        layer_name += f"_{time.time()}"

    if geom_type == GeoJsonGeometryTypesEnum.geometry_collection.value.__name__:
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
    elif geom_type == GeoJsonGeometryTypesEnum.multi_point.value.__name__:
        ...
    elif geom_type == GeoJsonGeometryTypesEnum.multi_line_string.value.__name__:
        ...
    elif geom_type == GeoJsonGeometryTypesEnum.multi_polygon.value.__name__:
        gm_group = qgis_instance_handle.temporary_group.addGroup(layer_name)

        g = geom
        uri = json.loads(g.asJson())["type"]
        sub_type = uri

        if crs:
            uri += f"?crs={crs}"

        if fields:
            for k, v in fields.items():
                uri += f"&field={k}:{v}"

        uri += f'&index={"yes" if index else "no"}'

        sub_layer = QgsVectorLayer(uri, f"{layer_name}_{sub_type}", "memory")

        features = []
        for g_ in [g]:
            feat = QgsFeature()
            feat.setGeometry(g_)
            features.append(feat)

        sub_layer.dataProvider().addFeatures(features)

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


@passes_kws_to(add_qgis_geometry)
def add_qgis_geometries(
    qgis_instance_handle: Any, geoms, **kwargs  # Mapping[str, QgsGeometry]
) -> None:
    for name, geom in geoms.items():
        add_qgis_geometry(qgis_instance_handle, geom, name, **kwargs)

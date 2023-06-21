from enum import Enum

from geojson import (
    Point,
    LineString,
    Polygon,
    MultiPoint,
    MultiLineString,
    MultiPolygon,
    GeometryCollection,
)


__all__ = ["GeoJsonGeometryTypesEnum"]


class GeoJsonGeometryTypesEnum(Enum):
    """
    This enum is useful for exhaustively iterating possible geojson types.
    """

    point = Point  #

    line_string = LineString  #

    polygon = Polygon  #

    multi_point = MultiPoint  #

    multi_line_string = MultiLineString  #

    multi_polygon = MultiPolygon  #

    geometry_collection = GeometryCollection  #

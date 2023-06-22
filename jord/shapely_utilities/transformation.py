from typing import List, Sequence
from shapely.geometry.base import BaseGeometry
from shapely.ops import transform
import pyproj

__all__ = ["crs_transform_shapely"]


def crs_transform_shapely(
    geoms: Sequence[BaseGeometry],
    from_coordinate_system: str,
    to_coordinate_system: str,
) -> List[BaseGeometry]:
    """
    Project space geometries from one coordinate system to another

    :param geoms: A list of SpacePolygons to project
    :param from_coordinate_system: The source coordinate system
    :param to_coordinate_system: The destination coordinate system
    :return: A list of SpacePolygons projected
    """

    source = pyproj.CRS(from_coordinate_system)
    destination = pyproj.CRS(to_coordinate_system)
    projection = pyproj.Transformer.from_crs(
        source, destination, always_xy=True
    ).transform

    return [transform(projection, geometry) for geometry in geoms]

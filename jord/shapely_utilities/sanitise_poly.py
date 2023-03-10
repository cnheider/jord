from typing import Union


from shapely.geometry.base import BaseGeometry
from shapely.geometry import MultiPolygon, LineString, Polygon, Point

__all__ = ["zero_buffer", "sanitise", "deflimmer"]

from jord.shapely_utilities.morphology import opening, closing


def zero_buffer(
    geom: BaseGeometry,
) -> Union[
    BaseGeometry
    # Point,
    # LineString,
    # Polygon,
    # MultiPolygon
]:
    return geom.buffer(0)


def deflimmer(geom: BaseGeometry, eps: float = 1e-7) -> BaseGeometry:
    return opening(closing(geom, eps), eps)


def std_dev_line_length():
    ...  # get std_dev of line length in geometry


def std_dev_area():
    ...  # get std_dev of areas in geometry


def filter_area():
    ...


def sanitise(geom: BaseGeometry, *args: callable) -> BaseGeometry:
    """

    #A positive distance produces a dilation, a negative distance an erosion. A very small or zero distance may sometimes be used to “tidy” a polygon.



    """

    if not len(args):
        args = (zero_buffer, deflimmer)

    for f in args:
        geom = f(geom)

    return geom


if __name__ == "__main__":

    def aishdjauisd():
        # Import constructors for creating geometry collections
        from shapely.geometry import MultiPoint, MultiLineString, MultiPolygon

        # Import necessary geometric objects from shapely module
        from shapely.geometry import Point, LineString, Polygon

        # Create Point geometric object(s) with coordinates
        point1 = Point(2.2, 4.2)
        point2 = Point(7.2, -25.1)
        point3 = Point(9.26, -2.456)
        # point3D = Point(9.26, -2.456, 0.57)

        # Create a MultiPoint object of our points 1,2 and 3
        multi_point = MultiPoint([point1, point2, point3])

        # It is also possible to pass coordinate tuples inside
        multi_point2 = MultiPoint([(2.2, 4.2), (7.2, -25.1), (9.26, -2.456)])

        # We can also create a MultiLineString with two lines
        line1 = LineString([point1, point2])
        line2 = LineString([point2, point3])
        multi_line = MultiLineString([line1, line2])
        polygon = Polygon([point2, point1, point3])

        from shapely.geometry import GeometryCollection
        from matplotlib import pyplot
        import geopandas as gpd

        geoms = GeometryCollection([multi_point, multi_point2, multi_line, polygon])
        geoms = sanitise(geoms)

        p = gpd.GeoSeries(geoms)
        p.plot()
        pyplot.show()

    aishdjauisd()

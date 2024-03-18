import numpy
from qgis.PyQt import QtGui
from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsPoint

__all__ = ["get_qimage_from_numpy"]


def get_qimage_from_numpy(img, debug=False) -> QtGui.QImage:
    # if isinstance(img, Image):
    #    img = img.data
    # if isinstance(img, numpy.ndarray):
    #    img = img.data

    # if isinstance(img, cv2.Image):
    #    img = img.data # QtGui.QImage.Format_BGR888
    # aformat = QImage.Format_RGB32

    img = img.data
    height, width, channels = img.shape
    if debug:
        print(f"height: {height}, width: {width}, channels: {channels}")
    bytes_per_line = channels * width
    img = numpy.require(img, numpy.uint8, "C")
    return QtGui.QImage(img, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)


def transform_coordinates(coordinates, fromCRS, toCRS) -> list:
    """

    function to transform a set of coordinates from one CRS to another"""
    crs_src = QgsCoordinateReferenceSystem(fromCRS)
    crs_dest = QgsCoordinateReferenceSystem(toCRS)
    xform = QgsCoordinateTransform(crs_src, crs_dest)

    coordinates_as_points = [
        QgsPoint(coordinates[0], coordinates[1]),
        QgsPoint(coordinates[2], coordinates[3]),
    ]  # convert list of coordinates to QgsPoint objects

    transformed_coordinates_as_points = [
        xform.transform(point) for point in coordinates_as_points
    ]  # do transformation for each point

    return [
        transformed_coordinates_as_points[0].x(),
        transformed_coordinates_as_points[0].y(),
        transformed_coordinates_as_points[1].x(),
        transformed_coordinates_as_points[1].y(),
    ]  # transform the QgsPoint objects back to a list of coordinates


def get_coordinates_of_layer_extent(layer) -> list:
    """

    function to get coordinates of a layer extent

    """

    layerRectangle = layer.extent()

    return [
        layerRectangle.xMinimum(),
        layerRectangle.yMinimum(),
        layerRectangle.xMaximum(),
        layerRectangle.yMaximum(),
    ]

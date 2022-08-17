import time

import numpy
from qgis.PyQt import QtGui, QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal, Qt
from qgis.core import QgsGeometry
from qgis.core import QgsVectorLayer, QgsCoordinateReferenceSystem, QgsProject


__all__ = ["qt_draw_timestamp"]


def qt_draw_timestamp(
    image,
    font_size=10,
    font_color=(255, 255, 255),
    font_family="Arial",
    font_style=QtGui.QFont.StyleNormal,
    font_weight=QtGui.QFont.Normal,
):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    font = QtGui.QFont(font_family, font_size, font_style, font_weight)
    font.setPixelSize(font_size)
    font.setBold(True)
    painter = QtGui.QPainter(image)
    painter.setFont(font)
    painter.setPen(QtGui.QColor(*font_color))
    painter.drawText(
        0,
        0,
        image.width(),
        image.height(),
        Qt.AlignCenter,
        timestamp,
    )
    painter.end()

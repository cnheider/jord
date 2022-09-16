# !/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 02-12-2020
           """

from qgis.PyQt import QtCore

__all__ = ["MyTableModel"]


class MyTableModel(QtCore.QAbstractTableModel):
    """
    A model that can be used to display a table of data.

    :param data: The data to display.
    :param parent: The parent object.

    """

    def __init__(self, data=(()), parent=None):
        super().__init__(parent)
        self.data = data

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return f"Column {str(section)}"
            else:
                return f"Row {str(section)}"

    def columnCount(self, parent=None):
        if self.rowCount():
            return len(self.data[0])
        return 0

    def rowCount(self, parent=None):
        return len(self.data)

    def data(self, index: QtCore.QModelIndex, role: int):
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            col = index.column()
            return str(self.data[row][col])

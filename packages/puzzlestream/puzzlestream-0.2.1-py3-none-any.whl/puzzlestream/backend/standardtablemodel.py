# -*- coding: utf-8 -*-
"""Puzzle Stream standard table model module.

contains PSStandardTableModel
"""

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore


class PSStandardTableModel(QtCore.QAbstractTableModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__keys, self.__data = [], []
        self.createKeyList()

    def createKeyList(self):
        keys = []

        for key in self.__data:
            if (isinstance(self.__data[key], np.ndarray) and
                    len(self.__data[key].shape) == 1):
                keys.append(key)

        self.__keys = sorted(keys)

    @property
    def keys(self):
        return self.__keys

    def addColumn(self, key, data):
        self.__keys.append(key)
        self.__keys.sort()
        self.__data.insert(self.__keys.index(key), data)

    def deleteColumn(self, key):
        index = self.__keys.index(key)
        del self.__keys[index], self.__data[index]

    def getColumn(self, index):
        if isinstance(index, str):
            return self.__data[index]
        else:
            index = self.__keys.index(index)
            return self.__data[index]

    def getPlotWidget(self, column):
        data = self.__data[column]

        try:
            w = pg.PlotWidget()
            w.getViewBox().setBackgroundColor("w")
            w.getPlotItem().hideAxis("bottom")
            w.getPlotItem().hideAxis("left")
            w.getPlotItem().hideButtons()
            w.getPlotItem().setMenuEnabled(False)
            w.getPlotItem().setMouseEnabled(False, False)
            w.getPlotItem().plot(np.arange(len(data)), data,
                                 pen=pg.mkPen("k"))
            return w
        except Exception:
            pass
        return None

    def rowCount(self, parent=None):
        counts = [len(item) for item in self.__data]
        if len(counts) > 0:
            return max(counts) + 1
        return 0

    def columnCount(self, parent=None):
        return len(self.keys)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                row = index.row()
                col = index.column()
                if row > 0 and row < len(self.__data[col]) + 1:
                    return QtCore.QVariant(str(self.getItemAt(row, col)))
        return QtCore.QVariant()

    def getItemAt(self, row, column):
        if row - 1 < len(self.__data[column]):
            return self.__data[column][row - 1]
        return None

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return QtCore.QVariant(self.__keys[section])
            else:
                if section > 0:
                    return QtCore.QVariant(section - 1)
        return QtCore.QVariant()

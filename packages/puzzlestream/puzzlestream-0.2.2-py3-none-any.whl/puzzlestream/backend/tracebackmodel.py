from PyQt5 import QtCore, QtGui
import os

from puzzlestream.backend.reference import PSCacheReference


class PSTracebackModel(QtCore.QAbstractListModel):

    def __init__(self, key, stream, modules):
        super().__init__()
        self.__key, self.__stream, self.__modules = key, stream, modules

        currentDir = os.path.dirname(__file__)
        self.__downIcon = QtGui.QIcon(
            os.path.join(currentDir, "../icons//down-arrow.svg"))
        self.__updateTraceback()

    def __splitKey(self, key):
        ID = key.split("-")[0]
        return int(ID), key.replace(ID + "-", "")

    def __updateTraceback(self):
        continueTraceback = True
        currentID, baseKey = self.__splitKey(self.__key)
        currentKey = self.__key
        self.__idList, self.__nameList = [], []

        while continueTraceback:
            if currentID in self.__modules:
                self.__idList.insert(0, currentID)
                self.__nameList.insert(0, str(self.__modules[currentID]))

            if isinstance(self.__stream[currentKey], PSCacheReference):
                currentID = int(self.__stream[currentKey])
                currentKey = str(currentID) + "-" + baseKey
            else:
                continueTraceback = False

    def rowCount(self, parent=None):
        return 2 * len(self.__nameList) - 1

    def columnCount(self, parent=None):
        return 1

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            row = index.row()
            col = index.column()

            if col == 0:
                if row % 2 == 0 and role == QtCore.Qt.DisplayRole:
                    return QtCore.QVariant(self.__nameList[int(row / 2)])
                elif row % 2 != 0 and role == QtCore.Qt.DecorationRole:
                    return self.__downIcon
        return QtCore.QVariant()

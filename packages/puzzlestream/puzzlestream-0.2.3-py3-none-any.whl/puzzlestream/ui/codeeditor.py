from pyqode.python.widgets import PyCodeEdit
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence


class PSCodeEdit(PyCodeEdit):

    def __init__(self, server_script=None, args=None):
        super().__init__(server_script=server_script, args=args)

        # shortcuts
        self.__shortcuts = {}

    def addShortcut(self, sequence, target):
        sc = QShortcut(QKeySequence(sequence), self)
        sc.activated.connect(target)
        self.__shortcuts[sequence] = sc

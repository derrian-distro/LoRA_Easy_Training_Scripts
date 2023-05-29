from PySide6 import QtWidgets
from PySide6 import QtGui
from PySide6 import QtCore


class LineEditWithHighlight(QtWidgets.QLineEdit):
    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super(LineEditWithHighlight, self).__init__(parent)
        self.highlight = True

    def focusInEvent(self, arg__1: QtGui.QFocusEvent) -> None:
        if not self.highlight or len(self.text()) == 0:
            super(LineEditWithHighlight, self).focusInEvent(arg__1)
        else:
            QtCore.QTimer.singleShot(0, self.selectAll)

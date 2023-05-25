from PySide6 import QtWidgets, QtGui, QtCore


class SpinBox(QtWidgets.QSpinBox):
    def __init__(self, parent: QtWidgets.QWidget = None):
        super(SpinBox, self).__init__(parent)
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        if self.hasFocus():
            super(SpinBox, self).wheelEvent(event)
        else:
            event.setAccepted(False)


class DoubleSpinBox(QtWidgets.QDoubleSpinBox):
    def __init__(self, parent: QtWidgets.QWidget = None):
        super(DoubleSpinBox, self).__init__(parent)
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        if self.hasFocus():
            super(DoubleSpinBox, self).wheelEvent(event)
        else:
            event.setAccepted(False)

class ComboBox(QtWidgets.QComboBox):
    def __init__(self, parent: QtWidgets.QWidget = None):
        super(ComboBox, self).__init__(parent)
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        if self.hasFocus():
            super(ComboBox, self).wheelEvent(event)
        else:
            event.setAccepted(False)
            
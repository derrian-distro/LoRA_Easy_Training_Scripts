from PySide6 import QtWidgets, QtGui, QtCore


class SpinBox(QtWidgets.QSpinBox):
    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super(SpinBox, self).__init__(parent)
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        if not self.hasFocus():
            event.setAccepted(False)
            return
        super(SpinBox, self).wheelEvent(event)


class DoubleSpinBox(QtWidgets.QDoubleSpinBox):
    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super(DoubleSpinBox, self).__init__(parent)
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        if not self.hasFocus():
            event.setAccepted(False)
            return
        super(DoubleSpinBox, self).wheelEvent(event)


class ComboBox(QtWidgets.QComboBox):
    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super(ComboBox, self).__init__(parent)
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        if not self.hasFocus():
            event.setAccepted(False)
            return
        super(ComboBox, self).wheelEvent(event)

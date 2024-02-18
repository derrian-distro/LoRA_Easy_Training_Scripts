from PySide6 import QtWidgets, QtCore, QtGui
from pathlib import Path
import time


class QueueItem(QtWidgets.QPushButton):
    QueueSelected = QtCore.Signal(object)

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super(QueueItem, self).__init__(parent)
        self.queue_file = Path(f"queue_store/{time.time_ns()}.toml")
        self.setCheckable(True)
        self.setChecked(False)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        self.clicked.connect(self.get_queue_file)

    @QtCore.Slot()
    def get_queue_file(self) -> None:
        if self.isChecked():
            self.QueueSelected.emit(self)

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        if self.isChecked():
            return
        super(QueueItem, self).mousePressEvent(e)

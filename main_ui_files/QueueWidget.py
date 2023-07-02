import os
from PySide6 import QtWidgets, QtCore, QtGui
from modules.QueueItem import QueueItem
from ui_files.QueueUI import Ui_queue_ui
import time


class QueueWidget(QtWidgets.QWidget):
    saveQueue = QtCore.Signal(str)
    loadQueue = QtCore.Signal(str)

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super(QueueWidget, self).__init__(parent)
        self.selected = None
        self.elements: list[QueueItem] = []
        self.widget = Ui_queue_ui()
        self.widget.setupUi(self)
        self.widget.add_to_queue_button.clicked.connect(self.add_to_queue)
        self.widget.remove_from_queue_button.clicked.connect(self.remove_from_queue)
        self.widget.queue_scroll_widget.layout().setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        self.widget.left_arrow.setIcon(QtGui.QIcon(os.path.join("icons", "chevron-left.svg")))
        self.widget.left_arrow.clicked.connect(lambda: self.change_position(True))
        self.widget.right_arrow.setIcon(QtGui.QIcon(os.path.join("icons", "chevron-right.svg")))
        self.widget.right_arrow.clicked.connect(lambda: self.change_position(False))

    def add_to_queue(self) -> None:
        new_item = QueueItem()
        new_item.queue_file = f"{time.time_ns()}"
        new_item.QueueSelected.connect(self.update_selected)
        new_item.setText("Unnamed" if not self.widget.queue_name.text() else self.widget.queue_name.text())
        self.elements.append(new_item)
        self.selected = None
        self.uncheck_elements(True)
        self.widget.queue_scroll_widget.layout().addWidget(new_item)
        self.saveQueue.emit(new_item.queue_file)

    def remove_from_queue(self) -> None:
        if not self.selected:
            return
        if os.path.exists(os.path.join("runtime_store", f"{self.selected.queue_file}.toml")):
            os.remove(os.path.join("runtime_store", f"{self.selected.queue_file}.toml"))
        self.widget.queue_scroll_widget.layout().removeWidget(self.selected)
        self.elements.remove(self.selected)
        self.selected.deleteLater()
        self.widget.queue_scroll_widget.layout().update()
        self.selected = None

    def remove_first_from_queue(self) -> None:
        elem = self.elements[0]
        if elem == self.selected:
            self.selected = None
            self.uncheck_elements()
        self.widget.queue_scroll_widget.layout().removeWidget(elem)
        self.elements.remove(elem)
        elem.deleteLater()
        self.widget.queue_scroll_widget.layout().update()

    def uncheck_elements(self, skip_save: bool = False) -> None:
        for elem in self.elements:
            if elem.isChecked() and elem is not self.selected:
                elem.setChecked(False)
                if not skip_save:
                    self.saveQueue.emit(elem.queue_file)

    @QtCore.Slot(object)
    def update_selected(self, widget: QueueItem) -> None:
        self.selected = widget
        self.uncheck_elements()
        self.selected.setChecked(True)
        self.loadQueue.emit(widget.queue_file)

    @QtCore.Slot(bool)
    def change_position(self, left: bool) -> None:
        if not self.selected:
            return
        index = self.elements.index(self.selected)
        if left and index == 0:
            return
        if not left and index == len(self.elements) - 1:
            return
        if left:
            self.elements[index - 1], self.elements[index] = self.elements[index], self.elements[index - 1]
        else:
            self.elements[index + 1], self.elements[index] = self.elements[index], self.elements[index + 1]
        self.update_layout()

    def update_layout(self) -> None:
        for elem in self.elements:
            self.widget.queue_scroll_widget.layout().removeWidget(elem)
        for elem in self.elements:
            self.widget.queue_scroll_widget.layout().addWidget(elem)

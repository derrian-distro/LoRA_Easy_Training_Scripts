import os
from PySide6 import QtCore
from pathlib import Path
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout
from modules.QueueItem import QueueItem
from ui_files.QueueUIVertical import Ui_queue_ui


class QueueWidget(QWidget):
    saveQueue = QtCore.Signal(Path)
    loadQueue = QtCore.Signal(Path)

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.selected = None
        self.elements: list[QueueItem] = []
        self.widget = Ui_queue_ui()
        self.content = QWidget()

        self.setup_widget()
        self.setup_connections()
        if not Path("queue_store").exists():
            Path("queue_store").mkdir()

    def setup_widget(self) -> None:
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.content)
        self.widget.setupUi(self.content)
        self.widget.top_arrow.setIcon(QIcon(str(Path("icons/chevron-up.svg"))))
        self.widget.bottom_arrow.setIcon(QIcon(str(Path("icons/chevron-down.svg"))))
        self.widget.queue_scroll_widget.layout().setAlignment(
            QtCore.Qt.AlignmentFlag.AlignTop
        )

    def setup_connections(self) -> None:
        self.widget.add_to_queue_button.clicked.connect(self.add_to_queue)
        self.widget.remove_from_queue_button.clicked.connect(self.remove_from_queue)
        self.widget.top_arrow.clicked.connect(lambda: self.change_position(up=True))
        self.widget.bottom_arrow.clicked.connect(lambda: self.change_position(up=False))

    def add_to_queue(self) -> None:
        new_item = QueueItem()
        new_item.QueueSelected.connect(self.update_selected)
        new_item.setText(self.widget.queue_name.text() or "Unnamed")
        self.elements.append(new_item)
        self.selected = new_item
        new_item.setChecked(True)
        self.uncheck_elements(True)
        self.widget.queue_scroll_widget.layout().addWidget(new_item)
        self.saveQueue.emit(new_item.queue_file)

    def remove_from_queue(self) -> None:
        if not self.selected:
            return
        file = self.selected.queue_file
        if file.exists():
            os.remove(file)
        self.elements.remove(self.selected)
        self.widget.queue_scroll_widget.layout().removeWidget(self.selected)
        self.selected.deleteLater()
        self.widget.queue_scroll_widget.layout().update()
        if self.elements:
            self.selected = self.elements[0]
            self.elements[0].setChecked(True)
            self.loadQueue.emit(self.elements[0].queue_file)
        else:
            self.selected = False

    def remove_first_from_queue(self) -> None:
        elem = self.elements[0]
        if elem == self.selected:
            self.selected = False
            self.uncheck_elements(True)
        self.widget.queue_scroll_widget.layout().removeWidget(elem)
        self.elements.remove(elem)
        elem.deleteLater()
        self.widget.queue_scroll_widget.layout().update()

    def update_selected(self, elem: QueueItem) -> None:
        self.selected = elem
        self.uncheck_elements()
        self.selected.setChecked(True)
        self.loadQueue.emit(elem.queue_file)

    def uncheck_elements(self, skip_save: bool = False) -> None:
        for elem in self.elements:
            if elem.isChecked() and elem is not self.selected:
                elem.setChecked(False)
                if not skip_save:
                    self.saveQueue.emit(elem.queue_file)

    def change_position(self, up: bool) -> None:
        if not self.selected:
            return
        index = self.elements.index(self.selected)
        if up and index == 0:
            return
        if not up and index == len(self.elements) - 1:
            return
        self.elements[index + (-1 if up else 1)], self.elements[index] = (
            self.elements[index],
            self.elements[index + (-1 if up else 1)],
        )
        self.update_layout()

    def update_layout(self) -> None:
        for elem in self.elements:
            self.widget.queue_scroll_widget.layout().removeWidget(elem)
        for elem in self.elements:
            self.widget.queue_scroll_widget.layout().addWidget(elem)

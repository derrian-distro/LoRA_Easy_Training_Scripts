from pathlib import Path

from PySide6 import QtWidgets, QtGui
from PySide6 import QtCore


class CollapsibleWidget(QtWidgets.QWidget):
    toggled = QtCore.Signal(bool)

    def __init__(
        self,
        parent: QtWidgets.QWidget = None,
        title: str = "",
        remove_elem: bool = False,
        enable: bool = False,
    ) -> None:
        super(CollapsibleWidget, self).__init__(parent)
        self.is_collapsed = True
        self.has_remove = remove_elem
        self.has_enable = enable
        self.widget_list = {}
        self.setLayout(QtWidgets.QGridLayout())

        self.content = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QVBoxLayout()
        self.content.setLayout(self.content_layout)
        self.content.setVisible(False)

        self.title_frame = CollapsibleButton(title=title)
        self.title_frame.clicked.connect(self.toggle_collapsed)

        self.layout().addWidget(self.title_frame, 0, 0, 1, 1)

        if self.has_remove:
            self.set_extra()
        elif self.has_enable:
            self.set_extra("enable")
        else:
            self.extra_elem = None
            self.layout().addWidget(self.content, 1, 0, 1, 1)

    def add_widget(self, widget: QtWidgets.QWidget, name: str) -> None:
        if name in self.widget_list:
            return
        self.widget_list[name] = widget
        self.content_layout.addWidget(widget)

    def remove_widget(self, name: str) -> None:
        if name not in self.widget_list:
            return
        temp = self.widget_list.pop(name)
        self.content_layout.removeWidget(temp)
        temp.deleteLater()
        self.content_layout.update()

    def set_extra(self, mode: str = "remove"):
        if mode == "enable":
            self.extra_elem = QtWidgets.QPushButton()
            self.extra_elem.setSizePolicy(
                QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Fixed
            )
            self.extra_elem.setCheckable(True)
            self.extra_elem.setChecked(False)
            self.extra_elem.setIcon(QtGui.QIcon(str(Path("icons/check.svg"))))
            self.extra_elem.clicked.connect(self.enable_disable)
            self.layout().addWidget(self.extra_elem, 0, 1, 1, 1)
            self.layout().addWidget(self.content, 1, 0, 1, 2)
        elif mode == "remove":
            self.extra_elem = QtWidgets.QPushButton()
            self.extra_elem.setSizePolicy(
                QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Fixed
            )
            self.extra_elem.setIcon(QtGui.QIcon(str(Path("icons/trash-2.svg"))))
            self.layout().addWidget(self.extra_elem, 0, 1, 1, 1)
            self.layout().addWidget(self.content, 1, 0, 1, 2)

    @QtCore.Slot()
    def toggle_collapsed(self) -> None:
        self.content.setVisible(self.is_collapsed)
        self.is_collapsed = not self.is_collapsed
        self.title_frame.update_arrow(self.is_collapsed)

    @QtCore.Slot(bool)
    def enable_disable(self, checked: bool) -> None:
        if not checked:
            if not self.is_collapsed:
                self.title_frame.click()
            self.title_frame.setEnabled(False)
        else:
            self.title_frame.setEnabled(True)
        self.toggled.emit(checked)

    def set_title(self, title: str) -> None:
        self.title_frame.set_title(title)


class CollapsibleButton(QtWidgets.QPushButton):
    def __init__(self, parent: QtWidgets.QWidget = None, title: str = "") -> None:
        super(CollapsibleButton, self).__init__(parent)
        self.setCheckable(True)
        self.setChecked(False)
        self.setText(title)
        self.setStyleSheet(
            """
            QPushButton {
                text-align: left
            }
        """
        )
        self.update_arrow()
        self.setMinimumHeight(40)

    def update_arrow(self, is_collapsed: bool = True) -> None:
        if is_collapsed:
            self.setIcon(QtGui.QIcon(str(Path("icons/chevron-right.svg"))))
        else:
            self.setIcon(QtGui.QIcon(str(Path("icons/chevron-down.svg"))))

    def set_title(self, title: str) -> None:
        self.setText(title)

import os.path

from PySide6 import QtWidgets, QtGui
from PySide6 import QtCore


class CollapsibleWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget = None, title: str = "", remove_elem: bool = False) -> None:
        super(CollapsibleWidget, self).__init__(parent)
        self.is_collapsed = True
        self.has_remove = remove_elem
        self.widget_list = {}

        self.content = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QVBoxLayout()
        self.content.setLayout(self.content_layout)
        self.content.setVisible(False)

        self.title_frame = CollapsibleButton(title=title)
        self.title_frame.clicked.connect(self.toggle_collapsed)

        if self.has_remove:
            self.extra_elem = QtWidgets.QPushButton()
            self.extra_elem.setIcon(QtGui.QIcon(os.path.join("icons", "trash-2.svg")))
            self.extra_elem.setSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Fixed)
        else:
            self.extra_elem = None

        self.setLayout(QtWidgets.QGridLayout())
        self.layout().addWidget(self.title_frame, 0, 0, 1, 1)
        if self.has_remove:
            self.layout().addWidget(self.extra_elem, 0, 1, 1, 1)
        self.layout().addWidget(self.content, 1, 0, 1, 2 if self.has_remove else 1)

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

    @QtCore.Slot()
    def toggle_collapsed(self) -> None:
        self.content.setVisible(self.is_collapsed)
        self.is_collapsed = not self.is_collapsed
        self.title_frame.update_arrow(self.is_collapsed)


class CollapsibleButton(QtWidgets.QPushButton):
    def __init__(self, parent: QtWidgets.QWidget = None, title: str = "") -> None:
        super(CollapsibleButton, self).__init__(parent)
        self.setCheckable(True)
        self.setChecked(False)
        self.setText(title)
        self.setStyleSheet('''
            QPushButton {
                text-align: left
            }
        ''')
        self.update_arrow()
        self.setMinimumHeight(40)

    def update_arrow(self, is_collapsed: bool = True) -> None:
        if is_collapsed:
            self.setIcon(QtGui.QIcon(os.path.join("icons", "chevron-right.svg")))
        else:
            self.setIcon(QtGui.QIcon(os.path.join("icons", "chevron-down.svg")))

import os.path

from PySide6 import QtCore, QtWidgets, QtGui
from modules.LineEditHighlight import LineEditWithHighlight


class OptimizerItem(QtWidgets.QWidget):
    delete_item = QtCore.Signal(object)
    item_updated = QtCore.Signal()

    def __init__(
        self,
        parent: QtWidgets.QWidget = None,
        arg_name: str = None,
        arg_value: str = None,
    ):
        super(OptimizerItem, self).__init__(parent)
        self.arg_name = arg_name
        self.arg_value = arg_value
        self.arg_name_input = LineEditWithHighlight()
        self.arg_name_input.setToolTip("There is no error checking on this.")
        self.arg_name_input.setPlaceholderText("enter arg name")
        self.arg_name_input.setText(self.arg_name or "")
        self.arg_value_input = LineEditWithHighlight()
        self.arg_value_input.setToolTip("There is no error checking on this.")
        self.arg_value_input.setText(self.arg_value or "")
        self.arg_value_input.setPlaceholderText("enter arg value")
        self.delete_button = QtWidgets.QPushButton()
        self.delete_button.setIcon(QtGui.QIcon(os.path.join("icons", "trash-2.svg")))
        self.delete_button.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Preferred
        )
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().addWidget(self.arg_name_input)
        self.layout().addWidget(self.arg_value_input)
        self.layout().addWidget(self.delete_button)
        self.arg_name_input.textChanged.connect(self.name_edited)
        self.arg_value_input.textChanged.connect(self.value_edited)
        self.delete_button.clicked.connect(self.delete_clicked)

    @QtCore.Slot(str)
    def name_edited(self, value: str):
        self.arg_name = value
        self.item_updated.emit()

    @QtCore.Slot(str)
    def value_edited(self, value: str):
        self.arg_value = value
        self.item_updated.emit()

    @QtCore.Slot()
    def delete_clicked(self):
        self.delete_item.emit(self)

    def get_arg(self):
        return self.arg_name, self.arg_value

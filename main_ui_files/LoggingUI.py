import os.path

from PySide6 import QtCore, QtWidgets, QtGui

import modules.DragDropLineEdit
from ui_files.LoggingUI import Ui_logging_ui
from modules.CollapsibleWidget import CollapsibleWidget
from modules.LineEditHighlight import LineEditWithHighlight


class LoggingWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super(LoggingWidget, self).__init__(parent)
        self.setLayout(QtWidgets.QVBoxLayout())

        self.args = {}
        self.name = "logging_args"
        self.edited_previously = False
        self.colap = CollapsibleWidget(self, "Logging Args")
        self.layout().addWidget(self.colap)
        self.layout().setContentsMargins(9, 0, 9, 0)
        self.content = QtWidgets.QWidget()
        self.colap.add_widget(self.content, "main_widget")

        self.widget = Ui_logging_ui()
        self.widget.setupUi(self.content)
        self.widget.log_wandb_key_input.setEnabled(False)
        self.widget.log_prefix_input.setEnabled(False)
        self.widget.log_tracker_name_input.setEnabled(False)
        self.widget.log_output_selector.setIcon(QtGui.QIcon(os.path.join("icons", "more-horizontal.svg")))

        self.widget.logging_group.clicked.connect(self.enable_disable)
        self.widget.log_mode_selector.currentIndexChanged.connect(self.change_log_system)

        self.widget.log_output_input.setMode("folder")
        self.widget.log_output_input.highlight = True
        self.widget.log_output_input.textChanged.connect(lambda x: self.edit_args("logging_dir", x,
                                                                                  elem=self.widget.log_output_input))
        self.widget.log_output_selector.clicked.connect(self.set_from_dialog)
        self.widget.log_prefix_input.textChanged.connect(lambda x: self.edit_args("log_prefix", x, True))
        self.widget.log_tracker_name_input.textChanged.connect(lambda x: self.edit_args("log_tracker_name", x, True))
        self.widget.log_wandb_key_input.textChanged.connect(lambda x: self.edit_args("wandb_api_key", x))

        self.widget.log_prefix_enable.clicked.connect(
            lambda x: self.enable_disable_lineEdit(x, self.widget.log_prefix_input, "log_prefix"))
        self.widget.log_tracker_name_enable.clicked.connect(
            lambda x: self.enable_disable_lineEdit(x, self.widget.log_tracker_name_input, "log_tracker_name")
        )

    @QtCore.Slot(str, object, bool, QtWidgets.QWidget)
    def edit_args(self, name: str, value: object, optional: bool = False, elem: QtWidgets.QWidget = None) -> None:
        if elem:
            if isinstance(elem, modules.DragDropLineEdit.DragDropLineEdit):
                self.edited_previously = True
                elem.update_stylesheet()
        if not optional:
            self.args[name] = value
            return
        if value:
            self.args[name] = value
        else:
            if name in self.args:
                del self.args[name]

    @QtCore.Slot()
    def set_from_dialog(self) -> None:
        default_dir = self.widget.log_output_input.text() if os.path.exists(self.widget.log_output_input.text()) else ""
        file_name = QtWidgets.QFileDialog.getExistingDirectory(self, "Open Logging Directory", dir=default_dir)
        if not file_name:
            return
        self.widget.log_output_input.setText(file_name)

    @QtCore.Slot(int)
    def change_log_system(self, index: int) -> None:
        if index == 0:
            if "wandb_api_key" in self.args:
                del self.args['wandb_api_key']
            self.widget.log_wandb_key_input.setEnabled(False)
        else:
            self.edit_args("wandb_api_key", self.widget.log_wandb_key_input.text())
            self.widget.log_wandb_key_input.setEnabled(True)
        self.args['log_with'] = self.widget.log_mode_selector.currentText().lower()

    @QtCore.Slot()
    def enable_disable(self) -> None:
        checked = self.widget.logging_group.isChecked()
        if checked:
            self.args = {}
            self.edit_args("logging_dir", self.widget.log_output_input.text())
            if self.widget.log_prefix_enable.isChecked():
                self.edit_args("log_prefix", self.widget.log_prefix_input.text(), True)
            if self.widget.log_tracker_name_enable.isChecked():
                self.edit_args("log_tracker_name", self.widget.log_tracker_name_input.text(), True)
            self.change_log_system(self.widget.log_mode_selector.currentIndex())
            if self.edited_previously:
                self.widget.log_output_input.update_stylesheet()
        else:
            self.widget.log_output_input.setStyleSheet("")
            self.args = {}

    @QtCore.Slot(bool, LineEditWithHighlight, str)
    def enable_disable_lineEdit(self, checked: bool, elem: LineEditWithHighlight, name: str) -> None:
        if checked:
            elem.setEnabled(True)
            self.edit_args(name, elem.text(), True)
        else:
            elem.setEnabled(False)
            if name in self.args:
                del self.args[name]

    def get_args(self, input_args: dict) -> None:
        if not self.widget.logging_group.isChecked():
            if "logging_args" in input_args:
                del input_args['logging_args']
            return
        valid = self.widget.log_output_input.update_stylesheet()
        input_args['logging_args'] = None if not valid else self.args
        if not valid:
            if self.colap.is_collapsed:
                self.colap.toggle_collapsed()
                self.colap.title_frame.update_arrow(False)
                self.colap.title_frame.setChecked(True)

    def get_dataset_args(self, input_args: dict) -> None:
        pass

    def load_args(self, args: dict) -> None:
        if self.name not in args:
            return
        args = args[self.name].get("args", None)
        if not args:
            self.widget.logging_group.setChecked(False)
            self.enable_disable()
            return
        index = 0 if args['log_with'] == "tensorboard" else 1 if args['log_with'] == "wandb" else 2
        self.widget.log_mode_selector.setCurrentIndex(index)
        self.widget.log_output_input.setText(args.get("logging_dir", ""))
        self.widget.log_prefix_input.setText(args.get("log_prefix", ""))
        self.widget.log_prefix_enable.setChecked(True if "log_prefix" in args else False)
        self.enable_disable_lineEdit(True if "log_prefix" in args else False, self.widget.log_prefix_input,
                                     "log_prefix")
        self.widget.log_tracker_name_input.setText(args.get("log_tracker_name", ""))
        self.widget.log_tracker_name_enable.setChecked(True if "log_tracker_name" in args else False)
        self.enable_disable_lineEdit(True if "log_tracker_name" in args else False, self.widget.log_tracker_name_input,
                                     "log_tracker_name")
        self.widget.log_wandb_key_input.setText(args.get("wandb_api_key", ""))
        self.widget.logging_group.setChecked(True)
        self.enable_disable()

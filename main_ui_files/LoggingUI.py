from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget
from modules.DragDropLineEdit import DragDropLineEdit
from modules.LineEditHighlight import LineEditWithHighlight
from ui_files.LoggingUI import Ui_logging_ui
from modules.BaseWidget import BaseWidget
from pathlib import Path


class LoggingWidget(BaseWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.colap.set_title("Logging Args")
        self.widget = Ui_logging_ui()

        self.name = "logging_args"

        self.setup_widget()
        self.setup_connections()

    def setup_widget(self) -> None:
        super().setup_widget()
        self.widget.setupUi(self.content)
        self.widget.log_output_input.setMode("folder")
        self.widget.log_output_input.highlight = True
        self.widget.log_wandb_key_input.setEnabled(False)
        self.widget.log_prefix_input.setEnabled(False)
        self.widget.log_tracker_name_input.setEnabled(False)
        self.widget.log_output_selector.setIcon(
            QIcon(str(Path("icons/more-horizontal.svg")))
        )

    def setup_connections(self) -> None:
        self.widget.logging_group.clicked.connect(self.enable_disable)
        self.widget.log_mode_selector.currentIndexChanged.connect(
            self.change_log_system
        )
        self.widget.log_output_input.textChanged.connect(
            lambda x: self.edit_args(
                "logging_dir", x, elem=self.widget.log_output_input
            )
        )
        self.widget.log_output_selector.clicked.connect(
            lambda: self.set_folder_from_dialog(
                self.widget.log_output_input, "Open Logging Directory"
            )
        )
        self.widget.log_prefix_enable.clicked.connect(
            lambda x: self.enable_disable_lineEdit(
                x, self.widget.log_prefix_input, "log_prefix"
            )
        )
        self.widget.log_prefix_input.textChanged.connect(
            lambda x: self.edit_args("log_prefix", x, True)
        )
        self.widget.log_tracker_name_enable.clicked.connect(
            lambda x: self.enable_disable_lineEdit(
                x, self.widget.log_tracker_name_input, "log_tracker_name"
            )
        )
        self.widget.log_tracker_name_input.textChanged.connect(
            lambda x: self.edit_args("log_tracker_name", x, True)
        )
        self.widget.log_wandb_key_input.textChanged.connect(
            lambda x: self.edit_args("wandb_api_key", x)
        )

    def edit_args(
        self,
        name: str,
        value: object,
        optional: bool = False,
        elem: DragDropLineEdit = None,
    ) -> None:
        if elem and elem.dirty:
            elem.update_stylesheet()
        return super().edit_args(name, value, optional)

    @Slot(bool)
    def enable_disable(self, checked: bool) -> None:
        self.args = {}
        if not checked:
            self.widget.log_output_input.setStyleSheet("")
            return
        self.edit_args("logging_dir", self.widget.log_output_input.text())
        if self.widget.log_prefix_enable.isChecked():
            self.enable_disable_lineEdit(
                True, self.widget.log_prefix_input, "log_prefix"
            )
        if self.widget.log_tracker_name_enable.isChecked():
            self.enable_disable_lineEdit(
                True, self.widget.log_tracker_name_input, "log_tracker_name"
            )
        self.change_log_system(self.widget.log_mode_selector.currentIndex())
        if self.widget.log_output_input.dirty:
            self.widget.log_output_input.update_stylesheet()

    def change_log_system(self, index: int) -> None:
        if "wandb_api_key" in self.args:
            del self.args["wandb_api_key"]
        self.widget.log_wandb_key_input.setEnabled(index != 0)
        self.edit_args(
            "wandb_api_key",
            self.widget.log_wandb_key_input.text() if index != 0 else None,
            True,
        )
        self.edit_args(
            "log_with", self.widget.log_mode_selector.currentText().lower(), True
        )

    def enable_disable_lineEdit(
        self, checked: bool, elem: LineEditWithHighlight, name: str
    ) -> None:
        elem.setEnabled(checked)
        self.edit_args(name, elem.text() if checked else None, True)

    def load_args(self, args: dict) -> bool:
        if not super().load_args(args):
            self.widget.logging_group.setChecked(False)
            self.enable_disable(False)
            return False

        args: dict = args[self.name]

        # update element inputs
        self.widget.logging_group.setChecked(True)
        self.widget.log_mode_selector.setCurrentText(
            args.get("log_with", "tensorboard").capitalize()
        )
        self.widget.log_output_input.setText(args.get("logging_dir", ""))
        self.widget.log_prefix_enable.setChecked("log_prefix" in args)
        self.widget.log_prefix_input.setText(args.get("log_prefix", ""))
        self.widget.log_tracker_name_enable.setChecked("log_tracker_name" in args)
        self.widget.log_tracker_name_input.setText(args.get("log_tracker_name", ""))
        self.widget.log_wandb_key_input.setText(args.get("wandb_api_key", ""))

        # edit args to match
        self.enable_disable(True)
        return True

import json
from pathlib import Path

from PySide6 import QtCore
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QCheckBox, QFileDialog, QMessageBox, QWidget

from modules.BaseWidget import BaseWidget
from modules.ExtraItem import ExtraItem
from ui_files.extra_fields import Ui_extra_fields_ui


class ExtraArgsWidget(BaseWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.colap.set_title("Extra Args")
        self.widget = Ui_extra_fields_ui()

        self.name = "extra_args"
        self.args = {}
        self.dataset_args = {}
        self.extra_args: list[ExtraItem] = []

        self.setup_widget()
        self.setup_connections()

    def setup_widget(self) -> None:
        super().setup_widget()
        self.widget.setupUi(self.content)
        load_args_icon = QIcon(str(Path("icons/folder.svg")))
        self.widget.load_extra_args_button.setIcon(load_args_icon)
        save_args_icon = QIcon(str(Path("icons/save.svg")))
        self.widget.save_extra_args_button.setIcon(save_args_icon)
        self.widget.extra_fields_item_widget.layout().setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.content.setFixedHeight(300)

    def setup_connections(self) -> None:
        self.widget.add_extra_arg_button.clicked.connect(self.add_extra_arg)
        self.widget.load_extra_args_button.clicked.connect(self.load_optional_args)
        self.widget.save_extra_args_button.clicked.connect(self.save_optional_args)

    def add_extra_arg(self):
        self.extra_args.append(ExtraItem())
        self.widget.extra_fields_item_widget.layout().addWidget(self.extra_args[-1])
        self.extra_args[-1].delete_item.connect(self.remove_extra_arg)
        self.extra_args[-1].item_updated.connect(self.modify_extra_args)

    def modify_extra_args(self):
        if len(self.extra_args) == 0:
            self.args = {}
            self.dataset_args = {}
            return
        self.args = {}
        self.dataset_args = {}
        for arg in self.extra_args:
            name, value, is_dataset = arg.get_arg()
            if not name or not value:
                continue
            if is_dataset:
                self.edit_dataset_args(name, value)
            else:
                self.edit_args(name, value)

    def remove_extra_arg(self, widget: ExtraItem):
        self.layout().removeWidget(widget)
        widget.deleteLater()
        self.extra_args.remove(widget)
        self.modify_extra_args()

    def load_optional_args(self):
        def update_config(checked: bool):
            config_path = Path("config.json")
            if not config_path.exists():
                config_path.write_text(json.dumps({}))
            config = json.loads(config_path.read_text())
            config["skip_extra_args_warning"] = checked
            config_path.write_text(json.dumps(config))

        config: dict = json.loads(Path("config.json").read_text())
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Load Extra Args",
            dir="",
            filter="Extra Args (*.json)",
        )
        if not file_name:
            return
        args = json.loads(Path(file_name).read_text())

        if not isinstance(args, dict) or not args:
            if not config.get("skip_extra_args_warning", False):
                checkbox = QCheckBox("Don't show this message again")
                checkbox.clicked.connect(update_config)
                message = QMessageBox(
                    QMessageBox.Icon.Warning,
                    "No Extra Args Found",
                    "No extra args found in the file. Are you sure you want to load the file?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    self,
                )
                message.setCheckBox(checkbox)
                result = message.exec()
                if result == QMessageBox.StandardButton.No:
                    return
            args = {}
        for _ in range(len(self.extra_args)):
            self.remove_extra_arg(self.extra_args[0])
        for arg in args:
            if not isinstance(args[arg], dict) or "value" not in args[arg]:
                continue
            self.add_extra_arg()
            self.extra_args[-1].arg_name_input.setText(str(arg))
            self.extra_args[-1].arg_value_input.setText(str(args[arg]["value"]))
            self.extra_args[-1].is_dataset_toggle.setChecked(args[arg].get("is_dataset", False))
            self.extra_args[-1].is_dataset = args[arg].get("is_dataset", False)
        self.modify_extra_args()

    def save_optional_args(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Extra Args",
            dir="",
            filter="Extra Args (*.json)",
        )
        if not file_name:
            return

        args = {}
        for extra_arg in self.extra_args:
            name, value, is_dataset = extra_arg.get_arg()
            if not name or not value:
                continue
            args[name] = {"value": value, "is_dataset": is_dataset}

        Path(file_name).write_text(json.dumps(args))

    def load_args(self, args: dict) -> bool:
        # sourcery skip: class-extract-method
        args: dict = args.get(self.name, {})
        i = 0
        while i < len(self.extra_args):
            if self.extra_args[i].is_dataset:
                i += 1
                continue
            self.remove_extra_arg(self.extra_args[i])
        self.args = {}
        self.load(args, False)

    def load_dataset_args(self, dataset_args: dict) -> bool:
        dataset_args: dict = dataset_args.get(self.name, {})
        i = 0
        while i < len(self.extra_args):
            if not self.extra_args[i].is_dataset:
                i += 1
                continue
            self.remove_extra_arg(self.extra_args[i])
        self.dataset_args = {}
        self.load(dataset_args, True)

    def load(self, args: dict, is_dataset: bool):
        for item, value in args.items():
            self.add_extra_arg()
            self.extra_args[-1].arg_name_input.setText(str(item))
            self.extra_args[-1].arg_value_input.setText(str(value))
            self.extra_args[-1].is_dataset_toggle.setChecked(is_dataset)
        self.modify_extra_args()

from modules.BaseWidget import BaseWidget
from PySide6 import QtCore
from PySide6.QtWidgets import QWidget
from ui_files.extra_fields import Ui_extra_fields_ui
from modules.ExtraItem import ExtraItem


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
        self.widget.extra_fields_item_widget.layout().setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.content.setFixedHeight(300)

    def setup_connections(self) -> None:
        self.widget.add_extra_arg_button.clicked.connect(self.add_extra_arg)

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

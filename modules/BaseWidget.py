from PySide6 import QtWidgets
from modules.CollapsibleWidget import CollapsibleWidget
from modules.DragDropLineEdit import DragDropLineEdit
from pathlib import Path


class BaseWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)
        self.colap = CollapsibleWidget(self)
        self.content = QtWidgets.QWidget()
        self.widget = None

        self.name = ""
        self.args = {}
        self.dataset_args = {}

    def setup_widget(self) -> None:
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(self.colap)
        self.layout().setContentsMargins(9, 0, 9, 0)
        self.colap.add_widget(self.content, "main_widget")

    def setup_connections(self) -> None:
        raise NotImplementedError

    def edit_args(self, name: str, value: object, optional: bool = False) -> None:
        if name in self.args:
            del self.args[name]
        if optional and (not value or value is False):
            return
        self.args[name] = value

    def edit_dataset_args(
        self, name: str, value: object, optional: bool = False
    ) -> None:
        if name in self.dataset_args:
            del self.dataset_args[name]
        if optional and (not value or value is False):
            return
        self.dataset_args[name] = value

    def set_folder_from_dialog(
        self, widget: DragDropLineEdit, title_str: str = ""
    ) -> None:
        default_dir = Path(widget.text())
        file_name = QtWidgets.QFileDialog.getExistingDirectory(
            self, title_str, dir=str(default_dir) if default_dir.exists() else ""
        )
        if not file_name:
            return
        widget.setText(Path(file_name).as_posix())
        widget.update_stylesheet()

    def set_file_from_dialog(
        self, widget: DragDropLineEdit, title_str: str = "", filter_string: str = ""
    ) -> None:
        extensions = " ".join([f"*{s}" for s in widget.extensions])
        default_dir = Path(widget.text())
        if default_dir.suffix != "":
            default_dir = default_dir.parent
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            title_str,
            dir=str(default_dir) if default_dir.exists() else "",
            filter=f"{filter_string} ({extensions})",
        )
        if not file_name:
            return
        widget.setText(Path(file_name).as_posix())
        widget.update_stylesheet()

    def save_args(self) -> dict:
        return self.args

    def save_dataset_args(self) -> dict:
        return self.dataset_args

    def load_args(self, args: dict) -> bool:
        return self.name in args

    def load_dataset_args(self, dataset_args: dict) -> bool:
        return self.name in dataset_args

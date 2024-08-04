from pathlib import Path
from PySide6 import QtWidgets

from modules.DragDropLineEdit import DragDropLineEdit


class BaseDialog(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.args = {}

    def setup_widget(self) -> None:
        raise NotImplementedError

    def setup_connections(self) -> None:
        raise NotImplementedError

    def edit_args(self, name: str, value: object, optional: bool = False) -> None:
        if name in self.args:
            del self.args[name]
        if optional and (not value or value is False):
            return
        self.args[name] = value

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

    def set_file_from_dialog(
        self, widget: DragDropLineEdit, title_str: str, filter_string: str = ""
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

    def process_args(self) -> list[str]:
        raise NotImplementedError

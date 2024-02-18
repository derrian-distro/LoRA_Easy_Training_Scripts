from pathlib import Path
import typing

from PySide6 import QtGui, QtCore, QtWidgets


class DragDropLineEdit(QtWidgets.QLineEdit):
    def __init__(
        self,
        parent: QtWidgets.QWidget = None,
        name: str = "",
        mode: str = "file",
        extensions: typing.Optional[list[str]] = None,
        auto_highlight: bool = False,
        allow_empty: bool = False,
    ) -> None:
        super(DragDropLineEdit, self).__init__(parent)
        self.mode = mode
        self.highlight = auto_highlight
        self.name = name
        self.allow_empty = allow_empty
        self.dirty = False
        self.setPlaceholderText(name)
        self.extensions = extensions
        self.setAcceptDrops(True)
        self.error_sheet = """
            border-color: #dc3545
        """

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        event.setDropAction(QtGui.Qt.CopyAction)
        event.acceptProposedAction()
        url = event.mimeData().urls()[0]
        if not url.isLocalFile():
            return
        path = Path(url.toLocalFile())
        if path.is_dir() and self.mode != "folder":
            return
        elif path.is_file() and self.mode != "file":
            return
        if self.mode == "file":
            ext = path.suffix
            if not ext or ext not in self.extensions:
                return
        self.setText(path.as_posix())

    def setName(self, name: str) -> None:
        self.name = name

    def setMode(self, mode: str, extensions: list[str] = None) -> None:
        self.mode = mode
        if extensions:
            self.extensions = extensions

    def focusInEvent(self, arg__1: QtGui.QFocusEvent) -> None:
        if not self.highlight or len(self.text()) == 0:
            super(DragDropLineEdit, self).focusInEvent(arg__1)
        else:
            QtCore.QTimer.singleShot(0, self.selectAll)

    def update_stylesheet(self) -> bool:
        path = Path(self.text())
        if path.exists() and self.mode == "file":
            valid = path.suffix in self.extensions
        elif path.is_dir():
            valid = True
        elif self.allow_empty and self.text() == "":
            valid = True
        else:
            valid = False

        if valid:
            self.setStyleSheet("")
            return True
        self.setStyleSheet(self.error_sheet)
        return False

    def setText(self, arg__1: str) -> None:
        self.dirty = True
        return super().setText(arg__1)

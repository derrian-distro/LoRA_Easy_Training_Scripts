import os.path
import typing

from PySide6 import QtGui, QtCore, QtWidgets


class DragDropLineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent: QtWidgets.QWidget = None, name: str = "", mode: str = 'file',
                 extensions: typing.Optional[list[str]] = None, auto_highlight: bool = False) -> None:
        super(DragDropLineEdit, self).__init__(parent)
        self.mode = mode
        self.highlight = auto_highlight
        self.name = name
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
        path = str(url.toLocalFile())
        if os.path.isdir(path) and self.mode != 'folder':
            return
        elif not os.path.isdir(path) and self.mode != 'file':
            return
        if self.mode == 'file':
            _, ext = os.path.splitext(path)
            if not ext or ext not in self.extensions:
                return
        self.setText(str(event.mimeData().urls()[0].toLocalFile()))

    def setName(self, name: str) -> None:
        self.name = name

    def setMode(self, mode: str, extensions: [str] = None) -> None:
        self.mode = mode
        if extensions:
            self.extensions = extensions

    def focusInEvent(self, arg__1: QtGui.QFocusEvent) -> None:
        if not self.highlight or len(self.text()) == 0:
            super(DragDropLineEdit, self).focusInEvent(arg__1)
        else:
            QtCore.QTimer.singleShot(0, self.selectAll)

    def update_stylesheet(self) -> bool:
        exist = os.path.exists(self.text())
        if exist and self.mode == 'file':
            valid = os.path.splitext(self.text())[1] in self.extensions
        elif exist and os.path.isdir(self.text()):
            valid = True
        else:
            valid = False

        if valid:
            self.setStyleSheet("")
            return True
        self.setStyleSheet(self.error_sheet)
        return False

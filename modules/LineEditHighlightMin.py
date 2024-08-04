from PySide6.QtWidgets import QWidget
from modules.LineEditHighlight import LineEditWithHighlight


class LineEditWithHighlightMin(LineEditWithHighlight):
    def __init__(
        self, parent: QWidget = None, valid: bool = True, min_allowed: int = 0
    ) -> None:
        super(LineEditWithHighlight, self).__init__(parent)
        self.isValid = valid
        self.min_allowed = min_allowed
        self.error_sheet = """
            border-color: #dc3545
        """
        self.dirty = False

    def setText(self, arg__1: str) -> None:
        self.dirty = True
        return super().setText(arg__1)

    def update_stylesheet(self) -> bool:
        self.isValid = len(self.text().strip()) >= self.min_allowed
        self.setStyleSheet("" if self.isValid else self.error_sheet)
        return self.isValid

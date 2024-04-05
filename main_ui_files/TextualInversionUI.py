from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget
from modules.LineEditHighlight import LineEditWithHighlight
from ui_files.TextualInversionUI import Ui_textual_inversion_ui
from modules.BaseWidget import BaseWidget


class TextualInversionWidget(BaseWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.colap.set_title("Textual Inversion")
        self.widget = Ui_textual_inversion_ui()

        self.name = "textual_inversion_args"
        self.args = {
            "token_string": "",
            "init_word": "",
            "vectors_per_token": 1
        }

        self.setup_widget()
        self.setup_connections()

    def setup_widget(self) -> None:
        super().setup_widget()
        self.widget.setupUi(self.content)

    def setup_connections(self) -> None:
        # TODO: add num vectors per token
        """
        self.widget.vectors_per_token.valueChanged.connect(
            lambda x: self.change_vectors_per_token( x )
        )
        """

        self.widget.token_string.textChanged.connect(
            lambda x: self.edit_args("token_string", x, optional=True)
        )


        self.widget.init_word.textChanged.connect(
            lambda x: self.edit_args("init_word", x, True)
        )


    def check_validity(self, elem: LineEditWithHighlight) -> None:
        # TODO: Add validity check
        pass


    def load_args(self, args: dict) -> bool:
        if not super().load_args(args):
            return False

        args: dict = args[self.name] if self.name in args else {}

        # update element inputs
        self.widget.token_string.setText(args.get("token_string", ""))
        self.widget.init_word.setText(args.get("init_word", ""))

        return True

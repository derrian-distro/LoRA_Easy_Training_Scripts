import contextlib
from PySide6.QtWidgets import QWidget
from ui_files.TextualInversionUI import Ui_textual_inversion_ui
from modules.BaseWidget import BaseWidget

from modules.NetworkManager import NetworkManager


class TextualInversionWidget(BaseWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.colap.set_title("Textual Inversion Args")
        self.widget = Ui_textual_inversion_ui()
        self.name = "textual_inversion_args"
        self.args = {
            "token_string": "",
            "init_word": "",
        }
        self.setup_widget()
        self.setup_connections()

    def setup_widget(self) -> None:
        super().setup_widget()
        self.widget.setupUi(self.content)

    def setup_connections(self) -> None:
        self.widget.token_string_input.textChanged.connect(
            lambda x: self.edit_args("token_string", x, True)
        )
        self.widget.initial_word_input.textChanged.connect(self.change_initial_word)
        self.widget.vectors_per_token_enable.clicked.connect(
            self.enable_disable_vectors_per_token
        )
        self.widget.vectors_per_token_input.valueChanged.connect(
            self.change_vectors_per_token
        )

    @NetworkManager.debounce(200)
    def debounce_tokenize(self):
        self.tokenize_input()

    def tokenize_input(self):
        if not self.widget.vectors_per_token_enable.isChecked():
            input_text = self.widget.initial_word_input.text()
            if not input_text:
                self.change_vectors_per_token(0)
                return
            with contextlib.suppress(Exception):
                NetworkManager().query(
                    "/tokenize",
                    {"text": input_text},
                    lambda x: self.change_vectors_per_token(x["length"]),
                )

    def change_initial_word(self, text: str) -> None:
        self.edit_args("init_word", text, True)
        with contextlib.suppress(Exception):
            self.debounce_tokenize()

    def change_vectors_per_token(self, value: int) -> None:
        if value and value > 0:
            self.widget.vectors_per_token_input.setValue(value)
            self.edit_args("num_vectors_per_token", value if value > 0 else None, True)

    def enable_disable_vectors_per_token(self, checked: bool) -> None:
        if "num_vectors_per_token" in self.args:
            del self.args["num_vectors_per_token"]
        self.widget.vectors_per_token_input.setEnabled(checked)
        if not checked:
            self.tokenize_input()
            return
        self.edit_args(
            "num_vectors_per_token", self.widget.vectors_per_token_input.value(), True
        )

    def load_args(self, args: dict) -> bool:
        args: dict = args.get(self.name, {})

        # update element inputs
        self.widget.token_string_input.setText(args.get("token_string", ""))
        self.widget.initial_word_input.setText(args.get("init_word", ""))
        self.widget.vectors_per_token_enable.setChecked(
            bool(args.get("num_vectors_per_token", False))
        )
        self.widget.vectors_per_token_input.setValue(
            args.get("num_vectors_per_token", 0)
        )

        # edit args to match
        self.edit_args("token_string", self.widget.token_string_input.text(), True)
        self.change_initial_word(self.widget.initial_word_input.text())
        self.enable_disable_vectors_per_token(
            self.widget.vectors_per_token_enable.isChecked()
        )

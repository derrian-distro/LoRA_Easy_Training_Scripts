from PySide6.QtCore import Slot, QUrl
from PySide6.QtWidgets import QWidget
from modules.LineEditHighlight import LineEditWithHighlight
from ui_files.TextualInversionUI import Ui_textual_inversion_ui
from modules.BaseWidget import BaseWidget

from modules.NetworkManager import NetworkManager, QNetworkReply


class TextualInversionWidget(BaseWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.colap.set_title("Textual Inversion")
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
        self.widget.token_string.textChanged.connect(
            lambda x: self.edit_args("token_string", x, optional=True)
        )


        self.widget.init_word.textChanged.connect(self.on_text_changed)
        self.widget.init_word.editingFinished.connect(self.tokenize_input)
        self.widget.vectors_per_token_enable.clicked.connect(self.enable_disable_vectors_per_token)
        self.widget.num_vectors_per_token.valueChanged.connect( self.change_num_vectors_per_token )



    @Slot(bool)
    def enable_disable_vectors_per_token(self, checked: bool) -> None:
        if "num_vectors_per_token" in self.args:
            del self.args["num_vectors_per_token"]
        self.widget.num_vectors_per_token.setEnabled(checked)
        if not checked:
            self.tokenize_input()
            return
        self.edit_args("num_vectors_per_token", self.widget.num_vectors_per_token.value(), True)


    def on_text_changed(self, text: str):
        self.edit_args("init_word", text, True)
        self.debounce_tokenize()

    @NetworkManager.debounce(200)
    def debounce_tokenize(self):
        self.tokenize_input()

    def tokenize_input(self):
        if not self.widget.vectors_per_token_enable.isChecked():
            input_text = self.widget.init_word.text()
            NetworkManager().query("/tokenize", {"text": input_text}, self.tokenizer_callback)

    @Slot(dict)
    def tokenizer_callback(self, data: dict) -> None:
        self.change_num_vectors_per_token(data['length'])


    def change_num_vectors_per_token(self, value: int) -> None:
        self.widget.num_vectors_per_token.setValue(value)
        self.edit_args("num_vectors_per_token", value if value > 0 else None, True)

    def load_args(self, args: dict) -> bool:
        if not super().load_args(args):
            return False

        args: dict = args[self.name] if self.name in args else {}

        # update element inputs
        self.widget.token_string.setText(args.get("token_string", ""))
        self.widget.init_word.setText(args.get("init_word", ""))

        self.widget.vectors_per_token_enable.setChecked(bool(args.get("min_snr_gamma", False)))
        self.change_num_vectors_per_token(args.get("num_vectors_per_token", None))
        return True

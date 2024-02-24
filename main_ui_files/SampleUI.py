from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget
from modules.DragDropLineEdit import DragDropLineEdit
from ui_files.SampleUI import Ui_sample_ui
from modules.BaseWidget import BaseWidget
from PySide6.QtGui import QIcon
from pathlib import Path


class SampleWidget(BaseWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.colap.set_title("Sample Args")
        self.widget = Ui_sample_ui()

        self.name = "sample_args"

        self.setup_widget()
        self.setup_connections()

    def setup_widget(self) -> None:
        super().setup_widget()
        self.widget.setupUi(self.content)
        self.widget.sample_prompt_selector.setIcon(
            QIcon(str(Path("icons/more-horizontal.svg")))
        )
        self.widget.sample_prompt_txt_file_input.setMode("file", [".txt"])
        self.widget.sample_prompt_txt_file_input.highlight = True

    def setup_connections(self) -> None:
        self.widget.sample_group.clicked.connect(self.enable_disable)
        self.widget.sampler_input.currentTextChanged.connect(
            lambda x: self.edit_args("sample_sampler", x.lower())
        )
        self.widget.steps_epochs_selector.currentIndexChanged.connect(
            self.change_steps_epochs
        )
        self.widget.steps_epoch_input.valueChanged.connect(
            lambda: self.change_steps_epochs(
                self.widget.steps_epochs_selector.currentIndex()
            )
        )
        self.widget.sample_prompt_txt_file_input.textChanged.connect(
            lambda x: self.edit_args(
                "sample_prompts",
                x,
                optional=True,
            )
        )
        self.widget.sample_prompt_txt_file_input.editingFinished.connect(
            lambda: self.check_validity(self.widget.sample_prompt_txt_file_input)
        )
        self.widget.sample_prompt_selector.clicked.connect(
            lambda: self.set_file_from_dialog(
                self.widget.sample_prompt_txt_file_input,
                "Prompt Text File",
                "txt files",
            )
        )

    def check_validity(self, elem: DragDropLineEdit) -> None:
        elem.dirty = True
        if not elem.allow_empty or elem.text() != "":
            elem.update_stylesheet()
        else:
            elem.setStyleSheet("")

    @Slot(bool)
    def enable_disable(self, checked: bool) -> None:
        self.args = {}
        if not checked:
            self.widget.sample_prompt_txt_file_input.setStyleSheet("")
            return
        self.edit_args(
            "sample_sampler", self.widget.sampler_input.currentText().lower()
        )
        self.change_steps_epochs(self.widget.steps_epochs_selector.currentIndex())
        self.edit_args(
            "sample_prompts",
            self.widget.sample_prompt_txt_file_input.text(),
            optional=True,
        )
        self.check_validity(self.widget.sample_prompt_txt_file_input)

    @Slot(int)
    def change_steps_epochs(self, index: int) -> None:
        args = ["sample_every_n_steps", "sample_every_n_epochs"]
        for arg in args:
            if arg in self.args:
                del self.args[arg]
        self.edit_args(args[index], self.widget.steps_epoch_input.value(), True)

    def load_args(self, args: dict) -> bool:
        if not super().load_args(args):
            self.widget.sample_group.setChecked(False)
            self.enable_disable(False)
            return False

        args: dict = args[self.name]

        # update element inputs
        self.widget.sample_group.setChecked(True)
        self.widget.sampler_input.setCurrentText(
            args.get("sample_sampler", "DDIM").upper()
        )
        self.widget.steps_epochs_selector.setCurrentIndex(
            0 if "sample_every_n_steps" in args else 1
        )
        self.widget.steps_epoch_input.setValue(
            args.get("sample_every_n_steps", args.get("sample_every_n_epochs", 1))
        )
        self.widget.sample_prompt_txt_file_input.setText(args.get("sample_prompts", ""))

        # edit args to match
        self.enable_disable(True)
        return True

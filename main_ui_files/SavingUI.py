from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QPushButton
from ui_files.SavingUI import Ui_saving_ui
from modules.BaseWidget import BaseWidget
from pathlib import Path
from modules.DragDropLineEdit import DragDropLineEdit


class SavingWidget(BaseWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.colap.set_title("Saving Args")
        self.widget = Ui_saving_ui()

        self.name = "saving_args"
        self.args = {"save_precision": "fp16", "save_model_as": "safetensors"}

        self.setup_widget()
        self.setup_connections()

    def setup_widget(self) -> None:
        super().setup_widget()
        self.widget.setupUi(self.content)

        def setup_folder(elem: DragDropLineEdit, selector: QPushButton):
            selector_icon = QIcon(str(Path("icons/more-horizontal.svg")))
            elem.setMode("folder")
            elem.highlight = True
            elem.allow_empty = True
            selector.setIcon(selector_icon)

        setup_folder(
            self.widget.output_folder_input, self.widget.output_folder_selector
        )
        self.widget.output_folder_input.allow_empty = False
        setup_folder(self.widget.resume_input, self.widget.resume_selector)
        setup_folder(self.widget.save_tag_input, self.widget.save_tag_selector)
        setup_folder(self.widget.save_toml_input, self.widget.save_toml_selector)

    def setup_connections(self) -> None:
        self.widget.output_folder_input.textChanged.connect(
            lambda x: self.edit_args("output_dir", x, optional=True)
        )
        self.widget.output_folder_input.editingFinished.connect(
            lambda: self.check_validity(self.widget.output_folder_input)
        )
        self.widget.output_folder_selector.clicked.connect(
            lambda: self.set_folder_from_dialog(
                self.widget.output_folder_input, "Output Folder"
            )
        )
        self.widget.output_name_enable.clicked.connect(self.enable_disable_output_name)
        self.widget.output_name_input.textChanged.connect(
            lambda x: self.edit_args("output_name", x, True)
        )
        self.widget.save_precision_selector.currentTextChanged.connect(
            lambda x: self.edit_args("save_precision", x)
        )
        self.widget.resume_enable.clicked.connect(self.enable_disable_resume)
        self.widget.resume_input.textChanged.connect(
            lambda x: self.edit_args("resume", x, optional=True)
        )
        self.widget.resume_input.editingFinished.connect(
            lambda: self.check_validity(self.widget.resume_input)
        )
        self.widget.resume_selector.clicked.connect(
            lambda: self.set_folder_from_dialog(
                self.widget.resume_input, "Folder To Resume From"
            )
        )
        self.widget.save_as_selector.currentTextChanged.connect(
            lambda x: self.edit_args("save_model_as", x)
        )
        self.widget.save_only_last_enable.clicked.connect(self.enable_disable_last)
        self.widget.save_last_selector.currentIndexChanged.connect(
            self.change_last_type
        )
        self.widget.save_last_input.valueChanged.connect(
            lambda: self.change_last_type(self.widget.save_last_selector.currentIndex())
        )
        self.widget.save_ratio_enable.clicked.connect(self.enable_disable_ratio)
        self.widget.save_ratio_input.valueChanged.connect(
            lambda x: self.edit_args("save_n_epoch_ratio", x, True)
        )
        self.widget.save_tag_enable.clicked.connect(self.enable_disable_tag_file)
        self.widget.save_tag_input.textChanged.connect(
            lambda x: self.edit_args(
                "tag_file_location",
                x,
                optional=True,
            )
        )
        self.widget.save_tag_input.editingFinished.connect(
            lambda: self.check_validity(self.widget.save_tag_input)
        )
        self.widget.save_tag_selector.clicked.connect(
            lambda: self.set_folder_from_dialog(
                self.widget.save_tag_input, "Folder to save tag occurrence file to"
            )
        )
        self.widget.save_freq_enable.clicked.connect(self.enable_disable_freq)
        self.widget.save_freq_selector.currentIndexChanged.connect(
            self.change_freq_type
        )
        self.widget.save_freq_input.valueChanged.connect(
            lambda: self.change_freq_type(self.widget.save_freq_selector.currentIndex())
        )
        self.widget.save_toml_enable.clicked.connect(self.enable_disable_toml)
        self.widget.save_toml_input.textChanged.connect(
            lambda x: self.edit_args("save_toml_location", x, optional=True)
        )
        self.widget.save_toml_input.editingFinished.connect(
            lambda: self.check_validity(self.widget.save_toml_input)
        )
        self.widget.save_toml_selector.clicked.connect(
            lambda: self.set_folder_from_dialog(
                self.widget.save_toml_input, "Folder to save toml file"
            )
        )
        self.widget.save_state_enable.clicked.connect(self.enable_disable_save_state)
        self.widget.save_last_state_enable.clicked.connect(
            self.enable_disable_last_state
        )
        self.widget.save_last_state_selector.currentIndexChanged.connect(
            self.change_state_type
        )
        self.widget.save_last_state_input.valueChanged.connect(
            lambda: self.change_state_type(
                self.widget.save_last_selector.currentIndex()
            )
        )

    def check_validity(self, elem: DragDropLineEdit) -> None:
        elem.dirty = True
        if not elem.allow_empty or elem.text() != "":
            elem.update_stylesheet()
        else:
            elem.setStyleSheet("")

    @Slot(int)
    def change_last_type(self, index: int) -> None:
        args = ["save_last_n_epochs", "save_last_n_steps"]
        for arg in args:
            if arg in self.args:
                del self.args[arg]
        self.edit_args(args[index], self.widget.save_last_input.value(), True)

    @Slot(int)
    def change_freq_type(self, index: int) -> None:
        args = ["save_every_n_epochs", "save_every_n_steps"]
        for arg in args:
            if arg in self.args:
                del self.args[arg]
        self.edit_args(args[index], self.widget.save_freq_input.value(), True)

    @Slot(int)
    def change_state_type(self, index: int) -> None:
        args = ["save_last_n_epochs_state", "save_last_n_steps_state"]
        for arg in args:
            if arg in self.args:
                del self.args[arg]
        self.edit_args(args[index], self.widget.save_last_state_input.value(), True)

    @Slot(bool)
    def enable_disable_output_name(self, checked: bool) -> None:
        if "output_name" in self.args:
            del self.args["output_name"]
        self.widget.output_name_input.setEnabled(checked)
        if not checked:
            return
        self.edit_args("output_name", self.widget.output_name_input.text(), True)

    @Slot(bool)
    def enable_disable_resume(self, checked: bool) -> None:
        if "resume" in self.args:
            del self.args["resume"]
            self.widget.resume_input.setStyleSheet("")

        self.widget.resume_input.setEnabled(checked)
        self.widget.resume_selector.setEnabled(checked)
        if not checked:
            return
        self.edit_args(
            "resume",
            self.widget.resume_input.text(),
            optional=True,
        )
        self.check_validity(self.widget.resume_input)

    @Slot(bool)
    def enable_disable_last(self, checked: bool) -> None:
        args = ["save_last_n_steps", "save_last_n_epochs"]
        for arg in args:
            if arg in self.args:
                del self.args[arg]

        self.widget.save_last_selector.setEnabled(checked)
        self.widget.save_last_input.setEnabled(checked)
        if not checked:
            return
        self.change_last_type(self.widget.save_last_selector.currentIndex())

    @Slot(bool)
    def enable_disable_ratio(self, checked: bool) -> None:
        if "save_n_epoch_ratio" in self.args:
            del self.args["save_n_epoch_ratio"]
        self.widget.save_ratio_input.setEnabled(checked)
        if not checked:
            return
        self.edit_args("save_n_epoch_ratio", self.widget.save_ratio_input.value(), True)

    @Slot(bool)
    def enable_disable_tag_file(self, checked: bool) -> None:
        args = ["tag_occurrence", "tag_file_location"]
        for arg in args:
            if arg in self.args:
                del self.args[arg]
        self.widget.save_tag_input.setEnabled(checked)
        self.widget.save_tag_selector.setEnabled(checked)
        if not checked:
            return
        self.edit_args("tag_occurrence", checked, True)
        self.edit_args(
            "tag_file_location",
            self.widget.save_tag_input.text(),
            optional=True,
        )
        self.check_validity(self.widget.save_tag_input)

    @Slot(bool)
    def enable_disable_freq(self, checked: bool) -> None:
        args = ["save_every_n_epochs", "save_every_n_steps"]
        for arg in args:
            if arg in self.args:
                del self.args[arg]
        self.widget.save_freq_input.setEnabled(checked)
        self.widget.save_freq_selector.setEnabled(checked)
        if not checked:
            return
        self.change_freq_type(self.widget.save_freq_selector.currentIndex())

    @Slot(bool)
    def enable_disable_toml(self, checked: bool) -> None:
        args = ["save_toml", "save_toml_location"]
        for arg in args:
            if arg in self.args:
                del self.args[arg]
        self.widget.save_toml_input.setEnabled(checked)
        self.widget.save_toml_selector.setEnabled(checked)
        if not checked:
            return
        self.edit_args("save_toml", checked, True)
        self.edit_args(
            "save_toml_location",
            self.widget.save_toml_input.text(),
            optional=True,
        )
        self.check_validity(self.widget.save_toml_input)

    @Slot(bool)
    def enable_disable_save_state(self, checked: bool) -> None:
        if "save_state" in self.args:
            del self.args["save_state"]
        self.widget.save_last_state_enable.setEnabled(checked)
        self.enable_disable_last_state(False)
        if not checked:
            return
        self.enable_disable_last_state(self.widget.save_last_state_enable.isChecked())
        self.edit_args("save_state", True)

    @Slot(bool)
    def enable_disable_last_state(self, checked: bool) -> None:
        args = ["save_last_n_epochs_state", "save_last_n_steps_state"]
        for arg in args:
            if arg in self.args:
                del self.args[arg]
        self.widget.save_last_state_selector.setEnabled(checked)
        self.widget.save_last_state_input.setEnabled(checked)
        if not checked:
            return
        self.change_state_type(self.widget.save_last_state_selector.currentIndex())

    def load_args(self, args: dict) -> bool:
        if not super().load_args(args):
            return False

        args: dict = args[self.name]

        # update element inputs
        self.widget.output_folder_input.setText(args.get("output_dir", ""))
        self.widget.output_name_enable.setChecked(bool(args.get("output_name", False)))
        self.widget.output_name_input.setText(args.get("output_name", ""))
        self.widget.save_precision_selector.setCurrentText(
            args.get("save_precision", "fp16")
        )
        self.widget.resume_enable.setChecked(bool(args.get("resume", False)))
        self.widget.resume_input.setText(args.get("resume", ""))
        self.widget.save_as_selector.setCurrentText(
            args.get("save_model_as", "safetensors")
        )
        self.widget.save_only_last_enable.setChecked(
            bool(args.get("save_last_n_epochs", args.get("save_last_n_steps", False)))
        )
        self.widget.save_last_selector.setCurrentIndex(
            0 if args.get("save_last_n_epochs") else 1
        )
        self.widget.save_last_input.setValue(
            args.get("save_last_n_epochs", args.get("save_last_n_steps", 1))
        )
        self.widget.save_ratio_enable.setChecked(
            bool(args.get("save_n_epoch_ratio", False))
        )
        self.widget.save_ratio_input.setValue(args.get("save_n_epoch_ratio", 1))
        self.widget.save_tag_enable.setChecked(bool(args.get("tag_occurrence", False)))
        self.widget.save_tag_input.setText(args.get("tag_file_location", ""))
        self.widget.save_freq_enable.setChecked(
            bool(args.get("save_every_n_epochs", args.get("save_every_n_steps", False)))
        )
        self.widget.save_freq_selector.setCurrentIndex(
            0 if args.get("save_every_n_epochs") else 1
        )
        self.widget.save_freq_input.setValue(
            args.get("save_every_n_epochs", args.get("save_every_n_steps", 1))
        )
        self.widget.save_toml_enable.setChecked(bool(args.get("save_toml", False)))
        self.widget.save_toml_input.setText(args.get("save_toml_location", ""))
        self.widget.save_state_enable.setChecked(args.get("save_state", False))
        self.widget.save_last_state_enable.setChecked(
            bool(
                args.get(
                    "save_last_n_epochs_state",
                    args.get("save_last_n_steps_state", False),
                )
            )
        )
        self.widget.save_last_state_selector.setCurrentIndex(
            0 if args.get("save_last_n_epochs_state") else 1
        )
        self.widget.save_last_state_input.setValue(
            args.get("save_last_n_epochs_state", args.get("save_last_n_steps_state", 1))
        )

        # edit args to match
        self.edit_args(
            "output_dir",
            self.widget.output_folder_input.text(),
            optional=True,
        )
        self.check_validity(self.widget.output_folder_input)
        self.enable_disable_output_name(self.widget.output_name_enable.isChecked())
        self.edit_args(
            "save_precision", self.widget.save_precision_selector.currentText()
        )
        self.enable_disable_resume(self.widget.resume_enable.isChecked())
        self.edit_args("save_model_as", self.widget.save_as_selector.currentText())
        self.enable_disable_last(self.widget.save_only_last_enable.isChecked())
        self.enable_disable_ratio(self.widget.save_ratio_enable.isChecked())
        self.enable_disable_tag_file(self.widget.save_tag_enable.isChecked())
        self.enable_disable_freq(self.widget.save_freq_enable.isChecked())
        self.enable_disable_toml(self.widget.save_toml_enable.isChecked())
        self.enable_disable_save_state(self.widget.save_state_enable.isChecked())

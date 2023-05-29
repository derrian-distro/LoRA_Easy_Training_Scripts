import os.path

from PySide6 import QtWidgets, QtCore, QtGui

import modules.DragDropLineEdit
from ui_files.SampleUI import Ui_sample_ui
from modules.CollapsibleWidget import CollapsibleWidget


class SampleWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super(SampleWidget, self).__init__(parent)

        self.args = {}
        self.name = "sample_args"
        self.edited_previously = False

        self.setLayout(QtWidgets.QVBoxLayout())
        self.colap = CollapsibleWidget(self, "Sample Args")
        self.layout().addWidget(self.colap)
        self.layout().setContentsMargins(9, 0, 9, 0)
        self.content = QtWidgets.QWidget()
        self.colap.add_widget(self.content, "main_widget")

        self.widget = Ui_sample_ui()
        self.widget.setupUi(self.content)
        self.widget.sample_prompt_selector.setIcon(QtGui.QIcon(os.path.join("icons", "more-horizontal.svg")))

        # handle logic
        self.widget.sampler_input.currentTextChanged.connect(self.change_sampler)
        self.widget.sample_prompt_txt_file_input.setMode("file", [".txt"])
        self.widget.sample_prompt_txt_file_input.highlight = True
        self.widget.sample_prompt_txt_file_input.textChanged.connect(lambda x: self.edit_args(
            "sample_prompts", x, elem=self.widget.sample_prompt_txt_file_input))
        self.widget.sample_prompt_selector.clicked.connect(self.set_from_dialog)
        self.widget.steps_epochs_selector.currentIndexChanged.connect(self.steps_epochs_changed)
        self.widget.steps_epoch_input.valueChanged.connect(self.steps_epochs_input_changed)
        self.widget.sample_args_box.clicked.connect(self.enable_disable)

    @QtCore.Slot(str)
    def change_sampler(self, elem: str) -> None:
        self.args['sample_sampler'] = elem.lower()

    @QtCore.Slot(str, object, QtWidgets.QWidget)
    def edit_args(self, name: str, value: object, elem: QtWidgets.QWidget = None) -> None:
        if elem:
            if isinstance(elem, modules.DragDropLineEdit.DragDropLineEdit):
                self.edited_previously = True
                elem.update_stylesheet()
        self.args[name] = value

    @QtCore.Slot()
    def set_from_dialog(self) -> None:
        extensions = " ".join(["*" + s for s in self.widget.sample_prompt_txt_file_input.extensions])
        path = self.widget.sample_prompt_txt_file_input.text()
        default_dir = os.path.split(path)[0] if os.path.exists(path) else ""
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open Text File With Prompts", dir=default_dir, filter=f"Text Files ({extensions})")
        self.widget.sample_prompt_txt_file_input.setText(file_name if file_name else path)

    @QtCore.Slot(int)
    def steps_epochs_changed(self, index: int) -> None:
        if index == 0:
            if "sample_every_n_epochs" in self.args:
                del self.args['sample_every_n_epochs']
            self.args['sample_every_n_steps'] = self.widget.steps_epoch_input.value()
        else:
            if "sample_every_n_steps" in self.args:
                del self.args['sample_every_n_steps']
            self.args['sample_every_n_epochs'] = self.widget.steps_epoch_input.value()

    @QtCore.Slot(int)
    def steps_epochs_input_changed(self, value: int) -> None:
        index = self.widget.steps_epochs_selector.currentIndex()
        if index == 0:
            if "sample_every_n_epochs" in self.args:
                del self.args['sample_every_n_epochs']
            self.args['sample_every_n_steps'] = value
        else:
            if "sample_every_n_steps" in self.args:
                del self.args['sample_every_n_steps']
            self.args['sample_every_n_epochs'] = value

    @QtCore.Slot()
    def enable_disable(self) -> None:
        checked = self.widget.sample_args_box.isChecked()
        if not checked:
            self.widget.sample_prompt_txt_file_input.setStyleSheet("")
            self.args = {}
        else:
            self.args['sample_prompts'] = self.widget.sample_prompt_txt_file_input.text()
            self.args['sample_sampler'] = self.widget.sampler_input.currentText().lower()
            self.steps_epochs_input_changed(self.widget.steps_epoch_input.value())
            if self.edited_previously:
                self.widget.sample_prompt_txt_file_input.update_stylesheet()

    def get_args(self, input_args: dict) -> None:
        if not self.widget.sample_args_box.isChecked():
            if "sample_args" in input_args:
                del input_args['sample_args']
            return
        valid = self.widget.sample_prompt_txt_file_input.update_stylesheet()
        input_args['sample_args'] = None if not valid else self.args
        if not valid:
            if self.colap.is_collapsed:
                self.colap.toggle_collapsed()
                self.colap.title_frame.update_arrow(False)
                self.colap.title_frame.setChecked(True)

    def get_dataset_args(self, input_args: dict) -> None:
        pass

    def load_args(self, args: dict) -> None:
        if self.name not in args:
            return
        args = args[self.name].get("args", None)
        if not args:
            self.widget.sample_args_box.setChecked(False)
            self.enable_disable()
            return
        self.widget.sampler_input.setCurrentText(args['sample_sampler'].upper())
        value = 'sample_every_n_epochs' if "sample_every_n_epochs" in args else "sample_every_n_steps"
        self.widget.steps_epoch_input.setValue(args[value])
        self.widget.steps_epochs_selector.setCurrentIndex(0 if value == "sample_every_n_steps" else 1)
        self.widget.sample_prompt_txt_file_input.setText(args['sample_prompts'])
        self.widget.sample_args_box.setChecked(True)
        self.enable_disable()

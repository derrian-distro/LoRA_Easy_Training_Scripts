import os.path
from typing import Union

from PySide6 import QtWidgets, QtCore, QtGui

import modules.DragDropLineEdit
from modules.CollapsibleWidget import CollapsibleWidget
from ui_files.SavingUI import Ui_saving_ui


class SavingWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super(SavingWidget, self).__init__(parent)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.args = {"output_dir": "", "save_precision": "fp16", "save_model_as": "safetensors"}
        self.name = "saving_args"
        self.resume_edited_previously = False
        self.colap = CollapsibleWidget(self, "Saving Args")
        self.content = QtWidgets.QWidget()
        self.widget = Ui_saving_ui()
        self.widget.setupUi(self.content)
        self.colap.add_widget(self.content, "main_widget")
        self.layout().addWidget(self.colap)
        self.layout().setContentsMargins(9, 0, 9, 0)

        # setup output_folder
        self.widget.output_folder_input.setMode('folder')
        self.widget.output_folder_input.highlight = True
        self.widget.output_folder_selector.setIcon(QtGui.QIcon(os.path.join("icons", "more-horizontal.svg")))

        # setup resume_folder
        self.widget.resume_input.setMode("folder")
        self.widget.resume_input.highlight = True
        self.widget.resume_selector.setIcon(QtGui.QIcon(os.path.join("icons", "more-horizontal.svg")))

        # setup tag occurance
        self.widget.save_tag_input.setMode('folder')
        self.widget.save_tag_input.highlight = True
        self.widget.save_tag_selector.setIcon(QtGui.QIcon(os.path.join("icons", "more-horizontal.svg")))

        # setup toml file
        self.widget.save_toml_input.setMode("folder")
        self.widget.save_toml_input.highlight = True
        self.widget.save_toml_selector.setIcon(QtGui.QIcon(os.path.join("icons", "more-horizontal.svg")))

        # connections for output folder
        self.widget.output_folder_input.textChanged.connect(lambda x: self.edit_args(
            "output_dir", x, elem=self.widget.output_folder_input))
        self.widget.output_folder_selector.clicked.connect(lambda: self.set_from_dialog(self.widget.output_folder_input,
                                                                                        "Select the output Directory"))

        # connections for output name
        self.widget.output_name_enable.clicked.connect(self.enable_disable_output_name)
        self.widget.output_name_input.textChanged.connect(lambda x: self.edit_args("output_name", x, True))

        # connections for save precision and save as
        self.widget.save_precision_selector.currentTextChanged.connect(lambda x: self.edit_args("save_precision", x))
        self.widget.save_as_selector.currentTextChanged.connect(lambda x: self.edit_args("save_model_as", x))

        # connections for save freq
        self.widget.save_freq_enable.clicked.connect(lambda x: self.enable_disable_freq_last(x, True))
        self.widget.save_freq_selector.currentIndexChanged.connect(self.set_freq_type)
        self.widget.save_freq_input.valueChanged.connect(lambda x: self.set_freq_type(
            self.widget.save_freq_selector.currentIndex()))

        # connections for save last
        self.widget.save_only_last_enable.clicked.connect(lambda x: self.enable_disable_freq_last(x, False))
        self.widget.save_last_selector.currentIndexChanged.connect(self.set_last_type)
        self.widget.save_last_input.valueChanged.connect(lambda x: self.set_last_type(
            self.widget.save_last_selector.currentIndex()))

        # connections for save ratio
        self.widget.save_ratio_enable.clicked.connect(self.enable_disable_ratio)
        self.widget.save_ratio_input.valueChanged.connect(lambda x: self.edit_args("save_n_epoch_ratio", x, True))

        # connections for save state and last state
        self.widget.save_state_enable.clicked.connect(self.enable_disable_save_state)
        self.widget.save_last_state_enable.clicked.connect(self.enable_disable_last_state)
        self.widget.save_last_state_selector.currentIndexChanged.connect(self.set_last_state)
        self.widget.save_last_state_input.valueChanged.connect(lambda x: self.set_last_state(
            self.widget.save_last_state_selector.currentIndex()
        ))

        # connections for resume
        self.widget.resume_input.textChanged.connect(lambda x: self.edit_args(
            "resume", x, elem=self.widget.resume_input))
        self.widget.resume_selector.clicked.connect(lambda: self.set_from_dialog(self.widget.resume_input,
                                                                                 "Select the resume folder"))
        self.widget.resume_enable.clicked.connect(self.enable_disable_resume)

        self.widget.save_tags_enable.clicked.connect(self.enable_disable_tag_file)
        self.widget.save_tag_input.textChanged.connect(lambda x: self.edit_args("tag_file_location", x, True))
        self.widget.save_tag_selector.clicked.connect(lambda: self.set_from_dialog(self.widget.save_tag_input,
                                                                                   "Select the output Directory"))

        self.widget.save_toml_on_train_enable.clicked.connect(self.enable_disable_toml_file)
        self.widget.save_toml_input.textChanged.connect(lambda x: self.edit_args("save_toml_location", x, True))
        self.widget.save_toml_selector.clicked.connect(lambda: self.set_from_dialog(self.widget.save_toml_input,
                                                                                    "Select the output Directory"))

    @QtCore.Slot(str, object, bool, QtWidgets.QWidget)
    def edit_args(self, name: str, value: object, optional: bool = False, elem: QtWidgets.QWidget = None) -> None:
        if elem:
            if isinstance(elem, modules.DragDropLineEdit.DragDropLineEdit):
                if elem == self.widget.resume_input and not self.resume_edited_previously:
                    self.resume_edited_previously = True
                else:
                    elem.update_stylesheet()
        if not optional:
            self.args[name] = value
            return
        if value:
            self.args[name] = value
        else:
            if name in self.args:
                del self.args[name]

    # @QtCore.Slot(bool)
    # def set_from_dialog(self, is_resume: bool = False) -> None:
    #     if is_resume:
    #         folder = self.widget.resume_input.text()
    #     else:
    #         folder = self.widget.output_folder_input.text()
    #     default_dir = folder if os.path.exists(folder) else ""
    #     file_name = QtWidgets.QFileDialog.getExistingDirectory(
    #         self, "Select the output Directory" if not is_resume else "Select the resume folder", dir=default_dir)
    #     if not file_name:
    #         return
    #     if not is_resume:
    #         self.widget.output_folder_input.setText(file_name)
    #     else:
    #         self.widget.resume_input.setText(file_name)

    @QtCore.Slot(modules.DragDropLineEdit.DragDropLineEdit, str)
    def set_from_dialog(self, text_edit: modules.DragDropLineEdit.DragDropLineEdit, prompt: str):
        folder = text_edit.text()
        default_dir = folder if os.path.exists(folder) else ""
        file_name = QtWidgets.QFileDialog.getExistingDirectory(self, prompt, dir=default_dir)
        if not file_name:
            return
        text_edit.setText(file_name)

    @QtCore.Slot(int)
    def set_freq_type(self, index: int) -> None:
        if "save_every_n_epochs" in self.args:
            del self.args['save_every_n_epochs']
        if "save_every_n_steps" in self.args:
            del self.args['save_every_n_steps']
        name = "save_every_n_epochs" if index == 0 else "save_every_n_steps"
        self.edit_args(name, self.widget.save_freq_input.value(), True)

    @QtCore.Slot(int)
    def set_last_type(self, index: int) -> None:
        if "save_last_n_epochs" in self.args:
            del self.args['save_last_n_epochs']
        if 'save_last_n_steps' in self.args:
            del self.args['save_last_n_steps']
        name = "save_last_n_epochs" if index == 0 else "save_last_n_steps"
        self.edit_args(name, self.widget.save_last_input.value(), True)

    @QtCore.Slot(bool)
    def enable_disable_output_name(self, checked: bool) -> None:
        if checked:
            self.widget.output_name_input.setEnabled(True)
            self.edit_args("output_name", self.widget.output_name_input.text(), True)
        else:
            self.widget.output_name_input.setEnabled(False)
            if "output_name" in self.args:
                del self.args["output_name"]

    @QtCore.Slot(bool, bool)
    def enable_disable_freq_last(self, checked: bool, is_freq: bool) -> None:
        if is_freq:
            if checked:
                self.widget.save_freq_selector.setEnabled(True)
                self.widget.save_freq_input.setEnabled(True)
                self.set_freq_type(self.widget.save_freq_selector.currentIndex())
            else:
                self.widget.save_freq_selector.setEnabled(False)
                self.widget.save_freq_input.setEnabled(False)
                for name in ['save_every_n_epochs', "save_every_n_steps"]:
                    if name in self.args:
                        del self.args[name]
        else:
            if checked:
                self.widget.save_last_selector.setEnabled(True)
                self.widget.save_last_input.setEnabled(True)
                self.set_last_type(self.widget.save_last_selector.currentIndex())
            else:
                self.widget.save_last_selector.setEnabled(False)
                self.widget.save_last_input.setEnabled(False)
                for name in ['save_last_n_steps', 'save_last_n_epochs']:
                    if name in self.args:
                        del self.args[name]

    @QtCore.Slot(bool)
    def enable_disable_ratio(self, checked: bool) -> None:
        if checked:
            self.widget.save_ratio_input.setEnabled(True)
            self.edit_args("save_n_epoch_ratio", self.widget.save_ratio_input.value(), True)
        else:
            self.widget.save_ratio_input.setEnabled(False)
            if "save_n_epoch_ratio" in self.args:
                del self.args['save_n_epoch_ratio']

    @QtCore.Slot(bool)
    def enable_disable_save_state(self, checked: bool) -> None:
        self.widget.save_last_state_enable.setEnabled(checked)
        if checked:
            self.enable_disable_last_state(self.widget.save_last_state_enable.isChecked())
            self.args['save_state'] = True
        else:
            self.enable_disable_last_state(False)
            if "save_state" in self.args:
                del self.args['save_state']

    @QtCore.Slot(bool)
    def enable_disable_last_state(self, checked: bool) -> None:
        self.widget.save_last_state_selector.setEnabled(checked)
        self.widget.save_last_state_input.setEnabled(checked)
        if checked:
            self.set_last_state(self.widget.save_last_state_selector.currentIndex())
        else:
            for name in ['save_last_n_epochs_state', 'save_last_n_steps_state']:
                if name in self.args:
                    del self.args[name]

    @QtCore.Slot(bool)
    def enable_disable_tag_file(self, checked: bool):
        self.widget.save_tag_input.setEnabled(checked)
        self.widget.save_tag_selector.setEnabled(checked)
        if checked:
            self.edit_args("tag_occurrence", checked, True)
            self.edit_args('tag_file_location', self.widget.save_tag_input.text(), True)
        else:
            if 'tag_occurrence' in self.args:
                del self.args['tag_occurrence']
            if "tag_file_location" in self.args:
                del self.args['tag_file_location']

    @QtCore.Slot(bool)
    def enable_disable_toml_file(self, checked: bool):
        self.widget.save_toml_selector.setEnabled(checked)
        self.widget.save_toml_input.setEnabled(checked)
        if checked:
            self.edit_args("save_toml", checked, True)
            self.edit_args("save_toml_location", self.widget.save_toml_input.text(), True)
        else:
            if 'save_toml' in self.args:
                del self.args['save_toml']
            if 'save_toml_location' in self.args:
                del self.args['save_toml_location']

    @QtCore.Slot(int)
    def set_last_state(self, index: int) -> None:
        names = ['save_last_n_epochs_state', 'save_last_n_steps_state']
        for name in names:
            if name in self.args:
                del self.args[name]
        self.edit_args(names[index], self.widget.save_last_state_input.value(), True)

    @QtCore.Slot(bool)
    def enable_disable_resume(self, checked: bool) -> None:
        self.widget.resume_selector.setEnabled(checked)
        self.widget.resume_input.setEnabled(checked)
        if checked:
            self.edit_args("resume", self.widget.resume_input.text(), elem=self.widget.resume_input)
        else:
            if "resume" in self.args:
                del self.args['resume']
            self.widget.resume_input.setStyleSheet("")

    def get_args(self, input_args: dict) -> None:
        valid = self.widget.output_folder_input.update_stylesheet()
        if valid and self.widget.resume_enable.isChecked():
            valid = self.widget.resume_input.update_stylesheet()
        input_args['saving_args'] = None if not valid else self.args
        if not valid:
            if self.colap.is_collapsed:
                self.colap.toggle_collapsed()
                self.colap.title_frame.update_arrow(False)
                self.colap.title_frame.setChecked(True)

    def get_dataset_args(self, input_args: dict) -> None:
        return

    def load_args(self, args: dict) -> None:
        if self.name not in args:
            return
        args = args[self.name]['args']
        self.widget.output_folder_input.setText(args['output_dir'])
        self.widget.output_name_input.setText(args.get("output_name", ""))
        self.widget.output_name_enable.setChecked(True if "output_name" in args else False)
        self.enable_disable_output_name(True if "output_name" in args else False)
        self.widget.save_precision_selector.setCurrentText(args['save_precision'])
        self.widget.save_as_selector.setCurrentText(args['save_model_as'])

        value = args['save_every_n_epochs'] if "save_every_n_epochs" in args else args.get("save_every_n_steps", None)
        if value:
            self.widget.save_freq_input.setValue(value)
            self.widget.save_freq_enable.setChecked(True)
            self.widget.save_freq_selector.setCurrentIndex(0 if "save_every_n_epochs" in args else 1)
            self.enable_disable_freq_last(True, True)
        else:
            self.widget.save_freq_enable.setChecked(False)
            self.enable_disable_freq_last(False, True)

        self.widget.save_ratio_input.setValue(args.get("save_n_epoch_ratio", 1))
        self.widget.save_ratio_enable.setChecked(True if "save_n_epoch_ratio" in args else False)
        self.enable_disable_ratio(True if "save_n_epoch_ratio" in args else False)

        value = args['save_last_n_epochs'] if "save_last_n_epochs" in args else args.get("save_last_n_steps", None)
        if value:
            self.widget.save_last_input.setValue(value)
            self.widget.save_only_last_enable.setChecked(True)
            self.widget.save_last_selector.setCurrentIndex(0 if "save_last_n_epochs" in args else 1)
            self.enable_disable_freq_last(True, False)
        else:
            self.widget.save_only_last_enable.setChecked(False)
            self.enable_disable_freq_last(False, False)

        value = args['save_last_n_epochs_state'] if "save_last_n_epochs_state" in args else \
            args.get("save_last_n_epochs_steps", None)
        if value:
            self.widget.save_last_state_input.setValue(value)
            self.widget.save_last_state_selector.setCurrentIndex(0 if "save_last_n_epochs_state" in args else 1)
            self.widget.save_last_state_enable.setChecked(True)
        self.widget.save_state_enable.setChecked(True if value else False)
        self.enable_disable_save_state(True if value else False)

        checked = True if args.get("resume", None) else False
        self.widget.resume_input.setText(args.get("resume", ""))
        self.widget.resume_enable.setChecked(checked)
        self.enable_disable_resume(checked)

        checked = args.get("tag_occurrence", False)
        self.widget.save_tags_enable.setChecked(checked)
        self.enable_disable_tag_file(checked)
        self.widget.save_tag_input.setText(args.get('tag_file_location', ""))

        checked = args.get("save_toml", False)
        self.widget.save_toml_on_train_enable.setChecked(checked)
        self.enable_disable_toml_file(checked)
        self.widget.save_toml_input.setText(args.get('save_toml_location', ""))

    def save_args(self) -> Union[dict, None]:
        return self.args

    def save_dataset_args(self) -> Union[dict, None]:
        pass

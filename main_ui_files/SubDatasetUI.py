import os.path
from typing import Union

from modules.CollapsibleWidget import CollapsibleWidget
from modules.DragDropLineEdit import DragDropLineEdit
from modules.LineEditHighlight import LineEditWithHighlight

from PySide6 import QtWidgets, QtCore, QtGui
from ui_files.sub_dataset_input import Ui_sub_dataset_input
from ui_files.sub_dataset_extra_input import Ui_sub_dataset_extra_input


class SubsetItem(QtWidgets.QWidget):
    args_edited = QtCore.Signal(str, object)

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super(SubsetItem, self).__init__(parent)
        self.args = {
            'num_repeats': 1, 'keep_tokens': 0, 'caption_extension': '.txt', 'shuffle_caption': False,
            'flip_aug': False, 'color_aug': False, 'random_crop': False, 'is_reg': False, "image_dir": ""
        }
        self.widget = Ui_sub_dataset_input()
        self.sub_widget = QtWidgets.QWidget()
        self.sub_widget_args = Ui_sub_dataset_extra_input()
        self.sub_widget_args.setupUi(self.sub_widget)
        self.widget.setupUi(self)
        self.layout().setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.widget.extra_args.add_widget(self.sub_widget, "sub_args")
        self.widget.extra_args.title_frame.setText("Optional Args")
        self.widget.file_dialog_button.setIcon(QtGui.QIcon(os.path.join("icons", "more-horizontal.svg")))

        # handle logic for image dir
        self.widget.lineEdit.setMode("folder")
        self.widget.lineEdit.highlight = True
        self.widget.lineEdit.textChanged.connect(lambda x: self.edit_args("image_dir", x, self.widget.lineEdit))
        self.widget.file_dialog_button.clicked.connect(self.set_from_dialog)

        # handle logic for the spin boxes and combobox
        self.widget.repeats_spinbox.valueChanged.connect(lambda x: self.edit_args("num_repeats", x))
        self.widget.keep_tokens_spinbox.valueChanged.connect(lambda x: self.edit_args("keep_tokens", x))
        self.widget.caption_extension.currentTextChanged.connect(lambda x: self.edit_args("caption_extension", x))

        # handle logic for the checkboxes
        self.widget.shuffle_captions.stateChanged.connect(lambda x: self.edit_args("shuffle_caption", x == 2))
        self.widget.flip_aug.stateChanged.connect(lambda x: self.edit_args("flip_aug", x == 2))
        self.widget.color_aug.stateChanged.connect(lambda x: self.edit_args("color_aug", x == 2))
        self.widget.random_crop.stateChanged.connect(lambda x: self.edit_args("random_crop", x == 2))
        self.widget.reg_images.stateChanged.connect(lambda x: self.edit_args("is_reg", x == 2))

        # handle logic for face crop
        self.sub_widget_args.face_crop_layout.clicked.connect(self.enable_disable_crop_aug)
        self.sub_widget_args.face_crop_width.valueChanged.connect(lambda x: self.edit_args("face_crop_aug_range", [
            x, self.sub_widget_args.face_crop_height.value()]))
        self.sub_widget_args.face_crop_height.valueChanged.connect(lambda x: self.edit_args("face_crop_aug_range", [
            self.sub_widget_args.face_crop_width.value(), x]))

        # handle logic for caption dropout
        self.sub_widget_args.caption_dropout_layout.clicked.connect(self.enable_disable_caption_dropout)
        self.sub_widget_args.caption_dropout_rate_input.valueChanged.connect(lambda x: self.edit_args(
            "caption_dropout_rate", round(x, 2)))
        self.sub_widget_args.caption_epoch_dropout_input.valueChanged.connect(lambda x: self.edit_args(
            "caption_dropout_every_n_epochs", x))
        self.sub_widget_args.caption_tag_dropout_input.valueChanged.connect(lambda x: self.edit_args(
            "caption_tag_dropout_rate", round(x, 2)))

        # handle tag warmup
        self.sub_widget_args.token_warmup_layout.clicked.connect(self.enable_disable_tag_warmup)
        self.sub_widget_args.token_warmup_step_input.valueChanged.connect(lambda x: self.edit_args(
            "token_warmup_step", round(x, 2)))
        self.sub_widget_args.token_minimum_warmup_input.valueChanged.connect(lambda x: self.edit_args(
            "token_warmup_min", x))

    @QtCore.Slot(str, object, QtWidgets.QWidget)
    def edit_args(self, name: str, value: object, widget: QtWidgets.QWidget = None) -> None:
        if widget:
            if isinstance(widget, DragDropLineEdit):
                widget.update_stylesheet()
        self.args[name] = value
        self.args_edited.emit(name, value)

    @QtCore.Slot()
    def set_from_dialog(self, path: str = None) -> None:
        folder = self.widget.lineEdit.text()
        default_dir = folder if os.path.exists(folder) else ""
        if not path:
            file_name = QtWidgets.QFileDialog.getExistingDirectory(self, "open directory containing images",
                                                                   dir=default_dir)
            if not file_name:
                return
        else:
            file_name = path
        try:
            repeats = int(os.path.split(file_name)[-1].split("_")[0])
            self.widget.repeats_spinbox.setValue(repeats)
        except ValueError:
            pass
        self.widget.lineEdit.setText(file_name)

    @QtCore.Slot(bool)
    def enable_disable_crop_aug(self, checked: bool) -> None:
        if checked:
            self.args['face_crop_aug_range'] = [
                self.sub_widget_args.face_crop_width.value(),
                self.sub_widget_args.face_crop_height.value()
            ]
        else:
            if 'face_crop_aug_range' in self.args:
                del self.args['face_crop_aug_range']

    @QtCore.Slot(bool)
    def enable_disable_caption_dropout(self, checked: bool) -> None:
        if checked:
            self.args['caption_dropout_rate'] = self.sub_widget_args.caption_dropout_rate_input.value()
            self.args['caption_dropout_every_n_epochs'] = self.sub_widget_args.caption_epoch_dropout_input.value()
            self.args['caption_tag_dropout_rate'] = self.sub_widget_args.caption_tag_dropout_input.value()
        else:
            if "caption_dropout_rate" in self.args:
                del self.args['caption_dropout_rate']
            if "caption_dropout_every_n_epochs" in self.args:
                del self.args['caption_dropout_every_n_epochs']
            if "caption_tag_dropout_rate" in self.args:
                del self.args['caption_tag_dropout_rate']

    @QtCore.Slot(bool)
    def enable_disable_tag_warmup(self, checked: bool) -> None:
        if checked:
            self.args['token_warmup_min'] = self.sub_widget_args.token_minimum_warmup_input.value()
            self.args['token_warmup_step'] = self.sub_widget_args.token_warmup_step_input.value()
        else:
            if "token_warmup_min" in self.args:
                del self.args['token_warmup_min']
                del self.args['token_warmup_step']

    @QtCore.Slot(bool)
    def enable_disable_cache_dependants(self, checked: bool) -> None:
        self.widget.color_aug.setEnabled(not checked)
        self.widget.random_crop.setEnabled(not checked)
        if not checked:
            self.edit_args("color_aug", self.widget.color_aug.isChecked())
            self.edit_args("random_crop", self.widget.random_crop.isChecked())
        else:
            for name in ['color_aug', "random_crop"]:
                if name in self.args:
                    del self.args[name]

    def load_args(self, args: dict) -> None:
        self.widget.lineEdit.setText(args['image_dir'])
        self.widget.repeats_spinbox.setValue(args['num_repeats'])
        self.edit_args("num_repeats", args['num_repeats'])

        self.widget.keep_tokens_spinbox.setValue(args['keep_tokens'])
        self.edit_args("keep_tokens", args['keep_tokens'])

        self.widget.caption_extension.setCurrentText(args['caption_extension'])

        self.widget.shuffle_captions.setChecked(args.get("shuffle_caption", False))
        self.edit_args("shuffle_caption", args.get("shuffle_caption", False))

        self.widget.flip_aug.setChecked(args.get("flip_aug", False))
        self.edit_args("flip_aug", args.get("flip_aug", False))

        self.widget.color_aug.setChecked(args.get("color_aug", False))
        self.edit_args("color_aug", args.get("color_aug", False))

        self.widget.random_crop.setChecked(args.get("random_crop", False))
        self.edit_args("random_crop", args.get("random_crop", False))

        self.widget.reg_images.setChecked(args.get("is_reg", False))
        self.edit_args("is_reg", args.get("is_reg", False))

        face_crop = args.get("face_crop_aug_range", None)
        self.sub_widget_args.face_crop_width.setValue(face_crop[0] if face_crop else 1)
        self.sub_widget_args.face_crop_height.setValue(face_crop[1] if face_crop else 1)
        self.sub_widget_args.face_crop_layout.setChecked(True if face_crop else False)
        self.enable_disable_crop_aug(True if face_crop else False)

        checked = True if "caption_dropout_rate" in args else False
        self.sub_widget_args.caption_dropout_rate_input.setValue(args.get("caption_dropout_rate", 0.01))
        self.sub_widget_args.caption_epoch_dropout_input.setValue(args.get("caption_dropout_every_n_epochs", 1))
        self.sub_widget_args.caption_tag_dropout_input.setValue(args.get("caption_tag_dropout_rate", 0.01))
        self.sub_widget_args.caption_dropout_layout.setChecked(checked)
        self.enable_disable_caption_dropout(checked)

        checked = True if "token_warmup_min" in args else False
        self.sub_widget_args.token_minimum_warmup_input.setValue(args.get("token_warmup_min", 1))
        self.sub_widget_args.token_warmup_step_input.setValue(args.get("token_warmup_step", 1))
        self.sub_widget_args.token_warmup_layout.setChecked(checked)
        self.enable_disable_tag_warmup(checked)


class SubDatasetWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super(SubDatasetWidget, self).__init__(parent)
        self.setMinimumSize(600, 300)

        self.cache_latents_checked = False
        self.elements: list[tuple[QtWidgets.QWidget, CollapsibleWidget, SubsetItem]] = []

        self.main_layout = QtWidgets.QGridLayout()
        self.setLayout(self.main_layout)
        self.main_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.add_bulk_button = QtWidgets.QPushButton()
        self.add_bulk_button.setText("Add all subfolders from folder")
        self.add_bulk_button.clicked.connect(self.add_from_root_folder)
        self.add_bulk_button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.main_layout.addWidget(self.add_bulk_button, 0, 0, 1, 2)

        self.add_button = QtWidgets.QPushButton()
        self.add_button.setText("Add Data Subset")
        self.add_button.clicked.connect(self.add_empty_subset)
        self.add_button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.main_layout.addWidget(self.add_button, 1, 1, 1, 1)

        self.add_label = LineEditWithHighlight()
        self.add_label.setPlaceholderText("Name of subset")
        self.add_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.main_layout.addWidget(self.add_label, 1, 0, 1, 1)

        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollWidget = QtWidgets.QWidget()
        self.scrollArea.setWidget(self.scrollWidget)
        self.main_layout.addWidget(self.scrollArea, 2, 0, 1, 2)
        self.scrollLayout = QtWidgets.QVBoxLayout(self.scrollWidget)
        self.scrollLayout.setSpacing(0)
        self.scrollLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.scrollLayout.setContentsMargins(9, 0, 9, 0)

    @QtCore.Slot()
    def add_empty_subset(self, name: str = "") -> SubsetItem:
        scroll_widget = QtWidgets.QWidget(self.scrollArea)
        scroll_widget.setLayout(QtWidgets.QHBoxLayout())
        self.scrollWidget.layout().addWidget(scroll_widget)

        colap = CollapsibleWidget(scroll_widget, title=self.add_label.text() if not name else name, remove_elem=True)
        colap.layout().setContentsMargins(9, 9, 9, 0)
        colap.extra_elem.clicked.connect(lambda: self.delete_subset((scroll_widget, colap, subset)))
        scroll_widget.layout().addWidget(colap)
        if len(self.elements) == 0:
            colap.toggle_collapsed()
            colap.title_frame.setChecked(True)

        subset = SubsetItem()
        subset.sub_widget.layout().setContentsMargins(9, 9, 9, 0)
        subset.enable_disable_cache_dependants(self.cache_latents_checked)
        colap.add_widget(subset, 'main_widget')
        self.elements.append((scroll_widget, colap, subset))
        return subset

    @QtCore.Slot(tuple)
    def delete_subset(self, elem: tuple) -> None:
        self.elements.pop(self.elements.index(elem))
        index = self.scrollWidget.layout().indexOf(elem[0])
        val = self.scrollWidget.layout().takeAt(index)
        if val.widget() is not None:
            val.widget().deleteLater()

    @QtCore.Slot(bool)
    def cache_checked(self, checked: bool) -> None:
        self.cache_latents_checked = checked
        for elem in self.elements:
            elem[2].enable_disable_cache_dependants(checked)

    @QtCore.Slot()
    def add_from_root_folder(self):
        file_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Root folder that all image folders are in")
        if not file_path or not os.path.isdir(file_path):
            return
        while len(self.elements) > 0:
            self.delete_subset(self.elements[0])
        for elem in os.listdir(file_path):
            if not os.path.isdir(os.path.join(file_path, elem)):
                continue
            subset = self.add_empty_subset(elem)
            subset.set_from_dialog(os.path.join(file_path, elem))

    def get_subset_args(self, skip_check: bool = False) -> Union[list[dict], None]:
        args_list = []
        failed_args = []
        if skip_check:
            for arg in self.elements:
                args_list.append(arg[2].args)
            return args_list
        for arg in self.elements:
            exists = os.path.exists(arg[2].args['image_dir'])
            if (not exists) or (not os.path.isdir(arg[2].args['image_dir'])):
                failed_args.append(arg)
                arg[2].widget.lineEdit.update_stylesheet()
                if arg[1].is_collapsed:
                    arg[1].toggle_collapsed()
                    arg[1].title_frame.update_arrow(False)
                    arg[1].title_frame.setChecked(True)
                continue
            args_list.append(arg[2].args)
        if len(failed_args) > 0 or len(self.elements) == 0:
            print("At least one subset arg doesn't have an input folder set properly")
            return None
        return args_list

    def load_args(self, args: dict) -> None:
        if "subsets" not in args:
            return
        while len(self.elements) > 0:
            self.delete_subset(self.elements[0])

        subsets = args['subsets']
        for subset in subsets:
            elem = self.add_empty_subset(os.path.split(subset['image_dir'])[-1])
            elem.load_args(subset)
        self.cache_checked(self.cache_latents_checked)

import os.path
from modules.DragDropLineEdit import DragDropLineEdit

from PySide6 import QtWidgets, QtCore, QtGui
from ui_files.sub_dataset_input import Ui_sub_dataset_input
from ui_files.sub_dataset_extra_input import Ui_sub_dataset_extra_input


class SubsetWidget(QtWidgets.QWidget):
    args_edited = QtCore.Signal(str, object)

    def __init__(self, parent: QtWidgets.QWidget = None):
        super(SubsetWidget, self).__init__(parent)
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
    def edit_args(self, name: str, value: object, widget: QtWidgets.QWidget = None):
        if widget:
            if isinstance(widget, DragDropLineEdit):
                widget.update_stylesheet()
        self.args[name] = value
        self.args_edited.emit(name, value)

    @QtCore.Slot()
    def set_from_dialog(self):
        file_name = QtWidgets.QFileDialog.getExistingDirectory(self, "open directory containing images")
        if not file_name:
            return
        try:
            repeats = int(os.path.split(file_name)[-1].split("_")[0])
            self.widget.repeats_spinbox.setValue(repeats)
        except ValueError:
            pass
        self.widget.lineEdit.setText(file_name)

    @QtCore.Slot(bool)
    def enable_disable_crop_aug(self, checked: bool):
        if checked:
            self.args['face_crop_aug_range'] = [
                self.sub_widget_args.face_crop_width.value(),
                self.sub_widget_args.face_crop_height.value()
            ]
        else:
            if 'face_crop_aug_range' in self.args:
                del self.args['face_crop_aug_range']

    @QtCore.Slot(bool)
    def enable_disable_caption_dropout(self, checked: bool):
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
    def enable_disable_tag_warmup(self, checked: bool):
        if checked:
            self.args['token_warmup_min'] = self.sub_widget_args.token_minimum_warmup_input.value()
            self.args['token_warmup_step'] = self.sub_widget_args.token_warmup_step_input.value()
        else:
            if "token_warmup_min" in self.args:
                del self.args['token_warmup_min']
                del self.args['token_warmup_step']

    @QtCore.Slot(bool)
    def enable_disable_cache_dependants(self, checked: bool):
        self.widget.color_aug.setEnabled(not checked)
        self.widget.random_crop.setEnabled(not checked)
        if not checked:
            self.edit_args("color_aug", self.widget.color_aug.isChecked())
            self.edit_args("random_crop", self.widget.random_crop.isChecked())
        else:
            for name in ['color_aug', "random_crop"]:
                if name in self.args:
                    del self.args[name]

    def load_args(self, args: dict):
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



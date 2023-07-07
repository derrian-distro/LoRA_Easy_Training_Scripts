import os.path
from typing import Union

from PySide6 import QtWidgets, QtCore, QtGui

import modules.DragDropLineEdit
from ui_files.BaseUI import Ui_base_args_ui
from modules.CollapsibleWidget import CollapsibleWidget


class BaseArgsWidget(QtWidgets.QWidget):
    CacheLatentsChecked = QtCore.Signal(bool)
    SdxlChecked = QtCore.Signal(bool)

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super(BaseArgsWidget, self).__init__(parent)
        self.args = {"pretrained_model_name_or_path": "", "mixed_precision": "fp16", "seed": 23, "clip_skip": 2,
                     "xformers": True, "max_train_epochs": 1, "max_data_loader_n_workers": 1,
                     "persistent_data_loader_workers": True, "max_token_length": 225, "prior_loss_weight": 1.0}
        self.dataset_args = {"resolution": 512, "batch_size": 1}
        self.name = "general_args"
        self.setLayout(QtWidgets.QVBoxLayout())
        self.colap = CollapsibleWidget(self, "General Args")
        self.layout().addWidget(self.colap)
        self.layout().setContentsMargins(9, 0, 9, 0)
        self.content = QtWidgets.QWidget()
        self.colap.add_widget(self.content, "main_widget")

        self.widget = Ui_base_args_ui()
        self.widget.setupUi(self.content)
        self.widget.base_model_input.highlight = True
        self.widget.base_model_input.setMode("file", ['.ckpt', '.pt', '.safetensors'])
        self.widget.base_model_selector.setIcon(QtGui.QIcon(os.path.join("icons", "more-horizontal.svg")))

        # Base Model connections
        self.widget.base_model_input.textChanged.connect(lambda x: self.edit_args("pretrained_model_name_or_path", x,
                                                                                  elem=self.widget.base_model_input))
        self.widget.base_model_selector.clicked.connect(self.set_from_dialog)
        self.widget.sdxl_enable.clicked.connect(self.enable_disable_sdxl)
        self.widget.v2_enable.clicked.connect(self.enable_disable_sd2)
        self.widget.v_param_enable.clicked.connect(lambda x: self.enable_disable_sd2(self.widget.v2_enable.isChecked()))
        self.widget.v_pred_enable.clicked.connect(lambda x: self.edit_args("scale_v_pred_loss_like_noise_pred", x, True))

        # resolution connections
        self.widget.width_input.valueChanged.connect(lambda x: self.change_resolution(True, x))
        self.widget.height_input.valueChanged.connect(lambda x: self.change_resolution(False, x))
        self.widget.height_enable.clicked.connect(self.enable_disable_height)

        # gradient connections
        self.widget.gradient_box.clicked.connect(self.enable_disable_gradient)
        self.widget.gradient_selector.currentIndexChanged.connect(lambda x: self.enable_disable_gradient(True))
        self.widget.gradient_steps_input.valueChanged.connect(
            lambda x: self.edit_args("gradient_accumulation_steps", x))

        # max training time connections
        self.widget.max_train_selector.currentIndexChanged.connect(self.max_training_select)
        self.widget.max_train_input.valueChanged.connect(
            lambda x: self.max_training_select(self.widget.max_train_selector.currentIndex()))

        # cache latents connections
        self.widget.cache_latents_enable.clicked.connect(self.enable_cache_latents)
        self.widget.cache_latents_to_disk_enable.clicked.connect(lambda x: self.enable_cache_latents(True))

        # Comment in Metadata
        self.widget.comment_enable.clicked.connect(self.enable_disable_comment)
        self.widget.comment_input.textChanged.connect(lambda: self.edit_args(
            "training_comment", self.widget.comment_input.toPlainText(), True))

        # generic connections
        self.widget.seed_input.valueChanged.connect(lambda x: self.edit_args("seed", x))
        self.widget.clip_skip_input.valueChanged.connect(lambda x: self.edit_args("clip_skip", x))
        self.widget.loss_weight_input.valueChanged.connect(lambda x: self.edit_args("prior_loss_weight",
                                                                                    round(x, 2)))
        self.widget.xformers_enable.clicked.connect(self.enable_disable_xformers)
        self.widget.batch_size_input.valueChanged.connect(lambda x: self.edit_dataset_args("batch_size", x))
        self.widget.max_token_selector.currentIndexChanged.connect(self.edit_token_length)
        self.widget.mixed_precision_selector.currentTextChanged.connect(lambda x: self.edit_args(
            "mixed_precision", x if x != "float" else "no"))

    @QtCore.Slot(str, object, bool, QtWidgets.QWidget)
    def edit_args(self, name: str, value: object, optional: bool = False, elem: QtWidgets.QWidget = None) -> None:
        if elem and isinstance(elem, modules.DragDropLineEdit.DragDropLineEdit):
            elem.update_stylesheet()
        if not optional:
            self.args[name] = value
            return
        if not value:
            if name in self.args:
                del self.args[name]
            return
        self.args[name] = value

    @QtCore.Slot(str, object, bool)
    def edit_dataset_args(self, name: str, value: object, optional: bool = False) -> None:
        if not optional:
            self.dataset_args[name] = value
            return
        if not value:
            if name in self.dataset_args:
                del self.dataset_args[name]
            return
        self.dataset_args[name] = value

    @QtCore.Slot()
    def set_from_dialog(self) -> None:
        extensions = " ".join(["*" + s for s in self.widget.base_model_input.extensions])
        default_folder = os.path.split(self.widget.base_model_input.text())[0] if \
            os.path.exists(self.widget.base_model_input.text()) else ""
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open Model File", dir=default_folder,
            filter=f"Stable Diffusion Models ({extensions})")
        self.widget.base_model_input.setText(file_name or self.widget.base_model_input.text())

    @QtCore.Slot(bool)
    def enable_disable_sd2(self, checked: bool) -> None:
        if checked:
            self.args['v2'] = True
            self.widget.v_param_enable.setEnabled(True)
            self.edit_args("v_parameterization", self.widget.v_param_enable.isChecked(), True)
            self.widget.sdxl_enable.setEnabled(False)
            if self.widget.v_param_enable.isChecked():
                self.widget.v_pred_enable.setEnabled(True)
                self.edit_args("scale_v_pred_loss_like_noise_pred", self.widget.v_pred_enable.isChecked(), True)
            else:
                self.widget.v_pred_enable.setEnabled(False)
                self.edit_args("scale_v_pred_loss_like_noise_pred", False, True)
        else:
            self.widget.v_param_enable.setEnabled(False)
            self.widget.v_pred_enable.setEnabled(False)
            self.widget.sdxl_enable.setEnabled(True)
            for name in ['v2', 'v_parameterization', 'scale_v_pred_loss_like_noise_pred']:
                if name in self.args:
                    del self.args[name]

    @QtCore.Slot(bool)
    def enable_disable_sdxl(self, checked: bool) -> None:
        if checked:
            self.args['sdxl'] = True
            self.widget.v2_enable.setEnabled(False)
            self.enable_disable_sd2(False)
            self.SdxlChecked.emit(True)
        else:
            if 'sdxl' in self.args:
                del self.args['sdxl']
            self.widget.v2_enable.setEnabled(True)
            if self.widget.v2_enable.isChecked():
                self.enable_disable_sd2(True)
            self.SdxlChecked.emit(False)

    @QtCore.Slot(bool)
    def enable_disable_height(self, checked: bool) -> None:
        if checked:
            self.widget.height_input.setEnabled(True)
            self.dataset_args['resolution'] = [self.widget.width_input.value(), self.widget.height_input.value()]
        else:
            self.widget.height_input.setEnabled(False)
            self.dataset_args['resolution'] = self.widget.width_input.value()

    @QtCore.Slot(bool, int)
    def change_resolution(self, width: bool, value: int) -> None:
        if width:
            self.dataset_args['resolution'] = [value, self.widget.height_input.value()] if \
                self.widget.height_input.isEnabled() else value
        else:
            self.dataset_args['resolution'] = [self.widget.width_input.value(), value]

    @QtCore.Slot(bool)
    def enable_disable_gradient(self, checked: bool) -> None:
        for name in ['gradient_checkpointing', 'gradient_accumulation_steps']:
            if name in self.args:
                del self.args[name]
        if checked:
            checkpointing = self.widget.gradient_selector.currentIndex() == 0
            if checkpointing:
                self.args['gradient_checkpointing'] = True
                self.widget.gradient_steps_input.setEnabled(False)
            else:
                self.args['gradient_accumulation_steps'] = self.widget.gradient_steps_input.value()
                self.widget.gradient_steps_input.setEnabled(True)

    @QtCore.Slot(bool)
    def enable_disable_comment(self, checked: bool) -> None:
        self.widget.comment_input.setEnabled(checked)
        self.edit_args("training_comment", self.widget.comment_input.toPlainText() if checked else None, True)

    @QtCore.Slot(int)
    def max_training_select(self, index: int) -> None:
        for name in ['max_train_epochs', "max_train_steps"]:
            if name in self.args:
                del self.args[name]
        self.args[f'max_train_{"epochs" if index == 0 else "steps"}'] = self.widget.max_train_input.value()

    @QtCore.Slot(bool)
    def enable_cache_latents(self, checked: bool) -> None:
        for name in ['cache_latents', "cache_latents_to_disk"]:
            if name in self.args:
                del self.args[name]
        self.CacheLatentsChecked.emit(checked)
        if checked:
            self.args['cache_latents'] = True
            self.widget.cache_latents_to_disk_enable.setEnabled(True)
            if self.widget.cache_latents_to_disk_enable.isChecked():
                self.args['cache_latents_to_disk'] = True
        else:
            self.widget.cache_latents_to_disk_enable.setEnabled(False)

    @QtCore.Slot(bool)
    def enable_disable_xformers(self, checked: bool) -> None:
        if "xformers" in self.args:
            del self.args['xformers']
        if checked:
            self.args['xformers'] = True

    @QtCore.Slot(int)
    def edit_token_length(self, index: int) -> None:
        if "max_token_length" in self.dataset_args:
            del self.args['max_token_length']
        if index != 2:
            self.args['max_token_length'] = int(self.widget.max_token_selector.currentText())

    def get_args(self, input_args: dict) -> None:
        valid = self.widget.base_model_input.update_stylesheet()
        input_args['general_args'] = self.args if valid else None
        if not valid and self.colap.is_collapsed:
            self.colap.toggle_collapsed()
            self.colap.title_frame.update_arrow(False)
            self.colap.title_frame.setChecked(True)

    def get_dataset_args(self, input_args: dict) -> None:
        valid = self.widget.base_model_input.update_stylesheet()
        input_args['general_args'] = self.dataset_args if valid else None

    def load_args(self, args: dict) -> None:
        if self.name not in args:
            return
        args, dataset_args = args[self.name]['args'], args[self.name]['dataset_args']

        # base model args
        self.widget.base_model_input.setText(args['pretrained_model_name_or_path'])

        # v2 args
        self.widget.v2_enable.setChecked(args.get('v2', False))
        self.widget.v_param_enable.setChecked(args.get("v_parameterization", False))
        self.widget.v_pred_enable.setChecked(args.get('scale_v_pred_loss_like_noise_pred', False))
        self.enable_disable_sd2(self.widget.v2_enable.isChecked())

        self.widget.sdxl_enable.setChecked(args.get('sdxl', False))
        if self.widget.sdxl_enable.isChecked():
            self.enable_disable_sdxl(True)
        else:
            self.enable_disable_sdxl(False)

        # resolution args
        if isinstance(dataset_args['resolution'], list):
            self.widget.height_input.setEnabled(True)
            self.widget.height_enable.setChecked(True)
            self.widget.width_input.setValue(dataset_args['resolution'][0])
            self.widget.height_input.setValue(dataset_args['resolution'][1])
        else:
            self.widget.height_input.setEnabled(False)
            self.widget.height_enable.setChecked(False)
            self.widget.width_input.setValue(dataset_args['resolution'])

        # gradient args
        if "gradient_checkpointing" in args or 'gradient_accumulation_steps' in args:
            self.widget.gradient_box.setChecked(True)
            self.widget.gradient_selector.setCurrentIndex(0 if "gradient_checkpointing" in args else 1)
            self.widget.gradient_steps_input.setValue(args.get('gradient_accumulation_steps', 1))
            self.enable_disable_gradient(True)
        else:
            self.widget.gradient_box.setChecked(False)
            self.enable_disable_gradient(False)

        self.widget.seed_input.setValue(args['seed'])
        self.widget.clip_skip_input.setValue(args['clip_skip'])
        self.widget.loss_weight_input.setValue(args['prior_loss_weight'])
        self.widget.xformers_enable.setChecked(args.get("xformers", False))
        self.widget.cache_latents_to_disk_enable.setChecked(args.get("cache_latents_to_disk", False))
        self.enable_cache_latents(args.get("cache_latents", False))
        self.widget.cache_latents_enable.setChecked(args.get("cache_latents", False))
        self.widget.batch_size_input.setValue(dataset_args['batch_size'])
        token_len = args['max_token_length']
        index = 0 if token_len == 225 else 1 if token_len == 150 else 2
        self.widget.max_token_selector.setCurrentIndex(index)
        train_prec = args['mixed_precision']
        index = 0 if train_prec == 'fp16' else 1 if train_prec == 'bf16' else 2
        self.widget.mixed_precision_selector.setCurrentIndex(index)
        index = 0 if args.get("max_train_epochs") else 1
        self.widget.max_train_selector.setCurrentIndex(index)
        self.widget.max_train_input.setValue(args['max_train_epochs'] if index == 0 else args['max_train_steps'])
        checked = True if args.get('training_comment', False) else False
        self.widget.comment_input.setText(args.get('training_comment', ""))
        self.widget.comment_enable.setChecked(checked)
        self.enable_disable_comment(checked)

    def save_args(self) -> Union[dict, None]:
        return self.args

    def save_dataset_args(self) -> Union[dict, None]:
        return self.dataset_args

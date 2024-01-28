import os.path
import subprocess
from typing import Union

from PySide6 import QtWidgets, QtCore, QtGui

import modules.DragDropLineEdit
import modules.LineEditHighlightMin
from ui_files.BaseUI import Ui_base_args_ui
from modules.CollapsibleWidget import CollapsibleWidget


class BaseArgsWidget(QtWidgets.QWidget):
    CacheLatentsChecked = QtCore.Signal(bool)
    SdxlChecked = QtCore.Signal(bool)
    keepTokensSepChecked = QtCore.Signal(bool)

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super(BaseArgsWidget, self).__init__(parent)
        realBits = subprocess.Popen(
            ["pip", "show", "bitsandbytes"], stdout=subprocess.PIPE
        )
        self.bf16_valid = (
            str(realBits.communicate()[0])
            .split(r"\n")[1]
            .split(r"\r")[0]
            .split(": ")[1]
        )
        self.bf16_valid = self.bf16_valid != "0.35.0"

        self.args = {
            "pretrained_model_name_or_path": "",
            "mixed_precision": "fp16",
            "seed": 23,
            "clip_skip": 2,
            "max_train_epochs": 1,
            "max_data_loader_n_workers": 1,
            "persistent_data_loader_workers": True,
            "max_token_length": 225,
            "prior_loss_weight": 1.0,
        }
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
        self.widget.base_model_input.setMode("file", [".ckpt", ".pt", ".safetensors"])
        self.widget.base_model_selector.setIcon(
            QtGui.QIcon(os.path.join("icons", "more-horizontal.svg"))
        )
        self.widget.vae_input.highlight = True
        self.widget.vae_input.setMode("file", [".pt", ".ckpt", ".safetensors"])
        self.widget.vae_selector.setIcon(
            QtGui.QIcon(os.path.join("icons", "more-horizontal.svg"))
        )

        self.widget.keep_tokens_seperator_input.highlight = True
        self.widget.keep_tokens_seperator_input.isValid = True
        self.widget.keep_tokens_seperator_input.min_allowed = 1

        # Base Model connections
        self.widget.base_model_input.textChanged.connect(
            lambda x: self.edit_args(
                "pretrained_model_name_or_path", x, elem=self.widget.base_model_input
            )
        )
        self.widget.base_model_selector.clicked.connect(
            lambda: self.set_from_dialog(True)
        )
        self.widget.vae_input.textChanged.connect(
            lambda x: self.edit_args("vae", x, elem=self.widget.vae_input)
        )
        self.widget.vae_selector.clicked.connect(lambda: self.set_from_dialog(False))
        self.widget.sdxl_enable.clicked.connect(self.enable_disable_sdxl)
        self.widget.v2_enable.clicked.connect(self.enable_disable_v2)
        self.widget.v_param_enable.clicked.connect(self.enable_disable_vparam)
        self.widget.v_pred_enable.clicked.connect(
            lambda x: self.edit_args("scale_v_pred_loss_like_noise_pred", x, True)
        )

        # resolution connections
        self.widget.width_input.valueChanged.connect(
            lambda x: self.change_resolution(True, x)
        )
        self.widget.height_input.valueChanged.connect(
            lambda x: self.change_resolution(False, x)
        )
        self.widget.height_enable.clicked.connect(self.enable_disable_height)

        # gradient connections
        self.widget.grad_checkpointing_enable.clicked.connect(
            lambda x: self.edit_args("gradient_checkpointing", x)
        )
        self.widget.grad_accumulation_enable.clicked.connect(
            self.enable_disable_grad_acc
        )
        self.widget.grad_accumulation_input.valueChanged.connect(
            lambda x: self.edit_args("gradient_accumulation_steps", x)
        )

        # max training time connections
        self.widget.max_train_selector.currentIndexChanged.connect(
            self.max_training_select
        )
        self.widget.max_train_input.valueChanged.connect(
            lambda x: self.max_training_select(
                self.widget.max_train_selector.currentIndex()
            )
        )

        # cache latents connections
        self.widget.cache_latents_enable.clicked.connect(self.enable_cache_latents)
        self.widget.cache_latents_to_disk_enable.clicked.connect(
            lambda x: self.enable_cache_latents(True)
        )

        # Comment in Metadata
        self.widget.comment_enable.clicked.connect(self.enable_disable_comment)
        self.widget.comment_input.textChanged.connect(
            lambda: self.edit_args(
                "training_comment", self.widget.comment_input.toPlainText(), True
            )
        )

        # generic connections
        self.widget.seed_input.valueChanged.connect(lambda x: self.edit_args("seed", x))
        self.widget.clip_skip_input.valueChanged.connect(
            lambda x: self.edit_args("clip_skip", x)
        )
        self.widget.loss_weight_input.valueChanged.connect(
            lambda x: self.edit_args("prior_loss_weight", round(x, 2))
        )
        self.widget.xformers_enable.clicked.connect(self.enable_disable_xformers)
        self.widget.sdpa_enable.clicked.connect(self.enable_disable_sdpa)
        self.widget.batch_size_input.valueChanged.connect(
            lambda x: self.edit_dataset_args("batch_size", x)
        )
        self.widget.max_token_selector.currentIndexChanged.connect(
            self.edit_token_length
        )
        self.widget.mixed_precision_selector.currentTextChanged.connect(
            lambda x: self.edit_args("mixed_precision", x if x != "float" else "no")
        )
        self.widget.no_half_vae_enable.clicked.connect(
            lambda x: self.edit_args("no_half_vae", x, True)
        )

        # full_bf16 and full_fp16 connections and setup
        self.widget.BF16_enable.setEnabled(self.bf16_valid)
        self.widget.BF16_enable.clicked.connect(self.enable_disable_full_bf16)
        self.widget.FP16_enable.clicked.connect(self.enable_disable_full_fp16)

        # max training time connections
        self.widget.max_train_selector.currentIndexChanged.connect(
            self.max_training_select
        )
        self.widget.max_train_input.valueChanged.connect(
            lambda x: self.max_training_select(
                self.widget.max_train_selector.currentIndex()
            )
        )

        # cache latents connections
        self.widget.cache_latents_enable.clicked.connect(self.enable_cache_latents)
        self.widget.cache_latents_to_disk_enable.clicked.connect(
            lambda x: self.enable_cache_latents(True)
        )

        # Comment in Metadata
        self.widget.comment_enable.clicked.connect(self.enable_disable_comment)
        self.widget.comment_input.textChanged.connect(
            lambda: self.edit_args(
                "training_comment", self.widget.comment_input.toPlainText(), True
            )
        )

        # generic connections
        self.widget.seed_input.valueChanged.connect(lambda x: self.edit_args("seed", x))
        self.widget.clip_skip_input.valueChanged.connect(
            lambda x: self.edit_args("clip_skip", x)
        )
        self.widget.loss_weight_input.valueChanged.connect(
            lambda x: self.edit_args("prior_loss_weight", round(x, 2))
        )
        self.widget.xformers_enable.clicked.connect(self.enable_disable_xformers)
        self.widget.sdpa_enable.clicked.connect(self.enable_disable_sdpa)
        self.widget.batch_size_input.valueChanged.connect(
            lambda x: self.edit_dataset_args("batch_size", x)
        )
        self.widget.max_token_selector.currentIndexChanged.connect(
            self.edit_token_length
        )
        self.widget.mixed_precision_selector.currentTextChanged.connect(
            lambda x: self.edit_args("mixed_precision", x if x != "float" else "no")
        )
        self.widget.no_half_vae_enable.clicked.connect(
            lambda x: self.edit_args("no_half_vae", x, True)
        )
        self.widget.keep_tokens_seperator_enable.clicked.connect(
            self.enable_disable_keep_tokens
        )
        self.widget.keep_tokens_seperator_input.textChanged.connect(
            lambda x: self.edit_args(
                "keep_tokens_separator",
                x,
                optional=True,
                elem=self.widget.keep_tokens_seperator_input,
            )
        )

        # full_bf16 and full_fp16 connections and setup
        self.widget.BF16_enable.setEnabled(self.bf16_valid)
        self.widget.BF16_enable.clicked.connect(self.enable_disable_full_bf16)
        self.widget.FP16_enable.clicked.connect(self.enable_disable_full_fp16)

    @QtCore.Slot(str, object, bool, QtWidgets.QWidget)
    def edit_args(
        self,
        name: str,
        value: object,
        optional: bool = False,
        elem: QtWidgets.QWidget = None,
    ) -> None:
        if elem and (
            isinstance(
                elem,
                (
                    modules.DragDropLineEdit.DragDropLineEdit,
                    modules.LineEditHighlightMin.LineEditWithHighlightMin,
                ),
            )
        ):
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
    def edit_dataset_args(
        self, name: str, value: object, optional: bool = False
    ) -> None:
        if not optional:
            self.dataset_args[name] = value
            return
        if not value:
            if name in self.dataset_args:
                del self.dataset_args[name]
            return
        self.dataset_args[name] = value

    @QtCore.Slot(bool)
    def set_from_dialog(self, is_base: bool = True) -> None:
        extensions = " ".join(
            [f"*{s}" for s in self.widget.base_model_input.extensions]
        )
        default_folder = (
            os.path.split(self.widget.base_model_input.text())[0]
            if os.path.exists(self.widget.base_model_input.text())
            else ""
        )
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Open Model File",
            dir=default_folder,
            filter=f"Stable Diffusion Models ({extensions})",
        )
        if is_base:
            self.widget.base_model_input.setText(
                file_name or self.widget.base_model_input.text()
            )
            return
        self.widget.vae_input.setText(file_name or self.widget.vae_input.text())

    @QtCore.Slot(bool)
    def enable_disable_v2(self, checked: bool) -> None:
        if checked:
            self.args["v2"] = True
            self.enable_disable_sdxl(False)
        else:
            self.enable_disable_sdxl(True)
            if "v2" in self.args:
                del self.args["v2"]

    @QtCore.Slot(bool)
    def enable_disable_vparam(self, checked: bool) -> None:
        self.widget.v_pred_enable.setEnabled(False)
        if checked:
            self.args["v_parameterization"] = True
            self.widget.v_pred_enable.setEnabled(True)
            self.edit_args(
                "scale_v_pred_loss_like_noise_pred",
                self.widget.v_pred_enable.isChecked(),
                True,
            )
        else:
            self.widget.v_pred_enable.setEnabled(False)
            for arg in ["v_parameterization", "scale_v_pred_loss_like_noise_pred"]:
                if arg in self.args:
                    del self.args[arg]

    @QtCore.Slot(bool)
    def enable_disable_sdxl(self, checked: bool) -> None:
        for arg in ["sdxl", "v2", "clip_skip"]:
            if arg in self.args:
                del self.args[arg]
        if checked:
            self.args["sdxl"] = True
            self.widget.v2_enable.setEnabled(False)
            self.widget.clip_skip_input.setEnabled(False)
            self.SdxlChecked.emit(True)
        else:
            self.widget.v2_enable.setEnabled(True)
            if self.widget.v2_enable.isChecked():
                self.args["v2"] = True
            self.widget.clip_skip_input.setEnabled(True)
            self.edit_args("clip_skip", self.widget.clip_skip_input.value())
            self.SdxlChecked.emit(False)

    @QtCore.Slot(bool)
    def enable_disable_full_fp16(self, checked: bool) -> None:
        if checked:
            self.widget.BF16_enable.setEnabled(False)
            self.edit_args("full_bf16", False, False)
            self.widget.mixed_precision_selector.setEnabled(False)
            self.edit_args("mixed_precision", "fp16", False)
            self.edit_args("full_fp16", True)
        else:
            if self.bf16_valid:
                self.widget.BF16_enable.setEnabled(True)
                self.edit_args("full_bf16", self.widget.BF16_enable.isChecked(), True)
            self.widget.mixed_precision_selector.setEnabled(True)
            text = self.widget.mixed_precision_selector.currentText()
            self.edit_args("mixed_precision", text if text != "float" else "no")
            self.edit_args("full_fp16", False, True)

    @QtCore.Slot(bool)
    def enable_disable_full_bf16(self, checked: bool) -> None:
        if not self.bf16_valid:
            return
        self.widget.FP16_enable.setEnabled(not checked)
        self.widget.mixed_precision_selector.setEnabled(not checked)
        if not checked:
            self.edit_args("full_fp16", self.widget.FP16_enable.isChecked(), True)
            text = self.widget.mixed_precision_selector.currentText()
            self.edit_args("mixed_precision", text if text != "float" else "no")
            self.edit_args("full_bf16", False, True)
        else:
            self.edit_args("full_fp16", False, True)
            self.edit_args("mixed_precision", "bf16", True)
            self.edit_args("full_bf16", True)

    @QtCore.Slot(bool)
    def enable_disable_height(self, checked: bool) -> None:
        if checked:
            self.widget.height_input.setEnabled(True)
            self.dataset_args["resolution"] = [
                self.widget.width_input.value(),
                self.widget.height_input.value(),
            ]
        else:
            self.widget.height_input.setEnabled(False)
            self.dataset_args["resolution"] = self.widget.width_input.value()

    @QtCore.Slot(bool, int)
    def change_resolution(self, width: bool, value: int) -> None:
        if width:
            self.dataset_args["resolution"] = (
                [value, self.widget.height_input.value()]
                if self.widget.height_input.isEnabled()
                else value
            )
        else:
            self.dataset_args["resolution"] = [self.widget.width_input.value(), value]

    @QtCore.Slot(bool)
    def enable_disable_comment(self, checked: bool) -> None:
        self.widget.comment_input.setEnabled(checked)
        self.edit_args(
            "training_comment",
            self.widget.comment_input.toPlainText() if checked else None,
            True,
        )

    @QtCore.Slot(int)
    def max_training_select(self, index: int) -> None:
        for name in ["max_train_epochs", "max_train_steps"]:
            if name in self.args:
                del self.args[name]
        self.args[
            f'max_train_{"epochs" if index == 0 else "steps"}'
        ] = self.widget.max_train_input.value()

    @QtCore.Slot(bool)
    def enable_cache_latents(self, checked: bool) -> None:
        for name in ["cache_latents", "cache_latents_to_disk"]:
            if name in self.args:
                del self.args[name]
        self.CacheLatentsChecked.emit(checked)
        if checked:
            self.args["cache_latents"] = True
            self.widget.cache_latents_to_disk_enable.setEnabled(True)
            if self.widget.cache_latents_to_disk_enable.isChecked():
                self.args["cache_latents_to_disk"] = True
        else:
            self.widget.cache_latents_to_disk_enable.setEnabled(False)

    @QtCore.Slot(bool)
    def enable_disable_xformers(self, checked: bool) -> None:
        if "xformers" in self.args:
            del self.args["xformers"]
        if "sdpa" in self.args:
            del self.args["sdpa"]
        if checked:
            self.args["xformers"] = True
            self.widget.sdpa_enable.setEnabled(False)
        else:
            self.widget.sdpa_enable.setEnabled(True)
            if self.widget.sdpa_enable.isChecked():
                self.args["sdpa"] = True

    @QtCore.Slot(bool)
    def enable_disable_sdpa(self, checked: bool) -> None:
        if "xformers" in self.args:
            del self.args["xformers"]
        if "sdpa" in self.args:
            del self.args["sdpa"]
        if checked:
            self.args["sdpa"] = True
            self.widget.xformers_enable.setEnabled(False)
        else:
            self.widget.xformers_enable.setEnabled(True)
            if self.widget.xformers_enable.isChecked():
                self.args["xformers"] = True

    @QtCore.Slot(bool)
    def enable_disable_grad_acc(self, checked: bool) -> None:
        self.widget.grad_accumulation_input.setEnabled(checked)
        self.edit_args(
            "gradient_accumulation_steps",
            self.widget.grad_accumulation_input.value() if checked else None,
            optional=True,
        )

    @QtCore.Slot(bool)
    def enable_disable_keep_tokens(self, checked: bool) -> None:
        if "keep_tokens_separator" in self.args:
            del self.args["keep_tokens_separator"]
        self.widget.keep_tokens_seperator_input.setEnabled(checked)
        modified = self.widget.keep_tokens_seperator_input.isModified()
        if checked:
            self.edit_args(
                "keep_tokens_separator",
                self.widget.keep_tokens_seperator_input.text(),
                optional=True,
                elem=self.widget.keep_tokens_seperator_input if modified else None,
            )
        else:
            self.widget.keep_tokens_seperator_input.setStyleSheet("")
        self.keepTokensSepChecked.emit(checked)

    @QtCore.Slot(int)
    def edit_token_length(self, index: int) -> None:
        if "max_token_length" in self.dataset_args:
            del self.args["max_token_length"]
        if index != 2:
            self.args["max_token_length"] = int(
                self.widget.max_token_selector.currentText()
            )

    def get_args(self, input_args: dict) -> None:
        valid = self.widget.base_model_input.update_stylesheet()
        input_args["general_args"] = self.args if valid else None
        if not valid and self.colap.is_collapsed:
            self.colap.toggle_collapsed()
            self.colap.title_frame.update_arrow(False)
            self.colap.title_frame.setChecked(True)

    def get_dataset_args(self, input_args: dict) -> None:
        valid = self.widget.base_model_input.update_stylesheet()
        input_args["general_args"] = self.dataset_args if valid else None

    def load_args(self, args: dict) -> None:
        if self.name not in args:
            return
        args, dataset_args = args[self.name]["args"], args[self.name]["dataset_args"]

        # base model args
        self.widget.base_model_input.setText(args["pretrained_model_name_or_path"])

        # v2 args
        self.widget.v2_enable.setChecked(args.get("v2", False))
        self.widget.v_param_enable.setChecked(args.get("v_parameterization", False))
        self.widget.v_pred_enable.setChecked(
            args.get("scale_v_pred_loss_like_noise_pred", False)
        )
        self.enable_disable_v2(self.widget.v2_enable.isChecked())
        self.enable_disable_vparam(self.widget.v_param_enable.isChecked())

        # SDXL args
        self.widget.sdxl_enable.setChecked(args.get("sdxl", False))
        self.enable_disable_sdxl(self.widget.sdxl_enable.isChecked())

        # resolution args
        if isinstance(dataset_args["resolution"], list):
            self.widget.height_input.setEnabled(True)
            self.widget.height_enable.setChecked(True)
            self.widget.width_input.setValue(dataset_args["resolution"][0])
            self.widget.height_input.setValue(dataset_args["resolution"][1])
        else:
            self.widget.height_input.setEnabled(False)
            self.widget.height_enable.setChecked(False)
            self.widget.width_input.setValue(dataset_args["resolution"])

        self.widget.seed_input.setValue(args["seed"])
        self.widget.clip_skip_input.setValue(args.get("clip_skip", 2))
        self.widget.loss_weight_input.setValue(args["prior_loss_weight"])
        self.widget.xformers_enable.setChecked(args.get("xformers", False))
        self.enable_disable_xformers(args.get("xformers", False))
        self.widget.sdpa_enable.setChecked(args.get("sdpa", False))
        self.enable_disable_sdpa(args.get("sdpa", False))
        self.widget.cache_latents_to_disk_enable.setChecked(
            args.get("cache_latents_to_disk", False)
        )
        self.enable_cache_latents(args.get("cache_latents", False))
        self.widget.cache_latents_enable.setChecked(args.get("cache_latents", False))
        self.widget.batch_size_input.setValue(dataset_args["batch_size"])
        token_len = args["max_token_length"]
        index = 0 if token_len == 225 else 1 if token_len == 150 else 2
        self.widget.max_token_selector.setCurrentIndex(index)
        train_prec = args.get("mixed_precision", "fp16")
        index = 0 if train_prec == "fp16" else 1 if train_prec == "bf16" else 2
        self.widget.mixed_precision_selector.setCurrentIndex(index)
        index = 0 if args.get("max_train_epochs") else 1
        self.widget.max_train_selector.setCurrentIndex(index)
        self.widget.max_train_input.setValue(
            args["max_train_epochs"] if index == 0 else args["max_train_steps"]
        )
        checked = True if args.get("training_comment", False) else False
        self.widget.comment_input.setText(args.get("training_comment", ""))
        self.widget.comment_enable.setChecked(checked)
        self.enable_disable_comment(checked)
        self.widget.no_half_vae_enable.setChecked(args.get("no_half_vae", False))
        self.edit_args("no_half_vae", args.get("no_half_vae", False), True)
        if self.bf16_valid:
            self.widget.BF16_enable.setChecked(args.get("full_bf16", False))
            if self.widget.BF16_enable.isChecked():
                self.enable_disable_full_bf16(True)
        self.widget.FP16_enable.setChecked(args.get("full_fp16", False))
        if self.widget.FP16_enable.isChecked() and self.widget.FP16_enable.isEnabled():
            self.enable_disable_full_fp16(True)
        self.widget.vae_input.setText(args.get("vae", ""))
        self.widget.keep_tokens_seperator_enable.setChecked(
            bool(args.get("keep_tokens_separator", False))
        )
        self.widget.keep_tokens_seperator_input.setText(
            args.get("keep_tokens_separator", "")
        )
        self.enable_disable_keep_tokens(
            self.widget.keep_tokens_seperator_enable.isChecked()
        )
        self.widget.grad_checkpointing_enable.setChecked(
            args.get("gradient_checkpointing", False)
        )
        self.edit_args(
            "gradient_checkpointing",
            args.get("gradient_checkpointing", False),
            optional=True,
        )
        self.widget.grad_accumulation_input.setValue(
            args.get("gradient_accumulation_steps", 1)
        )
        self.widget.grad_accumulation_enable.setChecked(
            bool(args.get("gradient_accumulation_steps", False))
        )
        self.enable_disable_grad_acc(
            bool(args.get("gradient_accumulation_steps", False))
        )

    def save_args(self) -> Union[dict, None]:
        return self.args

    def save_dataset_args(self) -> Union[dict, None]:
        return self.dataset_args

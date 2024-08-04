from pathlib import Path
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QPushButton
from ui_files.BaseUI import Ui_base_args_ui
from modules.BaseWidget import BaseWidget
from modules.DragDropLineEdit import DragDropLineEdit


class GeneralWidget(BaseWidget):
    sdxlChecked = Signal(bool)
    cacheLatentsChecked = Signal(bool)
    keepTokensSepChecked = Signal(bool)

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.colap.set_title("General Args")
        self.widget = Ui_base_args_ui()

        self.name = "general_args"
        self.args = {
            "mixed_precision": "fp16",
            "seed": 23,
            "clip_skip": 2,
            "max_train_epochs": 1,
            "max_data_loader_n_workers": 1,
            "persistent_data_loader_workers": True,
            "max_token_length": 225,
            "prior_loss_weight": 1.0,
        }
        self.dataset_args = {
            "resolution": 512,
            "batch_size": 1,
        }

        self.setup_widget()
        self.setup_connections()

    def setup_widget(self) -> None:
        super().setup_widget()
        self.widget.setupUi(self.content)

        def setup_file(elem: DragDropLineEdit, selector: QPushButton):
            selector_icon = QIcon(str(Path("icons/more-horizontal.svg")))
            elem.setMode("file", [".ckpt", ".pt", ".safetensors"])
            elem.highlight = True
            selector.setIcon(selector_icon)

        setup_file(self.widget.base_model_input, self.widget.base_model_selector)
        setup_file(self.widget.vae_input, self.widget.vae_selector)
        self.widget.vae_input.allow_empty = True

    def setup_connections(self) -> None:
        self.widget.base_model_input.textChanged.connect(
            lambda x: self.edit_args(
                "pretrained_model_name_or_path",
                x,
            )
        )
        self.widget.base_model_selector.clicked.connect(
            lambda: self.set_file_from_dialog(
                self.widget.base_model_input, "Base Model For Training", "SD Model"
            )
        )
        self.widget.vae_input.textChanged.connect(
            lambda x: self.edit_args("vae", x, optional=True)
        )
        self.widget.vae_selector.clicked.connect(
            lambda: self.set_file_from_dialog(
                self.widget.vae_input, "External VAE", "VAE file"
            )
        )
        self.widget.v2_enable.clicked.connect(
            lambda x: self.change_model_type(x, False)
        )
        self.widget.sdxl_enable.clicked.connect(
            lambda x: self.change_model_type(False, x)
        )
        self.widget.no_half_vae_enable.clicked.connect(
            lambda x: self.edit_args("no_half_vae", x, True)
        )
        self.widget.low_ram_enable.clicked.connect(
            lambda x: self.edit_args("lowram", x, True)
        )
        self.widget.v_param_enable.clicked.connect(self.enable_disable_v_param)
        self.widget.v_pred_enable.clicked.connect(
            lambda x: self.edit_args("scale_v_pred_loss_like_noise_pred", x, True)
        )
        self.widget.FP16_enable.clicked.connect(
            lambda x: self.change_full_type(x, False)
        )
        self.widget.BF16_enable.clicked.connect(
            lambda x: self.change_full_type(False, x)
        )
        self.widget.FP8_enable.clicked.connect(
            lambda x: self.edit_args("fp8_base", x, True)
        )
        self.widget.width_input.valueChanged.connect(self.change_resolution)
        self.widget.height_enable.clicked.connect(self.change_resolution)
        self.widget.height_input.valueChanged.connect(self.change_resolution)
        self.widget.grad_checkpointing_enable.clicked.connect(
            lambda x: self.edit_args("gradient_checkpointing", x, True)
        )
        self.widget.grad_accumulation_enable.clicked.connect(
            self.enable_disable_grad_acc
        )
        self.widget.grad_accumulation_input.valueChanged.connect(
            lambda x: self.edit_args("gradient_accumulation_steps", x, True)
        )
        self.widget.seed_input.valueChanged.connect(lambda x: self.edit_args("seed", x))
        self.widget.batch_size_input.valueChanged.connect(
            lambda x: self.edit_dataset_args("batch_size", x)
        )
        self.widget.clip_skip_input.valueChanged.connect(
            lambda x: self.edit_args("clip_skip", x)
        )
        self.widget.max_token_selector.currentIndexChanged.connect(
            lambda x: self.edit_args("max_token_length", [225, 150, None][x], True)
        )
        self.widget.loss_weight_input.valueChanged.connect(
            lambda x: self.edit_args("prior_loss_weight", x, True)
        )
        self.widget.mixed_precision_selector.currentTextChanged.connect(
            lambda x: self.edit_args("mixed_precision", x if x != "float" else "no")
        )
        self.widget.xformers_enable.clicked.connect(
            lambda x: self.change_optim_type(x, False)
        )
        self.widget.sdpa_enable.clicked.connect(
            lambda x: self.change_optim_type(False, x)
        )
        self.widget.max_train_selector.currentIndexChanged.connect(self.change_max_mode)
        self.widget.max_train_input.valueChanged.connect(
            lambda: self.change_max_mode(self.widget.max_train_selector.currentIndex())
        )
        self.widget.cache_latents_enable.clicked.connect(
            self.enable_disable_cache_latents
        )
        self.widget.cache_latents_to_disk_enable.clicked.connect(
            lambda x: self.edit_args("cache_latents_to_disk", x, True)
        )
        self.widget.keep_tokens_seperator_enable.clicked.connect(
            self.enable_disable_keep_tokens_sep
        )
        self.widget.keep_tokens_seperator_input.textChanged.connect(
            lambda x: self.edit_args(
                "keep_tokens_separator",
                x,
                optional=True,
            )
        )
        self.widget.comment_enable.clicked.connect(self.enable_disable_comment)
        self.widget.comment_input.textChanged.connect(
            lambda: self.edit_args(
                "training_comment", self.widget.comment_input.toPlainText(), True
            )
        )

    def check_validity(self, elem: DragDropLineEdit) -> None:
        elem.dirty = True
        if not elem.allow_empty or elem.text() != "":
            elem.update_stylesheet()
        else:
            elem.setStyleSheet("")

    def change_model_type(self, is_v2: bool, is_sdxl: bool) -> None:
        for arg in ["v2", "sdxl", "clip_skip"]:
            if arg in self.args:
                del self.args[arg]
        self.widget.v2_enable.setEnabled(not is_sdxl)
        self.widget.clip_skip_input.setEnabled(not is_sdxl)
        self.widget.sdxl_enable.setEnabled(not is_v2)

        self.edit_args("v2", is_v2, True)
        self.edit_args("sdxl", is_sdxl, True)
        self.edit_args(
            "clip_skip", None if is_sdxl else self.widget.clip_skip_input.value(), True
        )
        self.sdxlChecked.emit(is_sdxl)

    def change_full_type(self, is_fp: bool, is_bf: bool) -> None:
        for arg in ["full_fp16", "full_bf16", "mixed_precision"]:
            if arg in self.args:
                del self.args[arg]
        self.widget.FP16_enable.setEnabled(not is_bf)
        self.widget.BF16_enable.setEnabled(not is_fp)
        self.widget.mixed_precision_selector.setEnabled(not is_bf and not is_fp)

        self.edit_args("full_fp16", is_fp, True)
        self.edit_args("full_bf16", is_bf, True)
        text = self.widget.mixed_precision_selector.currentText()
        self.edit_args(
            "mixed_precision",
            "fp16" if is_fp else "bf16" if is_bf else text if text != "float" else "no",
        )

    def change_resolution(self) -> None:
        if "resolution" in self.dataset_args:
            del self.dataset_args["resolution"]
        if not self.widget.height_enable.isChecked():
            self.widget.height_input.setEnabled(False)
            self.edit_dataset_args("resolution", self.widget.width_input.value())
            return
        self.widget.height_input.setEnabled(True)
        self.edit_dataset_args(
            "resolution",
            [self.widget.width_input.value(), self.widget.height_input.value()],
        )

    def change_optim_type(self, is_xformers: bool, is_sdpa: bool) -> None:
        for arg in ["xformers", "sdpa"]:
            if arg in self.args:
                del self.args[arg]
        self.widget.xformers_enable.setEnabled(not is_sdpa)
        self.widget.sdpa_enable.setEnabled(not is_xformers)
        self.edit_args("xformers", is_xformers, True)
        self.edit_args("sdpa", is_sdpa, True)

    def change_max_mode(self, index: int) -> None:
        args = ["max_train_epochs", "max_train_steps"]
        for arg in args:
            if arg in self.args:
                del self.args[arg]
        self.edit_args(args[index], self.widget.max_train_input.value())

    def enable_disable_v_param(self, checked: bool) -> None:
        for arg in ["v_parameterization", "scale_v_pred_loss_like_noise_pred"]:
            if arg in self.args:
                del self.args[arg]
        self.widget.v_pred_enable.setEnabled(checked)
        if not checked:
            return
        self.edit_args("v_parameterization", checked, True)
        self.edit_args(
            "scale_v_pred_loss_like_noise_pred",
            self.widget.v_pred_enable.isChecked(),
            True,
        )

    def enable_disable_grad_acc(self, checked: bool) -> None:
        if "gradient_accumulation_steps" in self.args:
            del self.args["gradient_accumulation_steps"]
        self.widget.grad_accumulation_input.setEnabled(checked)
        if not checked:
            return
        self.edit_args(
            "gradient_accumulation_steps",
            self.widget.grad_accumulation_input.value(),
            True,
        )

    def enable_disable_cache_latents(self, checked: bool) -> None:
        args = ["cache_latents", "cache_latents_to_disk"]
        for arg in args:
            if arg in self.args:
                del self.args[arg]
        self.widget.cache_latents_to_disk_enable.setEnabled(checked)
        self.edit_args(args[0], checked, True)
        self.edit_args(
            args[1],
            self.widget.cache_latents_to_disk_enable.isChecked() and checked,
            True,
        )
        self.cacheLatentsChecked.emit(checked)

    def enable_disable_keep_tokens_sep(self, checked: bool) -> None:
        if "keep_tokens_separator" in self.args:
            del self.args["keep_tokens_separator"]
        self.widget.keep_tokens_seperator_input.setEnabled(checked)
        self.keepTokensSepChecked.emit(checked)
        self.edit_args(
            "keep_tokens_separator",
            self.widget.keep_tokens_seperator_input.text(),
            optional=True,
        )

    def enable_disable_comment(self, checked: bool) -> None:
        if "training_comment" in self.args:
            del self.args["training_comment"]
        self.widget.comment_input.setEnabled(checked)
        if not checked:
            return
        self.edit_args(
            "training_comment", self.widget.comment_input.toPlainText(), True
        )

    def load_args(self, args: dict) -> bool:
        args = args.get(self.name, {})

        # update element inputs
        self.widget.base_model_input.setText(
            args.get("pretrained_model_name_or_path", "")
        )
        self.widget.vae_input.setText(args.get("vae", ""))
        self.widget.v2_enable.setChecked(args.get("v2", False))
        self.widget.sdxl_enable.setChecked(args.get("sdxl", False))
        self.widget.no_half_vae_enable.setChecked(args.get("no_half_vae", False))
        self.widget.low_ram_enable.setChecked(args.get("lowram", False))
        self.widget.v_param_enable.setChecked(args.get("v_parameterization", False))
        self.widget.v_pred_enable.setChecked(
            args.get("scale_v_pred_loss_like_noise_pred", False)
        )
        self.widget.FP16_enable.setChecked(args.get("full_fp16", False))
        self.widget.BF16_enable.setChecked(args.get("full_bf16", False))
        self.widget.FP8_enable.setChecked(args.get("fp8_base", False))
        self.widget.grad_checkpointing_enable.setChecked(
            args.get("gradient_checkpointing", False)
        )
        self.widget.grad_accumulation_enable.setChecked(
            bool(args.get("gradient_accumulation_steps", False))
        )
        self.widget.grad_accumulation_input.setValue(
            args.get("gradient_accumulation_steps", 1)
        )
        self.widget.seed_input.setValue(args.get("seed", 23))
        self.widget.clip_skip_input.setValue(args.get("clip_skip", 2))
        self.widget.max_token_selector.setCurrentText(
            str(args.get("max_token_length", 225))
        )
        self.widget.loss_weight_input.setValue(args.get("prior_loss_weight", 1.0))
        mixed_prec = args.get("mixed_precision", "fp16")
        self.widget.mixed_precision_selector.setCurrentText(
            mixed_prec if mixed_prec != "no" else "float"
        )
        self.widget.xformers_enable.setChecked(args.get("xformers", False))
        self.widget.sdpa_enable.setChecked(args.get("sdpa", False))
        self.widget.max_train_selector.setCurrentIndex(
            0 if args.get("max_train_epochs", None) else 1
        )
        self.widget.max_train_input.setValue(
            args.get("max_train_epochs", args.get("max_train_steps", 1))
        )
        self.widget.cache_latents_enable.setChecked(args.get("cache_latents", False))
        self.widget.cache_latents_to_disk_enable.setChecked(
            args.get("cache_latents_to_disk", False)
        )
        self.widget.keep_tokens_seperator_enable.setChecked(
            bool(args.get("keep_tokens_separator", False))
        )
        self.widget.keep_tokens_seperator_input.setText(
            args.get("keep_tokens_separator", "")
        )
        self.widget.comment_enable.setChecked(bool(args.get("training_comment", False)))
        self.widget.comment_input.setText(args.get("training_comment", ""))

        # update args to match
        self.edit_args(
            "pretrained_model_name_or_path",
            self.widget.base_model_input.text(),
        )
        self.edit_args(
            "vae",
            self.widget.vae_input.text(),
            optional=True,
        )
        self.change_model_type(
            self.widget.v2_enable.isChecked(), self.widget.sdxl_enable.isChecked()
        )
        self.edit_args("no_half_vae", self.widget.no_half_vae_enable.isChecked(), True)
        self.edit_args("lowram", self.widget.low_ram_enable.isChecked(), True)
        self.enable_disable_v_param(self.widget.v_param_enable.isChecked())
        self.change_full_type(
            self.widget.FP16_enable.isChecked(), self.widget.BF16_enable.isChecked()
        )
        self.edit_args("fp8_base", self.widget.FP8_enable.isChecked(), True)
        self.edit_args(
            "gradient_checkpointing",
            self.widget.grad_checkpointing_enable.isChecked(),
            True,
        )
        self.enable_disable_grad_acc(self.widget.grad_accumulation_enable.isChecked())
        self.edit_args("seed", self.widget.seed_input.value())
        self.edit_args(
            "max_token_length",
            [225, 150, None][self.widget.max_token_selector.currentIndex()],
            True,
        )
        self.edit_args("prior_loss_weight", self.widget.loss_weight_input.value())
        self.change_optim_type(
            self.widget.xformers_enable.isChecked(), self.widget.sdpa_enable.isChecked()
        )
        self.change_max_mode(self.widget.max_train_selector.currentIndex())
        self.enable_disable_cache_latents(self.widget.cache_latents_enable.isChecked())
        self.enable_disable_keep_tokens_sep(
            self.widget.keep_tokens_seperator_enable.isChecked()
        )
        self.enable_disable_comment(self.widget.comment_enable.isChecked())
        return True

    def load_dataset_args(self, dataset_args: dict) -> bool:
        dataset_args = dataset_args.get(self.name, {})

        # update element inputs
        resolution = dataset_args.get("resolution", 512)
        self.widget.width_input.setValue(
            resolution[0] if isinstance(resolution, list) else resolution
        )
        self.widget.height_enable.setChecked(isinstance(resolution, list))
        self.widget.height_input.setValue(
            resolution[1] if isinstance(resolution, list) else resolution
        )
        self.widget.batch_size_input.setValue(dataset_args.get("batch_size", 1))

        # edit dataset_args to match
        self.change_resolution()
        self.edit_dataset_args("batch_size", self.widget.batch_size_input.value())
        return True

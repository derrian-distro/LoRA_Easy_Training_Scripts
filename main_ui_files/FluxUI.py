from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QPushButton
from modules.DragDropLineEdit import DragDropLineEdit
from ui_files.FluxUI import Ui_flux_ui
from modules.BaseWidget import BaseWidget
from pathlib import Path


class FluxWidget(BaseWidget):
    Toggled = Signal(bool)  # send to general args
    SplitMode = Signal(bool)  # send to network args
    SplitQKV = Signal(bool)  # send to network args

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.colap.set_title("Flux Args")
        self.widget = Ui_flux_ui()

        self.name = "flux_args"

        self.setup_widget()
        self.setup_connections()

    def setup_widget(self) -> None:
        super().setup_widget()
        self.widget.setupUi(self.content)

        def setup_file(elem: DragDropLineEdit, selector: QPushButton):
            selector_icon = QIcon(str(Path("icons/more-horizontal.svg")))
            elem.setMode("file", [".ckpt", ".pt", ".safetensors", ".sft"])
            elem.highlight = True
            selector.setIcon(selector_icon)

        setup_file(self.widget.ae_model_input, self.widget.ae_model_selector)
        setup_file(self.widget.clip_l_model_input, self.widget.clip_l_model_selector)
        setup_file(self.widget.t5_model_input, self.widget.t5_model_selector)

    def setup_connections(self) -> None:
        self.widget.flux_training_box.clicked.connect(self.enable_disable)
        self.widget.ae_model_input.textChanged.connect(lambda x: self.edit_args("ae", x))
        self.widget.ae_model_selector.clicked.connect(
            lambda: self.set_file_from_dialog(self.widget.ae_model_input, "Ae Model For Training", "Ae Model")
        )
        self.widget.clip_l_model_input.textChanged.connect(lambda x: self.edit_args("clip_l", x))
        self.widget.clip_l_model_selector.clicked.connect(
            lambda: self.set_file_from_dialog(
                self.widget.clip_l_model_input, "Clip L Model For Training", "Clip Model"
            )
        )
        self.widget.t5_model_input.textChanged.connect(lambda x: self.edit_args("t5xxl", x))
        self.widget.t5_model_selector.clicked.connect(
            lambda: self.set_file_from_dialog(
                self.widget.t5_model_input, "T5XXL Model For Training", "T5 Model"
            )
        )
        self.widget.t5_max_token_input.valueChanged.connect(
            lambda x: self.edit_args("t5xxl_max_token_length", x)
        )
        self.widget.discrete_flow_shift_input.valueChanged.connect(
            lambda x: self.edit_args("discrete_flow_shift", x)
        )
        self.widget.apply_t5_attention_mask_enable.clicked.connect(
            lambda x: self.edit_args("apply_t5_attn_mask", x, True)
        )
        self.widget.split_mode_enable.clicked.connect(self.split_mode_toggle)
        self.widget.timestep_sampling_selector.currentIndexChanged.connect(self.change_timestep_sampling_type)
        self.widget.weighting_scheme_selector.currentIndexChanged.connect(self.change_weighting_scheme_type)
        self.widget.logit_mean_input.valueChanged.connect(lambda x: self.edit_args("logit_mean", x))
        self.widget.logit_std_input.valueChanged.connect(lambda x: self.edit_args("logit_std", x))
        self.widget.mode_scale_input.valueChanged.connect(lambda x: self.edit_args("mode_scale", x))
        self.widget.sigmoid_scale_input.valueChanged.connect(lambda x: self.edit_args("sigmoid_scale", x))
        self.widget.guidance_scale_input.valueChanged.connect(lambda x: self.edit_args("guidance_scale", x))
        self.widget.model_prediction_type_selector.currentTextChanged.connect(
            lambda x: self.edit_args("model_prediction_type", x.replace(" ", "_").lower())
        )
        self.widget.split_qkv_enable.clicked.connect(lambda x: self.SplitQKV.emit(x))

    def enable_disable(self, checked: bool) -> None:
        self.args = {}
        self.Toggled.emit(checked)
        if not checked:
            return
        self.edit_args("ae", self.widget.ae_model_input.text())
        self.edit_args("clip_l", self.widget.clip_l_model_input.text())
        self.edit_args("t5xxl", self.widget.t5_model_input.text())
        self.edit_args("apply_t5_attn_mask", self.widget.apply_t5_attention_mask_enable.isChecked(), True)
        self.edit_args("t5xxl_max_token_length", self.widget.t5_max_token_input.value())
        self.edit_args("discrete_flow_shift", self.widget.discrete_flow_shift_input.value())
        self.edit_args("split_mode", self.widget.split_mode_enable.isChecked(), True)
        self.change_timestep_sampling_type(self.widget.timestep_sampling_selector.currentIndex())
        self.change_weighting_scheme_type(self.widget.weighting_scheme_selector.currentIndex())
        self.edit_args("guidance_scale", self.widget.guidance_scale_input.value())
        self.edit_args(
            "model_prediction_type",
            self.widget.model_prediction_type_selector.currentText().replace(" ", "_").lower(),
        )
        self.SplitMode.emit(self.widget.split_mode_enable.isChecked())
        self.SplitQKV.emit(self.widget.split_qkv_enable.isChecked())

    def external_enable_disable(self, checked: bool) -> None:
        self.args = {}
        self.widget.flux_training_box.setEnabled(not checked)
        if self.widget.flux_training_box.isEnabled() and self.widget.flux_training_box.isChecked():
            self.enable_disable(True)

    def split_mode_toggle(self, checked: bool) -> None:
        self.SplitMode.emit(checked)
        self.edit_args("split_mode", checked, True)

    def change_timestep_sampling_type(self, index: int) -> None:
        self.widget.sigmoid_scale_input.setEnabled(index == 0)
        self.widget.discrete_flow_shift_input.setEnabled(index == 3)
        for arg in ["sigmoid_scale", "discrete_flow_shift"]:
            if arg in self.args:
                del self.args[arg]
        self.edit_args("timestep_sampling", self.widget.timestep_sampling_selector.currentText().lower())
        self.edit_args(
            "sigmoid_scale",
            self.widget.sigmoid_scale_input.value() if self.widget.sigmoid_scale_input.isEnabled() else False,
            True,
        )
        self.edit_args(
            "discrete_flow_shift",
            (
                self.widget.discrete_flow_shift_input.value()
                if self.widget.discrete_flow_shift_input.isEnabled()
                else False
            ),
        )

    def change_weighting_scheme_type(self, index: int) -> None:
        self.widget.logit_mean_input.setEnabled(index == 2)
        self.widget.logit_std_input.setEnabled(index == 2)
        self.widget.mode_scale_input.setEnabled(index == 3)
        for arg in {"logit_mean", "logit_std", "mode_scale"}:
            if arg in self.args:
                del self.args[arg]
        self.edit_args(
            "weighting_scheme", self.widget.weighting_scheme_selector.currentText().replace(" ", "_").lower()
        )
        self.edit_args(
            "logit_mean",
            self.widget.logit_mean_input.value() if self.widget.logit_mean_input.isEnabled() else False,
            True,
        )
        self.edit_args(
            "logit_std",
            self.widget.logit_std_input.value() if self.widget.logit_std_input.isEnabled() else False,
            True,
        )
        self.edit_args(
            "mode_scale",
            self.widget.mode_scale_input.value() if self.widget.mode_scale_input.isEnabled() else False,
            True,
        )

    def load_args(self, args: dict) -> bool:
        net_args = args.get("network_args", {}).get("network_args", {})
        args: dict = args.get(self.name, {})

        self.widget.flux_training_box.setChecked(bool(args))
        self.widget.ae_model_input.setText(args.get("ae", ""))
        self.widget.clip_l_model_input.setText(args.get("clip_l", ""))
        self.widget.t5_model_input.setText(args.get("t5xxl", ""))
        self.widget.apply_t5_attention_mask_enable.setChecked(args.get("apply_t5_attn_mask", False))
        self.widget.t5_max_token_input.setValue(args.get("t5xxl_max_token_length", 512))
        self.widget.discrete_flow_shift_input.setValue(args.get("discrete_flow_shift", 1.15))
        self.widget.split_mode_enable.setChecked(args.get("split_mode", False))
        self.widget.timestep_sampling_selector.setCurrentText(
            args.get("timestep_sampling", "Sigma").capitalize()
        )
        option = " ".join([x.capitalize() for x in args.get("weighting_scheme", "None").split("_")])
        self.widget.weighting_scheme_selector.setCurrentText(option)
        self.widget.logit_mean_input.setValue(args.get("logit_mean", 0.0))
        self.widget.logit_std_input.setValue(args.get("logit_std", 1.0))
        self.widget.mode_scale_input.setValue(args.get("mode_scale", 1.29))
        self.widget.sigmoid_scale_input.setValue(args.get("sigmoid_scale", 1.0))
        self.widget.guidance_scale_input.setValue(args.get("guidance_scale", 3.5))
        option = " ".join(
            [x.capitalize() for x in args.get("model_prediction_type", "sigma_scaled").split("_")]
        )
        self.widget.model_prediction_type_selector.setCurrentText(option)
        self.widget.split_qkv_enable.setChecked(net_args.get("split_qkv", False))

        self.enable_disable(self.widget.flux_training_box.isChecked())

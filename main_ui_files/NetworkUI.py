from typing import Union
from PySide6 import QtWidgets, QtCore
from ui_files.NetworkUI import Ui_network_ui
from modules.CollapsibleWidget import CollapsibleWidget
from modules.BlockWeightWidgets import BlockWidget, BlockWeightWidget


class NetworkWidget(QtWidgets.QWidget):
    args_edited = QtCore.Signal(str, object)

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super(NetworkWidget, self).__init__(parent)
        self.args = {"network_dim": 32, "network_alpha": 16.0}
        self.network_args = {}
        self.name = "network_args"

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(9, 0, 9, 0)
        self.colap = CollapsibleWidget(self, "Network Args")

        self.content = QtWidgets.QWidget()
        self.colap.add_widget(self.content, "main_widget")

        self.widget = Ui_network_ui()
        self.widget.setupUi(self.content)
        self.layout().addWidget(self.colap)

        self.block_widgets_state = [
            [self.widget.block_weight_widget, False],
            [self.widget.dim_block_widget, False],
            [self.widget.alpha_block_widget, False],
            [self.widget.conv_block_widget, False],
            [self.widget.conv_alpha_block_widget, False],
        ]
        self.block_widgets = [
            BlockWeightWidget(),
            BlockWidget(mode="int", base_value=32),
            BlockWidget(mode="float", base_value=16.0),
            BlockWidget(mode="int", base_value=32),
            BlockWidget(mode="float", base_value=16.0),
        ]

        for i, elem in enumerate(self.block_widgets_state):
            elem[0].set_extra("enable")
            elem[0].title_frame.setEnabled(False)
            elem[0].add_widget(self.block_widgets[i], "main_widget")
        self.widget.block_weight_widget.title_frame.setText("Block Weights")
        self.widget.dim_block_widget.title_frame.setText("Block Dims")
        self.widget.alpha_block_widget.title_frame.setText("Block Alphas")
        self.widget.conv_block_widget.title_frame.setText("Block Conv Dims")
        self.widget.conv_alpha_block_widget.title_frame.setText("Block Conv Alphas")

        self.widget.block_weight_scroll_widget.layout().setAlignment(
            QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.widget.block_weight_scroll_widget.layout().setSpacing(0)

        self.widget.algo_select.currentTextChanged.connect(self.change_algo)
        self.widget.lycoris_preset_input.textChanged.connect(
            lambda x: self.edit_args("preset", x, optional=True, network_args=True)
        )

        self.widget.network_dim_input.valueChanged.connect(
            lambda x: self.edit_args("network_dim", x)
        )
        self.widget.network_alpha_input.valueChanged.connect(
            lambda x: self.edit_args("network_alpha", x)
        )
        self.widget.conv_dim_input.valueChanged.connect(
            lambda x: self.edit_args("conv_dim", x, optional=True, network_args=True)
        )
        self.widget.conv_alpha_input.valueChanged.connect(
            lambda x: self.edit_args("conv_alpha", x, optional=True, network_args=True)
        )
        self.widget.min_timestep_input.editingFinished.connect(
            lambda: self.edit_timesteps("min_timestep")
        )
        self.widget.max_timestep_input.editingFinished.connect(
            lambda: self.edit_timesteps("max_timestep")
        )

        self.widget.unet_te_both_select.currentTextChanged.connect(
            self.change_training_parts
        )
        self.widget.cache_te_outputs_enable.clicked.connect(self.toggle_cache_te)
        self.widget.cache_te_to_disk_enable.clicked.connect(
            lambda x: self.edit_args(
                "cache_text_encoder_outputs_to_disk", x, optional=True
            )
        )
        self.widget.dylora_unit_input.valueChanged.connect(
            lambda x: self.edit_args("unit", x, optional=True, network_args=True)
        )
        self.widget.cp_enable.clicked.connect(
            lambda x: self.edit_args("use_tucker", x, optional=True, network_args=True)
        )
        self.widget.train_norm_enable.clicked.connect(
            lambda x: self.edit_args("train_norm", x, optional=True, network_args=True)
        )

        self.widget.network_dropout_enable.clicked.connect(
            lambda x: self.toggle_network_dropout(x, self.is_lycoris())
        )
        self.widget.network_dropout_input.valueChanged.connect(
            lambda x: self.edit_args(
                "dropout" if self.is_lycoris() else "network_dropout",
                x,
                optional=True,
                network_args=self.is_lycoris(),
            )
        )
        self.widget.rank_dropout_enable.clicked.connect(self.toggle_rank_dropout)
        self.widget.rank_dropout_input.valueChanged.connect(
            lambda x: self.edit_args(
                "rank_dropout", x, optional=True, network_args=True
            )
        )
        self.widget.module_dropout_enable.clicked.connect(self.toggle_module_dropout)
        self.widget.module_dropout_input.valueChanged.connect(
            lambda x: self.edit_args(
                "module_dropout", x, optional=True, network_args=True
            )
        )
        self.widget.lora_fa_enable.clicked.connect(
            lambda x: self.edit_args("fa", x, optional=True)
        )
        self.widget.ip_gamma_enable.clicked.connect(self.toggle_ip_gamma)
        self.widget.ip_gamma_input.valueChanged.connect(
            lambda x: self.edit_args("ip_noise_gamma", x, optional=True)
        )

    @QtCore.Slot(str, object, bool, bool)
    def edit_args(
        self,
        name: str,
        value: object,
        optional: bool = False,
        network_args: bool = False,
    ) -> None:
        if not optional:
            if network_args:
                self.network_args[name] = value
                return
            self.args[name] = value
            return
        if not value or value is False:
            if network_args and name in self.network_args:
                del self.network_args[name]
            if not network_args and name in self.args:
                del self.args[name]
            return
        if network_args:
            self.network_args[name] = value
            return
        self.args[name] = value

    @QtCore.Slot(str)
    def change_algo(self, algo: str) -> None:
        if algo.lower() == "lora":
            self.toggle_conv(False)
            self.toggle_lycoris(False)
            self.toggle_dylora(False)
            self.toggle_kohya(True)
            self.toggle_block_weight(True, True)
            self.toggle_dropout(True, False)
        if algo.lower() == "locon":
            self.toggle_conv(True)
            self.toggle_lycoris(False)
            self.toggle_dylora(False)
            self.toggle_kohya(True)
            self.toggle_block_weight(True, False)
            self.toggle_dropout(True, False)
        if algo.lower() == "dylora":
            self.toggle_conv(True)
            self.toggle_lycoris(False)
            self.toggle_dylora(True)
            self.toggle_kohya(True)
            self.toggle_block_weight(True, False)
            self.toggle_dropout(True, False)
        if algo.lower() in {"locon (lycoris)", "lokr", "loha", "ia3"}:
            self.toggle_conv(True)
            self.toggle_lycoris(True)
            self.toggle_dylora(False)
            self.toggle_kohya(False)
            self.toggle_block_weight(False, False)
            self.toggle_dropout(algo.lower() != "ia3", True)

    def toggle_conv(self, toggle: bool) -> None:
        self.widget.conv_dim_input.setEnabled(toggle)
        self.widget.conv_alpha_input.setEnabled(toggle)

        self.edit_args(
            "conv_dim",
            self.widget.conv_dim_input.value() if toggle else False,
            optional=True,
            network_args=True,
        )
        self.edit_args(
            "conv_alpha",
            round(self.widget.conv_alpha_input.value(), 2) if toggle else False,
            optional=True,
            network_args=True,
        )

    def toggle_lycoris(self, toggle: bool) -> None:
        self.widget.cp_enable.setEnabled(toggle)
        self.widget.train_norm_enable.setEnabled(toggle)
        self.widget.lycoris_preset_input.setEnabled(toggle)

        self.edit_args(
            "use_tucker",
            self.widget.cp_enable.isChecked() if toggle else False,
            optional=True,
            network_args=True,
        )
        self.edit_args(
            "train_norm",
            self.widget.train_norm_enable.isChecked() if toggle else False,
            optional=True,
            network_args=True,
        )
        self.edit_args(
            "preset",
            self.widget.lycoris_preset_input.text() if toggle else False,
            optional=True,
            network_args=True,
        )
        self.edit_args(
            "algo",
            self.widget.algo_select.currentText().split(" ")[0].lower()
            if toggle
            else False,
            optional=True,
            network_args=True,
        )

    def toggle_dylora(self, toggle: bool) -> None:
        self.widget.dylora_unit_input.setEnabled(toggle)

        self.edit_args(
            "unit",
            self.widget.dylora_unit_input.value() if toggle else False,
            optional=True,
            network_args=True,
        )

    def toggle_kohya(self, toggle: bool) -> None:
        self.widget.lora_fa_enable.setEnabled(toggle)
        self.widget.ip_gamma_enable.setEnabled(toggle)
        self.toggle_ip_gamma(
            self.widget.ip_gamma_enable.isChecked() if toggle else False
        )

        self.edit_args(
            "fa",
            self.widget.lora_fa_enable.isChecked() if toggle else False,
            optional=True,
        )

    def toggle_block_weight(self, toggle: bool, lora: bool) -> None:
        self.widget.block_weight_tab.setEnabled(toggle)
        for elem in self.block_widgets_state:
            elem[0].setEnabled(False)
            elem[1] = elem[0].extra_elem.isChecked()
            elem[0].extra_elem.setChecked(False)
            elem[0].enable_disable(False)
        if not toggle:
            return
        for i, elem in enumerate(self.block_widgets_state):
            if i > 2 and lora:
                return
            elem[0].setEnabled(True)
            if elem[1]:
                elem[0].extra_elem.setChecked(True)
                elem[0].enable_disable(True)
                elem[1] = False

    def toggle_dropout(self, toggle: bool, lycoris: bool) -> None:
        self.widget.network_dropout_enable.setEnabled(toggle)
        self.widget.rank_dropout_enable.setEnabled(toggle)
        self.widget.module_dropout_enable.setEnabled(toggle)

        if not toggle:
            self.toggle_network_dropout(False, lycoris)
            self.toggle_rank_dropout(False)
            self.toggle_module_dropout(False)
            return

        self.toggle_network_dropout(
            self.widget.network_dropout_enable.isChecked(), lycoris
        )
        self.toggle_rank_dropout(self.widget.rank_dropout_enable.isChecked())
        self.toggle_module_dropout(self.widget.module_dropout_enable.isChecked())

    @QtCore.Slot(bool, bool)
    def toggle_network_dropout(self, toggle: bool, lycoris: bool) -> None:
        if "dropout" in self.network_args:
            del self.network_args["dropout"]
        if "network_dropout" in self.args:
            del self.args["network_dropout"]
        self.widget.network_dropout_input.setEnabled(toggle)
        if lycoris:
            self.edit_args(
                "dropout",
                round(self.widget.network_dropout_input.value(), 2)
                if toggle
                else False,
                optional=True,
                network_args=True,
            )
            return
        self.edit_args(
            "network_dropout",
            round(self.widget.network_dropout_input.value(), 2) if toggle else False,
            optional=True,
        )

    @QtCore.Slot(bool)
    def toggle_rank_dropout(self, toggle: bool) -> None:
        self.widget.rank_dropout_input.setEnabled(toggle)
        self.edit_args(
            "rank_dropout",
            round(self.widget.rank_dropout_input.value(), 2) if toggle else False,
            optional=True,
            network_args=True,
        )

    @QtCore.Slot(bool)
    def toggle_module_dropout(self, toggle: bool) -> None:
        self.widget.module_dropout_input.setEnabled(toggle)
        self.edit_args(
            "module_dropout",
            round(self.widget.module_dropout_input.value(), 2) if toggle else False,
            optional=True,
            network_args=True,
        )

    @QtCore.Slot(str)
    def edit_timesteps(self, name: str) -> None:
        if name == "min_timestep":
            self.edit_args("min_timestep", self.widget.min_timestep_input.value())
            if (
                self.widget.max_timestep_input.value()
                <= self.widget.min_timestep_input.value()
            ):
                self.widget.max_timestep_input.setValue(
                    self.widget.min_timestep_input.value() + 1
                )
                self.edit_args("max_timestep", self.widget.max_timestep_input.value())
        else:
            self.edit_args("max_timestep", self.widget.max_timestep_input.value())
            if (
                self.widget.max_timestep_input.value()
                <= self.widget.min_timestep_input.value()
            ):
                self.widget.min_timestep_input.setValue(
                    self.widget.max_timestep_input.value() - 1
                )
                self.edit_args("min_timestep", self.widget.min_timestep_input.value())

    @QtCore.Slot(str)
    def change_training_parts(self, name: str) -> None:
        if "network_train_unet_only" in self.args:
            del self.args["network_train_unet_only"]
        if "network_train_text_encoder_only" in self.args:
            del self.args["network_train_text_encoder_only"]
        if name.lower() == "unet only":
            self.edit_args("network_train_unet_only", True)
        elif name.lower() == "te only":
            self.edit_args("network_train_text_encoder_only", True)

    @QtCore.Slot(bool)
    def toggle_sdxl(self, toggle: bool) -> None:
        for arg in ["cache_text_encoder_outputs", "cache_text_encoder_outputs_to_disk"]:
            if arg in self.args:
                del self.args[arg]
        self.widget.cache_te_outputs_enable.setEnabled(toggle)
        self.widget.cache_te_to_disk_enable.setEnabled(
            self.widget.cache_te_outputs_enable.isChecked()
        )
        if not toggle:
            return
        self.toggle_cache_te(self.widget.cache_te_outputs_enable.isChecked())

    @QtCore.Slot(bool)
    def toggle_cache_te(self, toggle: bool) -> None:
        for arg in ["cache_text_encoder_outputs", "cache_text_encoder_outputs_to_disk"]:
            if arg in self.args:
                del self.args[arg]
        self.edit_args("cache_text_encoder_outputs", toggle, optional=True)
        self.widget.cache_te_to_disk_enable.setEnabled(toggle)
        if not toggle:
            return
        self.edit_args(
            "cache_text_encoder_outputs_to_disk",
            self.widget.cache_te_to_disk_enable.isChecked(),
            optional=True,
        )

    @QtCore.Slot(bool)
    def toggle_ip_gamma(self, toggle: bool) -> None:
        self.widget.ip_gamma_input.setEnabled(toggle)
        self.edit_args(
            "ip_noise_gamma",
            self.widget.ip_gamma_input.value()
            if self.widget.ip_gamma_enable.isChecked()
            else False,
            optional=True,
        )

    def is_lycoris(self) -> bool:
        return self.widget.algo_select.currentText().lower() not in [
            "lora",
            "locon",
            "dylora",
        ]

    def deep_dict_copy(self, original):
        if not isinstance(original, dict):
            return original
        return {key: self.deep_dict_copy(value) for key, value in original.items()}

    def get_args(self, input_args: dict) -> None:
        args = self.save_args()
        input_args["network_args"] = args

    def get_dataset_args(self, input_args: dict) -> None:
        pass

    def save_args(self) -> Union[dict, None]:
        args = {}
        args |= self.deep_dict_copy(self.args)
        if self.network_args:
            args["network_args"] = self.deep_dict_copy(self.network_args)
        if block_args := self.get_block_args():
            if "network_args" not in args:
                args["network_args"] = block_args
            else:
                args["network_args"].update(block_args)
        return args

    def save_dataset_args(self) -> Union[dict, None]:
        pass

    def get_block_args(self) -> dict:
        args = {}
        names = [
            ["down_lr_weight", "mid_lr_weight", "up_lr_weight"],
            "block_dims",
            "block_alphas",
            "conv_block_dims",
            "conv_block_alphas",
        ]
        for i, elem in enumerate(self.block_widgets_state):
            if not elem[0].isEnabled() or not elem[0].extra_elem.isChecked():
                continue
            vals = self.block_widgets[i].vals
            name = names[i]
            if i == 0:
                for n in name:
                    args[n] = vals[n]
            else:
                args[name] = vals
        return args

    def load_args(self, args: dict) -> None:
        if self.name not in args:
            return
        sdxl = args["general_args"]["args"].get("sdxl", False)
        args = args[self.name]["args"]
        network_args = args["network_args"] if "network_args" in args else {}

        # handle non network args
        self.widget.network_dim_input.setValue(args["network_dim"])
        self.widget.network_alpha_input.setValue(args["network_alpha"])
        self.widget.lora_fa_enable.setChecked(args.get("fa", False))
        self.widget.ip_gamma_enable.setChecked(bool(args.get("ip_noise_gamma", False)))
        self.widget.ip_gamma_input.setValue(args.get("ip_noise_gamma", 0.1))
        self.toggle_ip_gamma(self.widget.ip_gamma_enable.isChecked())
        # self.edit_args("fa", self.widget.lora_fa_enable.isChecked(), optional=True)

        self.widget.min_timestep_input.setValue(args.get("min_timestep", 0))
        self.widget.max_timestep_input.setValue(args.get("max_timestep", 1000))
        self.edit_timesteps("min_timestep")
        self.edit_timesteps("max_timestep")

        self.widget.unet_te_both_select.setCurrentIndex(
            1
            if "network_train_unet_only" in args
            else 2
            if "network_train_text_encoder_only" in args
            else 0
        )

        self.widget.cache_te_to_disk_enable.setChecked(
            args.get("cache_text_encoder_outputs_to_disk", False)
        )
        self.widget.cache_te_outputs_enable.setChecked(
            args.get("cache_text_encoder_outputs", False)
        )
        self.toggle_sdxl(sdxl)
        # self.toggle_cache_te(self.widget.cache_te_outputs_enable.isChecked())

        self.widget.network_dropout_input.setValue(args.get("network_dropout", 0.1))
        self.widget.network_dropout_enable.setChecked(
            bool(args.get("network_dropout", False))
        )
        self.toggle_network_dropout(
            self.widget.network_dropout_enable.isChecked(), False
        )

        # handle network args
        self.widget.conv_dim_input.setValue(network_args.get("conv_dim", 32))
        self.widget.conv_alpha_input.setValue(network_args.get("conv_alpha", 16.0))
        self.widget.dylora_unit_input.setValue(network_args.get("unit", 4))
        self.widget.cp_enable.setChecked(network_args.get("use_tucker", False))
        self.widget.train_norm_enable.setChecked(network_args.get("train_norm", False))
        self.widget.lycoris_preset_input.setText(network_args.get("preset", ""))

        if "network_dropout" not in args:
            self.widget.network_dropout_input.setValue(network_args.get("dropout", 0.1))
            self.widget.network_dropout_enable.setChecked(
                bool(network_args.get("dropout", False))
            )
            self.toggle_network_dropout(
                self.widget.network_dropout_enable.isChecked(), True
            )

        self.widget.rank_dropout_input.setValue(network_args.get("rank_dropout", 0.1))
        self.widget.rank_dropout_enable.setChecked(
            bool(network_args.get("rank_dropout", False))
        )
        self.toggle_rank_dropout(self.widget.rank_dropout_enable.isChecked())

        self.widget.module_dropout_input.setValue(
            network_args.get("module_dropout", 0.1)
        )
        self.widget.module_dropout_enable.setChecked(
            bool(network_args.get("module_dropout", False))
        )
        self.toggle_module_dropout(self.widget.module_dropout_enable.isChecked())

        if "algo" in network_args:
            if network_args["algo"] == "locon":
                self.widget.algo_select.setCurrentText("LoCon (LyCORIS)")
            elif network_args["algo"] == "loha":
                self.widget.algo_select.setCurrentText("LoHa")
            elif network_args["algo"] == "ia3":
                self.widget.algo_select.setCurrentText("IA3")
            else:
                self.widget.algo_select.setCurrentText("Lokr")
        if "unit" in network_args:
            self.widget.algo_select.setCurrentText("DyLoRA")
        elif "conv_dim" in network_args:
            self.widget.algo_select.setCurrentText("LoCon")
        else:
            self.widget.algo_select.setCurrentText("LoRA")
        self.change_algo(self.widget.algo_select.currentText())
        self.load_block_args(network_args)

    def load_block_args(self, network_args: dict) -> None:
        inputs = ["block_dims", "block_alphas", "conv_block_dims", "conv_block_alphas"]
        if "down_lr_weight" in network_args:
            self.load_block_weight(
                network_args["down_lr_weight"],
                network_args["mid_lr_weight"],
                network_args["up_lr_weight"],
            )
        else:
            self.set_block_widget_enable(0, False)
        for i, name in enumerate(inputs):
            if vals := network_args.get(name):
                self.set_block_widget_enable(i + 1, True)
                for j, val in enumerate(vals):
                    self.block_widgets[i + 1].vals[j] = val
                    if j < 12:
                        if isinstance(val, str):
                            if name in ["block_alphas", "conv_block_alphas"]:
                                try:
                                    val = float(val)
                                except Exception:
                                    print(
                                        "failed to load some or all of the block weights"
                                    )
                                    return
                            else:
                                try:
                                    val = int(val)
                                except Exception:
                                    print(
                                        "failed to load some of all of the block weights"
                                    )
                                    return
                        self.block_widgets[i + 1].down_widgets[j][1].setValue(val)
                    elif j == 12:
                        self.block_widgets[i + 1].mid_widget[1].setValue(val)
                    else:
                        self.block_widgets[i + 1].up_widgets[j % 12][1].setValue(val)
            else:
                self.set_block_widget_enable(i + 1, False)

    def load_block_weight(
        self, down_lr_rate: list[float], mid_lr_weight: float, up_lr_weight: list[float]
    ) -> None:
        self.set_block_widget_enable(0, True)

        for i, val in enumerate(down_lr_rate):
            self.block_widgets[0].vals["down_lr_weight"][i] = val
            self.block_widgets[0].down_widgets[i][1].setValue(val)
        self.block_widgets[0].vals["mid_lr_weight"] = mid_lr_weight
        self.block_widgets[0].mid_widget[1].setValue(mid_lr_weight)
        for i, val in enumerate(up_lr_weight):
            self.block_widgets[0].vals["up_lr_weight"][i] = val
            self.block_widgets[0].up_widgets[i][1].setValue(val)

    def set_block_widget_enable(self, index, enabled):
        self.block_widgets_state[index][0].extra_elem.setChecked(enabled)
        self.block_widgets_state[index][0].enable_disable(enabled)
        self.block_widgets_state[index][1] = False

import json
from pathlib import Path

from PySide6 import QtCore
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QCheckBox, QFileDialog, QMessageBox, QWidget

from modules.BaseWidget import BaseWidget
from modules.BlockWeightWidgets import BlockWeightWidget, BlockWidget
from modules.CollapsibleWidget import CollapsibleWidget
from modules.OptimizerItem import OptimizerItem
from ui_files.NetworkUI import Ui_network_ui


class NetworkWidget(BaseWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.colap.set_title("Network Args")
        self.widget = Ui_network_ui()

        self.name = "network_args"
        self.args = {
            "network_dim": 32,
            "network_alpha": 16.0,
            "min_timestep": 0,
            "max_timestep": 1000,
        }
        self.lycoris = False
        self.network_args: list[OptimizerItem] = []

        self.setup_widget()
        self.setup_connections()

    def setup_widget(self) -> None:
        super().setup_widget()
        self.widget.setupUi(self.content)
        self.block_widgets: list[tuple[CollapsibleWidget, BlockWidget | BlockWeightWidget]] = [
            (self.widget.block_weight_widget, BlockWeightWidget()),
            (
                self.widget.dim_block_widget,
                BlockWidget(mode="int", base_value=32, arg_name="block_dims"),
            ),
            (
                self.widget.alpha_block_widget,
                BlockWidget(mode="float", base_value=16.0, arg_name="block_alphas"),
            ),
            (
                self.widget.conv_block_widget,
                BlockWidget(mode="int", base_value=32, arg_name="conv_block_dims"),
            ),
            (
                self.widget.conv_alpha_block_widget,
                BlockWidget(mode="float", base_value=16.0, arg_name="conv_block_alphas"),
            ),
        ]
        load_args_icon = QIcon(str(Path("icons/folder.svg")))
        self.widget.load_network_args_button.setIcon(load_args_icon)
        save_args_icon = QIcon(str(Path("icons/save.svg")))
        self.widget.save_network_args_button.setIcon(save_args_icon)
        selector_icon = QIcon(str(Path("icons/folder.svg")))
        self.widget.network_weight_file_input.setMode("file", [".safetensors", ".ckpt", ".pt", ".sft"])
        self.widget.network_weight_file_input.highlight = True
        self.widget.network_weight_file_selector.setIcon(selector_icon)
        self.widget.network_dim_file_input.setMode("file", [".safetensors", ".ckpt", ".pt", ".sft"])
        self.widget.network_dim_file_input.highlight = True
        self.widget.network_dim_file_selector.setIcon(selector_icon)

        self.widget.network_args_item_widget.layout().setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        for i, elem in enumerate(self.block_widgets):
            elem[0].set_extra("enable")
            elem[0].title_frame.setEnabled(False)
            elem[0].add_widget(elem[1], "main_widget")
            elem[0].toggled.connect(elem[1].enable_disable)
            if i == 0:
                elem[1].edited.connect(self.update_block_weight)
            else:
                elem[1].edited.connect(self.update_blocks)

        self.widget.block_weight_widget.title_frame.setText("Block Weights")
        self.widget.dim_block_widget.title_frame.setText("Block Dims")
        self.widget.alpha_block_widget.title_frame.setText("Block Alphas")
        self.widget.conv_block_widget.title_frame.setText("Block Conv Dims")
        self.widget.conv_alpha_block_widget.title_frame.setText("Block Conv Alpha")
        self.widget.block_weight_scroll_widget.layout().setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.widget.block_weight_scroll_widget.layout().setSpacing(0)

    def setup_connections(self) -> None:
        self.widget.algo_select.currentTextChanged.connect(lambda x: self.change_algo(x))
        self.widget.lycoris_preset_input.textChanged.connect(
            lambda x: self.edit_network_args("preset", x, True)
        )
        self.widget.network_dim_input.valueChanged.connect(lambda x: self.edit_args("network_dim", x))
        self.widget.conv_dim_input.valueChanged.connect(lambda x: self.edit_network_args("conv_dim", x, True))
        self.widget.network_alpha_input.valueChanged.connect(
            lambda x: self.edit_args("network_alpha", round(x, 2))
        )
        self.widget.conv_alpha_input.valueChanged.connect(
            lambda x: self.edit_network_args("conv_alpha", x, True)
        )
        self.widget.min_timestep_input.valueChanged.connect(lambda x: self.change_min_timestep(x))
        self.widget.max_timestep_input.valueChanged.connect(lambda x: self.change_max_timestep(x))
        self.widget.unet_te_both_select.currentIndexChanged.connect(self.change_unet_te_only)
        self.widget.network_dropout_enable.clicked.connect(self.enable_disable_network_dropout)
        self.widget.network_dropout_input.valueChanged.connect(
            lambda: self.enable_disable_network_dropout(self.widget.network_dropout_enable.isChecked())
        )
        self.widget.cache_te_outputs_enable.clicked.connect(self.enable_disable_cache_te)
        self.widget.cache_te_to_disk_enable.clicked.connect(
            lambda x: self.edit_args("cache_text_encoder_outputs_to_disk", x, True)
        )
        self.widget.rank_dropout_enable.clicked.connect(self.enable_disable_rank_dropout)
        self.widget.rank_dropout_input.valueChanged.connect(
            lambda x: self.edit_network_args("rank_dropout", x, True)
        )
        self.widget.dylora_unit_input.valueChanged.connect(lambda x: self.edit_network_args("unit", x, True))
        self.widget.bypass_mode_enable.clicked.connect(
            lambda x: self.toggle_dora_bypass(self.widget.dora_enable.isChecked(), x)
        )
        self.widget.module_dropout_enable.clicked.connect(self.enable_disable_module_dropout)
        self.widget.module_dropout_input.valueChanged.connect(
            lambda x: self.edit_network_args("module_dropout", x, True)
        )
        self.widget.cp_enable.clicked.connect(lambda x: self.edit_network_args("use_tucker", x, True))
        self.widget.train_norm_enable.clicked.connect(lambda x: self.edit_network_args("train_norm", x, True))
        self.widget.dora_enable.clicked.connect(
            lambda x: self.toggle_dora_bypass(x, self.widget.bypass_mode_enable.isChecked())
        )
        self.widget.ip_gamma_enable.clicked.connect(self.enable_disable_ip_gamma)
        self.widget.ip_gamma_input.valueChanged.connect(
            lambda x: self.edit_args("ip_noise_gamma", round(x, 4), True)
        )
        self.widget.rescale_enable.clicked.connect(lambda x: self.edit_network_args("rescaled", x, True))
        self.widget.constrain_enable.clicked.connect(self.enable_disable_constrain)
        self.widget.constrain_input.textChanged.connect(
            lambda x: self.edit_network_args("constraint", self.parse_float(x), True)
        )
        self.widget.lora_fa_enable.clicked.connect(lambda x: self.edit_args("fa", x, True))
        self.widget.add_network_arg_button.clicked.connect(self.add_network_arg)
        self.widget.load_network_args_button.clicked.connect(self.load_optional_args)
        self.widget.save_network_args_button.clicked.connect(self.save_optional_args)
        self.widget.network_weight_file_input.textChanged.connect(
            lambda x: self.edit_args("network_weights", x, True)
        )
        self.widget.network_weight_file_selector.clicked.connect(
            lambda: self.set_file_from_dialog(
                self.widget.network_weight_file_input, "Network Weights", "LoRA Model"
            )
        )
        self.widget.network_dim_file_input.textChanged.connect(
            lambda x: self.edit_args("dim_from_weights", x, True)
        )
        self.widget.network_dim_file_selector.clicked.connect(
            lambda: self.set_file_from_dialog(
                self.widget.network_dim_file_input, "Network Dims", "LoRA Model"
            )
        )

    def edit_network_args(self, name: str, value: object, optional: bool = False) -> None:
        if "network_args" not in self.args:
            self.edit_args("network_args", {})
        if name in self.args["network_args"]:
            del self.args["network_args"][name]
        if optional and (not value or value is False):
            return

        self.args["network_args"][name] = value

    def remove_network_arg(self, widget: OptimizerItem):
        self.layout().removeWidget(widget)
        self.edit_network_args(widget.arg_name, False, True)
        widget.deleteLater()
        self.network_args.remove(widget)

    def add_network_arg(self, arg_name: str = None, arg_value: str = None):
        self.network_args.append(OptimizerItem(arg_name=arg_name, arg_value=arg_value))
        self.widget.network_args_item_widget.layout().addWidget(self.network_args[-1])
        self.network_args[-1].delete_item.connect(self.remove_network_arg)
        self.network_args[-1].item_updated.connect(self.modify_network_arg)

    def modify_network_arg(self, widget: OptimizerItem):
        if widget.arg_name != widget.previous_name:
            self.edit_network_args(widget.previous_name, False, True)
        self.edit_network_args(widget.arg_name, widget.arg_value)

    # handles the enable and disable of the following elements according to the algorithm selected from the top:
    # lycoris_preset, conv_dim, conv_alpha, dylora_unit, all dropouts, lora_fa
    # enable_tucker, train_norm, rescale, constrain, all block weights
    def change_algo(self, algo: str) -> None:
        algo = algo.lower()
        self.toggle_conv(algo != "lora")
        self.toggle_kohya(algo in {"lora", "locon", "dylora"})
        dora = self.toggle_lycoris(
            algo not in {"lora", "locon", "dylora"},
            algo in {"locon (lycoris)", "loha", "lokr"},
        )
        self.lycoris = algo not in {"lora", "locon", "dylora"}
        self.widget.bypass_mode_enable.setEnabled(self.lycoris and not dora)
        self.edit_network_args(
            "bypass_mode",
            self.widget.bypass_mode_enable.isChecked() if self.lycoris else False,
            True,
        )
        self.toggle_dylora(algo == "dylora")
        self.toggle_block_weight(algo in {"lora", "locon", "dylora"}, algo == "lora")
        self.toggle_dropout(
            algo != "ia3",
            algo in {"locon (lycoris)", "loha", "lokr"} and self.widget.dora_enable.isChecked(),
        )

    def change_min_timestep(self, value: int) -> None:
        if value >= self.widget.max_timestep_input.value():
            value = self.widget.max_timestep_input.value() - 1
            self.widget.min_timestep_input.setValue(value)
        self.edit_args("min_timestep", value)

    def change_max_timestep(self, value: int) -> None:
        if value <= self.widget.min_timestep_input.value():
            value = self.widget.min_timestep_input.value() + 1
            self.widget.max_timestep_input.setValue(value)
        self.edit_args("max_timestep", value)

    def change_unet_te_only(self, index: int) -> None:
        args = ["network_train_unet_only", "network_train_text_encoder_only"]
        for arg in args:
            if arg in self.args:
                del self.args[arg]
        if index == 0:
            return
        self.edit_args(args[index - 1], True)

    # handles enabling and disabling of conv_dim, and conv_alpha
    def toggle_conv(self, toggle: bool) -> None:
        self.widget.conv_dim_input.setEnabled(toggle)
        self.widget.conv_alpha_input.setEnabled(toggle)

        self.edit_network_args("conv_dim", self.widget.conv_dim_input.value() if toggle else None, True)
        self.edit_network_args("conv_alpha", self.widget.conv_alpha_input.value() if toggle else None, True)

    def toggle_lycoris(self, toggle: bool, toggle_dora: bool) -> None:
        self.widget.cp_enable.setEnabled(toggle)
        self.widget.train_norm_enable.setEnabled(toggle)
        self.widget.lycoris_preset_input.setEnabled(toggle)
        self.widget.rescale_enable.setEnabled(toggle)
        self.widget.constrain_enable.setEnabled(toggle)

        self.edit_network_args(
            "algo",
            (self.widget.algo_select.currentText().split(" ")[0].lower() if toggle else False),
            True,
        )
        self.edit_network_args("preset", self.widget.lycoris_preset_input.text() if toggle else False, True)
        self.toggle_dora_bypass(
            self.widget.dora_enable.isChecked() if toggle_dora else False,
            self.widget.bypass_mode_enable.isChecked(),
        )
        self.edit_network_args("use_tucker", self.widget.cp_enable.isChecked() if toggle else False, True)
        self.edit_network_args(
            "train_norm",
            self.widget.train_norm_enable.isChecked() if toggle else False,
            True,
        )
        self.edit_network_args(
            "rescaled",
            self.widget.rescale_enable.isChecked() if toggle else False,
            True,
        )
        self.enable_disable_constrain(self.widget.constrain_enable.isChecked() if toggle else False)
        return self.widget.dora_enable.isChecked() and toggle_dora

    def toggle_dylora(self, toggle: bool) -> None:
        self.widget.dylora_unit_input.setEnabled(toggle)

        self.edit_network_args("unit", self.widget.dylora_unit_input.value() if toggle else False, True)

    def toggle_kohya(self, toggle: bool) -> None:
        self.widget.lora_fa_enable.setEnabled(toggle)
        self.edit_args("fa", self.widget.lora_fa_enable.isChecked() if toggle else False, True)

    def toggle_block_weight(self, toggle: bool, is_lora: bool) -> None:
        self.widget.block_weight_tab.setEnabled(toggle)
        for i, elem in enumerate(self.block_widgets):
            if i > 2 and is_lora:
                toggle = False
            elem[0].setEnabled(toggle)
            if not toggle:
                elem[0].extra_elem.setChecked(False)
                elem[0].enable_disable(False)

    def toggle_dropout(self, toggle: bool, toggle_dora: bool) -> None:
        self.widget.network_dropout_enable.setEnabled(toggle and not toggle_dora)
        self.widget.rank_dropout_enable.setEnabled(toggle)
        self.widget.module_dropout_enable.setEnabled(toggle)

        self.enable_disable_network_dropout(
            self.widget.network_dropout_enable.isChecked() if toggle and not toggle_dora else False
        )
        self.enable_disable_rank_dropout(self.widget.rank_dropout_enable.isChecked() if toggle else False)
        self.enable_disable_module_dropout(self.widget.module_dropout_enable.isChecked() if toggle else False)

    def toggle_sdxl(self, toggle: bool) -> None:
        self.widget.cache_te_outputs_enable.setEnabled(toggle)
        self.enable_disable_cache_te(self.widget.cache_te_outputs_enable.isChecked() if toggle else False)

    def enable_disable_network_dropout(self, checked: bool) -> None:
        if "network_dropout" in self.args:
            del self.args["network_dropout"]
        if "network_args" in self.args and "dropout" in self.args["network_args"]:
            del self.args["network_args"]["dropout"]
        self.widget.network_dropout_input.setEnabled(checked)
        if not checked:
            return
        if self.lycoris:
            self.edit_network_args("dropout", self.widget.network_dropout_input.value(), True)
        else:
            self.edit_args("network_dropout", self.widget.network_dropout_input.value(), True)

    def enable_disable_cache_te(self, checked: bool) -> None:
        args = ["cache_text_encoder_outputs", "cache_text_encoder_outputs_to_disk"]
        for arg in args:
            if arg in self.args:
                del self.args[arg]
        self.widget.cache_te_to_disk_enable.setEnabled(checked)
        self.edit_args(args[0], checked, True)
        self.edit_args(
            args[1],
            self.widget.cache_te_to_disk_enable.isChecked() if checked else False,
            True,
        )

    def enable_disable_rank_dropout(self, checked: bool) -> None:
        if "network_args" in self.args and "rank_dropout" in self.args["network_args"]:
            del self.args["network_args"]["rank_dropout"]
        self.widget.rank_dropout_input.setEnabled(checked)
        if not checked:
            return
        self.edit_network_args(
            "rank_dropout",
            self.widget.rank_dropout_input.value(),
            True,
        )

    def toggle_dora_bypass(self, dora: bool, bypass: bool) -> None:
        if bypass:
            self.widget.dora_enable.setChecked(False)
            dora = False
        self.widget.dora_enable.setEnabled(
            not bypass
            and self.widget.algo_select.currentText().lower() in {"locon (lycoris)", "loha", "lokr"}
        )
        self.widget.bypass_mode_enable.setEnabled(not dora)
        self.edit_network_args("dora_wd", dora if self.widget.dora_enable.isEnabled() else False, True)
        self.edit_network_args(
            "bypass_mode",
            bypass if self.widget.bypass_mode_enable.isEnabled() else False,
            True,
        )
        self.toggle_dropout(
            self.widget.algo_select.currentText().lower() != "ia3",
            dora and self.widget.dora_enable.isEnabled(),
        )

    def enable_disable_module_dropout(self, checked: bool) -> None:
        if "network_args" in self.args and "module_dropout" in self.args["network_args"]:
            del self.args["network_args"]["module_dropout"]
        self.widget.module_dropout_input.setEnabled(checked)
        if not checked:
            return
        self.edit_network_args("module_dropout", self.widget.module_dropout_input.value(), True)

    def enable_disable_ip_gamma(self, checked: bool) -> None:
        if "ip_noise_gamma" in self.args:
            del self.args["ip_noise_gamma"]
        self.widget.ip_gamma_input.setEnabled(checked)
        if not checked:
            return
        self.edit_args("ip_noise_gamma", round(self.widget.ip_gamma_input.value(), 4), True)

    def enable_disable_constrain(self, checked: bool) -> None:
        self.widget.constrain_input.setEnabled(checked)
        self.edit_network_args("constraint", self.parse_float(self.widget.constrain_input.text()), True)

    def parse_float(self, value: str) -> float | bool:
        try:
            value = float(value)
        except ValueError:
            value = False
        return value

    def update_block_weight(self, weights: dict, active: bool = False) -> None:
        args = ["down_lr_weight", "mid_lr_weight", "up_lr_weight"]
        for arg in args:
            if "network_args" in self.args and arg in self.args["network_args"]:
                del self.args["network_args"][arg]
        if not active:
            return
        for key, value in weights.items():
            self.edit_network_args(key, value, True)

    def update_blocks(self, weights: list[int] | list[float], name: str, active: bool = False) -> None:
        if "network_args" in self.args and name in self.args["network_args"]:
            del self.args["network_args"][name]
        if not active:
            return
        self.edit_network_args(name, weights, True)

    def load_optional_args(self):
        def update_config(checked: bool):
            config_path = Path("config.json")
            if not config_path.exists():
                config_path.write_text(json.dumps({}))
            config = json.loads(config_path.read_text())
            config["skip_network_args_warning"] = checked
            config_path.write_text(json.dumps(config))

        config: dict = json.loads(Path("config.json").read_text())
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Load Network Args",
            dir="",
            filter="Network Args (*.json)",
        )
        if not file_name:
            return
        args = json.loads(Path(file_name).read_text())

        if not isinstance(args, dict) or not args:
            if not config.get("skip_network_args_warning", False):
                checkbox = QCheckBox("Don't show this message again")
                checkbox.clicked.connect(update_config)
                message = QMessageBox(
                    QMessageBox.Icon.Warning,
                    "No Network Args Found",
                    "No network args found in the file. Are you sure you want to load the file?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    self,
                )
                message.setCheckBox(checkbox)
                result = message.exec()
                if result == QMessageBox.StandardButton.No:
                    return
            args = {}
        for _ in range(len(self.network_args)):
            self.remove_network_arg(self.network_args[0])
        for arg in args:
            if not isinstance(args[arg], str):
                continue
            self.add_network_arg()
            self.network_args[-1].arg_name_input.setText(str(arg))
            self.network_args[-1].arg_value_input.setText(str(args[arg]))

    def save_optional_args(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Network Args",
            dir="",
            filter="Network Args (*.json)",
        )
        if not file_name:
            return

        args = {}
        for network_arg in self.network_args:
            name, value = network_arg.get_arg()
            if not name or not value:
                continue
            args[name] = value

        Path(file_name).write_text(json.dumps(args))

    def load_args(self, args: dict) -> bool:
        args: dict = args.get(self.name, {})
        network_args: dict = args.get("network_args", {})

        # update algo
        if not network_args or "conv_dim" not in network_args:
            self.widget.algo_select.setCurrentIndex(0)
        elif "algo" not in network_args:
            self.widget.algo_select.setCurrentIndex(1)
        else:
            algo_modes = {
                "locon": "LoCon (LyCORIS)",
                "loha": "LoHa",
                "ia3": "IA3",
                "lokr": "Lokr",
                "dylora": "DyLoRA",
                "boft": "BOFT",
                "diag-oft": "Diag-OFT",
                "full": "Full",
            }
            self.widget.algo_select.setCurrentText(algo_modes[network_args["algo"]])

        # update element inputs
        self.widget.lycoris_preset_input.setText(network_args.get("preset", ""))
        self.widget.network_dim_input.setValue(args.get("network_dim", 32))
        self.widget.conv_dim_input.setValue(network_args.get("conv_dim", 32))
        self.widget.network_alpha_input.setValue(args.get("network_alpha", 16.0))
        self.widget.conv_alpha_input.setValue(network_args.get("conv_alpha", 16.0))
        self.widget.min_timestep_input.setValue(args.get("min_timestep", 0))
        self.widget.max_timestep_input.setValue(args.get("max_timestep", 1000))
        if "network_train_unet_only" in args:
            self.widget.unet_te_both_select.setCurrentIndex(1)
        elif "network_train_text_encoder_only" in args:
            self.widget.unet_te_both_select.setCurrentIndex(2)
        else:
            self.widget.unet_te_both_select.setCurrentIndex(0)
        self.widget.network_dropout_enable.setChecked(
            bool(args.get("network_dropout", network_args.get("dropout", False)))
        )
        self.widget.network_dropout_input.setValue(
            args.get("network_dropout", network_args.get("dropout", 0.1))
        )
        self.widget.cache_te_outputs_enable.setChecked(args.get("cache_text_encoder_outputs", False))
        self.widget.cache_te_to_disk_enable.setChecked(args.get("cache_text_encoder_outputs_to_disk", False))
        self.widget.rank_dropout_enable.setChecked(bool(network_args.get("rank_dropout", False)))
        self.widget.rank_dropout_input.setValue(network_args.get("rank_dropout", 0.1))
        self.widget.dylora_unit_input.setValue(network_args.get("unit", 4))
        self.widget.module_dropout_enable.setChecked(bool(network_args.get("module_dropout", False)))
        self.widget.module_dropout_input.setValue(network_args.get("module_dropout", 0.1))
        self.widget.bypass_mode_enable.setChecked(network_args.get("bypass_mode", False))
        self.widget.cp_enable.setChecked(network_args.get("use_tucker", False))
        self.widget.train_norm_enable.setChecked(network_args.get("train_norm", False))
        self.widget.dora_enable.setChecked(network_args.get("dora_wd", False))
        self.widget.ip_gamma_enable.setChecked(bool(args.get("ip_noise_gamma", False)))
        self.widget.ip_gamma_input.setValue(args.get("ip_noise_gamma", 0.1))
        self.widget.rescale_enable.setChecked(network_args.get("rescaled", False))
        self.widget.constrain_enable.setChecked(bool(network_args.get("constraint", False)))
        self.widget.constrain_input.setText(str(network_args.get("constraint", "")))
        self.widget.lora_fa_enable.setEnabled(args.get("fa", False))
        self.widget.network_weight_file_input.setText(args.get("network_weights", ""))
        self.widget.network_dim_file_input.setText(args.get("dim_from_weights", ""))

        # update block widgets
        self.load_block_weights(network_args)

        # edit args to match
        self.change_algo(self.widget.algo_select.currentText())
        self.edit_args("network_dim", self.widget.network_dim_input.value())
        self.edit_args("network_alpha", self.widget.network_alpha_input.value())
        self.change_min_timestep(self.widget.min_timestep_input.value())
        self.change_max_timestep(self.widget.max_timestep_input.value())
        self.change_unet_te_only(self.widget.unet_te_both_select.currentIndex())
        self.enable_disable_cache_te(self.widget.cache_te_outputs_enable.isChecked())
        self.enable_disable_ip_gamma(self.widget.ip_gamma_enable.isChecked())
        self.edit_args("network_weights", self.widget.network_weight_file_input.text(), True)
        self.edit_args("dim_from_weights", self.widget.network_dim_file_input.text(), True)
        self.load_network_args(network_args)
        return True

    def load_block_weights(self, network_args: dict) -> None:
        if "down_lr_weight" in network_args:
            self.block_widgets[0][0].extra_elem.setChecked(True)
            self.block_widgets[0][0].enable_disable(True)
            self.block_widgets[0][1].update_vals(
                down_vals=network_args["down_lr_weight"],
                mid_val=network_args["mid_lr_weight"],
                up_vals=network_args["up_lr_weight"],
            )
        if "block_dims" in network_args:
            self.block_widgets[1][0].extra_elem.setChecked(True)
            self.block_widgets[1][0].enable_disable(True)
            self.block_widgets[1][1].update_vals(network_args["block_dims"])
        if "block_alphas" in network_args:
            self.block_widgets[2][0].extra_elem.setChecked(True)
            self.block_widgets[2][0].enable_disable(True)
            self.block_widgets[2][1].update_vals(network_args["block_alphas"])
        if "conv_block_dims" in network_args:
            self.block_widgets[3][0].extra_elem.setChecked(True)
            self.block_widgets[3][0].enable_disable(True)
            self.block_widgets[3][1].update_vals(network_args["conv_block_dims"])
        if "conv_block_alphas" in network_args:
            self.block_widgets[4][0].extra_elem.setChecked(True)
            self.block_widgets[4][0].enable_disable(True)
            self.block_widgets[4][1].update_vals(network_args["conv_block_alphas"])

    def load_network_args(self, network_args: dict) -> None:
        skip_list = [
            "preset",
            "conv_dim",
            "conv_alpha",
            "rank_dropout",
            "unit",
            "module_dropout",
            "use_tucker",
            "train_norm",
            "rescaled",
            "constraint",
            "bypass_mode",
            "algo",
            "dropout",
            "dora_wd",
            "down_lr_weight",
            "mid_lr_weight",
            "up_lr_weight",
            "wd_on_output",
        ]
        for _ in range(len(self.network_args)):
            self.remove_network_arg(self.network_args[0])

        for arg, value in network_args.items():
            if arg in skip_list:
                continue
            self.add_network_arg(arg, value)
            self.modify_network_arg(self.network_args[-1])

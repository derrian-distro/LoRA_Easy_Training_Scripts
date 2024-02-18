from PySide6 import QtCore
from PySide6.QtWidgets import QWidget
from modules.BlockWeightWidgets import BlockWeightWidget, BlockWidget
from ui_files.NetworkUI import Ui_network_ui
from modules.BaseWidget import BaseWidget
from modules.CollapsibleWidget import CollapsibleWidget


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

        self.setup_widget()
        self.setup_connections()

    def setup_widget(self) -> None:
        super().setup_widget()
        self.widget.setupUi(self.content)
        self.block_widgets: list[
            tuple[CollapsibleWidget, BlockWidget | BlockWeightWidget]
        ] = [
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
                BlockWidget(
                    mode="float", base_value=16.0, arg_name="conv_block_alphas"
                ),
            ),
        ]

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
        self.widget.block_weight_scroll_widget.layout().setAlignment(
            QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.widget.block_weight_scroll_widget.layout().setSpacing(0)

    def setup_connections(self) -> None:
        self.widget.algo_select.currentTextChanged.connect(self.change_algo)
        self.widget.lycoris_preset_input.textChanged.connect(
            lambda x: self.edit_network_args("preset", x, True)
        )
        self.widget.network_dim_input.valueChanged.connect(
            lambda x: self.edit_args("network_dim", x)
        )
        self.widget.conv_dim_input.valueChanged.connect(
            lambda x: self.edit_network_args("conv_dim", x, True)
        )
        self.widget.network_alpha_input.valueChanged.connect(
            lambda x: self.edit_args("network_alpha", round(x, 2))
        )
        self.widget.conv_alpha_input.valueChanged.connect(
            lambda x: self.edit_network_args("conv_alpha", x, True)
        )
        self.widget.min_timestep_input.valueChanged.connect(
            lambda x: self.change_min_timestep(x)
        )
        self.widget.max_timestep_input.valueChanged.connect(
            lambda x: self.change_max_timestep(x)
        )
        self.widget.unet_te_both_select.currentIndexChanged.connect(
            self.change_unet_te_only
        )
        self.widget.network_dropout_enable.clicked.connect(
            self.enable_disable_network_dropout
        )
        self.widget.network_dropout_input.valueChanged.connect(
            lambda: self.enable_disable_network_dropout(
                self.widget.network_dropout_enable.isChecked()
            )
        )
        self.widget.cache_te_outputs_enable.clicked.connect(
            self.enable_disable_cache_te
        )
        self.widget.cache_te_to_disk_enable.clicked.connect(
            lambda x: self.edit_args("cache_text_encoder_outputs_to_disk", x, True)
        )
        self.widget.rank_dropout_enable.clicked.connect(
            self.enable_disable_rank_dropout
        )
        self.widget.rank_dropout_input.valueChanged.connect(
            lambda x: self.edit_network_args("rank_dropout", x, True)
        )
        self.widget.dylora_unit_input.valueChanged.connect(
            lambda x: self.edit_network_args("unit", x, True)
        )
        self.widget.module_dropout_enable.clicked.connect(
            self.enable_disable_module_dropout
        )
        self.widget.module_dropout_input.valueChanged.connect(
            lambda x: self.edit_network_args("module_dropout", x, True)
        )
        self.widget.cp_enable.clicked.connect(
            lambda x: self.edit_network_args("use_tucker", x, True)
        )
        self.widget.train_norm_enable.clicked.connect(
            lambda x: self.edit_network_args("train_norm", x, True)
        )
        self.widget.ip_gamma_enable.clicked.connect(self.enable_disable_ip_gamma)
        self.widget.ip_gamma_input.valueChanged.connect(
            lambda x: self.edit_args("ip_noise_gamma", x, True)
        )
        self.widget.rescale_enable.clicked.connect(
            lambda x: self.edit_network_args("rescaled", x, True)
        )
        self.widget.constrain_enable.clicked.connect(self.enable_disable_constrain)
        self.widget.constrain_input.textChanged.connect(
            lambda x: self.edit_network_args("constrain", self.parse_float(x), True)
        )
        self.widget.lora_fa_enable.clicked.connect(
            lambda x: self.edit_args("fa", x, True)
        )

    def edit_network_args(
        self, name: str, value: object, optional: bool = False
    ) -> None:
        if "network_args" not in self.args:
            self.edit_args("network_args", {})
        if name in self.args["network_args"]:
            del self.args["network_args"][name]
        if optional and (not value or value is False):
            return

        self.args["network_args"][name] = value

    # handles the enable and disable of the following elements according to the algorithm selected from the top:
    # lycoris_preset, conv_dim, conv_alpha, dylora_unit, all dropouts, ip_noise_gamma, lora_fa
    # enable_tucker, train_norm, rescale, constrain, all block weights
    def change_algo(self, algo: str) -> None:
        algo = algo.lower()
        self.toggle_conv(algo != "lora")
        self.toggle_kohya(algo in {"lora", "locon", "dylora"})
        self.toggle_lycoris(algo not in {"lora", "locon", "dylora"})
        self.lycoris = algo not in {"lora", "locon", "dylora"}
        self.toggle_dylora(algo == "dylora")
        self.toggle_block_weight(algo in {"lora", "locon", "dylora"}, algo == "lora")
        self.toggle_dropout(algo != "ia3")

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

        self.edit_network_args(
            "conv_dim", self.widget.conv_dim_input.value() if toggle else None, True
        )
        self.edit_network_args(
            "conv_alpha", self.widget.conv_alpha_input.value() if toggle else None, True
        )

    def toggle_lycoris(self, toggle: bool) -> None:
        self.widget.cp_enable.setEnabled(toggle)
        self.widget.train_norm_enable.setEnabled(toggle)
        self.widget.lycoris_preset_input.setEnabled(toggle)
        self.widget.rescale_enable.setEnabled(toggle)
        self.widget.constrain_enable.setEnabled(toggle)

        self.edit_network_args(
            "use_tucker", self.widget.cp_enable.isChecked() if toggle else False, True
        )
        self.edit_network_args(
            "train_norm",
            self.widget.train_norm_enable.isChecked() if toggle else False,
            True,
        )
        self.edit_network_args(
            "preset", self.widget.lycoris_preset_input.text() if toggle else False, True
        )
        self.edit_network_args(
            "rescaled",
            self.widget.rescale_enable.isChecked() if toggle else False,
            True,
        )
        self.enable_disable_constrain(
            self.widget.constrain_enable.isChecked() if toggle else False
        )
        self.edit_network_args(
            "algo",
            (
                self.widget.algo_select.currentText().split(" ")[0].lower()
                if toggle
                else False
            ),
            True,
        )

    def toggle_dylora(self, toggle: bool) -> None:
        self.widget.dylora_unit_input.setEnabled(toggle)

        self.edit_network_args(
            "unit", self.widget.dylora_unit_input.value() if toggle else False, True
        )

    def toggle_kohya(self, toggle: bool) -> None:
        self.widget.lora_fa_enable.setEnabled(toggle)
        self.widget.ip_gamma_enable.setEnabled(toggle)

        self.enable_disable_ip_gamma(
            self.widget.ip_gamma_enable.isChecked() if toggle else False
        )
        self.edit_args(
            "fa", self.widget.lora_fa_enable.isChecked() if toggle else False, True
        )

    def toggle_block_weight(self, toggle: bool, is_lora: bool) -> None:
        self.widget.block_weight_tab.setEnabled(toggle)
        for i, elem in enumerate(self.block_widgets):
            if i > 2 and is_lora:
                toggle = False
            elem[0].setEnabled(toggle)
            if not toggle:
                elem[0].extra_elem.setChecked(False)
                elem[0].enable_disable(False)

    def toggle_dropout(self, toggle: bool) -> None:
        self.widget.network_dropout_enable.setEnabled(toggle)
        self.widget.rank_dropout_enable.setEnabled(toggle)
        self.widget.module_dropout_enable.setEnabled(toggle)

        self.enable_disable_network_dropout(
            self.widget.network_dropout_enable.isChecked() if toggle else False
        )
        self.enable_disable_rank_dropout(
            self.widget.rank_dropout_enable.isChecked() if toggle else False
        )
        self.enable_disable_module_dropout(
            self.widget.module_dropout_enable.isChecked() if toggle else False
        )

    def toggle_sdxl(self, toggle: bool) -> None:
        self.widget.cache_te_outputs_enable.setEnabled(toggle)
        self.enable_disable_cache_te(
            self.widget.cache_te_outputs_enable.isChecked() if toggle else False
        )

    def enable_disable_network_dropout(self, checked: bool) -> None:
        if "network_dropout" in self.args:
            del self.args["network_dropout"]
        if "network_args" in self.args and "dropout" in self.args["network_args"]:
            del self.args["network_args"]["dropout"]
        self.widget.network_dropout_input.setEnabled(checked)
        if not checked:
            return
        if self.lycoris:
            self.edit_network_args(
                "dropout", self.widget.network_dropout_input.value(), True
            )
        else:
            self.edit_args(
                "network_dropout", self.widget.network_dropout_input.value(), True
            )

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

    def enable_disable_module_dropout(self, checked: bool) -> None:
        if (
            "network_args" in self.args
            and "module_dropout" in self.args["network_args"]
        ):
            del self.args["network_args"]["module_dropout"]
        self.widget.module_dropout_input.setEnabled(checked)
        if not checked:
            return
        self.edit_network_args(
            "module_dropout", self.widget.module_dropout_input.value(), True
        )

    def enable_disable_ip_gamma(self, checked: bool) -> None:
        if "ip_noise_gamma" in self.args:
            del self.args["ip_noise_gamma"]
        self.widget.ip_gamma_input.setEnabled(checked)
        if not checked:
            return
        self.edit_args("ip_noise_gamma", self.widget.ip_gamma_input.value(), True)

    def enable_disable_constrain(self, checked: bool) -> None:
        self.widget.constrain_input.setEnabled(checked)
        self.edit_network_args(
            "constrain", self.parse_float(self.widget.constrain_input.text()), True
        )

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

    def update_blocks(
        self, weights: list[int] | list[float], name: str, active: bool = False
    ) -> None:
        if "network_args" in self.args and name in self.args["network_args"]:
            del self.args["network_args"][name]
        if not active:
            return
        self.edit_network_args(name, weights, True)

    def load_args(self, args: dict) -> bool:
        if not super().load_args(args):
            return False

        args: dict = args[self.name]
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
        self.widget.cache_te_outputs_enable.setChecked(
            args.get("cache_text_encoder_outputs", False)
        )
        self.widget.cache_te_to_disk_enable.setChecked(
            args.get("cache_text_encoder_outputs_to_disk", False)
        )
        self.widget.rank_dropout_enable.setChecked(
            bool(network_args.get("rank_dropout", False))
        )
        self.widget.rank_dropout_input.setValue(network_args.get("rank_dropout", 0.1))
        self.widget.dylora_unit_input.setValue(network_args.get("unit", 4))
        self.widget.module_dropout_enable.setChecked(
            bool(network_args.get("module_dropout", False))
        )
        self.widget.module_dropout_input.setValue(
            network_args.get("module_dropout", 0.1)
        )
        self.widget.cp_enable.setChecked(network_args.get("use_tucker", False))
        self.widget.train_norm_enable.setChecked(network_args.get("train_norm", False))
        self.widget.ip_gamma_enable.setChecked(bool(args.get("ip_noise_gamma", False)))
        self.widget.ip_gamma_input.setValue(args.get("ip_noise_gamma", 0.1))
        self.widget.rescale_enable.setChecked(network_args.get("rescaled", False))
        self.widget.constrain_enable.setChecked(
            bool(network_args.get("constrain", False))
        )
        self.widget.constrain_input.setText(str(network_args.get("constrain", "")))
        self.widget.lora_fa_enable.setEnabled(args.get("fa", False))

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

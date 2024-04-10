import json
from pathlib import Path
from PySide6.QtCore import Slot
from PySide6 import QtCore
from PySide6.QtWidgets import QWidget
from ui_files.OptimizerUI import Ui_optimizer_ui
from modules.BaseWidget import BaseWidget
from modules.OptimizerItem import OptimizerItem


class OptimizerWidget(BaseWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.colap.set_title("Optimizer Args")
        self.widget = Ui_optimizer_ui()

        self.name = "optimizer_args"
        self.args = {
            "optimizer_type": "AdamW",
            "lr_scheduler": "cosine",
            "learning_rate": 1e-4,
            "max_grad_norm": 1.0,
        }
        self.opt_args = [OptimizerItem(arg_name="weight_decay", arg_value="0.1")]

        self.setup_widget()
        self.setup_connections()

    def setup_widget(self) -> None:
        super().setup_widget()
        self.widget.setupUi(self.content)
        self.widget.optimizer_item_widget.layout().setAlignment(
            QtCore.Qt.AlignmentFlag.AlignTop
        )
        for opt_arg in self.opt_args:
            self.widget.optimizer_item_widget.layout().addWidget(opt_arg)
            opt_arg.delete_item.connect(self.remove_optimizer_arg)
            opt_arg.item_updated.connect(self.modify_optimizer_args)
        self.modify_optimizer_args()

    def setup_connections(self) -> None:
        self.widget.optimizer_type_selector.currentTextChanged.connect(
            self.change_optimizer
        )
        self.widget.lr_scheduler_selector.currentTextChanged.connect(
            self.change_scheduler
        )
        self.widget.main_lr_input.textChanged.connect(
            lambda x: self.edit_lr("learning_rate", x)
        )
        self.widget.warmup_enable.clicked.connect(self.enable_disable_warmup)
        self.widget.warmup_input.valueChanged.connect(
            lambda x: self.edit_args("warmup_ratio", round(x, 2), True)
        )
        self.widget.min_lr_input.textChanged.connect(
            lambda x: self.edit_lr_args("min_lr", x, True)
        )
        self.widget.cosine_restart_input.valueChanged.connect(
            lambda x: self.edit_args("lr_scheduler_num_cycles", x)
        )
        self.widget.unet_lr_enable.clicked.connect(self.enable_disable_unet)
        self.widget.unet_lr_input.textChanged.connect(
            lambda x: self.edit_lr("unet_lr", x, True)
        )
        self.widget.poly_power_input.valueChanged.connect(
            lambda x: self.edit_args("lr_scheduler_power", x)
        )
        self.widget.te_lr_enable.clicked.connect(self.enable_disable_te)
        self.widget.te_lr_input.textChanged.connect(
            lambda x: self.edit_lr("text_encoder_lr", x)
        )
        self.widget.gamma_input.valueChanged.connect(
            lambda x: self.edit_lr_args("gamma", 1 - x)
        )
        self.widget.scale_weight_enable.clicked.connect(
            self.enable_disable_scale_weight_norms
        )
        self.widget.scale_weight_input.valueChanged.connect(
            lambda x: self.edit_args("scale_weight_norms", x, True)
        )
        self.widget.max_grad_norm_input.valueChanged.connect(
            lambda x: self.edit_args("max_grad_norm", x)
        )
        self.widget.min_snr_enable.clicked.connect(self.enable_disable_min_snr_gamma)
        self.widget.min_snr_input.valueChanged.connect(
            lambda x: self.edit_args("min_snr_gamma", x)
        )
        self.widget.zero_term_enable.clicked.connect(
            lambda x: self.edit_args("zero_terminal_snr", x, True)
        )
        self.widget.add_opt_button.clicked.connect(self.add_optimizer_arg)

    def edit_lr(self, name: str, value: str, optional: bool = False) -> None:
        try:
            value = float(value)
        except ValueError:
            value = 0.0
        super().edit_args(name, value, optional)

    def edit_lr_args(self, name: str, value: object, optional: bool = False) -> None:
        if "lr_scheduler_args" not in self.args:
            self.edit_args("lr_scheduler_args", {})
        if name in self.args["lr_scheduler_args"]:
            del self.args["lr_scheduler_args"][name]
        if optional and (not value or value is False):
            return
        if isinstance(value, str):
            try:
                value = float(value)
            except ValueError:
                return
        self.args["lr_scheduler_args"][name] = value

    @Slot(object)
    def remove_optimizer_arg(self, widget: OptimizerItem):
        self.layout().removeWidget(widget)
        if (
            "optimizer_args" in self.args
            and widget.arg_name in self.args["optimizer_args"]
        ):
            del self.args["optimizer_args"][widget.arg_name]
        widget.deleteLater()
        self.opt_args.remove(widget)
        self.modify_optimizer_args()

    @Slot()
    def add_optimizer_arg(self):
        self.opt_args.append(OptimizerItem())
        self.widget.optimizer_item_widget.layout().addWidget(self.opt_args[-1])
        self.opt_args[-1].delete_item.connect(self.remove_optimizer_arg)
        self.opt_args[-1].item_updated.connect(self.modify_optimizer_args)

    @Slot()
    def modify_optimizer_args(self):
        if len(self.opt_args) == 0:
            self.edit_args("optimizer_args", None, True)
            return
        self.edit_args("optimizer_args", {})
        for opt_arg in self.opt_args:
            name, value = opt_arg.get_arg()
            if not name or not value:
                continue
            self.args["optimizer_args"][name] = value

    @Slot(str)
    def change_scheduler(self, value: str) -> None:
        value = value.replace(" ", "_")
        args = [
            "lr_scheduler_num_cycles",
            "lr_scheduler_power",
            "lr_scheduler_type",
            "lr_scheduler_args",
        ]
        for arg in args:
            if arg in self.args:
                del self.args[arg]
        self.widget.cosine_restart_input.setEnabled(False)
        self.widget.poly_power_input.setEnabled(False)
        self.widget.min_lr_input.setEnabled(False)
        self.widget.gamma_input.setEnabled(False)

        if value == "cosine_with_restarts":
            self.widget.cosine_restart_input.setEnabled(True)
            self.edit_args(
                "lr_scheduler_num_cycles",
                self.widget.cosine_restart_input.value(),
                True,
            )
        elif value == "cosine_annealing_warmup_restarts":
            self.widget.cosine_restart_input.setEnabled(True)
            self.widget.min_lr_input.setEnabled(True)
            self.widget.gamma_input.setEnabled(True)
            self.edit_args(
                "lr_scheduler_type",
                "LoraEasyCustomOptimizer.CustomOptimizers.CosineAnnealingWarmupRestarts",
            )
            self.edit_lr_args("min_lr", self.widget.min_lr_input.text(), True)
            self.edit_args(
                "lr_scheduler_num_cycles",
                self.widget.cosine_restart_input.value(),
                True,
            )
            self.edit_lr_args("gamma", 1 - self.widget.gamma_input.value(), True)
            return
        elif value == "polynomial":
            self.widget.poly_power_input.setEnabled(True)
            self.edit_args(
                "lr_scheduler_power", self.widget.poly_power_input.value(), True
            )
        elif value == "rex":
            self.widget.min_lr_input.setEnabled(True)
            self.edit_args(
                "lr_scheduler_type",
                "LoraEasyCustomOptimizer.CustomOptimizers.Rex",
            )
            self.edit_lr_args("min_lr", self.widget.min_lr_input.text(), True)
            return
        self.edit_args("lr_scheduler", value)

    @Slot(str)
    def change_optimizer(self, value: str) -> None:
        if value != "Came":
            self.edit_args("optimizer_type", value)
            return
        config = Path("config.json")
        config = json.loads(config.read_text()) if config.is_file() else {}
        if config.get("colab", False):
            self.edit_args("optimizer_type", "came_pytorch.CAME.CAME")
        else:
            self.edit_args("optimizer_type", "pytorch_optimizer.optimizer.came.CAME")

    @Slot(bool)
    def enable_disable_warmup(self, checked: bool) -> None:
        if "warmup_ratio" in self.args:
            del self.args["warmup_ratio"]
        self.widget.warmup_input.setEnabled(checked)
        if not checked:
            return
        self.edit_args("warmup_ratio", self.widget.warmup_input.value(), True)

    @Slot(bool)
    def enable_disable_unet(self, checked: bool) -> None:
        if "unet_lr" in self.args:
            del self.args["unet_lr"]
        self.widget.unet_lr_input.setEnabled(checked)
        if not checked:
            return
        self.edit_lr("unet_lr", self.widget.unet_lr_input.text(), True)

    @Slot(bool)
    def enable_disable_te(self, checked: bool) -> None:
        if "text_encoder_lr" in self.args:
            del self.args["text_encoder_lr"]
        self.widget.te_lr_input.setEnabled(checked)
        if not checked:
            return
        self.edit_lr("text_encoder_lr", self.widget.te_lr_input.text(), True)

    @Slot(bool)
    def enable_disable_scale_weight_norms(self, checked: bool) -> None:
        if "scale_weight_norms" in self.args:
            del self.args["scale_weight_norms"]
        self.widget.scale_weight_input.setEnabled(checked)
        if not checked:
            return
        self.edit_args(
            "scale_weight_norms", self.widget.scale_weight_input.value(), True
        )

    @Slot(bool)
    def enable_disable_min_snr_gamma(self, checked: bool) -> None:
        if "min_snr_gamma" in self.args:
            del self.args["min_snr_gamma"]
        self.widget.min_snr_input.setEnabled(checked)
        if not checked:
            return
        self.edit_args("min_snr_gamma", self.widget.min_snr_input.value(), True)

    def load_args(self, args: dict) -> bool:
        args: dict = args.get(self.name, {})

        # update element inputs
        optimizer_type = args.get("optimizer_type", "AdamW")
        self.widget.optimizer_type_selector.setCurrentText(
            "Came" if len(optimizer_type.split(".")) > 1 else optimizer_type
        )
        if "lr_scheduler_type" in args:
            self.widget.lr_scheduler_selector.setCurrentText(
                "cosine annealing warmup restarts"
                if args["lr_scheduler_type"].split(".")[-1] != "Rex"
                else "rex"
            )
        else:
            self.widget.lr_scheduler_selector.setCurrentText(
                args.get("lr_scheduler", "cosine").replace("_", " ")
            )
        self.widget.main_lr_input.setText(str(args.get("learning_rate", "1e-4")))
        self.widget.warmup_enable.setChecked(bool(args.get("warmup_ratio", False)))
        self.widget.warmup_input.setValue(args.get("warmup_ratio", 0.0))
        self.widget.min_lr_input.setText(
            str(args.get("lr_scheduler_args", {}).get("min_lr", "1e-6"))
        )
        self.widget.cosine_restart_input.setValue(
            args.get("lr_scheduler_num_cycles", 1)
        )
        self.widget.unet_lr_enable.setChecked(bool(args.get("unet_lr", False)))
        self.widget.unet_lr_input.setText(str(args.get("unet_lr", "1e-4")))
        self.widget.poly_power_input.setValue(args.get("lr_scheduler_power", 1.0))
        self.widget.te_lr_enable.setChecked(bool(args.get("text_encoder_lr", False)))
        self.widget.te_lr_input.setText(str(args.get("text_encoder_lr", "1e-4")))
        self.widget.gamma_input.setValue(
            round(1 - args.get("lr_scheduler_args", {}).get("gamma", 0.9), 2)
        )
        self.widget.scale_weight_enable.setChecked(
            bool(args.get("scale_weight_norms", False))
        )
        self.widget.scale_weight_input.setValue(args.get("scale_weight_norms", 1.0))
        self.widget.max_grad_norm_input.setValue(args.get("max_grad_norm", 1.0))
        self.widget.min_snr_enable.setChecked(bool(args.get("min_snr_gamma", False)))
        self.widget.min_snr_input.setValue(args.get("min_snr_gamma", 5))
        self.widget.zero_term_enable.setChecked(args.get("zero_terminal_snr", False))

        for _ in range(len(self.opt_args)):
            self.remove_optimizer_arg(self.opt_args[0])

        if opt_args := args.get("optimizer_args", {}):
            for name, value in opt_args.items():
                self.add_optimizer_arg()
                self.opt_args[-1].arg_name_input.setText(str(name))
                self.opt_args[-1].arg_value_input.setText(str(value))

        # edit args to match
        self.change_optimizer(self.widget.optimizer_type_selector.currentText())
        # also handles min_lr, num_restarts, poly_power, restart_decay
        self.change_scheduler(self.widget.lr_scheduler_selector.currentText())
        self.edit_lr("learning_rate", self.widget.main_lr_input.text())
        self.enable_disable_warmup(self.widget.warmup_enable.isChecked())
        self.enable_disable_unet(self.widget.unet_lr_enable.isChecked())
        self.enable_disable_te(self.widget.te_lr_enable.isChecked())
        self.enable_disable_scale_weight_norms(
            self.widget.scale_weight_enable.isChecked()
        )
        self.edit_args("max_grad_norm", self.widget.max_grad_norm_input.value())
        self.enable_disable_min_snr_gamma(self.widget.min_snr_enable.isChecked())
        self.edit_args(
            "zero_terminal_snr", self.widget.zero_term_enable.isChecked(), True
        )
        self.modify_optimizer_args()
        return True

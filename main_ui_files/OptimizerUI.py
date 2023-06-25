from typing import Union

from PySide6 import QtCore, QtWidgets
from ui_files.OptimizerUI import Ui_optimizer_ui
from modules.CollapsibleWidget import CollapsibleWidget
from modules.LineEditHighlight import LineEditWithHighlight
from modules.OptimizerItem import OptimizerItem


class OptimizerWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super(OptimizerWidget, self).__init__(parent)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.args = {"optimizer_type": "AdamW", "lr_scheduler": "cosine", "learning_rate": 1e-4}
        self.opt_arg_list = [OptimizerItem(arg_name="weight_decay", arg_value="0.1"),
                             OptimizerItem(arg_name="betas", arg_value="0.9,0.99")]
        self.name = "optimizer_args"
        self.colap = CollapsibleWidget(self, "Optimizer Args")
        self.content = QtWidgets.QWidget()
        self.colap.add_widget(self.content, "main_widget")
        self.widget = Ui_optimizer_ui()
        self.widget.setupUi(self.content)
        self.layout().addWidget(self.colap)
        self.layout().setContentsMargins(9, 0, 9, 0)
        self.widget.optimizer_item_widget.layout().setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        for opt_item in self.opt_arg_list:
            self.widget.optimizer_item_widget.layout().addWidget(opt_item)
            opt_item.delete_item.connect(self.remove_optimizer_arg)

        # set all of the slots for inputs
        self.widget.optimizer_type_selector.currentTextChanged.connect(lambda x: self.edit_args("optimizer_type", x))
        self.widget.lr_scheduler_selector.currentTextChanged.connect(self.edit_scheduler)
        self.widget.main_lr_input.textChanged.connect(lambda x: self.edit_lr("learning_rate", x))
        self.widget.min_lr_input.textChanged.connect(lambda x: self.edit_lr("min_lr", x, True))
        self.widget.unet_lr_input.textChanged.connect(lambda x: self.edit_lr("unet_lr", x, True))
        self.widget.te_lr_input.textChanged.connect(lambda x: self.edit_lr("text_encoder_lr", x, True))
        self.widget.cosine_restart_input.valueChanged.connect(lambda x: self.edit_args("lr_scheduler_num_cycles", x))
        self.widget.poly_power_input.valueChanged.connect(lambda x: self.edit_args("lr_scheduler_power", x))
        self.widget.warmup_ratio_input.valueChanged.connect(lambda x: self.edit_args("warmup_ratio", x, True))
        self.widget.gamma_input.valueChanged.connect(lambda x: self.edit_lr_args('gamma', 1 - x, True))
        self.widget.min_snr_input.valueChanged.connect(lambda x: self.edit_args("min_snr_gamma", x, True))
        self.widget.scale_weight_input.valueChanged.connect(lambda x: self.edit_args("scale_weight_norms", x))
        self.widget.add_opt_button.clicked.connect(self.add_optimizer_arg)

        # set all of the slots for enable and disable
        self.widget.unet_lr_enable.clicked.connect(
            lambda x: self.enable_disable_lr(x, self.widget.unet_lr_input, "unet_lr"))
        self.widget.te_lr_enable.clicked.connect(
            lambda x: self.enable_disable_lr(x, self.widget.te_lr_input, "text_encoder_lr"))
        self.widget.warmup_enable.clicked.connect(self.enable_disable_warmup)
        self.widget.min_snr_enable.clicked.connect(self.enable_disable_gamma)
        self.widget.scale_weight_enable.clicked.connect(self.enable_disable_scale_weight)

    @QtCore.Slot(str, object, bool)
    def edit_args(self, name: str, value: object, optional: bool = False) -> None:
        if not optional:
            if isinstance(value, str):
                value = value.replace(" ", "_")
            self.args[name] = value
            return
        if value:
            if isinstance(value, str):
                value = value.replace(" ", "_")
            self.args[name] = value
        else:
            if name in self.args:
                del self.args[name]

    @QtCore.Slot(str, str, bool)
    def edit_lr(self, name: str, value: str, optional: bool = False) -> None:
        if not optional:
            try:
                value = float(value)
                if name == "min_lr":
                    self.edit_lr_args(name, value, True)
                    return
                self.args[name] = value
            except ValueError:
                if name == 'min_lr':
                    self.edit_lr_args(name, 0.0, True)
                    return
                self.args[name] = 0.0
            return
        if value:
            try:
                value = float(value)
                if name == "min_lr":
                    self.edit_lr_args(name, value, True)
                    return
                self.args[name] = value
            except ValueError:
                if name == 'min_lr':
                    self.edit_lr_args(name, None, True)
                    return
                if name in self.args:
                    del self.args[name]
        else:
            if name == 'min_lr':
                self.edit_lr_args(name, None, True)
                return
            if name in self.args:
                del self.args[name]

    @QtCore.Slot(str, object, bool)
    def edit_lr_args(self, name: str, value: object, optional: bool = False) -> None:
        if "lr_scheduler_args" not in self.args:
            self.args['lr_scheduler_args'] = {}
        if not optional:
            self.args['lr_scheduler_args'][name] = value
            return
        if value is not None:
            self.args['lr_scheduler_args'][name] = value
        elif name in self.args['lr_scheduler_args']:
            del self.args['lr_scheduler_args'][name]

    @QtCore.Slot(str)
    def edit_scheduler(self, value: str) -> None:
        value = value.replace(" ", "_")
        if "lr_scheduler_num_cycles" in self.args:
            del self.args["lr_scheduler_num_cycles"]
        if "lr_scheduler_power" in self.args:
            del self.args['lr_scheduler_power']
        if "lr_scheduler_type" in self.args:
            del self.args['lr_scheduler_type']
        if "lr_scheduler_args" in self.args:
            del self.args['lr_scheduler_args']
        self.widget.cosine_restart_input.setEnabled(False)
        self.widget.poly_power_input.setEnabled(False)
        self.widget.min_lr_input.setEnabled(False)
        self.widget.gamma_input.setEnabled(False)
        if value == "cosine_with_restarts":
            self.widget.cosine_restart_input.setEnabled(True)
            self.edit_args("lr_scheduler_num_cycles", self.widget.cosine_restart_input.value())
        elif value == "cosine_annealing_warmup_restarts":
            self.args['lr_scheduler_type'] = "LoraEasyCustomOptimizer.CustomOptimizers.CosineAnnealingWarmupRestarts"
            self.widget.cosine_restart_input.setEnabled(True)
            self.widget.min_lr_input.setEnabled(True)
            self.widget.gamma_input.setEnabled(True)
            self.edit_lr("min_lr", self.widget.min_lr_input.text(), True)
            self.edit_args("lr_scheduler_num_cycles", self.widget.cosine_restart_input.value())
            self.edit_lr_args('gamma', 1 - self.widget.gamma_input.value(), True)
            return
        elif value == "polynomial":
            self.widget.poly_power_input.setEnabled(True)
            self.edit_args("lr_scheduler_power", self.widget.poly_power_input.value())
        self.args["lr_scheduler"] = value

    @QtCore.Slot(bool, LineEditWithHighlight, str)
    def enable_disable_lr(self, checked: bool, elem: LineEditWithHighlight, name: str) -> None:
        if checked:
            elem.setEnabled(True)
            self.edit_lr(name, elem.text(), True)
        else:
            elem.setEnabled(False)
            if name in self.args:
                del self.args[name]

    @QtCore.Slot(bool)
    def enable_disable_warmup(self, checked: bool) -> None:
        if checked:
            self.widget.warmup_ratio_input.setEnabled(True)
            self.edit_args("warmup_ratio", self.widget.warmup_ratio_input.value(), True)
        else:
            self.widget.warmup_ratio_input.setEnabled(False)
            if "warmup_ratio" in self.args:
                del self.args['warmup_ratio']

    @QtCore.Slot(bool)
    def enable_disable_gamma(self, checked: bool) -> None:
        if checked:
            self.widget.min_snr_input.setEnabled(True)
            self.edit_args("min_snr_gamma", self.widget.min_snr_input.value(), True)
        else:
            self.widget.min_snr_input.setEnabled(False)
            if "min_snr_gamma" in self.args:
                del self.args['min_snr_gamma']

    @QtCore.Slot(bool)
    def enable_disable_scale_weight(self, checked: bool) -> None:
        self.widget.scale_weight_input.setEnabled(checked)
        self.edit_args("scale_weight_norms", None if not checked else self.widget.scale_weight_input.value(), True)

    def get_args(self, input_args: dict) -> None:
        input_args['optimizer_args'] = self.save_args()

    def get_dataset_args(self, input_args: dict) -> None:
        pass

    @QtCore.Slot()
    def add_optimizer_arg(self):
        self.opt_arg_list.append(OptimizerItem())
        self.widget.optimizer_item_widget.layout().addWidget(self.opt_arg_list[-1])
        self.opt_arg_list[-1].delete_item.connect(self.remove_optimizer_arg)

    @QtCore.Slot(object)
    def remove_optimizer_arg(self, widget: OptimizerItem):
        self.layout().removeWidget(widget)
        if "optimizer_args" in self.args and widget.arg_name in self.args['optimizer_args']:
            del self.args['optimizer_args'][widget.arg_name]
        widget.deleteLater()
        self.opt_arg_list.remove(widget)

    def load_args(self, args: dict) -> None:
        if self.name not in args:
            return
        args = args[self.name]['args']

        self.widget.cosine_restart_input.setValue(args.get('lr_scheduler_num_cycles', 1))
        self.widget.poly_power_input.setValue(args.get("lr_scheduler_power", 1.00))

        if 'lr_scheduler_type' in args:
            self.widget.lr_scheduler_selector.setCurrentText("cosine annealing warmup restarts")
        else:
            if 'lr_scheduler_type' in self.args:
                del self.args['lr_scheduler_type']
            self.widget.lr_scheduler_selector.setCurrentText(args['lr_scheduler'].replace("_", " "))
        self.widget.optimizer_type_selector.setCurrentText(args['optimizer_type'])
        self.widget.main_lr_input.setText(str(args['learning_rate']))

        checked = True if args.get("unet_lr", False) else False
        self.widget.unet_lr_enable.setChecked(checked)
        self.widget.unet_lr_input.setText(str(args.get("unet_lr", 1e-4)))
        self.enable_disable_lr(checked, self.widget.unet_lr_input, "unet_lr")

        checked = True if args.get("text_encoder_lr", False) else False
        self.widget.te_lr_enable.setChecked(checked)
        self.widget.te_lr_input.setText(str(args.get("text_encoder_lr", 1e-4)))
        self.enable_disable_lr(checked, self.widget.te_lr_input, "text_encoder_lr")

        checked = True if args.get("warmup_ratio", False) else False
        self.widget.warmup_enable.setChecked(checked)
        self.widget.warmup_ratio_input.setValue(args.get("warmup_ratio", 0.00))
        self.enable_disable_warmup(checked)

        checked = True if args.get("min_snr_gamma", False) else False
        self.widget.min_snr_enable.setChecked(checked)
        self.widget.min_snr_input.setValue(args.get('min_snr_gamma', 5))
        self.enable_disable_gamma(checked)

        checked = True if args.get('scale_weight_norms', False) else False
        self.widget.scale_weight_enable.setChecked(checked)
        self.widget.scale_weight_input.setValue(args.get('scale_weight_norms', 1.0))
        self.enable_disable_scale_weight(checked)

        if 'optimizer_args' in args:
            for i in range(len(self.opt_arg_list)):
                self.remove_optimizer_arg(self.opt_arg_list[0])
            for key, value in args['optimizer_args'].items():
                if not isinstance(value, str):
                    value = str(value)
                self.opt_arg_list.append(OptimizerItem(arg_name=key, arg_value=value))
                self.widget.optimizer_item_widget.layout().addWidget(self.opt_arg_list[-1])
                self.opt_arg_list[-1].delete_item.connect(self.remove_optimizer_arg)
        else:
            for i in range(len(self.opt_arg_list)):
                self.remove_optimizer_arg(self.opt_arg_list[0])

        if "lr_scheduler_args" in args:
            if 'lr_scheduler_args' in self.args:
                del self.args['lr_scheduler_args']
            self.args['lr_scheduler_args'] = {}
            for key, value in args['lr_scheduler_args'].items():
                if key == 'min_lr':
                    self.widget.min_lr_input.setText(str(value))
                if key == 'gamma':
                    self.widget.gamma_input.setValue(1 - value)
                self.args['lr_scheduler_args'][key] = value
        else:
            if 'lr_scheduler_args' in self.args:
                del self.args['lr_scheduler_args']

    def save_args(self) -> Union[dict, None]:
        new_args = self.args.copy()
        for arg in self.opt_arg_list:
            if "optimizer_args" not in new_args:
                new_args['optimizer_args'] = {}
            name, value = arg.get_arg()
            new_args['optimizer_args'][name] = value
        if "optimizer_args" in new_args and len(new_args['optimizer_args']) == 0:
            del new_args['optimizer_args']
        return new_args

    def save_dataset_args(self) -> Union[dict, None]:
        pass

from PySide6 import QtWidgets, QtCore
from ui_files.NetworkUI import Ui_network_ui
from modules.CollapsibleWidget import CollapsibleWidget


class NetworkWidget(QtWidgets.QWidget):
    args_edited = QtCore.Signal(str, object)

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super(NetworkWidget, self).__init__(parent)
        self.args = {"network_dim": 32, "network_alpha": 16.0}
        self.name = "network_args"

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(9, 0, 9, 0)
        self.colap = CollapsibleWidget(self, "Network Args")

        self.widget = QtWidgets.QWidget()
        self.ui = Ui_network_ui()
        self.ui.setupUi(self.widget)

        self.ui.network_dim_input.valueChanged.connect(lambda x: self.edit_args("network_dim", x))
        self.ui.network_alpha_input.valueChanged.connect(lambda x: self.edit_args("network_alpha", round(x, 2)))
        self.ui.conv_dim_input.valueChanged.connect(lambda x: self.edit_network_args("conv_dim", x))
        self.ui.conv_alpha_input.valueChanged.connect(lambda x: self.edit_network_args("conv_alpha", round(x, 2)))
        self.ui.dylora_unit_input.valueChanged.connect(lambda x: self.edit_network_args("unit", x))
        self.ui.algo_select.currentTextChanged.connect(self.algo_changed)
        self.ui.unet_te_both_select.currentTextChanged.connect(self.change_training_parts)

        self.colap.add_widget(self.widget, "main_widget")
        self.layout().addWidget(self.colap)

    @QtCore.Slot(str, object)
    def edit_args(self, name: str, value: object) -> None:
        self.args[name] = value
        self.args_edited.emit(name, value)

    @QtCore.Slot(str, object)
    def edit_network_args(self, name: str, value: object) -> None:
        if "network_args" not in self.args:
            self.args['network_args'] = {}
        self.args['network_args'][name] = value

    @QtCore.Slot(str)
    def change_training_parts(self, name: str) -> None:
        if name == "Unet Only":
            self.args['network_train_unet_only'] = True
            if "network_train_text_encoder_only" in self.args:
                del self.args['network_train_text_encoder_only']
        elif name == "Text Encoder Only":
            self.args['network_train_text_encoder_only'] = True
            if "network_train_unet_only" in self.args:
                del self.args['network_train_unet_only']
        else:
            if "network_train_unet_only" in self.args:
                del self.args['network_train_unet_only']
            if "network_train_text_encoder_only" in self.args:
                del self.args['network_train_text_encoder_only']

    @QtCore.Slot(str)
    def algo_changed(self, name: str) -> None:
        if name == "LoRA":
            if "network_args" in self.args:
                del self.args['network_args']
            self.ui.conv_alpha_input.setEnabled(False)
            self.ui.conv_dim_input.setEnabled(False)
            self.ui.dylora_unit_input.setEnabled(False)
        else:
            self.ui.conv_alpha_input.setEnabled(True)
            self.ui.conv_dim_input.setEnabled(True)
            if "network_args" not in self.args:
                self.args['network_args'] = {}
            self.args['network_args']["conv_dim"] = self.ui.conv_dim_input.value()
            self.args['network_args']["conv_alpha"] = round(self.ui.conv_alpha_input.value(), 2)
            if name == "DyLoRA":
                self.ui.dylora_unit_input.setEnabled(True)
                self.args['network_args']['unit'] = self.ui.dylora_unit_input.value()
                if 'algo' in self.args['network_args']:
                    del self.args['network_args']['algo']
            else:
                self.ui.dylora_unit_input.setEnabled(False)
                if "unit" in self.args['network_args']:
                    del self.args['network_args']['unit']
            if name not in {"LoCon", "DyLoRA"}:
                self.args['network_args']['algo'] = name.lower()
            else:
                if "algo" in self.args['network_args']:
                    del self.args['network_args']['algo']

    def get_args(self, input_args: dict) -> None:
        input_args['network_args'] = self.args

    def get_dataset_args(self, input_args: dict) -> None:
        pass

    def load_args(self, args: dict) -> None:
        if self.name not in args:
            return
        args = args[self.name]['args']
        self.ui.network_dim_input.setValue(args['network_dim'])
        self.ui.network_alpha_input.setValue(args['network_alpha'])
        index = 1 if "network_train_unet_only" in args else 2 if "network_train_text_encoder_only" in args else 0
        self.ui.unet_te_both_select.setCurrentIndex(index)
        if "network_args" in args:
            self.ui.conv_dim_input.setValue(args['network_args'].get("conv_dim", 32))
            self.ui.conv_alpha_input.setValue(args['network_args'].get("conv_alpha", 16))
            self.ui.dylora_unit_input.setValue(args['network_args'].get("unit", 4))
            if "unit" in args['network_args']:
                self.ui.algo_select.setCurrentIndex(5)
            elif "algo" in args['network_args']:
                algo = args['network_args']['algo']
                index = 2 if algo == 'loha' else 3 if algo == "ia3" else 4
                self.ui.algo_select.setCurrentIndex(index)
            elif "conv_dim" in args['network_args']:
                self.ui.algo_select.setCurrentIndex(1)
        else:
            self.ui.algo_select.setCurrentIndex(0)

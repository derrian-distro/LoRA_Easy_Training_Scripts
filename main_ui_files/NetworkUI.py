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
        self.name = "network_args"

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(9, 0, 9, 0)
        self.colap = CollapsibleWidget(self, "Network Args")

        self.widget = QtWidgets.QWidget()
        self.ui = Ui_network_ui()
        self.ui.setupUi(self.widget)
        self.block_widgets_state = [[self.ui.block_weight_widget, False], [self.ui.dim_block_widget, False],
                                    [self.ui.alpha_block_widget, False], [self.ui.conv_block_widget, False],
                                    [self.ui.conv_alpha_block_widget, False]]
        self.block_widgets = [BlockWeightWidget(), BlockWidget(mode='int', base_value=32),
                              BlockWidget(mode="float", base_value=16.00), BlockWidget(mode='int', base_value=32),
                              BlockWidget(mode='float', base_value=16.00)]

        self.ui.block_weight_scroll_widget.layout().setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.ui.block_weight_scroll_widget.layout().setSpacing(0)

        for i, elem in enumerate(self.block_widgets_state):
            elem[0].set_extra('enable')
            elem[0].title_frame.setEnabled(False)
            elem[0].add_widget(self.block_widgets[i], 'main_widget')
        self.ui.block_weight_widget.title_frame.setText("Block Weights")
        self.ui.dim_block_widget.title_frame.setText("Block Dims")
        self.ui.alpha_block_widget.title_frame.setText("Block Alphas")
        self.ui.conv_block_widget.title_frame.setText("Block Conv Dims")
        self.ui.conv_alpha_block_widget.title_frame.setText("Block Conv Alphas")

        self.ui.network_dim_input.valueChanged.connect(lambda x: self.edit_args("network_dim", x))
        self.ui.network_dim_input.valueChanged.connect(self.block_widgets[1].update_base_value)
        self.ui.network_alpha_input.valueChanged.connect(lambda x: self.edit_args("network_alpha", round(x, 2)))
        self.ui.network_alpha_input.valueChanged.connect(self.block_widgets[2].update_base_value)
        self.ui.conv_dim_input.valueChanged.connect(lambda x: self.edit_network_args("conv_dim", x))
        self.ui.conv_dim_input.valueChanged.connect(self.block_widgets[3].update_base_value)
        self.ui.conv_alpha_input.valueChanged.connect(lambda x: self.edit_network_args("conv_alpha", round(x, 2)))
        self.ui.conv_alpha_input.valueChanged.connect(self.block_widgets[4].update_base_value)
        self.ui.dylora_unit_input.valueChanged.connect(lambda x: self.edit_network_args("unit", x))
        self.ui.algo_select.currentTextChanged.connect(self.algo_changed)
        self.ui.unet_te_both_select.currentTextChanged.connect(self.change_training_parts)

        self.ui.network_dropout_enable.clicked.connect(lambda x: self.enable_disable_dropout("network", x))
        self.ui.network_dropout_input.valueChanged.connect(self.change_network_dropout)

        self.ui.rank_dropout_enable.clicked.connect(lambda x: self.enable_disable_dropout('rank', x))
        self.ui.rank_dropout_input.valueChanged.connect(lambda x: self.edit_network_args('rank_dropout', x))

        self.ui.module_dropout_enable.clicked.connect(lambda x: self.enable_disable_dropout('module', x))
        self.ui.module_dropout_input.valueChanged.connect(lambda x: self.edit_network_args('module_dropout', x))

        self.ui.cp_enable.clicked.connect(lambda x: self.edit_network_args('use_conv_cp', x))

        self.ui.min_timestep_input.editingFinished.connect(lambda: self.edit_timesteps('min_timestep'))
        self.ui.max_timestep_input.editingFinished.connect(lambda: self.edit_timesteps('max_timestep'))
        self.ui.cache_te_outputs_enable.clicked.connect(self.enable_disable_cache_tenc)

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

    @QtCore.Slot(float)
    def change_network_dropout(self, value: float) -> None:
        if 'network_args' in self.args and 'dropout' in self.args['network_args']:
            del self.args['network_args']['dropout']
        if 'network_dropout' in self.args:
            del self.args['network_dropout']
        if self.ui.algo_select.currentText() in {'lora', 'locon', 'dylora'}:
            self.edit_args('network_dropout', value)
        else:
            self.edit_network_args('dropout', value)

    @QtCore.Slot(str)
    def edit_timesteps(self, name: str) -> None:
        if name == 'min_timestep':
            self.edit_args('min_timestep', self.ui.min_timestep_input.value())
            if self.ui.max_timestep_input.value() <= self.ui.min_timestep_input.value():
                self.ui.max_timestep_input.setValue(self.ui.min_timestep_input.value() + 1)
                self.edit_args('max_timestep', self.ui.max_timestep_input.value())
        else:
            self.edit_args('max_timestep', self.ui.max_timestep_input.value())
            if self.ui.max_timestep_input.value() <= self.ui.min_timestep_input.value():
                self.ui.min_timestep_input.setValue(self.ui.max_timestep_input.value() - 1)
                self.edit_args('min_timestep', self.ui.min_timestep_input.value())

    @QtCore.Slot(bool)
    def enable_disable_cache_tenc(self, checked: bool):
        if 'cache_text_encoder_outputs' in self.args:
            del self.args['cache_text_encoder_outputs']
        if checked:
            self.edit_args('cache_text_encoder_outputs', True)

    @QtCore.Slot(bool)
    def enable_disable_cache_text_encoder_outputs(self, checked: bool):
        self.ui.cache_te_outputs_enable.setEnabled(checked)
        self.enable_disable_cache_tenc(self.ui.cache_te_outputs_enable.isChecked() if checked else False)

    @QtCore.Slot(str, bool)
    def enable_disable_dropout(self, mode: str, checked: bool):
        if mode == 'network':
            if 'network_args' in self.args and 'dropout' in self.args['network_args']:
                del self.args['network_args']['dropout']
            if 'network_dropout' in self.args:
                del self.args['network_dropout']
            self.ui.network_dropout_input.setEnabled(checked)
            if checked:
                self.change_network_dropout(self.ui.network_dropout_input.value())
        elif mode == 'rank':
            if 'network_args' in self.args and 'rank_dropout' in self.args['network_args']:
                del self.args['network_args']['rank_dropout']
            self.ui.rank_dropout_input.setEnabled(checked)
            if checked:
                self.edit_network_args("rank_dropout", self.ui.rank_dropout_input.value())
        else:
            if 'network_args' in self.args and 'module_dropout' in self.args['network_args']:
                del self.args['network_args']['module_dropout']
            self.ui.module_dropout_input.setEnabled(checked)
            if checked:
                self.edit_network_args('module_dropout', self.ui.module_dropout_input.value())

    @QtCore.Slot(str)
    def algo_changed(self, name: str) -> None:
        if 'network_args' in self.args:
            del self.args['network_args']
        self.ui.conv_dim_input.setEnabled(False)
        self.ui.conv_alpha_input.setEnabled(False)
        self.ui.dylora_unit_input.setEnabled(False)
        self.ui.cp_enable.setEnabled(False)
        if name.lower() == 'lora':
            self.enable_dropouts(lyco=False)
        elif name.lower() in {'locon', 'dylora'}:
            self.enable_dropouts(lyco=False)
            self.ui.conv_dim_input.setEnabled(True)
            self.edit_network_args('conv_dim', self.ui.conv_dim_input.value())
            self.ui.conv_alpha_input.setEnabled(True)
            self.edit_network_args('conv_alpha', self.ui.conv_alpha_input.value())
            if name.lower() == 'dylora':
                self.ui.dylora_unit_input.setEnabled(True)
                self.edit_network_args('unit', self.ui.dylora_unit_input.value())
        elif name.lower() == 'lokr':
            self.disable_dropouts()
            self.ui.conv_dim_input.setEnabled(True)
            self.edit_network_args('conv_dim', self.ui.conv_dim_input.value())
            self.ui.conv_alpha_input.setEnabled(True)
            self.edit_network_args('conv_alpha', self.ui.conv_alpha_input.value())
            self.ui.cp_enable.setEnabled(True)
            if self.ui.cp_enable.isChecked():
                self.edit_network_args('use_conv_cp', True)
            self.edit_network_args('algo', name.lower().split(" (lycoris)")[0])
        else:
            self.enable_dropouts(lyco=True)
            self.ui.conv_dim_input.setEnabled(True)
            self.edit_network_args('conv_dim', self.ui.conv_dim_input.value())
            self.ui.conv_alpha_input.setEnabled(True)
            self.edit_network_args('conv_alpha', self.ui.conv_alpha_input.value())
            self.ui.cp_enable.setEnabled(True)
            if self.ui.cp_enable.isChecked():
                self.edit_network_args('use_conv_cp', True)
            if name.lower() == 'dylora (lycoris)':
                self.ui.dylora_unit_input.setEnabled(True)
                self.edit_network_args('block_size', self.ui.dylora_unit_input.value())
            self.edit_network_args('algo', name.lower().split(" (lycoris)")[0])
        self.change_block_weight_enable(name)

    def enable_dropouts(self, lyco: bool):
        self.ui.network_dropout_enable.setEnabled(True)
        self.ui.network_dropout_input.setEnabled(True)
        self.ui.rank_dropout_enable.setEnabled(True)
        self.ui.rank_dropout_input.setEnabled(True)
        self.ui.module_dropout_enable.setEnabled(True)
        self.ui.module_dropout_input.setEnabled(True)
        if self.ui.network_dropout_enable.isChecked():
            if lyco:
                self.edit_network_args('dropout', self.ui.network_dropout_input.value())
            else:
                self.edit_args('network_dropout', self.ui.network_dropout_input.value())
        if self.ui.rank_dropout_enable.isChecked():
            self.edit_network_args('rank_dropout', self.ui.rank_dropout_input.value())
        if self.ui.module_dropout_enable.isChecked():
            self.edit_network_args('module_dropout', self.ui.module_dropout_input.value())

    def disable_dropouts(self):
        if 'network_args' in self.args:
            for arg in ['dropout', 'rank_dropout', 'module_dropout']:
                if arg in self.args['network_args']:
                    del self.args['network_args'][arg]
        if 'network_dropout' in self.args:
            del self.args['network_dropout']
        self.ui.network_dropout_enable.setEnabled(False)
        self.ui.network_dropout_input.setEnabled(False)
        self.ui.rank_dropout_enable.setEnabled(False)
        self.ui.rank_dropout_input.setEnabled(False)
        self.ui.module_dropout_enable.setEnabled(False)
        self.ui.module_dropout_input.setEnabled(False)

    def change_block_weight_enable(self, algo: str):
        if algo.lower() == 'lora':
            for i, elem in enumerate(self.block_widgets_state):
                if i < 3:
                    elem[0].setEnabled(True)
                    if elem[1]:
                        elem[0].extra_elem.setChecked(True)
                        elem[0].enable_disable(True)
                    elem[1] = False
                else:
                    elem[0].setEnabled(False)
                    if elem[0].extra_elem.isChecked():
                        print(elem[0].title_frame.text())
                        elem[1] = True
                        elem[0].extra_elem.setChecked(False)
                        elem[0].enable_disable(False)
        elif algo.lower() == 'locon':
            for elem in self.block_widgets_state:
                elem[0].setEnabled(True)
                if elem[1]:
                    elem[0].extra_elem.setChecked(True)
                    elem[0].enable_disable(True)
                elem[1] = False
        else:
            for elem in self.block_widgets_state:
                elem[0].setEnabled(False)
                if elem[0].extra_elem.isChecked():
                    elem[1] = True
                    elem[0].extra_elem.setChecked(False)
                    elem[0].enable_disable(False)

    def get_args(self, input_args: dict) -> None:
        input_args['network_args'] = self.args
        self.get_block_args(input_args['network_args'])

    def get_dataset_args(self, input_args: dict) -> None:
        pass

    def get_block_args(self, input_args: dict) -> None:
        names = [['down_lr_weight', 'mid_lr_weight', 'up_lr_weight'], 'block_dims',
                 'block_alphas', 'conv_block_dims', 'conv_block_alphas']
        for i, elem in enumerate(self.block_widgets_state):
            if not elem[0].extra_elem.isChecked():
                if "network_args" in input_args:
                    if i == 0:
                        for n in names[i]:
                            if n in input_args['network_args']:
                                del input_args['network_args'][n]
                    else:
                        if names[i] in input_args['network_args']:
                            del input_args['network_args'][names[i]]
                continue
            if "network_args" not in input_args:
                input_args['network_args'] = {}
            vals = self.block_widgets[i].vals
            name = names[i]
            if isinstance(name, list):
                for n in name:
                    input_args['network_args'][n] = vals[n]
            else:
                input_args['network_args'][name] = vals
        if 'network_args' in input_args and len(input_args['network_args'].keys()) == 0:
            del input_args['network_args']

    def load_block_args(self, input_args: dict) -> None:
        net_args = input_args['network_args']
        inputs = ['block_dims', 'block_alphas', 'conv_block_dims', 'conv_block_alphas']
        if "down_lr_weight" in net_args:
            self.block_widgets_state[0][0].extra_elem.setChecked(True)
            self.block_widgets_state[0][0].enable_disable(True)
            self.block_widgets_state[0][1] = False
            for i, val in enumerate(net_args['down_lr_weight']):
                self.block_widgets[0].vals['down_lr_weight'][i] = val
                self.block_widgets[0].down_widgets[i][1].setValue(val)
            self.block_widgets[0].vals['mid_lr_weight'] = net_args['mid_lr_weight']
            self.block_widgets[0].mid_widget[1].setValue(net_args['mid_lr_weight'])
            for i, val in enumerate(net_args['up_lr_weight']):
                self.block_widgets[0].vals['up_lr_weight'][i] = val
                self.block_widgets[0].up_widgets[i][1].setValue(val)
        else:
            self.block_widgets_state[0][0].extra_elem.setChecked(False)
            self.block_widgets_state[0][0].enable_disable(False)
            self.block_widgets_state[0][1] = False
        for i, name in enumerate(inputs):
            vals = net_args.get(name, None)
            if vals:
                self.block_widgets_state[i + 1][0].extra_elem.setChecked(True)
                self.block_widgets_state[i + 1][0].enable_disable(True)
                self.block_widgets_state[i + 1][1] = False
                for j, val in enumerate(vals):
                    self.block_widgets[i + 1].vals[j] = val
                    if j < 12:
                        if isinstance(val, str):
                            if name in ['block_alphas', 'conv_block_alphas']:
                                try:
                                    val = float(val)
                                except:
                                    print("failed to load some or all of the block weights")
                                    return
                            else:
                                try:
                                    val = int(val)
                                except:
                                    print("failed to load some of all of the block weights")
                                    return
                        self.block_widgets[i + 1].down_widgets[j][1].setValue(val)
                    elif j == 12:
                        self.block_widgets[i + 1].mid_widget[1].setValue(val)
                    else:
                        self.block_widgets[i + 1].up_widgets[j % 12][1].setValue(val)
            else:
                self.block_widgets_state[i + 1][0].extra_elem.setChecked(False)
                self.block_widgets_state[i + 1][0].enable_disable(False)
                self.block_widgets_state[i + 1][1] = False

    def load_args(self, args: dict) -> None:
        if self.name not in args:
            return
        sdxl = args['general_args']['args'].get('sdxl', False)
        args = args[self.name]['args']
        self.ui.network_dim_input.setValue(args['network_dim'])
        self.ui.network_alpha_input.setValue(args['network_alpha'])
        index = 1 if "network_train_unet_only" in args else 2 if "network_train_text_encoder_only" in args else 0
        self.ui.unet_te_both_select.setCurrentIndex(index)

        checked = True if args.get('network_dropout', False) else False
        self.ui.network_dropout_enable.setChecked(checked)
        self.ui.network_dropout_input.setValue(args.get('network_dropout', 0.1))
        self.enable_disable_dropout('network', checked)

        self.ui.min_timestep_input.setValue(args.get('min_timestep', 0))
        self.ui.max_timestep_input.setValue(args.get('max_timestep', 1000))
        self.edit_timesteps('min_timestep')
        self.edit_timesteps('max_timestep')
        self.ui.cache_te_outputs_enable.setChecked(args.get('cache_text_encoder_outputs', False))
        self.enable_disable_cache_text_encoder_outputs(sdxl)


        if "network_args" in args:
            self.ui.conv_dim_input.setValue(args['network_args'].get("conv_dim", 32))
            self.ui.conv_alpha_input.setValue(args['network_args'].get("conv_alpha", 16))
            self.ui.dylora_unit_input.setValue(args['network_args'].get("unit", 4))

            checked = True if args['network_args'].get('dropout', False) else False
            self.ui.network_dropout_enable.setChecked(checked)
            self.ui.network_dropout_input.setValue(args['network_args'].get('dropout', 0.1))
            self.enable_disable_dropout('network', checked)

            checked = True if args['network_args'].get('rank_dropout', False) else False
            self.ui.rank_dropout_enable.setChecked(checked)
            self.ui.rank_dropout_input.setValue(args['network_args'].get('rank_dropout', 0.1))
            self.enable_disable_dropout('rank', checked)

            checked = True if args['network_args'].get('module_dropout', False) else False
            self.ui.module_dropout_enable.setChecked(checked)
            self.ui.module_dropout_input.setValue(args['network_args'].get('module_dropout', 0.1))
            self.enable_disable_dropout('module', checked)

            if "unit" in args['network_args']:
                self.ui.algo_select.setCurrentIndex(6)
            elif "algo" in args['network_args']:
                algo = args['network_args']['algo']
                index = 2 if algo == 'locon' else 3 if algo == 'loha' else 4 if algo == "ia3" else 5 if algo == 'lokr' \
                    else 7
                self.ui.cp_enable.setChecked(args['network_args'].get("use_conv_cp", False))
                self.ui.cp_enable.setEnabled(True)
                self.ui.algo_select.setCurrentIndex(index)
            elif "conv_dim" in args['network_args']:
                self.ui.algo_select.setCurrentIndex(1)
            else:
                self.ui.algo_select.setCurrentIndex(0)
            self.load_block_args(args)
        else:
            self.ui.algo_select.setCurrentIndex(0)

    def save_args(self) -> Union[dict, None]:
        self.get_block_args(self.args)
        return self.args

    def save_dataset_args(self) -> Union[dict, None]:
        pass

import json
import os
from typing import Union

from PySide6 import QtWidgets, QtCore
from modules import ScrollOnSelect


class BlockWidget(QtWidgets.QWidget):
    edited = QtCore.Signal(list, str, bool)

    def __init__(
        self,
        parent: QtWidgets.QWidget = None,
        mode: str = "int",
        base_value: Union[int, float] = None,
        arg_name: str = None,
    ):
        super(BlockWidget, self).__init__(parent)
        self.up_preset_label = None
        self.down_preset_label = None
        self.base_value_label = None
        self.main_layout = QtWidgets.QGridLayout()
        self.mode = mode
        self.arg_name = arg_name
        self.enabled = False

        self.vals = [0 for _ in range(25)]  # default all values to 0 on creation
        self.down_widgets = [
            (
                QtWidgets.QLabel(),
                (
                    ScrollOnSelect.SpinBox()
                    if mode == "int"
                    else ScrollOnSelect.DoubleSpinBox()
                ),
            )
            for _ in range(12)
        ]
        self.mid_widget = (
            QtWidgets.QLabel(),
            (
                ScrollOnSelect.SpinBox()
                if mode == "int"
                else ScrollOnSelect.DoubleSpinBox()
            ),
        )
        self.up_widgets = [
            (
                QtWidgets.QLabel(),
                (
                    ScrollOnSelect.SpinBox()
                    if mode == "int"
                    else ScrollOnSelect.DoubleSpinBox()
                ),
            )
            for _ in range(12)
        ]

        self.down_preset = ScrollOnSelect.ComboBox()
        self.base_value = (
            ScrollOnSelect.SpinBox()
            if mode == "int"
            else ScrollOnSelect.DoubleSpinBox()
        )
        self.base_value.setValue(base_value or 0)
        self.up_preset = ScrollOnSelect.ComboBox()
        self.presets = self.setup_presets()

        self.setup_layout()

    def setup_layout(self):
        self.down_preset_label = QtWidgets.QLabel("Down Preset")
        self.down_preset_label.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Preferred
        )
        self.main_layout.addWidget(self.down_preset_label, 0, 0, 1, 1)
        self.main_layout.addWidget(self.down_preset, 0, 1, 1, 1)
        self.base_value_label = QtWidgets.QLabel("Base Value")
        self.base_value_label.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Preferred
        )
        self.main_layout.addWidget(self.base_value_label, 0, 2, 1, 1)
        self.main_layout.addWidget(self.base_value, 0, 3, 1, 1)
        self.up_preset_label = QtWidgets.QLabel("Up Preset")
        self.up_preset_label.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Preferred
        )
        self.main_layout.addWidget(self.up_preset_label, 0, 4, 1, 1)
        self.main_layout.addWidget(self.up_preset, 0, 5, 1, 1)
        for i in range(len(self.down_widgets)):
            self.down_widgets[i][0].setText(f"DOWN{i}")
            self.down_widgets[i][0].setSizePolicy(
                QtWidgets.QSizePolicy.Policy.Maximum,
                QtWidgets.QSizePolicy.Policy.Preferred,
            )
            self.down_widgets[i][1].setValue(self.base_value.value())
            self.edit_args(i, self.base_value.value())
            self.down_widgets[i][1].valueChanged.connect(
                lambda x, index=i: self.edit_args(index, x)
            )
            self.main_layout.addWidget(self.down_widgets[i][0], i + 1, 0, 1, 1)
            self.main_layout.addWidget(self.down_widgets[i][1], i + 1, 1, 1, 1)
        self.mid_widget[0].setText("MID")
        self.mid_widget[0].setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Preferred
        )
        self.mid_widget[1].setValue(self.base_value.value())
        self.edit_args(12, self.base_value.value())
        self.mid_widget[1].valueChanged.connect(lambda x: self.edit_args(12, x))
        self.main_layout.addWidget(self.mid_widget[0], 12, 2, 1, 1)
        self.main_layout.addWidget(self.mid_widget[1], 12, 3, 1, 1)
        for i in range(len(self.up_widgets)):
            self.up_widgets[i][0].setText(f"UP{i}")
            self.up_widgets[i][0].setSizePolicy(
                QtWidgets.QSizePolicy.Policy.Maximum,
                QtWidgets.QSizePolicy.Policy.Preferred,
            )
            self.up_widgets[i][1].setValue(self.base_value.value())
            self.edit_args(i + 13, self.base_value.value())
            self.up_widgets[i][1].valueChanged.connect(
                lambda x, index=i: self.edit_args(index + 13, x)
            )
            self.main_layout.addWidget(self.up_widgets[i][0], 12 - i, 4, 1, 1)
            self.main_layout.addWidget(self.up_widgets[i][1], 12 - i, 5, 1, 1)
        self.setLayout(self.main_layout)

    def setup_presets(self):
        try:
            with open(
                os.path.join("block_weight_presets", "block_weights_preset.json"), "r"
            ) as f:
                presets = json.load(f)
                for key in presets.keys():
                    self.up_preset.addItem(key)
                    self.down_preset.addItem(key)
                self.up_preset.activated.connect(lambda x: self.modify_values(x, False))
                self.down_preset.activated.connect(
                    lambda x: self.modify_values(x, True)
                )
                return presets
        except FileNotFoundError:
            print("Preset file not found, skipping presets...")

    @QtCore.Slot(int, object)
    def edit_args(self, index: int, value: Union[int, float]):
        self.vals[index] = value
        self.edited.emit(self.vals, self.arg_name, self.enabled)

    @QtCore.Slot(object)
    def update_base_value(self, value: Union[int, float]):
        self.base_value.setValue(value)

    @QtCore.Slot(int, bool)
    def modify_values(self, index: int, down: bool):
        value = f"{'down' if down else 'up'}_lr_weight"
        values = [
            (
                int(s * self.base_value.value())
                if self.mode == "int"
                else s * self.base_value.value()
            )
            for s in self.presets[self.up_preset.itemText(index)][value]
        ]
        for i, val in enumerate(self.down_widgets if down else self.up_widgets):
            val[1].setValue(values[i])
            self.edit_args(i + (0 if down else 13), val[1].value())

    def enable_disable(self, checked: bool) -> None:
        self.enabled = checked
        self.edited.emit(self.vals, self.arg_name, self.enabled)

    def update_vals(self, new_vals: list[int] | list[float]) -> None:
        for i, down_val in enumerate(new_vals[:12]):
            self.down_widgets[i][1].setValue(down_val)
        self.mid_widget[1].setValue(new_vals[12])
        for i, up_val in enumerate(new_vals[13:]):
            self.up_widgets[i][1].setValue(up_val)
        for i, val in enumerate(new_vals):
            self.vals[i] = val
        self.enable_disable(True)


class BlockWeightWidget(BlockWidget):
    edited = QtCore.Signal(dict, bool)

    def __init__(self, parent: QtWidgets.QWidget = None):
        super(BlockWeightWidget, self).__init__(parent, "float")
        self.vals = {
            "down_lr_weight": [1.0 for _ in range(12)],
            "mid_lr_weight": 1.0,
            "up_lr_weight": [1.0 for _ in range(12)],
        }
        self.base_value.setVisible(False)
        self.base_value_label.setVisible(False)
        self.base_value.setValue(1)
        for i, elem in enumerate(self.up_widgets):
            elem[1].setValue(1)
            elem[1].valueChanged.disconnect()
            elem[1].valueChanged.connect(
                lambda x, index=i: self.edit_args(index, x, "up_lr_weight")
            )
        self.mid_widget[1].setValue(1)
        self.mid_widget[1].valueChanged.disconnect()
        self.mid_widget[1].valueChanged.connect(
            lambda x: self.edit_args(12, x, "mid_lr_weight")
        )
        for i, elem in enumerate(self.down_widgets):
            elem[1].setValue(1)
            elem[1].valueChanged.disconnect()
            elem[1].valueChanged.connect(
                lambda x, index=i: self.edit_args(index, x, "down_lr_weight")
            )

    @QtCore.Slot(int, object, str)
    def edit_args(self, index: int, value: Union[int, float], section: str = None):
        if section is None:
            return
        if section == "mid_lr_weight":
            self.vals[section] = value
            return
        self.vals[section][index] = value
        self.edited.emit(self.vals, self.enabled)

    def enable_disable(self, checked: bool) -> None:
        self.enabled = checked
        self.edited.emit(self.vals, self.enabled)

    def update_vals(
        self, down_vals: list[float], mid_val: float, up_vals: list[float]
    ) -> None:
        for i, down_val in enumerate(down_vals):
            self.down_widgets[i][1].setValue(down_val)
        self.mid_widget[1].setValue(mid_val)
        for i, up_val in enumerate(up_vals):
            self.up_widgets[i][1].setValue(up_val)
        for i, val in enumerate(down_vals):
            self.vals["down_lr_weight"][i] = val
        self.vals["mid_lr_weight"] = val
        for i, val in enumerate(up_vals):
            self.vals["up_lr_weight"][i] = val
        self.enable_disable(True)

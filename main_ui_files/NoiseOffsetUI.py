from typing import Union
from PySide6 import QtWidgets, QtCore
from modules.CollapsibleWidget import CollapsibleWidget
from ui_files.NoiseOffsetUI import Ui_noise_offset_UI


class NoiseOffsetWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super(NoiseOffsetWidget, self).__init__(parent)

        self.args = {}
        self.name = "noise_args"
        self.colap = CollapsibleWidget(self, "Noise Offset Args")
        self.content = QtWidgets.QWidget()
        self.widget = Ui_noise_offset_UI()
        self.widget.setupUi(self.content)
        self.widget.pyramid_discount_input.setEnabled(False)
        self.widget.pyramid_iteration_input.setEnabled(False)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(self.colap)
        self.layout().setContentsMargins(9, 0, 9, 0)
        self.colap.add_widget(self.content, "main_widget")

        self.widget.noise_offset_group.clicked.connect(self.enable_disable)
        self.widget.noise_offset_selector.currentIndexChanged.connect(self.swap_mode)
        self.widget.noise_offset_input.textChanged.connect(
            lambda x: self.edit_args("noise_offset", x)
        )
        self.widget.pyramid_iteration_input.valueChanged.connect(
            lambda x: self.edit_args("multires_noise_iterations", x, sig_digits=2)
        )
        self.widget.pyramid_discount_input.valueChanged.connect(
            lambda x: self.edit_args("multires_noise_discount", x, sig_digits=2)
        )

    @QtCore.Slot(str, object, int)
    def edit_args(self, name: str, value: object, sig_digits: int = -1) -> None:
        if name in self.args:
            del self.args[name]
        try:
            value = int(value) if sig_digits == 0 else float(value)
            if sig_digits > 0:
                value = round(value, sig_digits)
        except Exception:
            value = 0

        if not value or value == 0:
            return
        self.args[name] = value

    @QtCore.Slot(int)
    def swap_mode(self, index: int) -> None:
        self.args = {}
        self.widget.noise_offset_input.setEnabled(not index)
        self.widget.pyramid_discount_input.setEnabled(bool(index))
        self.widget.pyramid_iteration_input.setEnabled(bool(index))
        self.edit_args(
            "noise_offset",
            None if index else self.widget.noise_offset_input.text(),
        )
        self.edit_args(
            "multires_noise_iterations",
            self.widget.pyramid_iteration_input.value() if index else None,
            sig_digits=0,
        )
        self.edit_args(
            "multires_noise_discount",
            self.widget.pyramid_discount_input.value() if index else None,
            sig_digits=2,
        )

    @QtCore.Slot(bool)
    def enable_disable(self, checked: bool) -> None:
        self.args = {}
        if checked:
            self.swap_mode(self.widget.noise_offset_selector.currentIndex())

    def get_args(self, input_args: dict) -> None:
        if "noise_args" in input_args:
            del input_args["noise_args"]
        if not self.widget.noise_offset_group.isChecked():
            return
        input_args["noise_args"] = self.args

    def get_dataset_args(self, _: dict) -> None:
        pass

    def load_args(self, args: dict) -> None:
        self.widget.noise_offset_group.setChecked(False)
        self.enable_disable(False)
        if self.name not in args:
            return
        args = args[self.name].get("args", None)
        if not args:
            return
        self.widget.noise_offset_input.setText(str(args.get("noise_offset", "0.1")))
        self.widget.pyramid_iteration_input.setValue(
            args.get("multires_noise_iterations", 6)
        )
        self.widget.pyramid_discount_input.setValue(
            args.get("multires_noise_discount", 0.3)
        )
        self.widget.noise_offset_selector.setCurrentIndex(
            1 if "multires_noise_discount" in args else 0
        )
        checked = "noise_offset" in args or "multires_noise_discount" in args
        self.widget.noise_offset_group.setChecked(checked)
        self.enable_disable(checked)

    def save_args(self) -> Union[dict, None]:
        return self.args

    def save_dataset_args(self) -> Union[dict, None]:
        pass

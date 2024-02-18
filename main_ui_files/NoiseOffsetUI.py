from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget
from ui_files.NoiseOffsetUI import Ui_noise_offset_UI
from modules.BaseWidget import BaseWidget


class NoiseOffsetWidget(BaseWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.colap.set_title("Noise Offset Args")
        self.widget = Ui_noise_offset_UI()

        self.name = "noise_args"

        self.setup_widget()
        self.setup_connections()

    def setup_widget(self) -> None:
        super().setup_widget()
        self.widget.setupUi(self.content)
        self.widget.pyramid_iteration_input.setEnabled(False)
        self.widget.pyramid_discount_input.setEnabled(False)

    def setup_connections(self) -> None:
        self.widget.noise_offset_group.clicked.connect(self.enable_disable)
        self.widget.noise_offset_selector.currentIndexChanged.connect(self.swap_mode)
        self.widget.noise_offset_input.textChanged.connect(
            lambda x: self.edit_args("noise_offset", x, True)
        )
        self.widget.pyramid_iteration_input.valueChanged.connect(
            lambda x: self.edit_args("multires_noise_iterations", x, True)
        )
        self.widget.pyramid_discount_input.valueChanged.connect(
            lambda x: self.edit_args("multires_noise_discount", round(x, 2), True)
        )

    def edit_args(self, name: str, value: object, optional: bool = False) -> None:
        if isinstance(value, str):
            try:
                value = float(value)
            except ValueError:
                return super().edit_args(name, 0, optional)
        return super().edit_args(name, value, optional)

    @Slot(bool)
    def enable_disable(self, checked: bool) -> None:
        self.args = {}
        if not checked:
            return
        if self.widget.noise_offset_selector.currentIndex() == 0:
            self.edit_args("noise_offset", self.widget.noise_offset_input.text(), True)
            return
        self.edit_args(
            "multires_noise_iterations",
            self.widget.pyramid_iteration_input.value(),
            True,
        )
        self.edit_args(
            "multires_noise_discount",
            round(self.widget.pyramid_discount_input.value(), 2),
            True,
        )

    @Slot(int)
    def swap_mode(self, index: int) -> None:
        self.widget.noise_offset_input.setEnabled(not index)
        self.widget.pyramid_discount_input.setEnabled(bool(index))
        self.widget.pyramid_iteration_input.setEnabled(bool(index))
        self.enable_disable(True)

    def load_args(self, args: dict) -> bool:
        if not super().load_args(args):
            self.widget.noise_offset_group.setChecked(False)
            self.enable_disable(False)
            return False

        args = args[self.name]

        # update element inputs
        self.widget.noise_offset_group.setChecked(True)
        self.widget.noise_offset_selector.setCurrentIndex(
            0 if args.get("noise_offset", None) else 1
        )
        self.widget.noise_offset_input.setText(str(args.get("noise_offset", "0.1")))
        self.widget.pyramid_iteration_input.setValue(
            args.get("multires_noise_iterations", 6)
        )
        self.widget.pyramid_discount_input.setValue(
            args.get("multires_noise_discount", 0.3)
        )

        # edit args to match
        self.enable_disable(True)
        return True

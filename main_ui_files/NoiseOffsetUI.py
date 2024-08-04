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

    def setup_connections(self) -> None:
        self.widget.noise_offset_enable.clicked.connect(
            self.enable_disable_noise_offset
        )
        self.widget.noise_offset_input.textChanged.connect(
            lambda x: self.edit_args("noise_offset", x, True)
        )
        self.widget.pyramid_noise_enable.clicked.connect(
            self.enable_disable_pyramid_noise
        )
        self.widget.pyramid_iteration_input.valueChanged.connect(
            lambda x: self.edit_args("multires_noise_iterations", x, True)
        )
        self.widget.pyramid_discount_input.valueChanged.connect(
            lambda x: self.edit_args("multires_noise_discount", round(x, 4), True)
        )

    def edit_args(self, name: str, value: object, optional: bool = False) -> None:
        if isinstance(value, str):
            try:
                value = float(value)
            except ValueError:
                return super().edit_args(name, 0, optional)
        return super().edit_args(name, value, optional)

    def enable_disable_noise_offset(self, toggle: bool) -> None:
        if "noise_offset" in self.args:
            del self.args["noise_offset"]
        self.widget.noise_offset_input.setEnabled(toggle)
        if not toggle:
            return
        self.edit_args("noise_offset", self.widget.noise_offset_input.text(), True)

    def enable_disable_pyramid_noise(self, toggle: bool) -> None:
        args = ["multires_noise_iterations", "multires_noise_discount"]
        for arg in args:
            if arg in self.args:
                del self.args[arg]
        self.widget.pyramid_iteration_input.setEnabled(toggle)
        self.widget.pyramid_discount_input.setEnabled(toggle)
        if not toggle:
            return
        self.edit_args(
            "multires_noise_iterations",
            self.widget.pyramid_iteration_input.value(),
            True,
        )
        self.edit_args(
            "multires_noise_discount",
            round(self.widget.pyramid_discount_input.value(), 4),
            True,
        )

    def load_args(self, args: dict) -> bool:
        args: dict = args.get(self.name, {})

        # update element inputs
        self.widget.noise_offset_enable.setChecked(
            bool(args.get("noise_offset", False))
        )
        self.widget.noise_offset_input.setText(str(args.get("noise_offset", 0.1)))
        self.widget.pyramid_noise_enable.setChecked(
            bool(args.get("multires_noise_iterations", False))
        )
        self.widget.pyramid_iteration_input.setValue(
            args.get("multires_noise_iterations", 6)
        )
        self.widget.pyramid_discount_input.setValue(
            args.get("multires_noise_discount", 0.3)
        )

        # edit args to match
        self.enable_disable_noise_offset(self.widget.noise_offset_enable.isChecked())
        self.enable_disable_pyramid_noise(self.widget.pyramid_noise_enable.isChecked())
        return True

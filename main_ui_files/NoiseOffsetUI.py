from PySide6 import QtCore, QtWidgets
from modules.CollapsibleWidget import CollapsibleWidget
from ui_files.NoiseOffsetUI import Ui_noise_offset_UI


class NoiseOffsetWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget = None):
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

        self.widget.noise_offset_selector.currentIndexChanged.connect(self.pyramid_switch)
        self.widget.noise_offset_input.valueChanged.connect(lambda x: self.edit_args("noise_offset", round(x, 2)))
        self.widget.pyramid_discount_input.valueChanged.connect(lambda x: self.edit_args("multires_noise_discount",
                                                                                         round(x, 2)))
        self.widget.pyramid_iteration_input.valueChanged.connect(lambda x: self.edit_args("multires_noise_iterations",
                                                                                          x))
        self.widget.noise_offset_group.clicked.connect(self.enable_disable)

    @QtCore.Slot(int)
    def pyramid_switch(self, index: int):
        if index == 0:
            self.widget.pyramid_discount_input.setEnabled(False)
            self.widget.pyramid_iteration_input.setEnabled(False)
            self.widget.noise_offset_input.setEnabled(True)
            self.args = {"noise_offset": self.widget.noise_offset_input.value()}
        else:
            self.widget.noise_offset_input.setEnabled(False)
            self.widget.pyramid_iteration_input.setEnabled(True)
            self.widget.pyramid_discount_input.setEnabled(True)
            self.args = {"multires_noise_iterations": self.widget.pyramid_iteration_input.value(),
                         "multires_noise_discount": self.widget.pyramid_discount_input.value()}

    @QtCore.Slot(str, object)
    def edit_args(self, name: str, value: object):
        self.args[name] = value

    @QtCore.Slot()
    def enable_disable(self):
        checked = self.widget.noise_offset_group.isChecked()
        if not checked:
            self.args = {}
        else:
            self.pyramid_switch(self.widget.noise_offset_selector.currentIndex())

    def get_args(self, input_args: dict):
        if not self.widget.noise_offset_group.isChecked():
            if "noise_args" in input_args:
                del input_args['noise_args']
            return
        input_args['noise_args'] = self.args

    def get_dataset_args(self, input_args: dict):
        pass

    def load_args(self, args: dict):
        if self.name not in args:
            return
        args = args[self.name].get("args", None)
        if not args:
            self.widget.noise_offset_group.setChecked(False)
            self.enable_disable()
            return
        self.widget.noise_offset_input.setValue(args.get("noise_offset", 0.1))
        self.widget.pyramid_iteration_input.setValue(args.get("multires_noise_iterations", 6))
        self.widget.pyramid_discount_input.setValue(args.get("multires_noise_discount", 0.3))
        self.widget.noise_offset_selector.setCurrentIndex(1 if "multires_noise_iterations" in args else 0)
        checked = True if "noise_offset" in args or "multires_noise_iterations" in args else False
        self.widget.noise_offset_group.setChecked(checked)
        self.enable_disable()

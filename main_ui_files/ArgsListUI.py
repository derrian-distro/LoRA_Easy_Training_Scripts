from PySide6.QtCore import Signal
from PySide6 import QtWidgets, QtCore
from main_ui_files.BucketUI import BucketWidget
from main_ui_files.GeneralUI import GeneralWidget
from main_ui_files.LoggingUI import LoggingWidget
from main_ui_files.NetworkUI import NetworkWidget
from main_ui_files.NoiseOffsetUI import NoiseOffsetWidget
from main_ui_files.OptimizerUI import OptimizerWidget
from main_ui_files.SampleUI import SampleWidget
from main_ui_files.SavingUI import SavingWidget
from modules.BaseWidget import BaseWidget


class ArgsWidget(QtWidgets.QWidget):
    sdxlChecked = Signal(bool)
    cacheLatentsChecked = Signal(bool)
    keepTokensSepChecked = Signal(bool)

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_widget = QtWidgets.QWidget()
        self.args_widget_array: list[BaseWidget] = []

        self.setup_widget()
        self.setup_args_widgets()

    def setup_widget(self) -> None:
        self.setMinimumSize(600, 300)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget.setLayout(QtWidgets.QVBoxLayout())
        self.scroll_widget.layout().setSpacing(0)
        self.scroll_widget.layout().setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.scroll_widget.layout().setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setWidget(self.scroll_widget)
        self.layout().addWidget(self.scroll_area)

    def setup_args_widgets(self) -> None:
        general_args = GeneralWidget()
        general_args.colap.toggle_collapsed()
        general_args.colap.title_frame.setChecked(True)
        general_args.sdxlChecked.connect(lambda x: self.sdxlChecked.emit(x))
        general_args.cacheLatentsChecked.connect(
            lambda x: self.cacheLatentsChecked.emit(x)
        )
        general_args.keepTokensSepChecked.connect(
            lambda x: self.keepTokensSepChecked.emit(x)
        )
        self.args_widget_array.append(general_args)
        network_widget = NetworkWidget()
        self.sdxlChecked.connect(network_widget.toggle_sdxl)
        self.args_widget_array.append(network_widget)
        self.args_widget_array.append(OptimizerWidget())
        self.args_widget_array.append(SavingWidget())
        self.args_widget_array.append(BucketWidget())
        self.args_widget_array.append(NoiseOffsetWidget())
        self.args_widget_array.append(SampleWidget())
        self.args_widget_array.append(LoggingWidget())

        for widget in self.args_widget_array:
            self.scroll_widget.layout().addWidget(widget)

    def get_args(self) -> dict:
        args = {}
        dataset_args = {}
        for widget in self.args_widget_array:
            if widget.args:
                args[widget.name] = widget.args
            if widget.dataset_args:
                dataset_args[widget.name] = widget.dataset_args
        return {"args": args, "dataset": dataset_args}

    def load_args(self, args: dict, dataset_args: dict) -> None:
        for widget in self.args_widget_array:
            widget.load_args(args)
            widget.load_dataset_args(dataset_args)

import os.path

import toml
from PySide6 import QtWidgets, QtCore

from main_ui_files import GeneralUI, OptimizerUI, NetworkUI, SavingUI, BucketUI, NoiseOffsetUI, SampleUI, LoggingUI, \
    SubDatasetUI, QueueWidget


class MainWidget(QtWidgets.QWidget):
    BeginTraining = QtCore.Signal(object, object)
    BeginQueuedTraining = QtCore.Signal(object)

    def __init__(self, parent: QtWidgets.QWidget = None):
        super(MainWidget, self).__init__(parent)
        self.main_layout = QtWidgets.QGridLayout()
        self.setLayout(self.main_layout)

        self.args_widget = ArgsWidget()
        self.subset_widget = SubDatasetUI.SubDatasetWidget()
        self.subset_widget.add_empty_subset("subset 1")

        self.args = {}
        self.dataset_args = {}

        self.middle_divider = QtWidgets.QFrame()
        self.middle_divider.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.middle_divider.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)

        self.queue_widget = QueueWidget.QueueWidget()
        self.queue_widget.saveQueue.connect(self.save_for_queue)
        self.queue_widget.loadQueue.connect(self.load_for_queue)
        self.begin_training_button = QtWidgets.QPushButton("Start Training")
        self.begin_training_button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                 QtWidgets.QSizePolicy.Policy.Minimum)

        self.main_layout.addWidget(self.args_widget, 0, 0, 1, 1)
        self.main_layout.addWidget(self.middle_divider, 0, 1, 1, 1)
        self.main_layout.addWidget(self.subset_widget, 0, 2, 1, 1)
        self.main_layout.addWidget(self.queue_widget, 1, 0, 1, 2)
        self.main_layout.addWidget(self.begin_training_button, 1, 2, 1, 1)
        self.main_layout.setColumnStretch(0, 1)
        self.main_layout.setColumnStretch(2, 1)

        self.begin_training_button.clicked.connect(self.begin_train)
        self.args_widget.general_args.CacheLatentsChecked.connect(self.subset_widget.cache_checked)

    def begin_train(self):
        if len(self.queue_widget.elements) > 0:
            self.BeginQueuedTraining.emit(self.queue_widget.elements)
            return
        args = self.args_widget.collate_args()
        self.args = args[0].copy()
        self.dataset_args = args[1].copy()
        self.dataset_args['subsets'] = self.subset_widget.get_subset_args()
        self.BeginTraining.emit(self.args, self.dataset_args)

    def save_args(self):
        args = self.args_widget.save_args()
        args['subsets'] = self.subset_widget.get_subset_args(skip_check=True)
        return args

    def load_args(self, args: dict):
        self.args_widget.load_args(args)
        self.subset_widget.load_args(args)

    @QtCore.Slot(str)
    def save_for_queue(self, file_name: str):
        file_name = f"{file_name}.toml"
        args = self.args_widget.save_args()
        args['subsets'] = self.subset_widget.get_subset_args(skip_check=True)
        args = toml.dumps(args)
        with open(os.path.join("runtime_store", file_name), 'w') as f:
            f.write(args)

    @QtCore.Slot(str)
    def load_for_queue(self, file_name: str):
        file_name = f"{file_name}.toml"
        if not os.path.exists(os.path.join("runtime_store", file_name)):
            return
        with open(os.path.join("runtime_store", file_name)) as f:
            args = toml.load(f)
            self.load_args(args)


class ArgsWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget = None):
        super(ArgsWidget, self).__init__(parent)
        # setup default values
        self.setMinimumSize(600, 300)
        self.setLayout(QtWidgets.QVBoxLayout())

        # setup scroll area for the widget
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_area.setWidget(self.scroll_widget)
        self.layout().addWidget(self.scroll_area)

        # setup layout stuff for scroll_widget
        self.scroll_widget.setLayout(QtWidgets.QVBoxLayout())
        self.scroll_widget.layout().setSpacing(0)
        self.scroll_widget.layout().setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.scroll_widget.layout().setContentsMargins(0, 0, 0, 0)

        self.args_widget_array = []

        # add base_args
        self.general_args = GeneralUI.BaseArgsWidget()
        self.general_args.colap.toggle_collapsed()
        self.general_args.colap.title_frame.setChecked(True)
        self.args_widget_array.append(self.general_args)

        # add the rest of the args widgets
        self.network_args = NetworkUI.NetworkWidget()
        self.args_widget_array.append(self.network_args)
        self.optimizer_args = OptimizerUI.OptimizerWidget()
        self.args_widget_array.append(self.optimizer_args)
        self.saving_args = SavingUI.SavingWidget()
        self.args_widget_array.append(self.saving_args)
        self.bucket_args = BucketUI.BucketWidget()
        self.args_widget_array.append(self.bucket_args)
        self.noise_args = NoiseOffsetUI.NoiseOffsetWidget()
        self.args_widget_array.append(self.noise_args)
        self.sample_args = SampleUI.SampleWidget()
        self.args_widget_array.append(self.sample_args)
        self.logging_args = LoggingUI.LoggingWidget()
        self.args_widget_array.append(self.logging_args)

        # set all args widgets into layout
        for widget in self.args_widget_array:
            self.scroll_widget.layout().addWidget(widget)

    def collate_args(self):
        args = {}
        dataset_args = {}
        for widget in self.args_widget_array:
            widget.get_args(args)
            widget.get_dataset_args(dataset_args)
        return args, dataset_args

    def save_args(self):
        args = {}
        for widget in self.args_widget_array:
            widget_args = getattr(widget, "args", None)
            widget_dataset_args = getattr(widget, "dataset_args", None)
            args[widget.name] = {}
            if widget_args:
                args[widget.name]['args'] = widget_args.copy()
            if widget_dataset_args:
                args[widget.name]['dataset_args'] = widget_dataset_args.copy()
        return args

    def load_args(self, args: dict):
        for widget in self.args_widget_array:
            if hasattr(widget, "load_args"):
                widget.load_args(args)

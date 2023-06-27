import os.path
import subprocess
import sys
import threading
from PySide6 import QtWidgets, QtCore
from main_ui_files import GeneralUI, OptimizerUI, NetworkUI, SavingUI, BucketUI, NoiseOffsetUI, SampleUI, LoggingUI, \
    SubDatasetUI, QueueWidget
from modules import TomlFunctions, validator


class MainWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super(MainWidget, self).__init__(parent)
        self.main_layout = QtWidgets.QGridLayout()
        self.setLayout(self.main_layout)

        self.args_widget = ArgsWidget()
        self.subset_widget = SubDatasetUI.SubDatasetWidget()
        self.subset_widget.add_empty_subset("subset 1")

        self.args = {}
        self.dataset_args = {}
        self.training_thread = None

        self.middle_divider = QtWidgets.QFrame()
        self.middle_divider.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.middle_divider.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)

        self.queue_widget = QueueWidget.QueueWidget()
        self.queue_widget.saveQueue.connect(self.save_toml)
        self.queue_widget.loadQueue.connect(self.load_toml)
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

    @QtCore.Slot()
    def begin_train(self) -> None:
        if self.training_thread and self.training_thread.is_alive():
            return
        self.training_thread = threading.Thread(target=self.train_thread)
        self.training_thread.start()

    def validate_args(self) -> bool:
        args, dataset_args = self.args_widget.collate_args()
        dataset_args['subsets'] = self.subset_widget.get_subset_args()
        self.training_thread = threading.Thread(target=self.train_thread)
        args = validator.validate_args(args)
        dataset_args = validator.validate_dataset_args(dataset_args)
        if not args or not dataset_args:
            print("failed validation")
            return False
        validator.validate_restarts(args, dataset_args)
        validator.validate_warmup_ratio(args, dataset_args)
        validator.validate_save_tags(args, dataset_args)
        if "save_toml" in args:
            del args['save_toml']
            TomlFunctions.save_toml(self.save_args(), os.path.join(args['output_dir'],
                                                                   f"auto_save_{args.get('output_name', 'last')}.toml"))
        self.create_config_args_file(args)
        self.create_dataset_args_file(dataset_args)
        print("validated, starting training...")
        return True

    def train_thread(self):
        self.begin_training_button.setEnabled(False)
        python = sys.executable
        if len(self.queue_widget.elements) == 0:
            if not self.validate_args():
                self.begin_training_button.setEnabled(True)
                return
            try:
                subprocess.check_call([python, os.path.join("sd_scripts", "train_network.py"),
                                       f"--config_file={os.path.join('runtime_store', 'config.toml')}",
                                       f"--dataset_config={os.path.join('runtime_store', 'dataset.toml')}"])
            except subprocess.SubprocessError as e:
                print(f"Failed to train because of error:\n{e}")
            files = [os.path.join("runtime_store", "config.toml"), os.path.join("runtime_store", "dataset.toml")]
            for file in files:
                try:
                    os.remove(file)
                except FileNotFoundError:
                    pass
            self.begin_training_button.setEnabled(True)
            return
        while len(self.queue_widget.elements) > 0:
            try:
                file = os.path.join("runtime_store", f"{self.queue_widget.elements[0].queue_file}.toml")
                self.queue_widget.remove_first_from_queue()
                base_args = TomlFunctions.load_toml(file)
                args, dataset_args = validator.separate_and_validate(base_args)
                if not args or not dataset_args:
                    print("some args are not valid, skipping.")
                    continue
                validator.validate_restarts(args, dataset_args)
                validator.validate_warmup_ratio(args, dataset_args)
                validator.validate_save_tags(args, dataset_args)
                if "save_toml" in args:
                    del args['save_toml']
                    TomlFunctions.save_toml(base_args, os.path.join(args['output_dir'],
                                                                    f"auto_save_{args.get('output_name', 'last')}.toml"))
                self.create_config_args_file(args)
                self.create_dataset_args_file(dataset_args)
                print("validated, starting training...")
                subprocess.check_call([python, os.path.join("sd_scripts", "train_network.py"),
                                       f"--config_file={os.path.join('runtime_store', 'config.toml')}",
                                       f"--dataset_config={os.path.join('runtime_store', 'dataset.toml')}"])
            except BaseException as e:
                if not isinstance(e, subprocess.SubprocessError):
                    print(f"Failed to train because of error:\n{e}")
        for file in os.listdir("runtime_store"):
            if file != '.gitignore':
                os.remove(os.path.join("runtime_store", file))
        self.begin_training_button.setEnabled(True)

    def save_args(self) -> dict:
        args = self.args_widget.save_args()
        args['subsets'] = self.subset_widget.get_subset_args(skip_check=True)
        return args

    def load_args(self, args: dict) -> None:
        self.args_widget.load_args(args)
        self.subset_widget.load_args(args)

    @QtCore.Slot(str)
    def save_toml(self, file_name: str = None) -> None:
        args = self.save_args()
        if file_name:
            TomlFunctions.save_toml(args, os.path.join("runtime_store", f"{file_name}.toml"))
        else:
            TomlFunctions.save_toml(args)

    @QtCore.Slot(str)
    def load_toml(self, file_name: str = None) -> None:
        if file_name:
            args = TomlFunctions.load_toml(os.path.join("runtime_store", f"{file_name}.toml"))
        else:
            args = TomlFunctions.load_toml()
        if not args:
            return
        self.load_args(args)

    @staticmethod
    def create_config_args_file(args: dict) -> None:
        with open(os.path.join("runtime_store", "config.toml"), 'w') as f:
            for key, value in args.items():
                if isinstance(value, str):
                    value = f"\'{value}\'"
                if isinstance(value, bool):
                    value = f"{value}".lower()
                f.write(f"{key} = {value}\n")

    @staticmethod
    def create_dataset_args_file(args: dict) -> None:
        with open(os.path.join("runtime_store", "dataset.toml"), 'w') as f:
            f.write("[general]\n")
            for key, value in args['general'].items():
                if isinstance(value, str):
                    value = f"\'{value}\'"
                if isinstance(value, bool):
                    value = f"{value}".lower()
                f.write(f"{key} = {value}\n")
            f.write("\n[[datasets]]\n")
            for subset in args['subsets']:
                f.write("\n\t[[datasets.subsets]]\n")
                for key, value in subset.items():
                    if isinstance(value, str):
                        value = f"\'{value}\'"
                    if isinstance(value, bool):
                        value = f"{value}".lower()
                    f.write(f"\t{key} = {value}\n")


class ArgsWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
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

    def collate_args(self) -> tuple[dict, dict]:
        args = {}
        dataset_args = {}
        for widget in self.args_widget_array:
            widget.get_args(args)
            widget.get_dataset_args(dataset_args)
        return args, dataset_args

    def save_args(self) -> dict:
        args = {}
        for widget in self.args_widget_array:
            widget_args = widget.save_args()
            widget_dataset_args = widget.save_dataset_args()
            args[widget.name] = {}
            if widget_args:
                args[widget.name]['args'] = widget_args.copy()
            if widget_dataset_args:
                args[widget.name]['dataset_args'] = widget_dataset_args.copy()
        return args

    def load_args(self, args: dict) -> None:
        for widget in self.args_widget_array:
            if hasattr(widget, "load_args"):
                widget.load_args(args)

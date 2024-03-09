import contextlib
import json
import os
from PySide6 import QtWidgets
from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton
from main_ui_files.ArgsListUI import ArgsWidget
from main_ui_files.SubsetListUI import SubsetListWidget
from modules import ScrollOnSelect, TomlFunctions
from modules.LineEditHighlight import LineEditWithHighlight
from main_ui_files.QueueUI import QueueWidget
from pathlib import Path
from threading import Thread
import requests
from requests.exceptions import ConnectionError
from time import sleep
import shutil


class MainWidget(QWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.training_thread = None
        self.main_layout = QGridLayout()
        self.args_widget = ArgsWidget()
        self.subset_widget = SubsetListWidget()
        self.queue_widget = QueueWidget()
        self.begin_training_button = QPushButton("Start Training")
        self.backend_url_input = LineEditWithHighlight()
        self.tab_widget = ScrollOnSelect.TabView()

        self.setup_widget()
        self.setup_connections()

    def setup_widget(self) -> None:
        self.setLayout(self.main_layout)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.subset_widget.add_empty_subset("subset 1")
        config = Path("config.json")
        config_dict = json.loads(config.read_text()) if config.exists() else {}
        self.backend_url_input.setText(
            config_dict.get("backend_url", "http://127.0.0.1:8000")
        )
        self.backend_url_input.setPlaceholderText("Backend Server URL")
        self.tab_widget.addTab(self.args_widget, "Main Args")
        self.tab_widget.addTab(self.subset_widget, "Subset Args")

        self.main_layout.addWidget(self.tab_widget, 0, 0, 4, 1)
        self.main_layout.addWidget(self.queue_widget, 0, 1, 2, 1)
        self.main_layout.addWidget(self.backend_url_input, 2, 1, 1, 1)
        self.main_layout.addWidget(self.begin_training_button, 3, 1, 1, 1)
        self.queue_widget.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum
        )
        self.backend_url_input.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        self.begin_training_button.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Maximum
        )

    def setup_connections(self) -> None:
        self.args_widget.cacheLatentsChecked.connect(
            self.subset_widget.enable_disable_cache_latents
        )
        self.args_widget.keepTokensSepChecked.connect(
            self.subset_widget.enable_disable_variable_keep_tokens
        )
        self.queue_widget.saveQueue.connect(lambda x: self.save_toml(Path(x)))
        self.queue_widget.loadQueue.connect(lambda x: self.load_toml(Path(x)))
        self.begin_training_button.clicked.connect(self.start_training)
        self.backend_url_input.editingFinished.connect(self.update_url)

    def update_url(self) -> None:
        url = self.backend_url_input.text()
        if url.endswith("/"):
            self.backend_url_input.setText(url.strip("/"))
            url = url.strip("/")
        config = Path("config.json")
        config_dict = json.loads(config.read_text()) if config.exists() else {}
        config_dict["backend_url"] = url
        config.write_text(json.dumps(config_dict, indent=2))

    def get_args(self) -> tuple[dict, dict]:
        base_args = self.args_widget.get_args()
        subset_args = self.subset_widget.dataset_args
        return base_args, subset_args

    def save_toml(self, file_name: Path | None = None) -> None:
        args, subset_args = self.get_args()
        new_args = {arg: {"args": val} for arg, val in args["args"].items()}
        for arg, val in args["dataset"].items():
            if arg in new_args:
                new_args[arg]["dataset_args"] = val
            else:
                new_args[arg] = {"dataset_args": val}
        new_args["subsets"] = list(subset_args.values())
        TomlFunctions.save_toml(new_args, file_name)

    def load_toml(self, file_name: Path | None = None) -> None:
        args, dataset_args = self.process_toml(file_name)
        if not args and not dataset_args:
            return
        self.args_widget.load_args(args, dataset_args)
        self.subset_widget.load_dataset_args(dataset_args)

    def process_toml(self, file_name: Path | None = None) -> tuple[dict, dict]:
        loaded_args = TomlFunctions.load_toml(file_name)
        if not loaded_args:
            return {}, {}
        args = {}
        dataset_args = {}
        if "subsets" in loaded_args:
            dataset_args["subsets"] = loaded_args["subsets"]
            del loaded_args["subsets"]

        for arg, val in loaded_args.items():
            if "args" in val:
                args[arg] = val["args"]
            if "dataset_args" in val:
                dataset_args[arg] = val["dataset_args"]
        return args, dataset_args

    def start_training(self) -> None:
        if self.training_thread and self.training_thread.is_alive():
            with contextlib.suppress(Exception):
                requests.get(
                    f"{self.backend_url_input.text()}/stop_training?force=true"
                )
            self.begin_training_button.setText("Start Training")
            return
        self.training_thread = Thread(target=self.start_training_thread)
        self.training_thread.start()

    def start_training_thread(self) -> None:
        self.begin_training_button.setText("Stop Training")
        url = self.backend_url_input.text()
        if self.queue_widget.elements:
            while self.queue_widget.elements:
                queue_file = self.queue_widget.elements[0].queue_file
                is_checked = self.queue_widget.elements[0].isChecked()
                self.queue_widget.remove_first_from_queue()
                if is_checked:
                    self.save_toml(queue_file)
                if not self.train_helper(url, queue_file):
                    self.begin_training_button.setText("Start Training")
                    return
        else:
            self.save_toml(Path("queue_store/temp.toml"))
            self.train_helper(url, Path("queue_store/temp.toml"))
        self.begin_training_button.setText("Start Training")

    def train_helper(self, url: str, train_toml: Path) -> bool:
        args, dataset_args = self.process_toml(train_toml)
        final_args = {"args": args, "dataset": dataset_args}
        try:
            response = requests.post(
                f"{url}/validate", json=True, data=json.dumps(final_args)
            )
        except ConnectionError as e:
            print(e)
            return False
        if response.status_code != 200:
            print(f"Item Failed: {response.json()}")
            return False
        validation_data = response.json()
        if args.get("saving_args", {}).get("tag_occurrence", None):
            folder = args["saving_args"].get("tag_file_location", None)
            self.create_tag_file(
                validation_data.get("tags", {}),
                Path(folder) if folder else None,
                args["saving_args"].get("output_name", "output_tags"),
            )
        if args.get("saving_args", {}).get("save_toml", None):
            folder = args["saving_args"].get("save_toml_location", None)
            self.create_auto_save_toml(
                train_toml,
                Path(folder) if folder else None,
                args["saving_args"].get("output_name", "output_args"),
            )
        os.remove(train_toml)
        response = requests.get(f"{url}/train")
        training = True
        while training:
            sleep(5.0)
            try:
                response = requests.get(f"{url}/is_training")
            except Exception:
                print("Connection Failed, assuming training has stopped.")
                return False
            if response.status_code != 200:
                print("Connection Failed, assuming training has stopped.")
                return False
            response = response.json()
            if not response["training"]:
                training = False
            if response["errored"]:
                return False
        return True

    def create_tag_file(
        self,
        tags: dict,
        output_location: Path | None = None,
        output_name: str = "output_tags",
    ) -> None:
        if not tags:
            return
        if not output_location:
            output_location = Path("auto_save_store")
        if not output_location.exists():
            output_location.mkdir()
        if output_location.is_file():
            output_location = output_location.parent
        output_location = output_location.joinpath(f"{output_name}.txt")
        with output_location.open("w", encoding="utf-8") as f:
            f.write(
                "Below is a list of keywords used during the training of this model:\n"
            )
            for k, v in tags.items():
                f.write(f"[{v}] {k}\n")

    def create_auto_save_toml(
        self,
        input_toml: Path,
        output_location: Path | None = None,
        output_name: str = "output_toml",
    ):
        if not output_location:
            output_location = Path("auto_save_store")
        if not output_location.exists():
            output_location.mkdir()
        if output_location.is_file():
            output_location = output_location.parent
        output_location = output_location.joinpath(f"{output_name}.toml")
        offset = 1
        orig_name = output_location.stem
        while output_location.exists():
            output_location = output_location.with_stem(f"{orig_name}_{offset}")
            offset += 1
        shutil.copy(input_toml, output_location)

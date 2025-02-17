import json
import time
from pathlib import Path
from threading import Thread

import requests
from PySide6 import QtWidgets
from PySide6.QtGui import QIcon

from modules.BaseDialog import BaseDialog
from ui_files.LoraResizePopupUI import Ui_lora_resize_ui


class LoraResizePopup(BaseDialog):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.widget = Ui_lora_resize_ui()
        self.args = {
            "save_precision": "fp16",
            "new_rank": 4,
            "device": "cuda",
        }
        self.resize_queue = []
        self.resize_thread = None
        self.setup_widget()
        self.setup_connections()

    def setup_widget(self) -> None:
        self.widget.setupUi(self)
        self.widget.batch_input.setMode("folder")
        self.widget.batch_input.highlight = True
        self.widget.batch_selector.setIcon(QIcon(str(Path("icons/folder.svg"))))
        self.widget.model_input.setMode("file", [".ckpt", ".safetensors"])
        self.widget.model_input.highlight = True
        self.widget.model_selector.setIcon(QIcon(str(Path("icons/folder.svg"))))
        self.widget.output_folder_input.setMode("folder")
        self.widget.output_folder_selector.setIcon(QIcon(str(Path("icons/folder.svg"))))

    def setup_connections(self) -> None:
        self.widget.batch_enable.clicked.connect(self.enable_disable_batch_process)
        self.widget.batch_input.textChanged.connect(lambda x: self.edit_args("batch_process", x, True))
        self.widget.batch_selector.clicked.connect(
            lambda: self.set_folder_from_dialog(self.widget.batch_input, "Batch Process Folder")
        )
        self.widget.model_input.textChanged.connect(lambda x: self.edit_args("model", x))
        self.widget.model_selector.clicked.connect(
            lambda: self.set_file_from_dialog(self.widget.model_input, "Model To Resize", "lora files")
        )
        self.widget.save_precision_select.currentTextChanged.connect(
            lambda x: self.edit_args("save_precision", x)
        )
        self.widget.new_rank_input.valueChanged.connect(lambda x: self.edit_args("new_rank", x))
        self.widget.new_conv_enable.clicked.connect(self.enable_disable_conv_dims)
        self.widget.new_conv_rank_input.valueChanged.connect(
            lambda x: self.edit_args("new_conv_rank", x, True)
        )
        self.widget.output_folder_enable.clicked.connect(self.enable_disable_output_folder)
        self.widget.output_folder_input.textChanged.connect(
            lambda x: self.edit_args("output_folder", x, True)
        )
        self.widget.output_folder_selector.clicked.connect(
            lambda: self.set_folder_from_dialog(self.widget.output_folder_input, "Output Folder")
        )
        self.widget.output_name_enable.clicked.connect(self.enable_disable_output_name)
        self.widget.output_name_input.textChanged.connect(
            lambda x: self.edit_args("output_name", x.split(".")[0], True)
        )
        self.widget.dynamic_param_enable.clicked.connect(self.enable_disable_dynamic)
        self.widget.dynamic_param_select.currentTextChanged.connect(
            lambda x: self.edit_args("dynamic_method", x)
        )
        self.widget.dynamic_param_input.valueChanged.connect(
            lambda x: self.edit_args("dynamic_param", round(x, 4))
        )
        self.widget.use_gpu_enable.clicked.connect(
            lambda x: self.edit_args("device", "cuda" if x else False, True)
        )
        self.widget.verbose_enable.clicked.connect(lambda x: self.edit_args("verbose", x, True))
        self.widget.remove_conv_dims_enable.clicked.connect(lambda x: self.edit_args("del_conv", x, True))
        self.widget.remove_linear_dims_enable.clicked.connect(lambda x: self.edit_args("del_linear", x, True))
        self.widget.begin_resize_button.clicked.connect(self.start_resize)

    def enable_disable_batch_process(self, toggle: bool) -> None:
        self.widget.batch_input.setEnabled(toggle)
        self.widget.batch_selector.setEnabled(toggle)
        self.widget.model_input.setEnabled(not toggle)
        self.widget.model_selector.setEnabled(not toggle)
        if not toggle:
            self.edit_args("batch_process", False, True)
            return
        self.edit_args("batch_process", self.widget.batch_input.text(), True)

    def enable_disable_conv_dims(self, toggle: bool) -> None:
        if "new_conv_rank" in self.args:
            del self.args["new_conv_rank"]
        self.widget.new_conv_rank_input.setEnabled(toggle)
        if not toggle:
            return
        self.edit_args("new_conv_rank", self.widget.new_conv_rank_input.value(), True)

    def enable_disable_output_folder(self, toggle: bool) -> None:
        if "output_folder" in self.args:
            del self.args["output_folder"]
        self.widget.output_folder_input.setEnabled(toggle)
        self.widget.output_folder_selector.setEnabled(toggle)
        if not toggle:
            return
        self.edit_args("output_folder", self.widget.output_folder_input.text(), True)

    def enable_disable_output_name(self, toggle: bool) -> None:
        if "output_name" in self.args:
            del self.args["output_name"]
        self.widget.output_name_input.setEnabled(toggle)
        if not toggle:
            return
        self.edit_args("output_name", self.widget.output_name_input.text(), True)

    def enable_disable_dynamic(self, toggle: bool) -> None:
        for arg in ["dynamic_param", "dynamic_method"]:
            if arg in self.args:
                del self.args[arg]
        self.widget.dynamic_param_select.setEnabled(toggle)
        self.widget.dynamic_param_input.setEnabled(toggle)

        if not toggle:
            self.widget.new_rank_label.setText("New Rank")
            self.widget.new_conv_enable.setText("New Conv Rank")
            return
        self.widget.new_rank_label.setText("Max Rank")
        self.widget.new_conv_enable.setText("Max Conv Rank")
        self.edit_args("dynamic_method", self.widget.dynamic_param_select.currentText())
        self.edit_args("dynamic_param", round(self.widget.dynamic_param_input.value(), 4))

    def start_resize(self) -> None:
        lora_files = []

        if "batch_process" in self.args:
            batch_folder = Path(self.args["batch_process"])
            if not batch_folder.exists() or not batch_folder.is_dir():
                return
            lora_files.extend(batch_folder.glob("*.safetensors"))
            lora_files.extend(batch_folder.glob("*.ckpt"))
        elif "model" in self.args:
            lora_files.append(Path(self.args["model"]))
        else:
            return

        for lora_file in lora_files:
            output_name = self.args.get("output_name")
            prefix = output_name if "batch_process" in self.args else None
            file_args = [
                f"--save_to={self.get_output_name(prefix=prefix, output_name=output_name if "batch_process" not in self.args else None, model=lora_file)}"
            ]

            for key, value in self.args.items():
                if key in ["output_name", "output_folder", "batch_process", "model"]:
                    continue
                if value is True:
                    file_args.append(f"--{key}")
                else:
                    file_args.append(f"--{key}={value}")

            file_args.append(f"--model={lora_file.as_posix()}")
            self.resize_queue.append(file_args)

        if not self.resize_thread or not self.resize_thread.is_alive():
            self.resize_thread = Thread(target=self.process_resize_queue, daemon=True)
            self.resize_thread.start()

    def process_resize_queue(self) -> None:
        config = Path("config.json")
        config_dict = json.loads(config.read_text()) if config.exists() else {}
        url = config_dict.get("backend_url", "http://127.0.0.1:8000")

        while self.resize_queue:
            try:
                status_response = requests.get(f"{url}/is_training", timeout=5)
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    if status_data.get("training", False):
                        time.sleep(1)
                        continue
            except (ConnectionError, requests.exceptions.Timeout):
                print("Failed to check backend status")
                return

            args = self.resize_queue[0]
            if self.resize_helper(args):
                self.resize_queue.pop(0)
            else:
                print("Failed to process resize operation")
                return

    def resize_helper(self, args: str) -> bool:
        config = Path("config.json")
        config_dict = json.loads(config.read_text()) if config.exists() else {}
        url = config_dict.get("backend_url", "http://127.0.0.1:8000")
        try:
            response = requests.post(
                f"{url}/resize",
                data=json.dumps(args),
                timeout=0.05,
            )
        except ConnectionError as e:
            print(e)
            return False
        except requests.exceptions.Timeout:
            return True
        if response.status_code != 200:
            print(f"Failed to resize: {response.text}")
            return False
        return True

    def get_output_name(self, prefix: str = None, output_name: str = None, model: str = None) -> str:
        if output_name:
            name = output_name
        else:
            name = Path(model).stem
        if prefix:
            name = f"{prefix}-{name}"
        if "dynamic_method" in self.args:
            name += f"-{self.args['dynamic_method']}-{self.args['dynamic_param']}"
        if "del_linear" in self.args:
            name += "-no_linear"
        else:
            name += f"-{self.args['new_rank']}"
        if "del_conv" in self.args:
            name += "-no_conv"
        elif "new_conv_rank" in self.args:
            name += f"-{self.args['new_conv_rank']}"

        output_folder = self.args.get("output_folder", "default_output")
        return Path(output_folder).joinpath(f"{name}.safetensors").as_posix()

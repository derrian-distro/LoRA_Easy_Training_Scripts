import json
from pathlib import Path
from PySide6 import QtWidgets
from PySide6.QtGui import QIcon
import requests
from ui_files.LoraResizePopupUI import Ui_lora_resize_ui
from modules.BaseDialog import BaseDialog


class LoraResizePopup(BaseDialog):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.widget = Ui_lora_resize_ui()
        self.args = {
            "save_precision": "fp16",
            "new_rank": 4,
            "device": "cuda",
        }
        self.setup_widget()
        self.setup_connections()

    def setup_widget(self) -> None:
        self.widget.setupUi(self)
        self.widget.model_input.setMode("file", [".ckpt", ".safetensors"])
        self.widget.model_input.highlight = True
        self.widget.model_input_selector.setIcon(
            QIcon(str(Path("icons/more-horizontal.svg")))
        )
        self.widget.output_folder_input.setMode("folder")
        self.widget.output_folder_selector.setIcon(
            QIcon(str(Path("icons/more-horizontal.svg")))
        )

    def setup_connections(self) -> None:
        self.widget.model_input.textChanged.connect(
            lambda x: self.edit_args("model", x)
        )
        self.widget.model_input_selector.clicked.connect(
            lambda: self.set_file_from_dialog(
                self.widget.model_input, "Model To Resize", "lora files"
            )
        )
        self.widget.save_precision_select.currentTextChanged.connect(
            lambda x: self.edit_args("save_precision", x)
        )
        self.widget.new_rank_input.valueChanged.connect(
            lambda x: self.edit_args("new_rank", x)
        )
        self.widget.new_conv_enable.clicked.connect(self.enable_disable_conv_dims)
        self.widget.new_conv_rank_input.valueChanged.connect(
            lambda x: self.edit_args("new_conv_rank", x, True)
        )
        self.widget.output_folder_enable.clicked.connect(
            self.enable_disable_output_folder
        )
        self.widget.output_folder_input.textChanged.connect(
            lambda x: self.edit_args("output_folder", x, True)
        )
        self.widget.output_folder_selector.clicked.connect(
            lambda: self.set_folder_from_dialog(
                self.widget.output_folder_input, "Output Folder"
            )
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
        self.widget.verbose_enable.clicked.connect(
            lambda x: self.edit_args("verbose", x, True)
        )
        self.widget.remove_conv_dims_enable.clicked.connect(
            lambda x: self.edit_args("del_conv", x, True)
        )
        self.widget.remove_linear_dims_enable.clicked.connect(
            lambda x: self.edit_args("del_linear", x, True)
        )
        self.widget.begin_resize_button.clicked.connect(self.start_resize)

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
        self.edit_args(
            "dynamic_param", round(self.widget.dynamic_param_input.value(), 4)
        )

    def start_resize(self) -> None:
        if "model" not in self.args:
            return
        args = [f"--save_to={self.get_output_name()}"]
        for key, value in self.args.items():
            if key in ["output_name", "output_folder"]:
                continue
            if key == "model":
                value = Path(value).as_posix()
            if value is True:
                args.append(f"--{key}")
            else:
                args.append(f"--{key}={value}")
        self.resize_helper(args)

    def resize_helper(self, args: str) -> bool:
        config = Path("config.json")
        config_dict = (
            json.loads(config.read_text())
            if config.exists()
            else {}
        )
        try:
            response = requests.post(
                f"{config_dict.get("backend_url", "http://127.0.0.1:8000")}/resize",
                data=json.dumps(args),
                timeout=0.05,
            )
        except ConnectionError as e:
            print(e)
            return False
        except requests.exceptions.Timeout:
            return True
        if response.status_code != 200:
            print(f"Failed to resize: {response.json()}")
            return False

    def get_output_name(self) -> str:
        if "output_name" in self.args:
            name = self.args["output_name"]
        else:
            name = Path(self.args["model"]).stem
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

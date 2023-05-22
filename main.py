import os.path
import sys
import json
import toml
import subprocess
from validator import validate_args, validate_dataset_args, calculate_steps

from PySide6 import QtWidgets, QtCore, QtGui
from qt_material import apply_stylesheet, list_themes, QtStyleTools

from main_ui_files.MainWidget import MainWidget
from ui_files.MainUI import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, QtStyleTools):
    def __init__(self, app: QtWidgets.QApplication = None):
        self.app = app
        super(MainWindow, self).__init__()
        self.queue = []
        self.window_ = Ui_MainWindow()
        self.window_.setupUi(self)
        self.setMinimumSize(1450, 660)
        self.main_widget = MainWidget()
        self.setCentralWidget(self.main_widget)
        self.main_widget.BeginTraining.connect(self.begin_training)

        # setup theme actions for menu bar
        self.dark_themes, self.light_themes = self.process_themes()
        for theme in self.dark_themes:
            self.window_.dark_theme_menu.addAction(theme)
        for theme in self.light_themes:
            self.window_.light_theme_menu.addAction(theme)

        # setup theme switching
        for i in range(len(self.dark_themes)):
            self.dark_themes[i].triggered.connect(lambda x=False, index=i: self.change_theme(index, False))
        for i in range(len(self.light_themes)):
            self.light_themes[i].triggered.connect(lambda x=False, index=i: self.change_theme(index, True))

        # setup TOML saving and loading actions
        self.window_.save_toml.triggered.connect(self.save_toml)
        self.window_.load_toml.triggered.connect(self.load_toml)

    def process_themes(self):
        themes = os.listdir(os.path.join("css", "themes"))
        dark_themes = []
        light_themes = []
        for theme in themes:
            is_dark = len(theme.split("dark")) > 1
            if len(theme.split("500")) > 1:
                continue
            if is_dark:
                dark_themes.append(QtGui.QAction(theme.split("_")[1].replace(".xml", ""), self))
            else:
                light_themes.append(QtGui.QAction(theme.split("_")[1].replace(".xml", ""), self))
        return dark_themes, light_themes

    @QtCore.Slot()
    def save_toml(self):
        args = self.main_widget.save_args()
        args = toml.dumps(args)
        file_name = QtWidgets.QFileDialog().getSaveFileName(self, "Select Where to save to",
                                                            filter="Config File (*.toml)")
        print(file_name)
        if not file_name[0]:
            return
        if len(os.path.splitext(file_name[0])) > 1:
            file = file_name[0]
        else:
            file = file_name[0] + file_name[1]
        with open(file, 'w') as f:
            f.write(args)

    @QtCore.Slot()
    def load_toml(self):
        file_name, _ = QtWidgets.QFileDialog().getOpenFileName(self, "Select the config file",
                                                               filter="Config File (*.toml)")
        if not file_name:
            return
        with open(file_name, 'r') as f:
            args = toml.load(f)
        self.main_widget.load_args(args)
        print(args)

    @QtCore.Slot(int, bool)
    def change_theme(self, theme_index: int, is_light: bool) -> None:
        prefix = "light" if is_light else "dark"
        name = self.dark_themes[theme_index].text() if not is_light else self.light_themes[theme_index].text()
        apply_stylesheet(self.app, theme=os.path.join("css", "themes", f"{prefix}_{name}.xml"),
                         invert_secondary=is_light)
        if os.path.exists("config.json"):
            with open("config.json", 'r') as f:
                config = json.load(f)
            config['theme'] = {
                'location': os.path.join("css", "themes", f"{prefix}_{name}.xml"),
                'is_light': is_light
            }
            with open("config.json", 'w') as f:
                json.dump(config, f, indent=4)
        else:
            with open("config.json", 'w') as f:
                config = {"theme": {
                    "location": os.path.join("css", "themes", f"{prefix}_{name}.xml"),
                    "is_light": is_light
                }}
                json.dump(config, f, indent=4)

    @QtCore.Slot(dict, dict, bool)
    def begin_training(self, args: dict, dataset_args: dict):
        args_valid = validate_args(args)
        dataset_args_valid = validate_dataset_args(dataset_args)
        if not args_valid or not dataset_args_valid:
            print("failed validation")
            return
        if "warmup_ratio" in args_valid:
            steps = calculate_steps(dataset_args_valid['subsets'], args_valid['max_train_epochs'],
                                    dataset_args_valid['general']['batch_size']) \
                if "max_train_steps" not in args_valid else args_valid['max_train_steps']
            steps = steps * args_valid['warmup_ratio']
            del args_valid['warmup_ratio']
            args_valid['lr_warmup_steps'] = round(steps)
        self.create_config_args_file(args_valid)
        self.create_dataset_args_file(dataset_args_valid)
        print("validated, starting training...")
        python = sys.executable
        subprocess.check_call([python, os.path.join("sd_scripts", "train_network.py"),
                               f"--config_file={os.path.join('runtime_store', 'config.toml')}",
                               f"--dataset_config={os.path.join('runtime_store', 'dataset.toml')}"])
        os.remove(os.path.join("runtime_store", "config.toml"))
        os.remove(os.path.join("runtime_store", "dataset.toml"))

    @staticmethod
    def create_config_args_file(args: dict):
        with open(os.path.join("runtime_store", "config.toml"), 'w') as f:
            for key, value in args.items():
                if isinstance(value, str):
                    value = f"\'{value}\'"
                if isinstance(value, bool):
                    value = f"{value}".lower()
                f.write(f"{key} = {value}\n")

    @staticmethod
    def create_dataset_args_file(args: dict):
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

    @QtCore.Slot(dict)
    def create_config_args(self, args: dict):
        valid = validate_args(args)
        print(valid)
        if not valid:
            print("failed validation")

    @QtCore.Slot(dict)
    def create_dataset_args(self, args: dict):
        valid = validate_dataset_args(args)
        print(valid)
        if not valid:
            print("failed validation")


def main():
    if os.path.exists("config.json"):
        with open("config.json", 'r') as f:
            config = json.load(f)
            print(config)
    else:
        config = {"theme": {
            "location": os.path.join("css", "themes", "dark_teal.xml"),
            "is_light": False
        }}
        fp = open("config.json", 'w')
        json.dump(config, fp=fp, indent=4)
        fp.close()
    app = QtWidgets.QApplication(sys.argv)
    apply_stylesheet(app, theme=config['theme']['location'], invert_secondary=config['theme']['is_light'])
    window = MainWindow(app)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

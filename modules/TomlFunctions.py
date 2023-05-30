import os.path
import toml
from PySide6 import QtWidgets


def save_toml(args: dict, file: str = None):
    if not file:
        file = QtWidgets.QFileDialog().getSaveFileName(caption="Select Where to save to",
                                                       filter="Config File (*.toml)")
        if not file[0]:
            return
        if len(os.path.splitext(file[0])) > 1:
            file = file[0]
        else:
            file = file[0] + file[1]
    with open(file, 'w') as f:
        toml.dump(args, f)


def load_toml(file: str = None):
    if not file:
        file, _ = QtWidgets.QFileDialog().getOpenFileName(caption="Select the config file",
                                                          filter="Config File (*.toml)")
        if not file:
            return
    if not os.path.exists(file):
        return
    with open(file, 'r') as f:
        args = toml.load(f)
        return args

import json
import os.path
import toml
from PySide6 import QtWidgets


def save_toml(args: dict, file: str = ''):

    if os.path.exists(file) and os.path.isfile(file):
        with open(file, 'w') as f:
            toml.dump(args, f)
        return
    print(file)
    file = "" if not os.path.exists(file) else file
    file = QtWidgets.QFileDialog().getSaveFileName(caption="Select Where to save to",
                                                   filter="Config File (*.toml)", dir=file)
    if not file[0]:
        return
    if os.path.exists('config.json'):
        with open('config.json', 'r') as f:
            config = json.load(f)
        config['toml_default'] = os.path.split(file[0])[0]
        with open('config.json', 'w') as f:
            json.dump(config, f)
    if len(os.path.splitext(file[0])) > 1:
        file = file[0]
    else:
        file = file[0] + file[1]
    with open(file, 'w') as f:
        toml.dump(args, f)


def load_toml(file: str = ""):
    if os.path.exists(file) and os.path.isfile(file):
        with open(file, 'r') as f:
            args = toml.load(f)
            return args
    file = "" if not os.path.exists(file) else file
    file, _ = QtWidgets.QFileDialog().getOpenFileName(caption="Select the config file",
                                                      filter="Config File (*.toml)", dir=file)
    if not file:
        return
    if os.path.exists('config.json'):
        with open('config.json', 'r') as f:
            config = json.load(f)
        config['toml_default'] = os.path.split(file)[0]
        with open('config.json', 'w') as f:
            json.dump(config, f)
    if not os.path.exists(file):
        return
    with open(file, 'r') as f:
        return toml.load(f)

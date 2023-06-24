import os.path
import sys
import json

from PySide6 import QtWidgets
from qt_material import apply_stylesheet
from main_ui_files.MainWindow import MainWindow


def main() -> None:
    if os.path.exists("config.json"):
        with open("config.json", 'r') as f:
            config = json.load(f)
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
    app.exec()
    for file in os.listdir("runtime_store"):
        if file in ["config.toml", "dataset.toml", r".gitignore"]:
            continue
        try:
            os.remove(os.path.join("runtime_store", file))
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    main()

import os.path
import sys
import json

from PySide6 import QtWidgets
from qt_material import apply_stylesheet
from main_ui_files.MainWindow import MainWindow


def CreateConfig():
    config = {"theme": {
        "location": os.path.join("css", "themes", "dark_teal.xml"),
        "is_light": False
    }}
    fp = open("config.json", 'w')
    json.dump(config, fp=fp, indent=4)
    fp.close()
    return config
    
def main() -> None:
    if os.path.exists("config.json"):
        try:
            with open("config.json", 'r') as f:
                config = json.load(f)
        except json.decoder.JSONDecodeError as Error:
                print("Could not load config. Recreating...")
                config = CreateConfig()
    else:
        config = CreateConfig()
        
    app = QtWidgets.QApplication(sys.argv)
    apply_stylesheet(app, theme=config['theme']['location'], invert_secondary=config['theme']['is_light'])
    window = MainWindow(app)
    window.setWindowTitle('LoRA Trainer')
    window.show()
    app.exec()


if __name__ == "__main__":
    main()

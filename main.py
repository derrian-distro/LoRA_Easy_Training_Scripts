import contextlib
from pathlib import Path
import sys
import json
from threading import Thread

from PySide6 import QtWidgets
from qt_material import apply_stylesheet
import requests
from main_ui_files.MainWindow import MainWindow
import subprocess
import time


def run_backend():
    if sys.platform == "linux":
        python = Path("backend/sd_scripts/venv/bin/python")
    else:
        python = Path("backend/sd_scripts/venv/Scripts/python.exe")
    with contextlib.suppress(Exception):
        subprocess.check_call(
            f"{python} backend/main.py backend", shell=sys.platform == "linux"
        )


def CreateConfig():
    return {
        "theme": {
            "location": Path("css/themes/dark_teal.xml").as_posix(),
            "is_light": False,
        }
    }


def main() -> None:
    queue_store = Path("queue_store")
    if not queue_store.exists():
        queue_store.mkdir()
    config = Path("config.json")
    config_dict = json.loads(config.read_text()) if config.exists() else CreateConfig()
    if "theme" not in config_dict:
        config_dict.update(CreateConfig())
    config.write_text(json.dumps(config_dict, indent=2))
    backend_thread = None
    if "run_local" in config_dict and config_dict["run_local"]:
        backend_thread = Thread(target=run_backend, daemon=True)
        backend_thread.start()
    app = QtWidgets.QApplication(sys.argv)
    if config_dict["theme"]["location"]:
        apply_stylesheet(
            app,
            theme=config_dict["theme"]["location"],
            invert_secondary=config_dict["theme"]["is_light"],
        )
    window = MainWindow(app)
    window.setWindowTitle("LoRA Trainer")
    window.show()
    app.exec()
    if window.main_widget.training_thread:
        while window.main_widget.training_thread.is_alive():
            time.sleep(5.0)
    requests.get(f"{window.main_widget.backend_url_input.text()}/stop_server")


if __name__ == "__main__":
    main()

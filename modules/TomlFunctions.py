from PySide6.QtWidgets import QFileDialog
from pathlib import Path
import toml
import json


def save_toml(args: dict, file_path: Path | None = None) -> None:
    if file_path:
        file_path.write_text(toml.dumps(args))
        return
    config = Path("config.json")
    config_dict = json.loads(config.read_text()) if config.exists() else {}

    file = QFileDialog().getSaveFileName(
        caption="Select config file save location",
        filter="Config File (*.toml)",
        dir=config_dict["toml_default"] if "toml_default" in config_dict else "",
    )[0]
    if not file:
        return
    file = Path(file)
    config_dict["toml_default"] = file.parent.as_posix()
    config.write_text(json.dumps(config_dict, indent=2))
    file.write_text(toml.dumps(args))


def load_toml(file_path: Path | None = None) -> dict:
    if file_path and file_path.exists():
        return toml.loads(file_path.read_text())
    config = Path("config.json")
    config_dict = json.loads(config.read_text()) if config.exists() else {}

    file, _ = QFileDialog().getOpenFileName(
        caption="Select config file",
        filter="Config File (*.toml)",
        dir=config_dict["toml_default"] if "toml_default" in config_dict else "",
    )
    if not file:
        return
    file = Path(file)
    config_dict["toml_default"] = file.parent.as_posix()
    config.write_text(json.dumps(config_dict, indent=2))
    return toml.loads(file.read_text())

from pathlib import Path
from sys import platform
from subprocess import check_call
import json
import os


def main():
    pip = Path("venv/Scripts/pip.exe" if platform == "win32" else "venv/bin/pip")
    backend_python = Path(
        "sd_scripts/venv/Scripts/python.exe"
        if platform == "win32"
        else "sd_scripts/venv/bin/python"
    )
    check_call(f"{pip} install -U -r requirements.txt", shell=platform == "linux")
    config = Path("config.json")
    config_dict = json.loads(config.read_text()) if config.exists() else {}
    if "run_local" in config_dict and config_dict["run_local"]:
        check_call("git submodule update", shell=platform == "linux")
        os.chdir("backend")
        check_call(
            f"{backend_python} updater.py",
            shell=platform == "linux",
        )


if __name__ == "__main__":
    main()

from pathlib import Path
from sys import platform
from subprocess import check_call
import json
import os


def main():
    pip = Path("venv/Scripts/pip.exe" if platform == "win32" else "venv/bin/pip")
    check_call(f"{pip} install -U -r requirements.txt", shell=platform == "linux")
    config = Path("config.json")
    config_dict = json.loads(config.read_text()) if config.exists() else {}
    if "run_local" in config_dict and config_dict["run_local"]:
        os.chdir("backend")
        check_call(
            "update.bat" if platform == "win32" else "update.sh",
            shell=platform == "linux",
        )


if __name__ == "__main__":
    main()

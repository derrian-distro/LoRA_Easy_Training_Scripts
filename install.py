import json
from pathlib import Path
import sys
import subprocess
import os


def check_version_and_platform() -> bool:
    version = sys.version_info
    if not (
        False
        if version.major != 3 and version.minor < 10
        else sys.platform in ["win32", "linux"]
    ):
        print("ERROR: you have too old of a python version")
        return False
    return True


def check_git_install() -> None:
    try:
        subprocess.check_call(
            "git --version",
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=sys.platform == "linux",
        )
    except FileNotFoundError:
        print("ERROR: git is not installed, please install git")
        return False
    return True


def main():
    if not check_version_and_platform():
        return
    if not check_git_install():
        return
    python = sys.executable
    subprocess.check_call(f"{python} -m venv venv", shell=sys.platform == "linux")
    venv_path = Path(
        "venv/Scripts/pip.exe" if sys.platform == "win32" else "venv/bin/pip"
    )
    subprocess.check_call(
        f"{venv_path} install -r requirements.txt", shell=sys.platform == "linux"
    )

    install_backend = None
    while install_backend not in ("y", "n"):
        install_backend = input("Are you using this locally? (y/n): ").lower()
    config = Path("config.json")
    config_dict = json.loads(config.read_text()) if config.exists() else {}
    if install_backend == "n":
        config_dict["run_local"] = False
        config.write_text(json.dumps(config_dict, indent=2))
        return
    config_dict["run_local"] = True
    config.write_text(json.dumps(config_dict, indent=2))

    subprocess.check_call("git submodule init", shell=sys.platform == "linux")
    subprocess.check_call("git submodule update", shell=sys.platform == "linux")
    os.chdir(Path("backend"))
    subprocess.check_call(f"{python} installer.py", shell=sys.platform == "linux")


if __name__ == "__main__":
    main()

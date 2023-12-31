import shutil
import sys
import subprocess
import os
from pathlib import Path
from zipfile import ZipFile

try:
    import requests
except ModuleNotFoundError:
    print("installing requests...")
    python = sys.executable
    subprocess.check_call(
        [python, "-m", "pip", "install", "requests"], stdout=subprocess.DEVNULL
    )


def check_version_and_platform():
    if sys.platform != "win32":
        print("ERROR: This installer only works on windows")
        return False

    version = sys.version_info
    if version.major != 3 or version.minor != 10:
        print(
            "ERROR: You don't have python 3.10 installed, please install python 3.10, preferably 3.10.6, and add it to path"
        )
        return False
    return True


def check_git_install():
    try:
        subprocess.check_call(
            "git --version", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    except FileNotFoundError:
        print("ERROR: Git is not installed, please install git")
        return False
    return True


def set_execution_policy():
    try:
        subprocess.check_call(str(Path("installables/change_execution_policy.bat")))
    except subprocess.SubprocessError:
        try:
            subprocess.check_call(
                str(Path("installables/change_execution_policy_backup.bat"))
            )
        except subprocess.SubprocessError as e:
            print(f"Failed to change the execution policy with error:\n {e}")
            return False
    return True


def ask_10_series(venv_pip):
    reply = None
    while reply not in ("y", "n"):
        reply = input("Are you using a 10X0 series card? (y/n): ")
    if reply == "n":
        return False

    torch_version = "torch==1.12.1+cu116 torchvision==0.13.1+cu116 --extra-index-url https://download.pytorch.org/whl/cu116"
    subprocess.check_call(f"{venv_pip} install {torch_version}")
    subprocess.check_call(f"{venv_pip} install -r requirements.txt")
    subprocess.check_call(
        f"{venv_pip} install -U -I --no-deps https://github.com/C43H66N12O12S2/stable-diffusion-webui/releases/download/f/xformers-0.0.14.dev0-cp310-cp310-win_amd64.whl"
    )
    subprocess.check_call(f"{venv_pip} install -r ../requirements_ui.txt")
    subprocess.check_call(f"{venv_pip} install ../LyCORIS/.")
    subprocess.check_call(f"{venv_pip} install ../custom_scheduler/.")
    subprocess.check_call(f"{venv_pip} install bitsandbytes==0.35.0")

    shutil.copy(
        Path("../installables/libbitsandbytes_cudaall.dll"),
        Path("venv/Lib/site-packages/bitsandbytes"),
    )
    os.remove(Path("venv/Lib/site-packages/bitsandbytes/cuda_setup/main.py"))
    shutil.copy(
        Path("../installables/main.py"),
        Path("venv/Lib/site-packages/bitsandbytes/cuda_setup"),
    )
    return True


def setup_normal(venv_pip):
    torch_version = (
        "torch torchvision --index-url https://download.pytorch.org/whl/cu118"
    )
    subprocess.check_call(f"{venv_pip} install {torch_version}")
    subprocess.check_call(f"{venv_pip} install -r requirements.txt")
    subprocess.check_call(
        f"{venv_pip} install xformers --index-url https://download.pytorch.org/whl/cu118"
    )
    subprocess.check_call(f"{venv_pip} install -r ../requirements_ui.txt")
    subprocess.check_call(f"{venv_pip} install ../LyCORIS/.")
    subprocess.check_call(f"{venv_pip} install ../custom_scheduler/.")
    subprocess.check_call(
        f"{venv_pip} install https://github.com/jllllll/bitsandbytes-windows-webui/releases/download/wheels/bitsandbytes-0.41.1-py3-none-win_amd64.whl"
    )


def setup_accelerate():  # sourcery skip: extract-method
    with open("default_config.yaml", "w") as f:
        f.write("command_file: null\n")
        f.write("commands: null\n")
        f.write("compute_environment: LOCAL_MACHINE\n")
        f.write("deepspeed_config: {}\n")
        f.write("distributed_type: 'NO'\n")
        f.write("downcase_fp16: 'NO'\n")
        f.write("dynamo_backend: 'NO'\n")
        f.write("fsdp_config: {}\n")
        f.write("gpu_ids: '0'\n")
        f.write("machine_rank: 0\n")
        f.write("main_process_ip: null\n")
        f.write("main_process_port: null\n")
        f.write("main_training_function: main\n")
        f.write("megatron_lm_config: {}\n")
        f.write("mixed_precision: bf16\n")
        f.write("num_machines: 1\n")
        f.write("num_processes: 1\n")
        f.write("rdzv_backend: static\n")
        f.write("same_network: true\n")
        f.write("tpu_name: null\n")
        f.write("tpu_zone: null\n")
        f.write("use_cpu: false")
    if os.path.exists(
        os.path.join(
            os.environ["USERPROFILE"],
            ".cache",
            "huggingface",
            "accelerate",
            "default_config.yaml",
        )
    ):
        os.remove(
            os.path.join(
                os.environ["USERPROFILE"],
                ".cache",
                "huggingface",
                "accelerate",
                "default_config.yaml",
            )
        )
    shutil.move(
        "default_config.yaml",
        os.path.join(os.environ["USERPROFILE"], ".cache", "huggingface", "accelerate"),
    )


def setup_cudnn():
    reply = None
    while reply not in ("y", "n"):
        reply = input(
            "Do you want to install the optional cudnn patch for faster "
            "training on high end 30X0 and 40X0 cards? (y/n): "
        ).casefold()
    if reply == "n":
        return

    r = requests.get(
        "https://developer.download.nvidia.com/compute/redist/cudnn/v8.6.0/local_installers/11.8/cudnn-windows-x86_64-8.6.0.163_cuda11-archive.zip"
    )
    with open("cudnn.zip", "wb") as f:
        f.write(r.content)
    with ZipFile("cudnn.zip", "r") as f:
        f.extractall(path="cudnn_patch")
    shutil.move(
        "cudnn_patch\\cudnn-windows-x86_64-8.6.0.163_cuda11-archive\\bin",
        "cudnn_windows",
    )
    os.mkdir("temp")
    r = requests.get(
        "https://raw.githubusercontent.com/bmaltais/kohya_ss/9c5bdd17499e3f677a5d7fa081ee0b4fccf5fd4a/tools/cudann_1.8_install.py"
    )
    with open(os.path.join("temp", "cudnn.py"), "wb") as f:
        f.write(r.content)
    subprocess.check_call(
        f"{os.path.join('venv', 'Scripts', 'python.exe')} {os.path.join('temp', 'cudnn.py')}".split(
            " "
        )
    )
    shutil.rmtree("temp")
    shutil.rmtree("cudnn_windows")
    shutil.rmtree("cudnn_patch")
    os.remove("cudnn.zip")


def main():
    if not check_version_and_platform() or not check_git_install():
        quit()

    python_real = sys.executable
    venv_pip = r"venv\Scripts\pip.exe"

    subprocess.check_call("git submodule init")
    subprocess.check_call("git submodule update")

    print("setting execution policy to unrestricted")
    if not set_execution_policy():
        quit()

    os.chdir("sd_scripts")

    print("creating venv and installing requirements")
    subprocess.check_call([python_real, "-m", "venv", "venv"])

    if ask_10_series(venv_pip):
        setup_accelerate()
        print("Completed installing, you can launch the ui by launching run.bat")
        quit()
    setup_normal(venv_pip)
    setup_accelerate()
    setup_cudnn()

    print("Completed installing, you can launch the ui bu launching run.bat")


if __name__ == "__main__":
    main()

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

PLATFORM = "windows" if sys.platform == "win32" else "linux" if sys.platform == "linux" else ""


def check_version_and_platform() -> bool:
    version = sys.version_info
    return False if version.major != 3 and version.minor < 10 else PLATFORM != ""


def check_git_install() -> None:
    try:
        subprocess.check_call(
            "git --version",
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=PLATFORM == "linux",
        )
    except FileNotFoundError:
        print("ERROR: git is not installed, please install git")
        return False
    return True


# windows only
def set_execution_policy() -> None:
    try:
        subprocess.check_call(str(Path("installables/change_execution_policy.bat")))
    except subprocess.SubprocessError:
        try:
            subprocess.check_call(str(Path("installables/change_execution_policy_backup.bat")))
        except subprocess.SubprocessError as e:
            print(f"Failed to change the execution policy with error:\n {e}")
            return False
    return True


def setup_accelerate(platform: str) -> None:
    if platform == "windows":
        path = Path(f"{os.environ['USERPROFILE']}")
    else:
        path = Path.home()
    path = path.joinpath(".cache/huggingface/accelerate/default_config.yaml")
    if path.exists():
        print("Default accelerate config already exists, skipping.")
        return
    if not path.parent.exists():
        path.parent.mkdir(parents=True)
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

    shutil.move("default_config.yaml", str(path.resolve()))


def check_50_series_gpu():
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            check=True,
        )
        print(result.stdout)
        gpu_name = result.stdout.strip()
        if "RTX 50" in gpu_name:
            return True
        elif "NVIDIA" in gpu_name:
            return False
        else:
            return False
    except subprocess.CalledProcessError:
        print("No NVIDIA GPU detected or nvidia-smi not found.")
        return False
    except FileNotFoundError:
        print("nvidia-smi command not found. Ensure NVIDIA drivers are installed.")
        return False


def setup_venv(venv_pip):
    if check_50_series_gpu():
        subprocess.check_call(
            f"{venv_pip} install -U --pre torch torchvision --index-url https://download.pytorch.org/whl/nightly/cu128",
            shell=PLATFORM == "linux",
        )
        print("50 series GPU doesn't have xformers support!")
    else:
        subprocess.check_call(
            f"{venv_pip} install -U torch==2.6.0 torchvision==0.21.0 --index-url https://download.pytorch.org/whl/cu124",
            shell=PLATFORM == "linux",
        )

        # Skip xformers due to compatibility issues with current PyTorch version
        # Can be installed manually later if needed: pip install xformers --no-deps
    if PLATFORM == "windows":
        subprocess.check_call("venv\\Scripts\\python.exe ..\\fix_torch.py")
    # Install packages that have pre-built wheels first to avoid build issues
    subprocess.check_call(f"{venv_pip} install -U --only-binary=all schedulefree sentencepiece", shell=PLATFORM == "linux")
    subprocess.check_call(f"{venv_pip} install -U -r requirements.txt --no-deps", shell=PLATFORM == "linux")
    # Install missing dependencies
    subprocess.check_call(f"{venv_pip} install -U accelerate transformers diffusers ftfy opencv-python einops pytorch-lightning bitsandbytes lion-pytorch pytorch-optimizer prodigy-plus-schedule-free prodigyopt tensorboard safetensors altair easygui toml voluptuous huggingface-hub imagesize rich", shell=PLATFORM == "linux")
    subprocess.check_call(f"{venv_pip} install -U ../custom_scheduler/.", shell=PLATFORM == "linux")
    subprocess.check_call(f"{venv_pip} install -U -r ../requirements.txt", shell=PLATFORM == "linux")
    subprocess.check_call(f"{venv_pip} install -U ../lycoris/.", shell=PLATFORM == "linux")


# colab only
def setup_colab(venv_pip):
    setup_venv(venv_pip)
    setup_accelerate("linux")


def ask_yes_no(question: str) -> bool:
    reply = None
    while reply not in ("y", "n"):
        reply = input(f"{question} (y/n): ")
    return reply == "y"


def setup_config(colab: bool = False, local: bool = False) -> None:
    if colab:
        config = {
            "remote": True,
            "remote_mode": "cloudflared",
            "kill_tunnel_on_train_start": True,
            "kill_server_on_train_end": True,
            "colab": True,
            "port": 8000,
        }
        with open("config.json", "w") as f:
            f.write(json.dumps(config, indent=2))
        return
    is_remote = False if local else ask_yes_no("are you using this remotely?")
    remote_mode = "none"
    if is_remote:
        remote_mode = "ngrok" if ask_yes_no("do you want to use ngrok?") else "cloudflared"
    ngrok_token = ""
    if remote_mode == "ngrok":
        ngrok_token = input(
            "copy paste your token from your ngrok dashboard (https://dashboard.ngrok.com/get-started/your-authtoken) (requires account): "
        )

    with open("config.json", "w") as f:
        f.write(
            json.dumps(
                {
                    "remote": is_remote,
                    "remote_mode": remote_mode,
                    "ngrok_token": ngrok_token,
                    "port": 8000,
                },
                indent=2,
            )
        )


def main():
    if not check_version_and_platform() or not check_git_install():
        quit()

    subprocess.check_call("git submodule init", shell=PLATFORM == "linux")
    subprocess.check_call("git submodule update", shell=PLATFORM == "linux")

    if PLATFORM == "windows":
        print("setting execution policy to unrestricted")
        if not set_execution_policy():
            quit()

    setup_config(
        len(sys.argv) > 1 and sys.argv[1] == "colab",
        len(sys.argv) > 1 and sys.argv[1] == "local",
    )

    os.chdir("sd_scripts")
    if PLATFORM == "windows":
        pip = Path("venv/Scripts/pip.exe")
    else:
        pip = Path("venv/bin/pip")

    print("creating venv and installing requirements")
    subprocess.check_call(f"{sys.executable} -m venv venv", shell=PLATFORM == "linux")

    if len(sys.argv) > 1 and sys.argv[1] == "colab":
        setup_colab(pip)
        print("completed installing")
        quit()

    setup_venv(pip)
    setup_accelerate(PLATFORM)

    print("Completed installing, you can run the server via the run.bat or run.sh files")


if __name__ == "__main__":
    main()

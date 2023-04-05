import shutil
import sys
import subprocess
import os
import pkg_resources
from zipfile import ZipFile

try:
    import requests
except ModuleNotFoundError as error:
    required = {'requests'}
    installed = {p.key for p in pkg_resources.working_set}
    missing = required - installed
    if missing:
        print("installing requests...")
        python = sys.executable
        subprocess.check_call([python, "-m", "pip", "install", *missing], stdout=subprocess.DEVNULL)
        import requests


def main():
    if sys.platform != "win32":
        print("ERROR: This installer only works on Windows")
        quit()
    else:
        print("Running on windows...")

    version = sys.version_info
    if version.major != 3 or version.minor != 10 or version.micro < 6:
        print("ERROR: You don't have python 3.10 installed, please install python 3.10, preferably 3.10.6, and add it to path")
        quit()
    else:
        print("Python version 3.10 detected...")

    try:
        subprocess.check_call(['git', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("ERROR: Git is not installed, please install git")
        quit()
    print("Git is installed... installing")

    python_real = sys.executable
    python = r"venv\Scripts\pip.exe"

    print("cloning repositories")
    subprocess.check_call(['git', 'clone', 'https://github.com/derrian-distro/LoRA_Easy_Training_Scripts'])
    os.chdir("LoRA_Easy_Training_Scripts")
    subprocess.check_call(['git', 'submodule', "init"])
    subprocess.check_call(['git', 'submodule', 'update'])

    print("setting execution policy to unrestricted")
    subprocess.check_call(f"{os.path.join('installables', 'change_execution_policy.bat')}")

    os.chdir("sd_scripts")

    print("creating venv and installing requirements")
    subprocess.check_call([python_real, "-m", "venv", "venv"])

    reply = None
    while reply not in ("0", "1", "2"):
        reply = input("which version of torch do you want to install?\n"
                      "0 = 1.12.1\n"
                      "1 = 2.0.0\n"
                      "2 = 2.1.0: ").casefold()

    if reply == "2":
        torch_version = "torch==2.1.0.dev20230320+cu118 torchvision==0.16.0.dev20230320+cu118 --extra-index-url https://download.pytorch.org/whl/nightly/cu118"
    elif reply == '1':
        torch_version = "torch==2.0.0+cu118 torchvision==0.15.0+cu118 --extra-index-url https://download.pytorch.org/whl/cu118"
    else:
        torch_version = "torch==1.12.1+cu116 torchvision==0.13.1+cu116 --extra-index-url https://download.pytorch.org/whl/cu116"
    print("installing torch")
    subprocess.check_call(f"{python} install {torch_version}".split(" "))

    print("installing other requirements")
    subprocess.check_call(f"{python} install -r requirements.txt".split(" "))

    print("installing xformers")
    if reply == '2':
        xformers = "https://github.com/DDStorage/LoRA_Easy_Training_Scripts/releases/download/torch2.1.0/xformers-0.0.17+c36468d.d20230318-cp310-cp310-win_amd64.whl"
    elif reply == '1':
        xformers = "https://github.com/DDStorage/LoRA_Easy_Training_Scripts/releases/download/torch2.0.0/xformers-0.0.17+b3d75b3.d20230320-cp310-cp310-win_amd64.whl"
    else:
        xformers = "https://github.com/C43H66N12O12S2/stable-diffusion-webui/releases/download/f/xformers-0.0.14.dev0-cp310-cp310-win_amd64.whl"
    subprocess.check_call(f"{python} install -U -I --no-deps {xformers}".split(' '))
    if reply in {'1', '2'}:
        reply = None
        while reply not in ("y", "n"):
            reply = input(f"Do you want to install the triton built for torch 2?").casefold()
        if reply == 'y':
            subprocess.check_call(f"{python} install -U -I --no-deps {os.path.join('..', 'installables', 'triton-2.0.0-cp310-cp310-win_amd64.whl')}".split(" "))

    print("Setting up default config of accelerate")
    with open("default_config.yaml", 'w') as f:
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
        f.write("mixed_precision: fp16\n")
        f.write("num_machines: 1\n")
        f.write("num_processes: 1\n")
        f.write("rdzv_backend: static\n")
        f.write("same_network: true\n")
        f.write("tpu_name: null\n")
        f.write("tpu_zone: null\n")
        f.write("use_cpu: false")
    if os.path.exists(os.path.join(os.environ['USERPROFILE'], '.cache', 'huggingface',
                                   'accelerate', 'default_config.yaml')):
        os.remove(os.path.join(os.environ['USERPROFILE'], '.cache', 'huggingface', 'accelerate', 'default_config.yaml'))
    shutil.move("default_config.yaml", os.path.join(os.environ['USERPROFILE'], ".cache", "huggingface", "accelerate"))

    for file in os.listdir("bitsandbytes_windows"):
        shutil.copy(os.path.join('bitsandbytes_windows', file),
                    os.path.join('venv', 'Lib', 'site-packages', 'bitsandbytes'))
    shutil.copy(os.path.join('venv', 'Lib', 'site-packages', 'bitsandbytes', 'main.py'),
                os.path.join('venv', 'Lib', 'site-packages', 'bitsandbytes', 'cuda_setup'))

    reply = None
    while reply not in ("y", "n"):
        reply = input(f"Do you want to install the optional cudnn patch for faster "
                      f"training on high end 30X0 and 40X0 cards? (y/n): ").casefold()

    if reply == 'y':
        r = requests.get("https://b1.thefileditch.ch/mwxKTEtelILoIbMbruuM.zip")
        with open("cudnn.zip", 'wb') as f:
            f.write(r.content)
        with ZipFile("cudnn.zip", 'r') as f:
            f.extractall(path="cudnn_windows")
        os.mkdir("temp")
        r = requests.get("https://raw.githubusercontent.com/bmaltais/kohya_ss/9c5bdd17499e3f677a5d7fa081ee0b4fccf5fd4a/tools/cudann_1.8_install.py")
        with open(os.path.join('temp', 'cudnn.py'), 'wb') as f:
            f.write(r.content)
        subprocess.check_call(f"{os.path.join('venv', 'Scripts', 'python.exe')} {os.path.join('temp', 'cudnn.py')}".split(" "))
        shutil.rmtree("temp")
        shutil.rmtree("cudnn_windows")
    else:
        reply = None
        while reply not in ('y', 'n'):
            reply = input("Are you using a 10X0 series card? (y/n): ")
        if reply:
            shutil.copy(os.path.join("..", "installables", "libbitsandbytes_cudaall.dll"),
                        os.path.join("venv", 'Lib', 'site-packages', 'bitsandbytes'))
            os.remove(os.path.join('venv', 'Lib', 'site-packages', 'bitsandbytes', 'cuda_setup', 'main.py'))
            shutil.copy(os.path.join('..', 'installables', 'main.py'),
                        os.path.join('venv', 'Lib', 'site-packages', 'bitsandbytes', 'cuda_setup'))
    print("Completed installing, you can launch by using 'run_popup.bat'")


if __name__ == "__main__":
    main()

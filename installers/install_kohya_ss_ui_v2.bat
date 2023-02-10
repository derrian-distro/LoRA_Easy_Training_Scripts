@echo off

openfiles > nul 2>&1
if not %ERRORLEVEL% equ 0 goto noAdmin

reg query "hkcu\software\Python\PythonCore\3.10" > nul
if errorlevel 1 goto noPython

reg query "HKLM\software\GitForWindows" > nul
if errorlevel 1 goto noGit

echo Setting execution policy to unrestricted
Call PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& {Start-Process PowerShell -ArgumentList 'Set-ExecutionPolicy Unrestricted -Force' -Verb RunAs}"
cd /d %~dp0
echo cloning khoya_ss
git clone https://github.com/bmaltais/kohya_ss > nul
cd kohya_ss
echo creating venv for python
python -m venv venv
call venv\Scripts\activate

echo installing dependancies, this may take a while
echo installing torch
pip install torch==1.12.1+cu116 torchvision==0.13.1+cu116 --extra-index-url https://download.pytorch.org/whl/cu116 > nul

echo installing other dependancies
pip install --use-pep517 --upgrade -r requirements.txt > nul

echo installing xformers
pip install -U -I --no-deps https://github.com/C43H66N12O12S2/stable-diffusion-webui/releases/download/f/xformers-0.0.14.dev0-cp310-cp310-win_amd64.whl > nul

echo moving required bitsandbytes files
IF NOT exist venv\Lib\site-packages\bitsandbytes (mkdir venv\Lib\site-packages\bitsandbytes)
If NOT exist venv\Lib\site-packages\bitsandbytes\cuda_setup (mkdir venv\Lib\site-packages\bitsandbytes\cuda_setup)
copy bitsandbytes_windows\*.dll venv\Lib\site-packages\bitsandbytes > nul
copy bitsandbytes_windows\cextension.py venv\Lib\site-packages\bitsandbytes > nul
copy bitsandbytes_windows\main.py venv\Lib\site-packages\bitsandbytes\cuda_setup > nul

echo creating config file for accelerate
md "%USERPROFILE%\.cache\huggingface\accelerate"
echo command_file: null > default_config.yaml
echo commands: null >> default_config.yaml
echo compute_environment: LOCAL_MACHINE >> default_config.yaml
echo deepspeed_config: {} >> default_config.yaml
echo distributed_type: 'NO' >> default_config.yaml
echo downcast_bf16: 'no' >> default_config.yaml
echo dynamo_backend: 'NO' >> default_config.yaml
echo fsdp_config: {} >> default_config.yaml
echo gpu_ids: '0' >> default_config.yaml
echo machine_rank: 0 >> default_config.yaml
echo main_process_ip: null >> default_config.yaml
echo main_process_port: null >> default_config.yaml
echo main_training_function: main >> default_config.yaml
echo megatron_lm_config: {} >> default_config.yaml
echo mixed_precision: fp16 >> default_config.yaml
echo num_machines: 1 >> default_config.yaml
echo num_processes: 1 >> default_config.yaml
echo rdzv_backend: static >> default_config.yaml
echo same_network: true >> default_config.yaml
echo tpu_name: null >> default_config.yaml
echo tpu_zone: null >> default_config.yaml
echo use_cpu: false >> default_config.yaml
move default_config.yaml "%USERPROFILE%\.cache\huggingface\accelerate" > nul

echo generating lora_gui.bat for easy launching
echo @echo off > lora_gui.bat
echo call venv\Scripts\activate >> lora_gui.bat
echo python lora_gui.py >> lora_gui.bat
echo pause >> lora_gui.bat

choice /C YN /M "Do you want to install the optional cudnn1.8 for faster training on high end 30X0 and 40X0 cards?"
if ERRORLEVEL 2 goto complete

echo installing cudnn1.8 for faster training on 40X0 cards
curl "https://b1.thefileditch.ch/mwxKTEtelILoIbMbruuM.zip" -o "cudnn.zip"
Call Powershell Expand-Archive "cudnn.zip" -DestinationPath ".\\"
del "cudnn.zip"
python tools\cudann_1.8_install.py
rmdir cudnn_windows /s /q
goto complete

:noAdmin
echo you are not running as admin
goto end

:noPython
echo you do not have python 3.10 installed, please install python 3.10 and add to path
goto end

:noGit
echo you do not have git installed, please install it
goto end

:complete
echo installation complete, to run the program for LoRA training, just run lora_gui.bat
:end
pause
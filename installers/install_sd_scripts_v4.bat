@echo off

openfiles > nul 2>&1
if not %ERRORLEVEL% equ 0 goto noAdmin

rem subroutine for python checking
rem call :pythonChecker

rem reg query "hklm\software\GitForWindows" > nul 2>&1
rem if not %ERRORLEVEL% equ 0 goto noGit

echo Setting execution policy to unrestricted
Call PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& {Start-Process PowerShell -ArgumentList 'Set-ExecutionPolicy Unrestricted -Force' -Verb RunAs}"
cd /d %~dp0
echo cloning required repos and moving files
git clone "https://github.com/kohya-ss/sd-scripts" > nul
git clone "https://github.com/derrian-distro/LoRA_Easy_Training_Scripts" > nul
copy LoRA_Easy_Training_Scripts\*.py sd-scripts > nul
copy LoRA_Easy_Training_Scripts\*.bat sd-scripts > nul
copy LoRA_Easy_Training_Scripts\installables\requirements_startup.txt sd-scripts > nul
cd sd-scripts
echo creating python venv
python -m venv venv
call venv\Scripts\activate

echo installing dependancies, this may take a while
echo installing torch
pip3 install torch==1.12.1+cu116 torchvision==0.13.1+cu116 --extra-index-url https://download.pytorch.org/whl/cu116 > nul

echo installing other dependancies
pip3 install --upgrade -r requirements.txt > nul

echo installing xformers
pip3 install -U -I --no-deps "https://github.com/C43H66N12O12S2/stable-diffusion-webui/releases/download/f/xformers-0.0.14.dev0-cp310-cp310-win_amd64.whl" > nul

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

choice /C YN /M "Do you want to install the optional cudnn1.8 for faster training on high end 30X0 and 40X0 cards?"
if ERRORLEVEL 2 goto pascalFix

echo installing cudnn1.8 for faster training on 40X0 cards
curl -k "https://b1.thefileditch.ch/mwxKTEtelILoIbMbruuM.zip" -o "cudnn.zip"
Call Powershell Expand-Archive "cudnn.zip" -DestinationPath ".\\"
del "cudnn.zip"
md temp
curl "https://raw.githubusercontent.com/bmaltais/kohya_ss/9c5bdd17499e3f677a5d7fa081ee0b4fccf5fd4a/tools/cudann_1.8_install.py" -o "temp\cudann_1.8_install.py"
python temp\cudann_1.8_install.py
rmdir temp /s /q
rmdir cudnn_windows /s /q
goto complete

:pascalFix
choice /C YN /M "Do you have a 10X0 card?"
if ERRORLEVEL 2 goto complete

echo installing 10X0 card fix
move ..\LoRA_Easy_Training_Scripts\installables\libbitsandbytes_cudaall.dll venv\Lib\site-packages\bitsandbytes > nul
move ..\LoRA_Easy_Training_Scripts\installables\main.py venv\Lib\site-packages\bitsandbytes\cuda_setup > nul
goto complete

:pythonChecker

reg query "hkcu\Software\Python\PythonCore\3.10" > nul 2>&1
if not %ERRORLEVEL% equ 0 (
	echo Can't find Python 3.10 in current user registry; checking local machine registry...
	rem Now we check HKLM...
	
	reg query "hklm\Software\Python\PythonCore\3.10" > nul 2>&1
	if not %ERRORLEVEL% equ 0 (
		goto noPython
	) else (
		echo Found Python version 3.10 installed for all users
		exit /b
	)
) else (
	echo Found Python version 3.10
	rem return control to the caller
	exit /b
)

:noAdmin
echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
set params= %*
echo UAC.ShellExecute "cmd.exe", "/c ""%~s0"" %params:"=""%", "", "runas", 1 >> "%temp%\getadmin.vbs"

"%temp%\getadmin.vbs"
del "%temp%\getadmin.vbs"
exit /B

:noPython
echo Can't continue as you do not have python 3.10 installed, please install python 3.10 and ensure you select the 'add to path' option. Then run this script again.
goto end

:noGit
echo Can't continue as you do not have git installed, please install it and ensure it's added to the path. Then run this script again.
goto end

:complete
echo installation complete, to run the program just double click the batch file named run_popup.bat
echo if you intend to use the popup version, or edit and use the command_line files to have greater control
:end
pause
exit
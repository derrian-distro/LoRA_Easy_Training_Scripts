@echo off

cd /d %~dp0\sd_scripts
echo %CD%

choice /C 012 /M "Which torch version do you want to change to? 1.12.1, 2.0, or 2.1"
if ERRORLEVEL 3 goto torcha
if ERRORLEVEL 2 goto torchb

rmdir venv /s /q 2>null
echo creating new venv
python -m venv venv
call venv\Scripts\activate
echo installing torch 1.12.1
pip install torch==1.12.1+cu116 torchvision==0.13.1+cu116 --extra-index-url https://download.pytorch.org/whl/cu116 > nul
echo installing requirements
pip install -r requirements.txt > nul
echo installing xformers for torch 1.12.1
pip install -U -I --no-deps "https://github.com/C43H66N12O12S2/stable-diffusion-webui/releases/download/f/xformers-0.0.14.dev0-cp310-cp310-win_amd64.whl" > nul
echo moving required bitsandbytes files
IF NOT exist venv\Lib\site-packages\bitsandbytes (mkdir venv\Lib\site-packages\bitsandbytes)
If NOT exist venv\Lib\site-packages\bitsandbytes\cuda_setup (mkdir venv\Lib\site-packages\bitsandbytes\cuda_setup)
copy bitsandbytes_windows\*.dll venv\Lib\site-packages\bitsandbytes > nul
copy bitsandbytes_windows\cextension.py venv\Lib\site-packages\bitsandbytes > nul
copy bitsandbytes_windows\main.py venv\Lib\site-packages\bitsandbytes\cuda_setup > nul
goto complete

:torcha
rmdir venv /s /q 2>null
echo creating new venv
python -m venv venv
call venv\Scripts\activate
echo installing torch 2.1.0
pip install torch==2.1.0.dev20230320+cu118 torchvision==0.16.0.dev20230320+cu118 --extra-index-url https://download.pytorch.org/whl/nightly/cu118 > nul
echo installing requirements
pip install -r requirements.txt > nul
echo installing xformers for torch 2.1.0
pip install -U -I --no-deps "https://github.com/DDStorage/LoRA_Easy_Training_Scripts/releases/download/torch2.1.0/xformers-0.0.17+c36468d.d20230318-cp310-cp310-win_amd64.whl" > nul
goto end

:torchb
rmdir venv /s /q 2>null
echo creating new venv
python -m venv venv
call venv\Scripts\activate
echo installing torch 2.0.0
pip install torch==2.0.0+cu118 torchvision==0.15.0+cu118 --extra-index-url https://download.pytorch.org/whl/cu118 > nul
echo installing requirements
pip install -r requirements.txt
echo installing xformers for torch 2.0.0
pip install -U -I --no-deps "https://github.com/DDStorage/LoRA_Easy_Training_Scripts/releases/download/torch2.0.0/xformers-0.0.17+b3d75b3.d20230320-cp310-cp310-win_amd64.whl" > nul

:end
echo moving required bitsandbytes files
IF NOT exist venv\Lib\site-packages\bitsandbytes (mkdir venv\Lib\site-packages\bitsandbytes)
If NOT exist venv\Lib\site-packages\bitsandbytes\cuda_setup (mkdir venv\Lib\site-packages\bitsandbytes\cuda_setup)
copy bitsandbytes_windows\*.dll venv\Lib\site-packages\bitsandbytes > nul
copy bitsandbytes_windows\cextension.py venv\Lib\site-packages\bitsandbytes > nul
copy bitsandbytes_windows\main.py venv\Lib\site-packages\bitsandbytes\cuda_setup > nul
choice /C YN /M "Do you want to install the triton built for torch 2?"
if errorlevel 2 goto complete
echo installing triton
pip install -I -U --no-deps "..\installables\triton-2.0.0-cp310-cp310-win_amd64.whl"

:complete
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
goto done

:pascalFix
choice /C YN /M "Do you have a 10X0 card?"
if ERRORLEVEL 2 goto done

echo installing 10X0 card fix
move ..\installables\libbitsandbytes_cudaall.dll venv\Lib\site-packages\bitsandbytes > nul
move ..\installables\main.py venv\Lib\site-packages\bitsandbytes\cuda_setup > nul

:done
pause
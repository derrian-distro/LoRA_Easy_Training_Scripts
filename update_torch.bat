@echo off

cd /d %~dp0\sd_scripts

choice /C 01 /M "Which torch version do you want to upgrade to? 2.0 or 2.1"
if ERRORLEVEL 2 goto torcha

rm -rf venv > nul
python -m venv venv
call venv\Scripts\activate
echo installing torch 2.0.0
pip install torch==2.0.0+cu118 torchvision==0.15.0+cu118 --extra-index-url https://download.pytorch.org/whl/nightly/cu118 > nul
echo installing requirements again
pip install -r requirements.txt
echo installing xformers for torch 2.0.0
pip install -U -I --no-deps "https://github.com/DDStorage/LoRA_Easy_Training_Scripts/releases/download/torch2.0.0/xformers-0.0.17+b3d75b3.d20230320-cp310-cp310-win_amd64.whl" > nul
goto end

:torcha
echo installing torch 2.1.0
pip install torch==2.1.0.dev20230320+cu118 torchvision==0.16.0.dev20230320+cu118 --extra-index-url https://download.pytorch.org/whl/nightly/cu118 > nul
echo installing requirements again
pip install -r requirements.txt
echo installing xformers for torch 2.1.0
pip install -U -I --no-deps "https://github.com/DDStorage/LoRA_Easy_Training_Scripts/releases/download/torch2.1.0/xformers-0.0.17+c36468d.d20230318-cp310-cp310-win_amd64.whl" > nul

:end
choice /C YN /M "Do you want to install the triton built for torch 2?"
if errorlevel 2 goto complete
echo installing triton
pip install "..\installables\triton-2.0.0-cp310-cp310-win_amd64.whl"

:complete
pause
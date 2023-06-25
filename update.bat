@echo off
cd /d %~dp0

git pull
git submodule init
git submodule update

cd sd_scripts
call venv\Scripts\activate
pip install -U -r requirements.txt
cd ..
pip install -U -r requirements_ui.txt
pip install -U LyCORIS\.
pip install -U custom_scheduler\.
pause
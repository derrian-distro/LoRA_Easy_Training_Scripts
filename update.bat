@echo off
cd /d %~dp0

git pull
git submodule init
git submodule update

cd sd_scripts
call venv\Scripts\activate
pip install -r requirements.txt
cd ..
pip install -r requirements_ui.txt
pip install LyCORIS\.
pause
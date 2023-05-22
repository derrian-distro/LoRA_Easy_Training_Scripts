@echo off

cd %~dp0
call sd_scripts\venv\Scripts\activate
python main.py
pause
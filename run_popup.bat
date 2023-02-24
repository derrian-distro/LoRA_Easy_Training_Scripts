@echo off

echo Starting popup training...
call sd_scripts\venv\Scripts\activate
accelerate launch main.py --popup
pause
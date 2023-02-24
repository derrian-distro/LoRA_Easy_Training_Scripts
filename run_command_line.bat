@echo off

echo Starting command_line training...
call sd_scripts\venv\Scripts\activate
accelerate launch main.py
pause
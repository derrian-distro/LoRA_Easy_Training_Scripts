@echo off

title LoRA Trainer
cd %~dp0
call sd_scripts\venv\Scripts\activate
python main.py
pause

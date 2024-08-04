@echo off

title LoRA Trainer
cd %~dp0
call venv\Scripts\activate
python main.py
pause

@echo off

echo Starting command_line training...
call venv\Scripts\activate
accelerate launch lora_train_command_line.py
pause
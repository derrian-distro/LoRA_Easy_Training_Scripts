@echo off

echo Starting command_line training...
venv\Scripts\accelerate.exe launch lora_train_command_line.py
echo Training complete.
pause
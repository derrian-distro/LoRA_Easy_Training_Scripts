@echo off

echo Starting popup training...
call venv\Scripts\activate
accelerate launch lora_train_popup.py
pause
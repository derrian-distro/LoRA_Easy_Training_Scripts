@echo off

echo Starting popup training...
venv\Scripts\accelerate.exe launch lora_train_popup.py
echo Training complete.
pause
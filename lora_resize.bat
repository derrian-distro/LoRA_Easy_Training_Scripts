@echo off

echo starting resizing...
call venv\Scripts\activate
python lora_resize.py
pause
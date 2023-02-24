@echo off

echo starting resizing...
call sd_scripts\venv\Scripts\activate
python lora_resize.py
pause
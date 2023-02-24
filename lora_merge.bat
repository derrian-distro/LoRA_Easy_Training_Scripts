@echo off
echo starting lora merging...
call sd_scripts\venv\Scripts\activate
python lora_merge.py
pause
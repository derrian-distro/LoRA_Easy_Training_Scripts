@echo off
echo starting extraction...
call sd_scripts\venv\Scripts\activate
python lora_locon_extract.py
pause
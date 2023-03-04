@echo off

echo starting extract locon
call sd_scripts\venv\Scripts\activate
python locon_extract.py
pause
@echo off

echo starting extract locon
call sd_scripts\venv\Scripts\activate
python lycoris_extract.py
pause
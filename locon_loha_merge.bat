@echo off

echo starting locon merge...
call sd_scripts\venv\Scripts\activate
python locon_loha_merge.py
pause
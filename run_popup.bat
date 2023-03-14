@echo off

echo Starting popup training...
call sd_scripts\venv\Scripts\activate
echo updating LyCORIS if needed...
pip install LyCORIS\. > nul
accelerate launch main.py --popup
pause
@echo off

echo Starting command_line training...
call sd_scripts\venv\Scripts\activate
echo updating LyCORIS if needed...
pip install LyCORIS\. > nul
python main.py
pause
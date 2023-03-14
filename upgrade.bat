@echo off

echo running through requirements...
cd /d %~dp0
cd sd_scripts
call venv\Scripts\activate
pip install -r requirements.txt > nul
cd ..
echo updating LyCORIS if needed...
pip install LyCORIS\. > nul
echo completed updating any requirements
pause
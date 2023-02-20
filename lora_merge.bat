@echo off
echo starting lora merging...
call venv\Scripts\activate
echo ensuring lora library is installed
pip install lora > nul
echo running python script...
python lora_merge.py
pause
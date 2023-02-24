@echo off

echo starting resize of images...
call sd_scripts\venv\Scripts\activate
python image_resize.py
pause
@echo off

echo starting resize of images...
call venv\Scripts\activate
python image_resize.py
pause
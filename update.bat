@echo off
cd /d %~dp0

git pull
python update.py
pause

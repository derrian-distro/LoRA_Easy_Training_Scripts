@echo off
cd /d %~dp0

git pull
git submodule update --init --recursive
cd backend
python updater.py
pause

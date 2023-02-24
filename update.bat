@echo off

set "scriptDir=%~dp0"
set "scriptDir=%scriptDir:~0,-1%"

git config --global --add safe.directory %scriptDir%
git pull
git submodule init
git submodule update
goto end

:end
pause
#!/bin/bash

git pull
git submodule update --init --recursive
source venv/bin/activate
cd backend
python updater.py

deactivate

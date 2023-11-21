#!/bin/bash

## Clone the git repo and change to that directory
git clone https://github.com/derrian-distro/LoRA_Easy_Training_Scripts
cd LoRA_Easy_Training_Scripts

## Init git submodules
git submodule init
git submodule update

## Change to sd-scripts directory, generate your python virtual environment and activate it
cd sd_scripts
python3.10 -m venv venv
source venv/bin/activate

## Install additional packages with pip
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
pip install xformers
pip install -r ../requirements_ui.txt
pip install ../LyCORIS/.
pip install ../custom_scheduler/.
pip install bitsandbytes

## Configure accelerate
accelerate config

## Mark the run script executable
chmod u+x ../run.sh

## Run the damn thing
cd ../
./run.sh
# LoRA_Easy_Training_Scripts
A set of two training scripts written in python for use in Kohya's SD-Scripts repository.

The command line version is designed to be used by those who are already used to the already existing scripts out there for training LoRAs.
The popup version is designed for those who haven't, The way it gathers the data is slower by neccessity, however it means you don't need to go into the script at all to change elements.

no matter which script you use, you must activate the venv in your SD-Scripts install. Please make sure you are using the most up-to-date version of SD-Scripts as this was written to work with the new version, trying to do so on a previous version will give a `ModuleNotFoundError: No module named 'library.train_util'` error.

## Installation
All you have to do to install it is move the scripts into your install of Kohya's SD-Scripts
after that to use it you can activate your venv then type this command

for the command line version
```
venv\Scripts\activate
accelerate launch --num_cpu_threads_per_process 12 lora_train_command_line.py
```


for the popup verison
```
venv\Scripts\activate
accelerate launch --num_cpu_threads_per_process 12 lora_train_popup.py
```

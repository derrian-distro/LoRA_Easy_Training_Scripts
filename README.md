# LoRA_Easy_Training_Scripts

A set of two training scripts written in python for use in Kohya's SD-Scripts repository.

The command line version is designed to be used by those who are already used to the already existing scripts out there for training LoRAs.
The popup version is designed for those who haven't, The way it gathers the data is slower by neccessity, however it means you don't need to go into the script at all to change elements.

no matter which script you use, you must activate the venv in your SD-Scripts install. Please make sure you are using the most up-to-date version of SD-Scripts as this was written to work with the new version, trying to do so on a previous version will give a `ModuleNotFoundError: No module named 'library.train_util'` error.

## New easy install scripts

If you don't know how to set up sd-scripts or kohya_ss for that matter I have created some batch files to make installing that easy! It does everything for you, all you need to do is right click -> run as administrator. **This only works for windows!** you can grab it [here](https://github.com/derrian-distro/LoRA_Easy_Training_Scripts/releases/latest).

## alternative Installation

All you have to do to install it is move the scripts into your install of Kohya's SD-Scripts
after that to use it you just put this one command into whatever your terminal is.
if you're on a linux system or using bash on windows for some reason make sure you flip the `\` to `/`

command line version

```
venv\Scripts\accelerate.exe launch --num_cpu_threads_per_process 12 lora_train_command_line.py
```

popup version

```
venv\Scripts\accelerate.exe launch --num_cpu_threads_per_process 12 lora_train_popup.py
```

## JSON Rework, and More

Json got a major rework in the last update I posted, changing how it works to load everything by default if you are using `command_line.py` and almost everything if you are using `popup.py`.
Additionally, it has a whole new way to exclude parameters so that the user can decide what gets loaded and what doesn't.
It still has support for the UI version of json files, and will support new options as they get added.
Also, for those who would rather not have to change the variables for loading or saving json files, there is an argument
you can add for both, `--save_json_path "path\to\folder"` for saving and `--load_json_path "path\to\json.json"` for loading.
## Other Updates

- First, I added an option to `command_line.py` which allows you to generate a json file and skip training. This was to facilitate
a new way of training that I added as well
- I added a way to queue training for both `command_lin.py` and `popup.py`, though they are done slightly differently
  - `popup.py` handles it by repeating the popups until you say do don't want to queue any more. This is done this way for those who
  are worse with tech than others
  - `command_line.py` does it by adding a variable called `multi_run_folder` to the args list. setting this will completely
  ignore all other inputs and just take the json files in that folder and load them. in this, you do multiple runs at a time
  by putting all of your json files into one folder and giving it that folder. If you don't want to go into the script, you can
  just add the argument `--multi_run_path "path\to\folder"` to when you run the script.
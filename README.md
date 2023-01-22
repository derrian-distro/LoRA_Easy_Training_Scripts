# LoRA_Easy_Training_Scripts
A set of two training scripts written in python for use in Kohya's SD-Scripts repository.

The command line version is designed to be used by those who are already used to the already existing scripts out there for training LoRAs.
The popup version is designed for those who haven't, The way it gathers the data is slower by neccessity, however it means you don't need to go into the script at all to change elements.

no matter which script you use, you must activate the venv in your SD-Scripts install. Please make sure you are using the most up-to-date version of SD-Scripts as this was written to work with the new version, trying to do so on a previous version will give a `ModuleNotFoundError: No module named 'library.train_util'` error.

## Installation
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

## New JSON saving and loading
### Now supports the UI version JSON files!
Now you can save and load json files of your configs. When saving a json file, it just saves everything. When loading one if only loads the following (on command line):
net dim, scheduler, warmup lr ratio, learning rate, text encoder lr, unet lr, and clip skip
and optionally (asks the user):
train resolution, min and max bucket resolution, batch size, num epochs, shuffle captions, and keep tokens

The popup version loads the same amount, but it loads them without asking the user as much. This is to keep the popup.py version as user-friendly as possible. the only time it asks for an input is when the resolution has changed. This might change in the future because I'm not entirely set on that.

## Other Updates
* Since sd-scripts has changed a big thing, I had to delay the UI update I was working on to fix this issue. Now you can set an Alpha, either by hand in the command_line version, or through a popup in the popup.py version.
* I have also added support for the new training_comment which allows you to put a comment into the metadata. This should be nice to use for things like use case, or activation codes. You can either write the comment in the script in command_line, or through a popup, in popup.py
* Popup.py has added popups for the unet_lr and the text_encoder_lr so that those values can also be changed when you want.
* In command_line.py I have made a slight modification to make all input strings a literal string. Now you don't need to do `\\` when specifying a path. just make sure to have your path be in the format of r"path\to\model" for example.
* I set up some batch files which you can also just drop into the root folder of sd-scripts which you can just open to run the script. Keep in mind, this doesn't automatically fill things out for command_line.py, nor does it have --save_json_path or --load_json_path pre applied. You can still manually set the save_json_path or the load_json_path manually.
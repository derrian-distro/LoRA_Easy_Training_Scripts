# LoRA_Easy_Training_Scripts

A set of training scripts written in python for use in Kohya's [SD-Scripts](https://github.com/kohya-ss/sd-scripts).

The main two scripts, titled `lora_train_command_line.py` and `lora_train_popup.py` are the main training scripts. They both effectively do the same thing, just in different ways.

`lora_train_command_line.py` is designed for those who want to directly edit the script, if you need some help on what the various commands are, you can just run the script like so to get help with for every arg, at the bottom of this readme will be a big list of all of the commands as well

```
venv\Scripts\accelerate.exe launch lora_train_command_line.py -h
or
venv\Scripts\accelerate.exe launch lora_train_popup.py -h
```

`lora_train_popup.py` is designed for those who are unable or unwilling to directly edit the script, you give up some control this way, but the defaults are generally good, so you won't need to worry too much about the hidden elements. It attempts to keep things simple by asking the user questions through popups, it's slower than `lora_train_command_line.py` but it is a guided experience

`lora_resize.py` is a third script that is to be used for _resizing_ lora, as SD-Scripts includes a way to do that now. This is a great way to reduce your dim size after training. It should be plenty easy to use as well because it uses popups much like `lora_train_popup.py` does.

## Installation

### Windows

If you have a windows device I have created batch files [here](https://github.com/derrian-distro/LoRA_Easy_Training_Scripts/releases/latest) that auto install for you. if you want to specifically use _my_ scripts, then grab the one titled `install_sd_scripts.bat` which will install SD-Scripts as well as my scripts. **Make sure you don't have spaces in your path when you install them**

### Linux

Unfortunatly, I haven't actually gotten around to creating installers for Linux devices, mainly because I don't use a Linux device as my daily driver. that being said, you can still install SD-Scripts! Follow the install instructions on SD-Scripts then just move these files over to the SD-Scripts directory.

## Usage

### Windows

If you are using windows, then you can just run any of the scripts by using their respective `run_*.bat` files, so `lora_train_popup.py` would have you run `run_popup.py`. Just make sure that they are in the same folder as the `.py` files, which should be the root of SD-Scripts.

### Linux

If you are using Linux, you can run it by running accelerate like so.

```
venv/Scripts/accelerate launch lora_train_command_line.py
or
venv/Scripts/accelerate launch lora_train_popup.py
```

I believe it also works without accelerate if you just want to run it from the venv and python directly.

## JSON Saving And Loading

One of the big features of this set of scripts is that they can create and use JSON files.
how they load json files are slightly different between the two training scripts, so lets explain why.

`lora_train_command_line.py` will load everything unconditionally by default. There is a way to exclude things though. you must modify the variable called `json_load_skip_list` which can be added to to exclude things, more explanation of it will be below

`lora_train_popup.py` will load everything except for the following items, the path to save a json, the path to load regularization images, the path to a lora model to resume training, the name you can set to change the output name, your training comment, and the skip list itself

Additionally, you can load or save JSON files from the command line with their respective commands, `--save_json_path "path\to\folder"` for saving, and `--load_json_path "path\to\json.json"` for loading. You can also just set them, in `lora_train_command_line.py` and it is asked in `lora_train_popup.py`

Finally, I also set up the JSON loading so that it supports the JSON files Kohya_ss generates

## Queuing Training

I have implemented queues to both the `lora_train_command_line.py` and `lora_train_popup.py`
like the JSON saving, they work slightly differently from one another. so I'll explain the differences.

`lora_train_command_line.py` has a variable called `multi_run_folder` that can take a path to a folder that has a bunch of JSON files in it. it will run through all of them one by one, and train every model in that folder. Unlike when loading JSON files normally, this will ignore the exclude list because it cannot wait for the user to change the variables during run time. Since it loads everything through JSON files, I have opted to have it create a "completed" folder of the JSON files that have already been trained, doing this means that if you quit before all are finished, you know what hasn't been done. If you would rather set it through the command line, you can call `--multi_run_path "path\to\folder"`

`lora_train_popup.py` just loops through the popups until you say you want to stop, and then queues them up to run after you are done entering them. I don't have a way to track what has been done for this version because of the way it's implemented.

## Tag Occurrence Printout

new with this update is a way to generate a txt file that outputs all of the tags that was used to train with in an easy to read way that has both the number of times it appeared in all caption files, as well as the tag itself, it is ordered from most to least.

## LoRA Resize Script

`lora_resize.py` is a script I wrote to run the resize script that is within SD-Scripts, much like the other two, it has a batch file that can be used to run it. It does things in the popup way, and currently _doesn't_ support queuing, It will be added another time. This script should simplify reducing the dim size of LoRA.

## Changelog

- Feb 9, 2023
  - I modified the bat files to work a bit better on the off chance that bitsandbytes needed to be installed to a different place than expected.
  - I also fixed the bat file for `lora_resize.bat` because it was looking for the wrong file name.
  - Added new button prompts for some of the popups to make it easier to know what options you have.
  - Added in the new arguments that Kohya introduced, as well as added in the arguments for training on SD2 based models, popups got added to change the ckip skip to 1 if using a realistic models as well. new arguments are as follows:
    - v2
    - v_parameterization
    - caption_dropout_rate
    - caption_dropout_every_n_epochs
    - caption_tag_dropout_rate
  - The new paramaters are added at the bottom of the list of arguments
  - Additionally, I finally decided to rename save_at_n_epochs to save_every_n_epochs internally. This doesn't break the json saving and loading system

## List Of Arguments

| Argument                       | Type      | Required | What It Does                                                                                                                                                                                                                                                             |
| ------------------------------ | --------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| base_model                     | str       | YES      | Path to the base model                                                                                                                                                                                                                                                   |
| img_folder                     | str       | YES      | Path to the image folder, make sure to set the folder your image folders are in, not the folders named 1_something                                                                                                                                                       |
| output_folder                  | str       | YES      | Path to the output of all of your checkpoints                                                                                                                                                                                                                            |
| save_json_folder               | str       | NO       | Path to the folder where your generated json config files will be placed                                                                                                                                                                                                 |
| load_json_path                 | str       | NO       | Path to the json file to be loaded                                                                                                                                                                                                                                       |
| json_load_skip_list            | list[str] | NO       | Is the list of items that will not get loaded when you load a json file, make sure that you type in the exact arg name. example: ["base_model", "img_folder", "output_folder"]                                                                                           |
| multi_run_folder               | str       | NO       | Is the path to the folder that contains the JSON files to be loaded for queued training. This is exclusive to `lora_train_command_line.py`                                                                                                                               |
| save_json_only                 | bool      | NO       | Is a switch to prevent training so that you can generate a JSON file                                                                                                                                                                                                     |
| net_dim                        | int       | YES      | This is the the amount of datapoints that exist within the LoRA, the more you have the more data can be added, as well as the bigger size. However the more you have, the more junk data can be added as well                                                            |
| alpha                          | float     | YES      | This is the scalar based on the net_dim. you can figure out how much it is scaling by doing the simple calculation of alpha / dim_size.                                                                                                                                  |
| scheduler                      | str       | YES      | This is the way the learning rate is modified as it trains. the list of schedulers are as follows: linear, cosine, cosine_with_restarts, polynomial, constant, and constant_with_warmup                                                                                  |
| cosine_restarts                | int       | NO       | This is a value that is only set when cosine_with_restarts is set. This value represents how many times during training the scheduler will reset the learning rate back to default                                                                                       |
| scheduler_power                | float     | NO       | This is a value that is only set when polynomial is set. This value represents the X in the polynomial function, the higher this is, the faster the learning rate decays, 1 means that it decays "normally", 2 means it decays very fast, and 0.5 means it decays slower |
| warmup_lr_ratio                | float     | NO       | This is the ratio of steps that will be warmup steps, it is dynamically calculated based on the total number of steps that was given                                                                                                                                     |
| learning_rate                  | float     | NO       | This is the base learning rate, it determines how much is learned per step. If it is not set, it defaults to 1e-3                                                                                                                                                        |
| text_encoder_lr                | float     | NO       | This is the lr for specifically the text encoder. it overwrites the base lr                                                                                                                                                                                              |
| unet_lr                        | float     | NO       | This is the lr for specifically the unet. it overwrites the base lr                                                                                                                                                                                                      |
| num_workers                    | int       | YES      | This is the number of threads that are used for data processing, lower numbers mean faster epoch starting time, but supposedly slower data loading                                                                                                                       |
| save_every_n_epochs            | int       | NO       | Saves a checkpoint every n epochs, so save_at_n_epochs = 1 means that it saves every epoch                                                                                                                                  											   |
| shuffle_captions               | bool      | NO       | This is a switch to turn on shuffle_captions, doing so will shuffle all of the tags in the caption files                                                                                                                                                                 |
| keep_tokens                    | int       | NO       | This is a way to keep certain tokens at the front of the captions files when shuffling. This only matters if you are shuffling captions                                                                                                                                  |
| max_steps                      | int       | NO       | This is a way to specify an amount of steps without needing to calculate it. If it is a step amount that doesn't end it a full epoch, it will just train until it hits the final step, then output the final epoch, even if it was not a full epoch                      |
| tag_occurrence_txt_file        | bool      | NO       | Creates a txt file that contains the list of tags used during training in the order of most to least                                                                                                                                                                     |
| train_resolution               | int       | YES      | The resolution that is trained at                                                                                                                                                                                                                                        |
| min_bucket_resolution          | int       | YES      | the minimum bucket size when creating buckets                                                                                                                                                                                                                            |
| max_bucket_resolution          | int       | YES      | the maximum bucket size when creating buckets                                                                                                                                                                                                                            |
| lora_model_for_resume          | str       | NO       | Loads a "Hypernetwork" into the training model, also works for LoRA, which is why I have it here, this is not the intended way to continue training though                                                                                                               |
| clip_skip                      | int       | YES      | Works the same way clip skip does when using webui, defines what layer its trained on                                                                                                                                                                                    |
| test_seed                      | int       | YES      | represents the "reproducable seed" as well as decides the seed for the RNG used while training, sometimes changing this value is enough to improve a bake                                                                                                                |
| priot_loss_weight              | float     | YES      | Is something directly related to how Dreambooth is trained, LoRA are trained in a Dreambooth-y way so I guess this is required as well, I honestly don't understand what it is though                                                                                    |
| gradient_checkpointing         | bool      | NO       | enables or disables gradient checkpointing, allows bigger batch sizes for lower vram, much slower though                                                                                                                                                                 |
| gradient_acc_steps             | int       | NO       | honestly, I don't exactly know what this means, but I believe it has to do with the size of the batch size                                                                                                                                                               |
| mixed_precision                | str       | YES      | Is a modification to how it is trained, having mixed precision means that it trains in both fp32 and fp16, the only options are fp16, bf16, and none                                                                                                                     |
| save_precicion                 | str       | YES      | Determines how it is saved, it can be saved in float(fp32), fp16, and bf16                                                                                                                                                                                               |
| save_as                        | str       | YES      | the file type that it gets saved as, by default this is set to .safetensors, and should stay that way, but the other two options are .ckpt and .pt                                                                                                                       |
| caption_extension              | str       | YES      | the file types the captions are in, by default this is set to .txt, but it can accept any filetype it looks like                                                                                                                                                         |
| max_clip_token_length          | int       | YES      | can be set to any of 75, 150, or 225. 150 is default, and generally, unless you have really long prompts, don't need it to be higher                                                                                                                                     |
| buckets                        | bool      | NO       | enables/disables buckets, usually you want this on, especially when you didn't crop your images                                                                                                                                                                          |
| xformers                       | bool      | NO       | enables/disables xformers, I don't believe that AMD cards can use them, so make sure to disable it if you are using one                                                                                                                                                  |
| use_8bit_adam                  | bool      | NO       | enables/diables 8bit Adam, great as an optimizer but some cards don't support it, if the program fails with it on, try turning it off                                                                                                                                    |
| cache_latents                  | bool      | NO       | enables/disables caching the latents of the input images, having this enabled will reduce the vram spikes as you train, but it prevents certain things from being enabled                                                                                                |
| color_aug                      | bool      | NO       | enables/disables color augmentation, this is one of the things that are unable to work with cache latents. it hue shifts the images, so that they provide different colors to input                                                                                      |
| flip_aug                       | bool      | NO       | enables/disables flip augmentation, flips every image by reversing it's latents, I believe, good to have on usually, but turn it off if you are dealing with something asymetric                                                                                         |
| random_crop                    | bool      | NO       | enables/disables random cropping, newly available to use with buckets, it is able to crop the images randomly when it fits them into the buckets, this also doesn't work with cache latents                                                                              |
| vae                            | str       | NO       | allows you to set a vae to train with, You are better off not training with one.                                                                                                                                                                                         |
| no_meta                        | bool      | NO       | Keep this disabled, enabling it prevents the metadata from being added to the model                                                                                                                                                                                      |
| log_dir                        | str       | NO       | allows you to output training logs, most people won't be able to make sense of it, so It's not really useful.                                                                                                                                                            |
| bucket_reso_steps              | int       | NO       | allows you to change how often a new bucket is created, default is 64, under that is untested, can be any value 1 or up                                                                                                                                                  |
| bucket_no_upscale              | bool      | NO       | enables/disables upscaling images when applying buckets.                                                                                                                                                                                                                 |
| v2                             | bool      | NO       | Is the switch to set if you are training on a model that is based on SD2                                                                                                                                                                                                 |
| v_parameterization             | bool      | NO       | Enable this only if you have v2 enabled and are using a model based on the 768x version of SD2                                                                                                                                                                           |
| caption_dropout_rate           | float     | NO       | The rate at which caption files get dropped while training, not entirely sure what this does, except for the fact that it will occasionally not use the caption file for images                                                                                          |
| caption_dropout_every_n_epochs | int       | NO       | How often an epoch ignores captions while training, the number set means that every N epochs have ingored captions, EX: 3 = (3, 6, 9,...)                                                                                                                                |
| caption_tag_dropout_rate       | float     | NO       | The rate at which _tags_ within caption files get ignored, this will not drop tags that are being kept by the keep_tokens argument.                                                                                                                                      |

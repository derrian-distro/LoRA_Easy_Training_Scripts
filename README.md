# LoRA_Easy_Training_Scripts

A set of training scripts written in python for use in Kohya's [SD-Scripts](https://github.com/kohya-ss/sd-scripts).

**Please ensure you have python 3.10.6 and git installed**

Gone is the two scripts of the past, and now everything is handled in one simple `main.py` and the two accompanying bat files `run_popup.bat` and `run_command_line.bat`. If you are on a linux system you can run them by activating the venv, which has moved to the sd_scripts folder within this project then run it using the command `accelerate launch main.py` for the command line, or `accelerate launch main.py --popup` if you want the popups.


the base version was designed for people who want to directly modify the script themselves, which you can now do so in the file `ArgsList.py`. to find out all of the commands and what they do you can run the script with the -h command to list every argument or just look at the list of arguments below

the popups are designed for those who are unable or unwilling to directly edit the script, you give up some control this way, but the defaults are generally good, so you won't need to worry too much about the hidden elements. It attempts to keep things simple by asking the user questions through popups, it's slower than the command line but it is a guided experience

there are also a bunch of small scripts meant to do other things that sd-scripts can do, such as resizing and merging LoRA, or down scaling images for datasets.

## Installation

### Windows

If you have a windows device I have created batch files [here](https://github.com/derrian-distro/LoRA_Easy_Training_Scripts/releases/latest) that auto install for you. if you want to specifically use _my_ scripts, then grab the one titled `install_sd_scripts.bat` which will install SD-Scripts as well as my scripts. **Make sure you don't have spaces in your path when you install them**

### Linux

I don't have installers for my scripts for linux, but here is the setup process so you can do it yourself.
```
git clone https://github.com/derrian-distro/LoRA_Easy_Training_Scripts
cd LoRA_Easy_Training_Scripts
git submodule init
git submodule update
cd sd_scripts
python -m venv venv
source venv/bin/activate
pip install torch torchvision --extra-index-url https://download.pytorch.org/whl/cu116
pip install --upgrade -r requirements.txt
pip install -U xformers
accelerate config
```
follow these answers when setting up accelerate
```
- This machine
- No distributed training
- NO
- NO
- NO
- all
- fp16
```

## Usage

### Windows

If you are using windows, then you can just run any of the scripts by using their respective `run_*.bat` files.

### Linux

If you are using Linux, you can run it by activating your venv then running the scripts like so.

```
source sd_scripts/venv/bin/activate
then
accelerate launch main.py
or
accelerate launch main.py --popup
```

I believe it also works without accelerate if you just want to run it from the venv and python directly.

## Updating
To check for updates on windows you can use the new `update.bat` that will automatically check for updates and apply them when it finds one, it should also update sd_scripts when there is an update as well. Sometimes when you update you will also need to use the `upgrade.bat` file to make things run, so don't forget to run that once an update as well.

## JSON Saving And Loading

One of the special features of the project is that you can save and load json files.

command_line and popup now handle this the same way as they now use the exact same backend.
if you load a json file when the `--popup` arg is active, it will skip all popups and just load the json in full, rather than only load parts of it.

Additionally, you can load or save JSON files from the command line with their respective commands, `--save_json_path "path\to\folder"` for saving, and `--load_json_path "path\to\json.json"` for loading. You can also just set them, in `ArgsList.py` and it is asked when using `--popup`. Keep in mind that if you use `--save_json_path` and `--load_json_path` it will take precidence over whatever you inserted into the ArgsList or popups.

Finally, I also set up the JSON loading so that it supports the JSON files Kohya_ss generates

## Queuing Training

I have implemented queues into the project so that it will be able to take in a folder that has a bunch of json files and run through them all. Unlike the previous version, which had the popup version run through the popups for each time you wanted to queue up something, it now just uses the same method as the previous command line version.

you can also supply the path to the folder through the command line argument `--multi_run_path "path\to\folder"`. keep in mind that setting this will override any value set in `ArgsList.py` or through the popups

if you need to generate json files you can do use through changing the `ArgsList.py` and setting the variable `save_json_only` to True, or through the popups by selecting yes on the associated popup. for that popup to appear you must also select yes to generating a json file

## Tag Occurrence Printout

With my scripts, you can create a txt file with a list of all tags used during training. The tags can be output in one of two ways, according to most used to least, or alphabetically.

## LoRA Resize Script

`lora_resize.py` and it's accompanying bat file `lora_resize.bat` is a script I wrote to run the resize script that is within SD-Scripts, much like the other two, it has a batch file that can be used to run it. It does things in the popup style, and supports queueing. This script should simplify reducing the dim size of LoRA. I have changed the queue system to better support multiple resizes, either through providing a txt file, or providing multiple values. Because of this, however, it is more prone to failures. the txt file only contains the values used, no the mode of resize or the model to resize. So, if you are planning on doing a fixed resize, you would only need to enter in 1 value per line, but if you are planning on doing a dynamic resize, you want to put two values per line, the dynamic value, and then the max dim size.

## LoRA Merging and Image Resizing scripts

I added two new scripts to handle the scripts that sd-scripts added since I created the resizing script. The first one, `lora_merge.py` and it's accompanying bat file `lora_merge.bat` can take in any number of loras to merge together, it walks you through the process, so you shouldn't need to know how it works under the hood! I also added support for merging lora into models with this most recent update.

The second one, `image_resize.py` and it's accompanying bat file `image_resize.bat` is a script for downscaling your images. This is great if you are training at a high resolution as you can disable bucket upscaling and have a set of images that are "different" to the model, it should improve gens at lower resolutions, and might even help smaller datasets

## Lion Optimizer

I added support for the new Lion optimizer in both scripts. I don't know what the best lr is for them, and still have 8bit adam as the default for now. if you want to know more, take a look at the original github [here](https://github.com/lucidrains/lion-pytorch). They seem to have some insights, namely, use less steps than usual and a smaller lr. stating that lr should be anywhere from 3-10x _smaller_ than normal.

## D-Adaption
I also added support for the new D-Adaption which works differently from the other optimizers.
It handles the lr by itself, you just need to set the lr values to a value close to or at 1 for each lr. in order to seperate out the lr's for d-adaption though, you must also add the args `{"decouple": "True"}` to seperate the lr's for d-adaption. using the popups automatically sets this for you

## LoCon and LoHa and ia3 Training
I have added support for locon, loha, and ia3 training. You can set the variable `lyco` in the `ArgsList.py` to use LyCORIS, which also has a few variables that need to be set. in the `networks_args` variable, you can set the `conv_dim` and `conv_alpha` as well as the `algo` and if you are using `cp_decomp`. Typically, an example is like so:
```python
self.network_args = {
  'algo': 'lora', # lora corresponds to locon, loha corresponds to loha, and ia3 corresponds to ia3
  'conv_dim': '8',
  'conv_alpha': '1'
}
```
The popups handle setting these values for you, if you don't want to set them yourself.

## LoCon Extraction
I have added a popup style script for extracting LoCon from models. It does this using an Add Difference style approach, you much have a base model to compare against to extract this data. The process should guide you through the process. you can start it by running the bat file `locon_extract.bat`. I added a new way to do multiple extractions quickly through either using a txt file or giving multiple values, this is a much better way to set up queues than my original approach, however is more prone to failure. the txt file only contains the values used, not the mode of extract or the models to extract. Since all modes have two values, you can just put each set of two per line. There is an example included in the examples folder

## LoCon and loha merging
I have added a popup style script for merging LoCon models into normal models. all you need to do is follow the popups. you can start it by running the bat file `locon_loha_merge.bat`

## Changelog
- Apr 4, 2023
  - Updated sd-scripts and LyCORIS, however sd-scripts is one version behind as I still need time to work in the new sd-scripts elements. Note, this next update will disable LyCORIS for the time being until Kohaku can update their code.
  - Added new queue systems to the `lora_resize` and `locon_extract` scripts. They allow for much easier queues but it does mean it's more prone to failure. I have included example txt files in the examples folder.
- Mar 28, 2023
  - Updated sd-scripts and LyCORIS
  - Added the new parameters added by sd-scripts for min snr gamma and token warmup
    - `min_snr_gamma` is an argument that takes in a float, and seemingly improves training
    - `token_warmup_min` takes in an int, is the smallest amount of tokens that are used when using token warmup
    - `token_warmup_step` takes in a float, is the last step before all tokens are used in training
  - Added `min_snr_gamma` to popups as it seems to be a worthwhile addition
- Mar 21, 2023
  - Updated sd-scripts and LyCORIS
  - Added the new parameters added by sd-scripts for a custom scheduler, however I don't do any sort of error checking for it
  - Added support for torch 2.0.0 and 2.1.0 along with built xformers for both
  - Added support for triton for torch 2, however it may not be working as expected.
  - Updated the number of workers to be be 1 by default, as to make it more accessable
  - Changed the main batch files to not use accelerate to launch anymore, instead option to use python directly instead.
  - Added a new batch file for updating to torch 2.0.0 or 2.1.0 with the option to install triton as well.
  - Added new installer that is python based, as to make it easier to check for the correct version of python, as well as check for git being installed. This installer is _still_ only for windows as linux is different for every distro.
- Mar 13, 2023
  - Updated sd-scripts and LyCORIS
  - with it came an update to the resizing scripts, and the locon extraction scripts.
  - Added new parameters for specifying height seperately from width for training at non square resolutions
  - Added new popups to handle CP Decomposition for locon and loha as well as the change to how resolution is handled
- Mar 10, 2023
  - Updated sd-scripts to the newest version which now natively supports LoCon models
  - did a small refactor of the arguments to support the new LyCORIS that replaced the old LoCon repo
  - Removed the old LoCon repo, replacing it with the new LyCORIS repo
  - Added support for Loha models, as well as changed support for LoCon to follow the new pattern that was introduced in LyCORIS
  - depricated the original LoCon variables, in favor of using a singluar variable `network_args` which works much like `optimizer_args`.
  - popups were updated to support the new loha and other changes to setup
  - Updated both the LoCon extract and merge script to support the changes, extract still only works with LoCon, but you can merge Loha using the new merge script.
- Mar 7, 2023
  - Updated the locon dependancies to support the new extraction methods, this also includes writing up a new version of locon extraction to follow the update
  - Kohya updated their readme with more details on how to use the image preview system. In the attempt to make this a bit more transparent I'm also adding it here
    - `--n` is the neg prompt, you want to put it _after_ the main prompt
    - `--h` is height
    - `--w` is width
    - `--d` is the seed of the image
    - `--l` is the CFG scale
    - `--s` is the step count.
    - a sample prompt txt document might be like this
    ```
    # prompt 1
    masterpiece, best quality, 1girl, white t-shirt, upper body, looking at viewer, simple background --n low quality, worst quality, bad anatomy, bad composition, poor, low effort --w 768 --h 768 --d 1 --l 7.5 --s 28

    # prompt 2
    masterpiece, best quality, 1boy, in business suit, standing at street, looking back --n low quality, worst quality, bad anatomy, bad composition, poor, low effort --w 576 --h 832 --d 2 --l 5.5 --s 40
    ```
- Mar, 4, 2023
  - Updated the scripts to support LyCORIS's new algo ia3. Cant guarentee anything at all, have no clue how to train it, and know nothing about it other than that it is seemingly another loha style algo.
  - Updated the scripts to support the new arguments that Kohya introduced
    - `dataset config` for the toml file support, I haven't actually played with it, so for now it just sets it and that's it
    - all of the sample arguments
      - `sample_every_n_steps` and `sample_every_n_epochs` which allows you to generate a sample image every n steps or epochs
      - `sample_prompts` which is the file you pass in to generate the preview images. you can only specify a positive prompt, there is no support for negative prompts
      - `sample_sampler` which is the sampler that is used for generating images, it defaults to ddim, but there are a lot of options, I list them all in ArgsList.py
    - `tokenizer_cache_dir` which, to be honest, I don't really know what this means, it seems to talk about using this for offline training, but I'm pretty sure training is already offline.
    - `locon alpha` because this was added as a variable once it was fixed
  - Added all of the LoCon args to the popups as they have been tested enough that I feel comfortable adding them in as a whole
  - Added LoCon extracting and merging through their respective scripts `locon_extract.bat` and `locon_merge.bat`. look above for a bit more info on them, but the popups will generally guide you enough.
- Feb 27, 2023
  - Updated the LoRA merging scripts to allow for merging LoRA to models, I don't believe this works for locon models for now, I'll look into adding support another time
  - Added LoCon training to the scripts, as well as added the LoCon repo as a submodule. I added two new commands to facilite this
    - `locon` which is a bool that activates training with LoCon
    - `locon_dim` which is the dim for the LoCon layers, you must still set the main dim size
- Feb 23, 2023
  - Completely overhauled the scripts, changing everything
  - command line and popup are no longer seperate scripts
    - you can acces the popup version by adding --popup to the command call, or by using the associated batch file for that purpose.
    - you no longer modify the variables directly in the command_line.py script as it no longer exists, instead, there is a script specifically made to house all of the arguments that is seperated from the running logic.
  - changed the entire structure of the file system so that sd_scripts is now a submodule of my scripts, so that things don't break when sd_scripts updates until I update the scripts to support the new updates.
  - Updated all of the smaller side scripts to allow them to work with the new structure.
  - Added the new args, and shuffled around all of the old args to better organize them.
  - Created a new installer to support the new way everything is set up. (soon, gotta get this up first) This is windows only unfortunately
- Feb 20, 2023
  - Updated the scripts to support the new parameters added
    - Lion support added on both scripts, under the param `use_lion`
    - added the `lowram` option even though I don't think it will be needed for anybody who actually uses my scripts, as that seems to be geared towards colab users.
  - Added a script for merging LoRA, called `lora_merge.py` and it's bat file `lora_merge.bat`
    - It uses the same popup style for the other sub scripts, and will walk you through the process. This script seems to be able to merge more than one LoRA at a time
  - Added a script for downscaling images, called `image_resize.py` and it's bat file `image_resize.bat`. This will be a very useful tool for replacing repeats with a better alternative if you use the no_upscale feature.
- Feb 14, 2023
  - Updated the scripts to support the new parameter Kohya added, noise_offset
    - I haven't tested it myself yet, but supposedly having this set will improve generation of very bright and very dark elements. Kohya recommends a value of 0.1
  - Added the verbose option to the `lora_resize` script, I also wanted to add a way to output this to a text file, but I wan't able to find a way to do so cleanly. I will revisit this another time.
  - Added a queue system to the `lora_resize` script, it works very similar to my queue system when using the `lora_train_popup.py` queue system.
  - It seems like the multi-gpu option is baked into the code and will automatically use the gpus you have set when using `accelerate config`, I suggest that if you want to use multiple gpus to re-run the `accelerate config` to account for that, as right now, most people have it set up such that only one gpu is used.
- Feb 12, 2023
  - released v4 of the installers
    - had to remove the python and git check because it wasn't working as expected
    - also fixed an issue where ther cudnn wouldn't download because the website had an incorrect certificate
  - Small change to the txt file generation system so that you can output the files alphabetically
  - Added the option to turn on flip_aug for `lora_train_popup.py`
- Feb 11, 2023
  - released v3 of the installers
    - Added the python check system wide as well as user wide, rather than just user wide
    - Decluttered thing's a bit more for easier reading
    - Added a way to ask for admin so you no longer need to run it as admin
- Fab 10, 2023
  - released v2 of the installers
    - New guards to make sure that python 3.10 and git are installed
    - less cluttered messages so that is makes more sense what is going on
    - the option to install the cudnn patch for higher end 30X0 cards as well as 40X0 cards, using the installer script written by bmaltais. Thanks bmaltais
    - the option to auto install the patch for 10X0 cards, for the sd-scripts installer only
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
| save_every_n_epochs            | int       | NO       | Saves a checkpoint every n epochs, so save_every_n_epochs = 1 means that it saves every epoch                                                                                                                                                                            |
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
| noise_offset                   | float     | NO       | Seemingly allows generation of darker and lighter than usual images. Kohya suggests 0.1, as does the paper on this technique, so I will parrot this and also suggest that you set it to 0.1 if you use it.                                                               |
| lowram                         | bool      | NO       | Changes how the model is loaded so that it loads into vram, pretty much only useful for people with a lot of vram and no system ram, or colab users.                                                                                                                     |
| use_lion                       | bool      | NO       | Is the flag to enable using the new lion optimizer. it obviously can't be used with 8bit_adam as they are both optimizers.                                                                                                                                               |
|save_json_name|str|NO|Is the name that will be appended to the end of the config file output|
|locon|bool|NO|Enables locon training, which is new, basically works like LoRA but holds more information.|
|locon_dim|int |NO|The dim that is seperate to the normal network dim, it serves as the dim size for the other layers that aren't the default LoRA layers. No recommendation because not enough testing has been done.|
